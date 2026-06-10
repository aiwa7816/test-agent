# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **skill/plugin collection** (26 Cursor Agent Skills for academic research), not a traditional runnable application. There are no servers, databases, or Docker services to start.

### Project structure

- `.cursor/skills/` — Canonical Cursor-discoverable `SKILL.md` tree (7 categories: orchestration, research, analysis, writing, review, office, utilities)
- `.claude/skills/` — Parallel flat layout for Claude Code (same 26 skills)
- `.claude/shared/` — JSON schemas and sprint/passport contracts used by orchestration skills
- `scripts/activate-skills.sh` — Symlinks `.cursor/skills/` → `~/.cursor/skills` for global discovery in Cloud VMs

### Activating skills

Run `./scripts/activate-skills.sh` (also executed by the VM update script). Verify with:

```bash
find .cursor/skills -name SKILL.md | wc -l   # expect 26
readlink -f ~/.cursor/skills               # expect /workspace/.cursor/skills
```

Project-local discovery works without the symlink when the repo is opened in Cursor; the script is for Cloud/global `~/.cursor/skills` parity.

### Python dependencies

No root `requirements.txt`. Per-skill manifests:

- `.cursor/skills/research/aminer-deep-search/requirements.txt` — `openai`, `requests`
- `.cursor/skills/research/aminer-daily-paper/requirements.txt` — `PyYAML`

Additional packages used by bundled helper scripts (installed by update script): `requests`, `bibtexparser`, `jsonschema`.

`pip install --user` places CLIs under `~/.local/bin`; add to `PATH` if invoking `jsonschema` or other entrypoints directly.

### Lint / validation

```bash
# Syntax-check all Python helpers
find . -name '*.py' -not -path './.git/*' -print0 | xargs -0 python3 -m py_compile

# Validate shared JSON schemas
python3 -c "
import json
from pathlib import Path
from jsonschema import Draft202012Validator
for p in sorted(Path('.claude/shared').rglob('*.schema.json')):
    Draft202012Validator.check_schema(json.loads(p.read_text()))
print('schemas ok')
"
```

### Smoke-test helper scripts (no API keys)

```bash
# DOI → BibTeX via Crossref (citation-management)
python3 .cursor/skills/research/citation-management/scripts/doi_to_bibtex.py 10.1038/nature14539

# BibTeX format lint (citation-verification)
python3 .cursor/skills/research/citation-verification/scripts/format-checker.py \
  .cursor/skills/research/citation-management/assets/bibtex_template.bib

# AMiner client dry-run (no token)
python3 .cursor/skills/research/aminer-academic-search/scripts/aminer_client.py \
  --action paper_deep_dive --title "BERT" --dry-run
```

### External API keys (optional, per-skill)

| Variable | Used by |
|----------|---------|
| `AMINER_API_KEY` | aminer-daily-paper, aminer-deep-search, aminer-free-academic, aminer-academic-search |
| `S2_API_KEY` | deep-research (Semantic Scholar; degrades gracefully if unset) |
| `NCBI_API_KEY` | citation-management (PubMed search) |
| `OPENROUTER_API_KEY` | scientific-writing schematic generation |

### Gotchas

- Core product surface is **Cursor/Claude agent runtime** loading `SKILL.md` files — not a dev server.
- `.claude/CLAUDE.md` documents the upstream full ARS suite (CI, tests, docs); this checkout is the **skills bundle only**.
- `.cursor/skills/` (categorized) and `.claude/skills/` (flat) are parallel trees; prefer `.cursor/skills/` paths in Cloud agents.
- `SKILL.md` files use YAML-style frontmatter without a leading `#` title; that is intentional.
