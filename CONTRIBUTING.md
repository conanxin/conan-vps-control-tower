# Contributing

Thanks for considering a contribution. This project is intentionally small, personal, and read-only.

## How to Run Locally

```bash
cp config.example.yaml config.yaml
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --host 127.0.0.1 --port 3001
```

## How to Run Tests

```bash
python -m pytest
```

## How to Propose a Feature

Open an issue and describe:

- The user problem
- Whether the feature stays read-only
- Whether it could affect proxy services
- Whether it is suitable for a low-resource VPS

Do not include real IPs, domains, tokens, UUIDs, passwords, subscription links, or proxy plaintext.

## Project Principles

- Keep it lightweight.
- Keep it read-only.
- Prefer simple Python, FastAPI, YAML, and native browser features.
- Do not modify 3X-UI, proxy configuration, firewall rules, or running proxy services.
- Avoid enterprise architecture unless the project truly needs it.
