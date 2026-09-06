# Contributing to Thirai Kuzhu AI (திரை குழு AI)

Thank you for your interest in contributing to **Thirai Kuzhu AI** — the Screen Crew AI for Cinematic Observability.

We welcome contributions from film engineers, SREs, AI architects, and open-source developers worldwide.

---

## Development Standards & Quality Gates

All contributions must strictly satisfy our four non-negotiable quality gates before being merged:

1. **100% Statement Test Coverage**:
   - Every single statement must be covered by tests (`pytest --cov=src --cov-fail-under=100`).
   - Use of coverage cheat annotations (`# pragma: no cover`) is strictly prohibited.
2. **Zero Linter & Formatter Errors**:
   - Code must pass `ruff check src tests` with zero errors and zero warnings.
   - Formatting must conform to `ruff format --check src tests`.
3. **Automated AST Security Scan**:
   - Must produce zero issues under Bandit: `bandit -r src/ -c pyproject.toml`.
4. **Secret Scanning**:
   - Zero hardcoded secrets, tokens, private keys, or passwords.
   - Verified via `gitleaks detect --verbose` and Bandit security profiles.
5. **Modular Architecture & Zero Leaks**:
   - Never create monolithic files. Each subagent must have its own `.py` class.
   - Frontend must use discrete `.jsx` components and individual locale files in `src/i18n/locales/`.
   - Symmetrical teardown of event listeners, SSE streams, and timers to prevent memory leaks.

---

## Getting Started Locally

### Prerequisites
- Python 3.12+
- Node.js 20+ & npm
- Google Cloud SDK (`gcloud`)
- Terraform 1.8+ (for infra modules)

### Quickstart Setup
```bash
# 1. Clone repository
git clone https://github.com/your-org/thiraikuzhuai.git
cd thiraikuzhuai

# 2. Set up Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Or on Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Run Quality Suite
pytest tests -v --cov=src --cov-fail-under=100
ruff check src tests
bandit -r src/ -c pyproject.toml

# 4. Set up Frontend
cd ../frontend
npm install
npm run build
```

---

## Pull Request Guidelines

1. **Branch Naming**:
   - `feat/feature-name`
   - `fix/bug-description`
   - `docs/documentation-update`
2. **Commit Messages**: Follow Conventional Commits:
   - `feat(agents): add sound stem phase alignment subagent`
   - `fix(governance): sanitize nested JSON Loki log strings`
   - `test(eval): add 100% coverage assertions for CRI calculation`
3. **CI/CD Execution**: All automated GitHub Actions checks must turn green before requesting review.
