#!/usr/bin/env python3
import os
import sys
import secrets
import subprocess
import argparse
import re

COMPOSE_PATH = "/root/stacks/main/docker-compose.yml"
ENV_PATH = "/root/stacks/main/.env"

SANDBOX_SERVICES_YAML = """
  n8n-sandbox-tls-init:
    image: n8nio/n8n-sandbox-service-api:latest
    user: "0:0"
    entrypoint: ["sh", "-c"]
    command:
      - >-
        bootstrap-mtls.sh
        --out-dir /tls
        --api-san n8n-sandbox-api
        --control-san-prefix n8n-sandbox-runner
        && chown -R sandbox-api:sandbox-api /tls/api
    environment:
      NUM_RUNNERS: 1
    volumes:
      - ./.tls:/tls
    networks:
      - caddy_network

  n8n-sandbox-api:
    image: n8nio/n8n-sandbox-service-api:latest
    container_name: n8n-sandbox-api
    restart: unless-stopped
    depends_on:
      n8n-sandbox-tls-init:
        condition: service_completed_successfully
    volumes:
      - ./.tls/api:/tls:ro
      - n8n-sandbox-api-data:/var/lib/n8n-sandbox-api
    env_file: .env
    environment:
      SANDBOX_API_GRPC_TLS_CERT_FILE: /tls/grpc-server.crt
      SANDBOX_API_GRPC_TLS_KEY_FILE: /tls/grpc-server.key
      SANDBOX_API_GRPC_TLS_CLIENT_CA_FILE: /tls/ca.crt
      SANDBOX_API_RUNNER_CONTROL_GRPC_TLS_CA_FILE: /tls/ca.crt
      SANDBOX_API_RUNNER_CONTROL_GRPC_TLS_CERT_FILE: /tls/control-grpc-api-client.crt
      SANDBOX_API_RUNNER_CONTROL_GRPC_TLS_KEY_FILE: /tls/control-grpc-api-client.key
      SANDBOX_API_RUNNER_CONTROL_GRPC_TLS_SERVER_NAME: n8n-sandbox-runner
    networks:
      - caddy_network

  n8n-sandbox-runner:
    image: n8nio/n8n-sandbox-service-runner-dind:latest
    container_name: n8n-sandbox-runner
    privileged: true
    restart: unless-stopped
    depends_on:
      n8n-sandbox-tls-init:
        condition: service_completed_successfully
      n8n-sandbox-api:
        condition: service_started
    volumes:
      - ./.tls/runner:/tls:ro
    env_file: .env
    environment:
      SANDBOX_RUNNER_DOCKER_SANDBOX_IMAGE: n8nio/n8n-sandbox-service-sandbox:latest
      SANDBOX_RUNNER_API_GRPC_ADDR: n8n-sandbox-api:9090
      SANDBOX_RUNNER_HTTP_BASE_URL: http://n8n-sandbox-runner:8080
      SANDBOX_RUNNER_CONTROL_GRPC_LISTEN_ADDR: ":9091"
      SANDBOX_RUNNER_CONTROL_GRPC_ADVERTISE_ADDR: n8n-sandbox-runner:9091
      SANDBOX_RUNNER_REGISTRATION_GRPC_CA_FILE: /tls/ca.crt
      SANDBOX_RUNNER_REGISTRATION_GRPC_CERT_FILE: /tls/grpc-client.crt
      SANDBOX_RUNNER_REGISTRATION_GRPC_KEY_FILE: /tls/grpc-client.key
      SANDBOX_RUNNER_REGISTRATION_GRPC_SERVER_NAME: n8n-sandbox-api
      SANDBOX_RUNNER_CONTROL_GRPC_TLS_CERT_FILE: /tls/control-grpc-server.crt
      SANDBOX_RUNNER_CONTROL_GRPC_TLS_KEY_FILE: /tls/control-grpc-server.key
      SANDBOX_RUNNER_CONTROL_GRPC_TLS_CLIENT_CA_FILE: /tls/ca.crt
    networks:
      - caddy_network
"""

def generate_key():
    return secrets.token_hex(24)

