---
name: github-actions-ci
description: CI/CD patterns with GitHub Actions - workflows, best practices, and maintenance
technologies: [GitHub Actions, YAML, CI/CD]
repositories: [all]
---

# GitHub Actions CI/CD Patterns

## When to Use

Use this skill when creating or modifying GitHub Actions workflows for CI/CD.

## Prerequisites

- Basic understanding of Git and GitHub
- Familiarity with YAML syntax
- Understanding of CI/CD concepts

## Step-by-Step Instructions

### 1. Workflow Structure

```yaml
name: CI — Lint & Test

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  lint:
    name: Lint Code
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v6

      - name: Set up environment
        uses: actions/setup-python@v6
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt

      - name: Run linter
        run: python scripts/lint_repo.py

  test:
    name: Run Tests
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - name: Checkout code
        uses: actions/checkout@v6

      - name: Set up environment
        uses: actions/setup-python@v6
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements-dev.txt

      - name: Run tests
        run: python -m pytest -q
```

### 2. Action Version Management

**Always use specific versions for actions:**

```yaml
# ✅ GOOD - Specific version
uses: actions/checkout@v6
uses: actions/setup-python@v6
uses: trufflesecurity/trufflehog@v3.63.2

# ❌ BAD - Using main branch or no version
uses: actions/checkout@main
uses: actions/checkout
```

**Latest stable versions (as of 2026):**
- `actions/checkout` → `@v6`
- `actions/setup-python` → `@v6`
- `actions/setup-node` → `@v4`
- `actions/labeler` → `@v6`
- `actions/stale` → `@v10`
- `trufflesecurity/trufflehog` → `@v3.63.2`

### 3. Security Scanning

```yaml
name: TruffleHog Secret Scan

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
  schedule:
    - cron: "0 15 * * *" # Daily at 11 PM SGT

jobs:
  trufflehog:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - name: TruffleHog OSS
        uses: trufflesecurity/trufflehog@v3.63.2
        with:
          path: ./
          extra_args: --only-verified

      - name: Check for secrets
        if: failure()
        run: echo "TruffleHog detected secrets or encountered a configuration error." && exit 1
```

### 4. Caching Dependencies

```yaml
- name: Cache pip dependencies
  uses: actions/cache@v4
  with:
    paths: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### 5. Matrix Builds

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v6
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.python-version }}
```

## Common Pitfalls

1. **Using @main or @latest** - Always pin to specific versions
2. **Not using fetch-depth: 0** - Required for full git history in security scans
3. **Missing needs dependencies** - Jobs run in parallel by default
4. **Hardcoding environment variables** - Use GitHub secrets and env
5. **Not cleaning up after jobs** - Use temporary directories for builds

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Keeping your GitHub Actions up to date](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot)
- [Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
