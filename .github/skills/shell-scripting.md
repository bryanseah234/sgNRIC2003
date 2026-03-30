---
name: shell-scripting
description: Best practices for writing robust, cross-platform shell scripts
---

# Shell Scripting Patterns

## When to Use
Apply these patterns when writing utility scripts, CI/CD automation, or local development setup scripts (Bash, sh, zsh, or PowerShell).

## Core Principles
1. **Fail Fast**: Scripts should exit immediately on error.
2. **Idempotency**: Running a script multiple times should have the same effect as running it once.
3. **Cross-Platform Consideration**: Be mindful of differences between Linux/macOS and Windows environments.

## Step-by-Step (Bash/sh)

### 1. The Safe Bash Preamble
Always start bash scripts with strict error handling:

```bash
#!/usr/bin/env bash
# Exit on error, undefined variables, and pipe failures
set -euo pipefail

# Optional: Enable debug mode via environment variable
if [[ "${DEBUG:-false}" == "true" ]]; then
    set -x
fi
```

### 2. Directory Resolution
Ensure scripts run reliably regardless of where they are invoked from:

```bash
# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Move to the project root (assuming script is in scripts/)
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_ROOT}"
```

### 3. Checking Dependencies
Fail early if required tools are missing:

```bash
check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        echo "Error: Required command '$1' is not installed." >&2
        exit 1
    fi
}

check_dependency "jq"
check_dependency "docker"
```

### 4. Cross-Platform Windows Batch/PowerShell
When writing `.bat` or `.ps1` files for Windows users:

**Batch (.bat) Safe Preamble:**
```cmd
@echo off
setlocal EnableDelayedExpansion
:: Your code here
```

**PowerShell (.ps1) Error Handling:**
```powershell
$ErrorActionPreference = "Stop"
$WarningPreference = "Continue"

# Check if running as admin
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning "This script may require Administrator privileges."
}
```

## References
- [Bash Strict Mode](http://redsymbol.net/articles/unofficial-bash-strict-mode/)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)