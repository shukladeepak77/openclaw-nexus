# TOOLS.md — Open Claw Virtual Company Tool System

## Overview

This file defines **tool access and permissions** for each role in the Open Claw Virtual Company.

Tools represent **real execution capabilities** such as:
- creating files
- running shell commands
- managing Git
- interacting with CI/CD systems

Each role has **strictly controlled access**.

No role should use tools outside its allowed scope.

---

## Available Tools

### 1. File System Tool

Capabilities:
- Create files
- Modify files
- Read files
- Create directories

Used for:
- Writing code
- Creating project structure
- Updating configuration files

---

### 2. Shell Tool

Capabilities:
- Run terminal commands
- Execute scripts
- Run tests
- Install dependencies

Used for:
- Running Python scripts
- Running unittest / pytest
- Executing build commands

---

### 3. Git Tool

Capabilities:
- git add
- git commit
- git push
- git pull
- git status

Used for:
- Version control
- Committing changes
- Syncing with remote repository

---

### 4. CI/CD Tool (GitHub Actions)

Capabilities:
- Create/update workflow files
- Trigger CI pipelines (via push)
- Validate builds through CI

Used for:
- Automating tests
- Ensuring code quality
- Running pipelines on push/PR

---

### 5. Analysis / Review Tool

Capabilities:
- Analyze code
- Validate logic
- Identify bugs
- Suggest improvements

Used for:
- QA validation
- Code review
- Test validation

---

## Tool Access by Role

### Manager

Tools: NONE

Responsibilities:
- Planning only
- Delegation only

Restrictions:
- Must NOT create files
- Must NOT run commands
- Must NOT modify code

---

### Researcher

Tools:
- Analysis / Review Tool (read-only usage)

Responsibilities:
- Research and comparison

Restrictions:
- Must NOT create files
- Must NOT run shell commands
- Must NOT modify system state

---

### Developer

Tools:
- File System Tool

Responsibilities:
- Create and modify code
- Build project structure

Restrictions:
- Must NOT run shell commands unless explicitly required
- Must NOT perform Git operations

---

### QA (Reviewer)

Tools:
- Analysis / Review Tool
- Shell Tool (for running tests only)

Responsibilities:
- Validate outputs
- Run tests
- Check correctness

Restrictions:
- Must NOT create new features from scratch
- Must NOT perform Git operations

---

### DevOps

Tools:
- Shell Tool
- Git Tool
- CI/CD Tool

Responsibilities:
- Execute commands
- Run scripts
- Manage Git operations
- Handle CI/CD workflows

Restrictions:
- Must NOT change application logic
- Must NOT create business features

---

## Execution Rules

- Developer creates files
- QA validates outputs
- DevOps executes commands and manages Git

Tools must be used **only by the appropriate role**.

---

## Safety Rules

The following actions REQUIRE explicit user confirmation:

- Deleting files or directories
- Overwriting critical files
- Running destructive shell commands
- Deploying to external systems
- Pushing to production branches
- Exposing secrets or credentials

---

## Command Execution Guidelines

- Prefer safe, minimal commands
- Avoid chaining destructive commands
- Always verify before execution
- Provide command output in logs

---

## Logging Requirements

Whenever a tool is used, the system must log:

- Tool name
- Action performed
- Target (file, command, repo, etc.)
- Result/output

Example:

```text
DevOps:
- Shell Tool → python3 -m unittest
- Result → All tests passed