def setup_sandbox(model=None, api_key=None):
    print("=== Setting up n8n Sandbox Service ===")

    # 1. Update .env
    if not os.path.exists(ENV_PATH):
        print(f"Error: .env not found at {ENV_PATH}")
        sys.exit(1)

    with open(ENV_PATH, "r") as f:
        env_content = f.read()

    # Check if sandbox keys already exist
    updated_env = env_content
    added_keys = False

    if "N8N_SANDBOX_SERVICE_API_KEY" not in env_content:
        api_key_gen = generate_key()
        reg_token = generate_key()
        runner_key = generate_key()

        sandbox_env = f"\n# n8n Sandbox Service\n" \
                      f"N8N_SANDBOX_SERVICE_API_KEY={api_key_gen}\n" \
                      f"SANDBOX_API_KEYS={api_key_gen}\n" \
                      f"SANDBOX_API_RUNNER_REGISTRATION_TOKEN={reg_token}\n" \
                      f"SANDBOX_API_RUNNER_API_KEY={runner_key}\n" \
                      f"SANDBOX_RUNNER_API_KEYS={runner_key}\n" \
                      f"SANDBOX_RUNNER_REGISTRATION_TOKEN={reg_token}\n"
        updated_env += sandbox_env
        added_keys = True
        print("Generated and added secure sandbox API keys to .env.")

    # Check if n8n AI Assistant vars already exist
    if "N8N_ENABLED_MODULES=instance-ai" not in env_content:
        assistant_env = f"\n# n8n AI Assistant Configuration\n" \
                        f"N8N_ENABLED_MODULES=instance-ai\n" \
                        f"N8N_INSTANCE_AI_SANDBOX_ENABLED=true\n" \
                        f"N8N_INSTANCE_AI_SANDBOX_PROVIDER=n8n-sandbox\n"
        if model:
            assistant_env += f"N8N_INSTANCE_AI_MODEL={model}\n"
        else:
            assistant_env += f"N8N_INSTANCE_AI_MODEL=openai/gpt-4o-mini\n"
        
        if api_key:
            assistant_env += f"N8N_INSTANCE_AI_MODEL_API_KEY={api_key}\n"
        else:
            assistant_env += f"N8N_INSTANCE_AI_MODEL_API_KEY=dein-openai-oder-anthropic-api-key\n"
        
        updated_env += assistant_env
        added_keys = True
        print("Added n8n AI Assistant configuration boilerplate to .env.")

    if added_keys:
        with open(ENV_PATH, "w") as f:
            f.write(updated_env)

    # 2. Update docker-compose.yml
    if not os.path.exists(COMPOSE_PATH):
        print(f"Error: docker-compose.yml not found at {COMPOSE_PATH}")
        sys.exit(1)

    with open(COMPOSE_PATH, "r") as f:
        compose_content = f.read()

    # Check if sandbox containers are already in compose
    if "n8n-sandbox-api:" not in compose_content:
        print("Adding sandbox services to docker-compose.yml...")
        
        # 2a. Add environment variables to n8n container
        # Find the environment block of n8n service and insert them
        n8n_env_vars = [
            "      - N8N_ENABLED_MODULES=${N8N_ENABLED_MODULES}",
            "      - N8N_INSTANCE_AI_SANDBOX_ENABLED=${N8N_INSTANCE_AI_SANDBOX_ENABLED}",
            "      - N8N_INSTANCE_AI_SANDBOX_PROVIDER=${N8N_INSTANCE_AI_SANDBOX_PROVIDER}",
            "      - N8N_SANDBOX_SERVICE_URL=http://n8n-sandbox-api:8080",
            "      - N8N_SANDBOX_SERVICE_API_KEY=${N8N_SANDBOX_SERVICE_API_KEY}",
            "      - N8N_INSTANCE_AI_MODEL=${N8N_INSTANCE_AI_MODEL}",
            "      - N8N_INSTANCE_AI_MODEL_API_KEY=${N8N_INSTANCE_AI_MODEL_API_KEY}"
        ]
        
        # Look for N8N_RUNNERS_AUTH_TOKEN line inside n8n environment
        token_match = re.search(r"(\s+-\s+N8N_RUNNERS_AUTH_TOKEN=\S+)", compose_content)
        if token_match:
            insert_pos = token_match.end()
            insert_str = "\n" + "\n".join(n8n_env_vars)
            compose_content = compose_content[:insert_pos] + insert_str + compose_content[insert_pos:]
            print("Mapped sandbox environment variables to n8n container.")
        else:
            print("Warning: Could not automatically map env variables to n8n service. Please map them manually.")

        # 2b. Add sandbox containers before networks:
        networks_match = re.search(r"(\nnetworks:\s*)", compose_content)
        if networks_match:
            insert_pos = networks_match.start()
            compose_content = compose_content[:insert_pos] + SANDBOX_SERVICES_YAML + compose_content[insert_pos:]
            print("Added sandbox containers to docker-compose.yml.")
        else:
            print("Error: Could not locate 'networks:' section in docker-compose.yml.")
            sys.exit(1)

        # 2c. Add volume n8n-sandbox-api-data
        if "n8n-sandbox-api-data:" not in compose_content:
            # Append it right under volumes:
            volumes_match = re.search(r"(\nvolumes:\s*)", compose_content)
            if volumes_match:
                insert_pos = volumes_match.end()
                compose_content = compose_content[:insert_pos] + "  n8n-sandbox-api-data: {}\n" + compose_content[insert_pos:]
                print("Added sandbox persistent volume definition.")

        with open(COMPOSE_PATH, "w") as f:
            f.write(compose_content)

    # 3. Pull images and restart compose
    print("Pulling required sandbox service docker images...")
    subprocess.run(["docker", "pull", "n8nio/n8n-sandbox-service-api:latest"])
    subprocess.run(["docker", "pull", "n8nio/n8n-sandbox-service-runner-dind:latest"])
    subprocess.run(["docker", "pull", "n8nio/n8n-sandbox-service-sandbox:latest"])

    print("Restarting docker stack to apply changes...")
    subprocess.run(["docker", "compose", "-f", COMPOSE_PATH, "up", "-d"])
    print("Sandbox setup complete! n8n restarted and configured.")

