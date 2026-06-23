# alpha1visionai Claude Skills

Shared skills for the alpha1visionai team. Install any skill with:

```bash
npx skills add alpha1visionai-stack/claude-skills@<skill-name> -g -y
```

## Available Skills

| Skill | Install | Description |
|---|---|---|
| `expert-council` | `npx skills add alpha1visionai-stack/claude-skills@expert-council -g -y` | Multi-perspective decision framework using llm-council CLI and /der-rat |

## Add a new skill

1. Create `skills/<skill-name>/SKILL.md`
2. Add frontmatter with `name` and `description`
3. Push to `main`
4. Team installs with `npx skills add alpha1visionai-stack/claude-skills@<skill-name> -g -y`
