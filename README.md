# Maha Skills

A collection of installable skills for the Maha Agent, designed to automate and standardize project scaffolding, API creation, and rule enforcement.

## Repository Information

- **URL:** `https://github.com/mmtaee/ai_skills.git`
- **SSH:** `git@github.com:mmtaee/ai_skills.git`

---

## Installation & Usage

You can use these skills in two ways: via `npx` for a quick setup, or as a `git submodule` for ongoing synchronization.

### 1. Using `npx` (Recommended)

This is the fastest way to install the skills directly into your project's `.agent/` directory.

#### Install all skills:
```bash
npx skills add git@github.com:mmtaee/ai_skills.git
```

#### Install only specific framework skills (e.g., FastAPI):
```bash
npx skills add git@github.com:mmtaee/ai_skills.git fastapi
```

This will:
1. Create a `.agent/` directory in your current path if it doesn't exist.
2. Flatten the framework contents (e.g., `fastapi/*`) directly into `.agent/`.
3. Add `registry.json` to `.agent/`.

### 2. Using Git Submodule

If you want to keep the skills synchronized with the repository, you can add it as a submodule.

#### Add as submodule:
```bash
git submodule add git@github.com:mmtaee/ai_skills.git .agent/skills
```

#### Note on Submodule Usage:
When using submodules, the skills will reside in `.agent/skills/`. You may need to configure your agent to look in that specific path or manually link the contents to `.agent/`.

---

## Available Skills

### FastAPI Framework
- **[project-creator](fastapi/project-creator/SKILL.md)**: Generates a complete FastAPI backend scaffold using DDD and Clean Architecture.
- **[api-creator](fastapi/api-creator/SKILL.md)**: Standardized API endpoint generation.
- **[model-creator](fastapi/model-creator/SKILL.md)**: Database model generation.
- **[master-rules](fastapi/master-rules/SKILL.md)**: Core architecture and documentation standards.

---

## Structure

The repository is organized by framework:

```text
.
├── fastapi/              # FastAPI specific skills
│   ├── project-creator/
│   ├── api-creator/
│   └── ...
├── bin/                  # CLI tool for npx installation
├── registry.json         # Skills registry
└── package.json          # Node.js package configuration
```

## Contribution

To add a new skill:
1. Create a directory under the relevant framework.
2. Add a `SKILL.md` defining the prompt and logic.
3. Update `registry.json` to include the new skill.
4. Ensure `bin/cli.js` is updated if a new framework category is added.
