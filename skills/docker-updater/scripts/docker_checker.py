#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import sys

def run_cmd(args, cwd=None, check=True):
    try:
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd, check=check)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(args)} in {cwd or '.'}: {e.stderr.strip()}", file=sys.stderr)
        if check:
            raise e
        return "", e.stderr.strip()

def get_running_containers():
    stdout, _ = run_cmd(["docker", "ps", "--format", "{{.ID}}|{{.Names}}|{{.Image}}|{{.State}}"])
    containers = []
    if not stdout:
        return containers
    for line in stdout.split("\n"):
        if not line.strip():
            continue
        parts = line.split("|")
        if len(parts) == 4:
            containers.append({
                "id": parts[0],
                "name": parts[1],
                "image": parts[2],
                "state": parts[3]
            })
    return containers

def get_container_image_id(container_id):
    stdout, _ = run_cmd(["docker", "inspect", "-f", "{{.Image}}", container_id], check=False)
    return stdout.strip()

def get_image_id(image_name):
    stdout, _ = run_cmd(["docker", "inspect", "-f", "{{.Id}}", image_name], check=False)
    return stdout.strip()

def main():
    parser = argparse.ArgumentParser(description="Docker Image Update and Rebuild Utility")
    parser.add_argument("-c", "--check", action="store_true", help="Only check for updates (default)")
    parser.add_argument("-b", "--build", action="store_true", help="Rebuild custom Dockerfiles if base image was updated")
    parser.add_argument("-r", "--recreate", action="store_true", help="Recreate containers if images were updated")
    parser.add_argument("-a", "--all", action="store_true", help="Perform check, rebuild, and recreate")
    
    args = parser.parse_args()
    
    # If no flags are passed, default to check-only
    if not (args.build or args.recreate or args.all):
        args.check = True
        
    if args.all:
        args.build = True
        args.recreate = True
        args.check = True

    print("=== DOCKER IMAGE UPDATE CHECKER ===")
    
    # 1. Get running containers
    running = get_running_containers()
    print(f"Found {len(running)} running containers.")
    
    # Define stacks
    stacks = {
        "main": "/root/stacks/main",
        "plane": "/root/stacks/plane"
    }
    
    # Map running containers to their service / stack / build if possible
    registry_updates = []
    built_services_to_check = []
    
    # We'll pull running registry images to see if there are updates
    checked_registry_images = {}
    
    for container in running:
        c_name = container["name"]
        c_image = container["image"]
        c_id = container["id"]
        
        # Get container's running image ID
        running_img_id = get_container_image_id(c_id)
        
        # Check if it's a locally built image
        is_local_build = c_image.startswith("root-") or c_image in ["pii_filter_service", "semantic_pii_service", "n8n-task-runners"]
        
        if is_local_build:
            built_services_to_check.append({
                "container_name": c_name,
                "local_image_name": c_image,
                "running_img_id": running_img_id
            })
        else:
            # Registry image
            if c_image not in checked_registry_images:
                print(f"Checking registry image: {c_image}...")
                old_id = get_image_id(c_image)
                
                # Pull the registry image if not check-only or if we need fresh check
                _, pull_err = run_cmd(["docker", "pull", c_image], check=False)
                new_id = get_image_id(c_image)
                
                checked_registry_images[c_image] = {
                    "old_id": old_id,
                    "new_id": new_id,
                    "updated": old_id != new_id
                }
            
            status = checked_registry_images[c_image]
            if status["updated"] or running_img_id != status["new_id"]:
                registry_updates.append({
                    "container_name": c_name,
                    "image": c_image,
                    "running_id": running_img_id,
                    "latest_id": status["new_id"],
                    "reason": "Newer image pulled from registry" if status["updated"] else "Container running older version of image"
                })

    # 2. Check Dockerfiles for base image updates
    print("\n=== CHECKING INDIVIDUAL DOCKERFILES ===")
    dockerfiles = [
        {"path": "/root/stacks/main/dockerfile-firefox", "service": "firefox", "stack": "main", "disabled": True},
        {"path": "/root/stacks/main/dockerfile-openwebui", "service": "open-webui", "stack": "main", "disabled": False},
        {"path": "/root/stacks/main/Dockerfile-n8n-runners", "service": "n8n-task-runners", "stack": "main", "disabled": False},
        {"path": "/root/stacks/main/ocr-service/dockerfile", "service": "ocr_service", "stack": "main", "disabled": True},
        {"path": "/root/stacks/main/pdf-service/dockerfile", "service": "pdf_service", "stack": "main", "disabled": True},
        {"path": "/root/stacks/main/pii-filter-service/dockerfile", "service": "pii_filter", "stack": "main", "disabled": False},
        {"path": "/root/stacks/main/easyocr-service/dockerfile", "service": "easyocr_service", "stack": "main", "disabled": True},
        {"path": "/root/stacks/main/semantic-pii-service/dockerfile", "service": "semantic_pii", "stack": "main", "disabled": False},
        {"path": "/root/stacks/main/paddleocr-service/dockerfile", "service": "paddleocr_service", "stack": "main", "disabled": True},
    ]
    
    base_image_updates = {}
    rebuild_required = []
    
    # Copy requirements to requirements.txt if needed
    for folder in ["easyocr-service", "paddleocr-service"]:
        req_path = f"/root/stacks/main/{folder}/requirements"
        req_txt_path = f"/root/stacks/main/{folder}/requirements.txt"
        if os.path.exists(req_path) and not os.path.exists(req_txt_path):
            print(f"Copying {req_path} to {req_txt_path}...")
            run_cmd(["cp", req_path, req_txt_path])

    for df in dockerfiles:
        df_path = df["path"]
        service = df["service"]
        stack = df["stack"]
        
        if not os.path.exists(df_path):
            print(f"Dockerfile not found: {df_path}")
            continue
            
        print(f"Parsing Dockerfile: {df_path} for service {service}...")
        base_images = []
        with open(df_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = re.match(r"^\s*FROM\s+([^\s]+)", line, re.IGNORECASE)
                if match:
                    base_img = match.group(1)
                    if " as " in base_img.lower():
                        base_img = re.split(r"\s+as\s+", base_img, flags=re.IGNORECASE)[0]
                    if base_img not in ["ffmpeg"]:
                        base_images.append(base_img)
        
        df_needs_rebuild = False
        updates_found_for_df = []
        
        for base_img in base_images:
            if base_img not in base_image_updates:
                print(f"  Checking base image: {base_img}...")
                old_id = get_image_id(base_img)
                # Pull the base image
                _, pull_err = run_cmd(["docker", "pull", base_img], check=False)
                new_id = get_image_id(base_img)
                base_image_updates[base_img] = {
                    "old_id": old_id,
                    "new_id": new_id,
                    "updated": old_id != new_id
                }
            
            img_status = base_image_updates[base_img]
            if img_status["updated"]:
                df_needs_rebuild = True
                updates_found_for_df.append(f"{base_img} (updated)")
                
        # Check if compile service image exists
        local_img = f"root-{service}"
        if service == "pii_filter":
            local_img = "root-pii_filter"
        elif service == "semantic_pii":
            local_img = "root-semantic_pii"
        elif service == "n8n-task-runners":
            local_img = "root-n8n-task-runners"
        elif service == "open-webui":
            local_img = "root-open-webui"
            
        local_img_exists = get_image_id(local_img) != ""
        if not local_img_exists:
            df_needs_rebuild = True
            updates_found_for_df.append("Image does not exist locally")
            
        if df_needs_rebuild:
            rebuild_required.append({
                "service": service,
                "path": df_path,
                "stack": stack,
                "disabled": df["disabled"],
                "reasons": updates_found_for_df
            })

    # Summary of changes
    print("\n=== SUMMARY OF UPDATES ===")
    
    # 1. Registry image updates
    if registry_updates:
        print("\nRunning registry-based containers with updates:")
        for update in registry_updates:
            print(f" - Container: {update['container_name']} ({update['image']})")
            print(f"   Reason: {update['reason']}")
    else:
        print("\nAll running registry-based containers are up-to-date.")
        
    # 2. Rebuilds needed
    if rebuild_required:
        print("\nLocal images needing build/rebuild:")
        for r in rebuild_required:
            status_str = "[DISABLED]" if r["disabled"] else "[ACTIVE]"
            print(f" - Service: {r['service']} {status_str} (Dockerfile: {r['path']})")
            print(f"   Reason: {', '.join(r['reasons'])}")
    else:
        print("\nAll custom Dockerfiles are up-to-date and have current base images.")

    # 3. Action Execution
    # Build if requested
    if args.build and rebuild_required:
        print("\n=== REBUILDING CUSTOM IMAGES ===")
        # Build active services
        active_to_build = [r["service"] for r in rebuild_required if not r["disabled"]]
        disabled_to_build = [r["service"] for r in rebuild_required if r["disabled"]]
        
        # Build open-webui2 if open-webui is built since they share the same dockerfile
        if "open-webui" in active_to_build and "open-webui2" not in active_to_build:
            active_to_build.append("open-webui2")
            
        # Perform build
        build_services = active_to_build + disabled_to_build
        if build_services:
            print(f"Building services: {', '.join(build_services)}...")
            cmd = ["docker", "compose", "-f", "docker-compose.yml", "-f", "docker-compose.disabled.yml", "build"] + build_services
            run_cmd(cmd, cwd=stacks["main"])
            print("Successfully rebuilt custom images.")

    # Recreate containers if requested
    if args.recreate:
        print("\n=== RECREATING CONTAINERS ===")
        # Recreate main stack
        print("Recreating Main stack...")
        run_cmd(["docker", "compose", "up", "-d"], cwd=stacks["main"])
        
        # Recreate plane stack
        print("Recreating Plane PM stack...")
        run_cmd(["docker", "compose", "up", "-d"], cwd=stacks["plane"])
        
        print("All stacks recreated successfully.")

    # Save JSON report
    result_data = {
        "registry_updates": registry_updates,
        "rebuild_required": rebuild_required,
        "rebuilt": args.build and len(rebuild_required) > 0,
        "recreated": args.recreate
    }
    report_path = "/root/docker_checker_result.json"
    with open(report_path, "w") as f:
        json.dump(result_data, f, indent=2)
    print(f"\nReport saved to {report_path}")

if __name__ == "__main__":
    main()
