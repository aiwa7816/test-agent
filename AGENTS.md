# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **skill/plugin collection** (26 Cursor Agent Skills for academic research), not a traditional runnable application. There are no servers, databases, or CI pipelines to start.

### Project structure

- `.cursor/skills/` — 26 Cursor-discoverable SKILL.md definitions (7 categories: orchestration, research, analysis, writing, review, office, utilities)
- `.claude/skills/` — Parallel Claude Code skill definitions with Python helper scripts
- `scripts/activate-skills.sh` — Symlinks `.cursor/skills/` to `~/.cursor/skills` for global discovery

### Python dependencies

Some skills include Python helper scripts that require `PyYAML`, `openai`, and `requests`. These are installed by the update script. There is no project-level `requirements.txt`; dependencies come from per-skill `requirements.txt` files in `.claude/skills/aminer-daily-paper/` and `.claude/skills/aminer-deep-search/`.

### Lint / validation

- **Syntax check all Python files**: `find . -name '*.py' -not -path './.git/*' -print0 | xargs -0 python3 -m py_compile`
- **Verify skill discovery**: `find .cursor/skills -name SKILL.md | wc -l` (expect 26)

### Activating skills

Run `./scripts/activate-skills.sh` to create the `~/.cursor/skills` symlink. This is done by the update script.

### External API keys (all optional, per-skill)

| Variable | Used By |
|----------|---------|
| `AMINER_API_KEY` | aminer-daily-paper, aminer-deep-search, aminer-free-academic, aminer-academic-search |
| `OPENROUTER_API_KEY` | scientific-writing (schematic generation) |
| `S2_API_KEY` | deep-research (Semantic Scholar lookups) |
| `NCBI_API_KEY` | citation-management (PubMed search) |

### Testing the aminer-academic-search client

Use `--dry-run` to preview API call chains without a token:

```bash
python3 .claude/skills/aminer-academic-search/scripts/aminer_client.py --action paper_deep_dive --title "BERT" --dry-run
```

### Gotchas

- The SKILL.md files do not start with a markdown `#` heading; they use a YAML-frontmatter-like format. `title=False` in validation is expected.
- The `.claude/` and `.cursor/` skill trees are parallel but not identical — `.claude/` contains additional orchestration/pipeline skills and schema files.
