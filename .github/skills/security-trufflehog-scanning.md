---
name: security-trufflehog-scanning
description: Secret scanning with TruffleHog - configuration, best practices, and troubleshooting
technologies: [TruffleHog, Security, GitHub Actions]
repositories: [all]
---

# TruffleHog Secret Scanning

## When to Use

Use this skill when configuring or troubleshooting TruffleHog secret scanning in GitHub Actions workflows.

## Prerequisites

- Basic understanding of Git and GitHub Actions
- Familiarity with secret management concepts

## Step-by-Step Instructions

### 1. Workflow Configuration

```yaml
name: TruffleHog Secret Scan

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
  schedule:
    - cron: "0 15 * * *" # Daily at 11 PM SGT (15:00 UTC)

jobs:
  trufflehog:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v6
        with:
          fetch-depth: 0  # CRITICAL: Full history for scanning

      - name: TruffleHog OSS
        uses: trufflesecurity/trufflehog@v3.63.2
        with:
          path: ./
          extra_args: --only-verified

      - name: Check for secrets
        if: failure()
        run: echo "TruffleHog detected secrets or encountered a configuration error." && exit 1
```

### 2. Action Version Management

**Always use specific versions:**
- `actions/checkout@v6` (latest stable)
- `trufflesecurity/trufflehog@v3.63.2` (latest stable)

**Never use:**
- `@main` or `@latest` tags
- Unpinned versions

### 3. Common Issues and Solutions

**Issue: TruffleHog fails with "configuration error"**
```yaml
# ❌ WRONG - Missing fetch-depth
- uses: actions/checkout@v6

# ✅ CORRECT - Full history
- uses: actions/checkout@v6
  with:
    fetch-depth: 0
```

**Issue: False positives on test files**
```yaml
# Add exclusions for test files
- name: TruffleHog OSS
  uses: trufflesecurity/trufflehog@v3.63.2
  with:
    extra_args: --only-verified --exclude-paths=tests/
```

### 4. Secret Detection Rules

TruffleHog detects:
- API keys and tokens
- Private keys
- Database connection strings
- AWS credentials
- GitHub tokens
- JWT secrets
- And many more...

### 5. Handling Real Secrets

If TruffleHog finds real secrets:

1. **Rotate immediately** - Change the compromised secret
2. **Remove from history** - Use `git filter-branch` or BFG
3. **Update environment** - Use GitHub Secrets or environment variables
4. **Never commit** - Add to `.gitignore`

## Common Pitfalls

1. **Not using `fetch-depth: 0`** - Required for full history scanning
2. **Using outdated action versions** - Always pin to specific versions
3. **Ignoring failures** - Treat all TruffleHog failures as critical
4. **Committing .env files** - Always add to `.gitignore`

## References

- [TruffleHog Documentation](https://github.com/trufflesecurity/trufflehog)
- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [Keeping Actions Up to Date](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot)
