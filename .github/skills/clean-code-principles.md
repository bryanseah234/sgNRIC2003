---
name: clean-code-principles
description: Language-agnostic principles for writing maintainable, readable, and robust code
---

# Clean Code Principles

## When to Use
These are universal software engineering principles that should be applied across all languages and frameworks in this workspace (Python, JS/TS, React, Go, etc.).

## Core Principles

### 1. Naming Matters (Intention-Revealing Names)
Variables, functions, and classes should tell you why they exist, what they do, and how they are used. If a name requires a comment, the name does not reveal its intent.

- **Bad**: `int d; // elapsed time in days`
- **Good**: `int elapsedTimeInDays;`
- **Bad**: `function handleData(data)`
- **Good**: `function processUserRegistration(userPayload)`

### 2. Functions Should Do One Thing (Single Responsibility Principle)
A function should do one thing, do it well, and do it only. If a function contains sections (e.g., "Step 1: Validate", "Step 2: Save", "Step 3: Notify"), it is doing too much and should be extracted into smaller functions.

### 3. Keep it DRY (Don't Repeat Yourself)
Avoid duplicating code. If you see the same logic in two or more places, extract it into a shared helper function, utility, or base class.
*Caveat: Do not prematurely abstract. Sometimes a little duplication is better than the wrong abstraction (AHA - Avoid Hasty Abstractions).*

### 4. Early Returns (Guard Clauses)
Avoid deep nesting of `if/else` statements. Check for error conditions or edge cases first, and return/throw immediately. This keeps the "happy path" un-nested at the bottom of the function.

**Bad:**
```javascript
function processOrder(order) {
  if (order != null) {
    if (order.isPaid) {
      if (order.items.length > 0) {
        // Do the actual work
        ship(order);
      } else {
        throw new Error("No items");
      }
    } else {
      throw new Error("Not paid");
    }
  }
}
```

**Good (Guard Clauses):**
```javascript
function processOrder(order) {
  if (order == null) return;
  if (!order.isPaid) throw new Error("Not paid");
  if (order.items.length === 0) throw new Error("No items");
  
  // Happy path
  ship(order);
}
```

### 5. Comments are Failures to Express Intent in Code
Do not use comments to explain *what* the code is doing (the code itself should be readable enough to tell you that). Use comments only to explain *why* the code is doing something (business rules, hacks, edge cases, or "gotchas").

## References
- Clean Code by Robert C. Martin
- [Refactoring Guru](https://refactoring.guru/)