def check_status():
    print("=== Checking Sandbox Service Status ===")
    
    # Check container status
    containers = ["n8n-sandbox-api", "n8n-sandbox-runner", "n8n"]
    all_running = True
    
    for container in containers:
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", container],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        running = result.stdout.strip() == "true"
        status_str = "RUNNING" if running else "STOPPED/NOT CREATED"
        print(f"Container '{container}': {status_str}")
        if not running:
            all_running = False

    if all_running:
        print("\nChecking runner registration logs...")
        logs_result = subprocess.run(
            ["docker", "logs", "--tail", "50", "n8n-sandbox-runner"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        logs = logs_result.stdout + logs_result.stderr
        if "runner registration stream established" in logs:
            print("[SUCCESS] Sandbox runner registration stream established with API.")
        else:
            print("[WARNING] Could not confirm registration stream in recent runner logs.")
            print("Please inspect runner logs manually: docker logs n8n-sandbox-runner")
    else:
        print("[ERROR] One or more containers are not running. Please check logs.")

def remove_sandbox():
    print("=== Uninstalling Sandbox Service ===")
    if not os.path.exists(COMPOSE_PATH):
        print("Compose file not found.")
        sys.exit(1)

    # Stop and remove containers
    print("Stopping sandbox containers...")
    subprocess.run(["docker", "stop", "n8n-sandbox-runner", "n8n-sandbox-api"], stderr=subprocess.DEVNULL)
    subprocess.run(["docker", "rm", "n8n-sandbox-runner", "n8n-sandbox-api"], stderr=subprocess.DEVNULL)

    # Read config files
    with open(COMPOSE_PATH, "r") as f:
        compose_content = f.read()

    # 1. Remove services block
    # Match from n8n-sandbox-tls-init to caddy_network network mount
    compose_content = re.sub(
        r"\s*n8n-sandbox-tls-init:.*n8n-sandbox-runner:.*?networks:.*?- caddy_network\n",
        "", compose_content, flags=re.DOTALL
    )
    
    # 2. Remove n8n env mappings
    compose_content = re.sub(
        r"\s+-\s+N8N_ENABLED_MODULES=\S+\n"
        r"\s+-\s+N8N_INSTANCE_AI_SANDBOX_ENABLED=\S+\n"
        r"\s+-\s+N8N_INSTANCE_AI_SANDBOX_PROVIDER=\S+\n"
        r"\s+-\s+N8N_SANDBOX_SERVICE_URL=\S+\n"
        r"\s+-\s+N8N_SANDBOX_SERVICE_API_KEY=\S+\n"
        r"\s+-\s+N8N_INSTANCE_AI_MODEL=\S+\n"
        r"\s+-\s+N8N_INSTANCE_AI_MODEL_API_KEY=\S+\n",
        "\n", compose_content
    )

    # 3. Remove volume definition
    compose_content = compose_content.replace("  n8n-sandbox-api-data: {}\n", "")

    with open(COMPOSE_PATH, "w") as f:
        f.write(compose_content)
    print("Removed sandbox configuration from docker-compose.yml.")

    # 4. Remove .env vars
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r") as f:
            env_content = f.read()
        
        # Regex out sandbox block
        env_content = re.sub(r"\n# n8n Sandbox Service.*?(?=\n#|\Z)", "", env_content, flags=re.DOTALL)
        env_content = re.sub(r"\n# n8n AI Assistant Configuration.*?(?=\n#|\Z)", "", env_content, flags=re.DOTALL)
        
        with open(ENV_PATH, "w") as f:
            f.write(env_content)
        print("Removed sandbox variables from .env.")

    # Apply changes
    print("Re-evaluating docker compose stack...")
    subprocess.run(["docker", "compose", "-f", COMPOSE_PATH, "up", "-d", "--remove-orphans"])
    print("Uninstallation complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="n8n AI Assistant Sandbox Manager")
    parser.add_argument("--setup", action="store_true", help="Set up and configure the sandbox service")
    parser.add_argument("--status", action="store_true", help="Check the running status of sandbox services")
    parser.add_argument("--remove", action="store_true", help="Uninstall and remove sandbox services")
    parser.add_argument("--model", type=str, help="AI model to configure in .env (e.g. openrouter/z-ai/glm-5.2)")
    parser.add_argument("--key", type=str, help="LLM API key to configure in .env")

    args = parser.parse_args()

    if args.setup:
        setup_sandbox(args.model, args.key)
    elif args.status:
        check_status()
    elif args.remove:
        remove_sandbox()
    else:
        parser.print_help()
