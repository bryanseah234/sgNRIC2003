---
name: git-best-practices
description: Universal Git workflows, commit conventions, and branch management strategies
---

# Git Best Practices

## When to Use
Apply these rules to all repositories in the workspace when committing code, managing branches, or handling pull requests.

## Core Principles
1. **Atomic Commits**: Each commit should do exactly one thing (fix a bug, add a feature, refactor a module).
2. **Clear History**: Maintain a clean, readable git history to facilitate debugging (e.g., `git bisect`) and code reviews.
3. **Never rewrite shared history**: Never force push (`git push -f`) to `main` or any branch that other developers are actively using.

## Step-by-Step

### 1. Commit Message Convention (Conventional Commits)
All commit messages must follow the Conventional Commits specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Allowed Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries such as documentation generation

**Example:**
```
feat(auth): add JWT token validation middleware

Added middleware to validate JWT tokens on all protected /api/v1 routes.
Resolves issue #123.
```

### 2. Branching Strategy (Trunk-Based / GitHub Flow)
- **`main` branch**: Always deployable. Protection rules should require passing CI and reviews.
- **Feature branches**: Branched off `main`. Should be short-lived (merged within a few days).
  - Naming convention: `type/short-description` or `type/issue-number`
  - Examples: `feat/user-login`, `fix/123-memory-leak`, `chore/update-deps`

### 3. Merging and Rebasing
- **Update frequently**: Regularly update your feature branch from `main` to avoid massive merge conflicts later.
  - Prefer `git pull --rebase origin main` to keep a linear history.
- **Squash on Merge**: When merging a feature branch into `main` via PR, use "Squash and Merge" to collapse the feature's WIP commits into a single cohesive commit on `main`.

## References
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)