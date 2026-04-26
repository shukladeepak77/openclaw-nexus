# TOOLS.md — Open Claw Nexus Tool System

## Overview

Tools define what each agent is allowed to do.

Each agent must use only the tools assigned to it.

No agent should use tools outside its scope.

---

## Available Tools

### 1. File System Tool

Capabilities:
- Read files
- Write files
- Create files
- Modify files

Allowed Agents:
- Nexus-Builder
- Nexus-Reviewer

Restrictions:
- Must not overwrite important files without confirmation

---

### 2. Shell / Command Tool

Capabilities:
- Run shell commands
- Execute scripts
- Run programs

Allowed Agents:
- Nexus-Builder

Restrictions:
- Must not run destructive commands
- Must ask for user confirmation before risky operations

Examples of restricted commands:
- rm
- chmod
- sudo operations

---

### 3. Research / Search Tool

Capabilities:
- Search for information
- Retrieve documentation
- Compare tools and technologies

Allowed Agents:
- Nexus-Scout

Restrictions:
- Must only be used when explicitly required by Nexus-Core

---

### 4. Code Generation Tool

Capabilities:
- Generate code
- Modify code
- Suggest improvements

Allowed Agents:
- Nexus-Builder

---

### 5. Review / Analysis Tool

Capabilities:
- Analyze code
- Detect issues
- Suggest improvements

Allowed Agents:
- Nexus-Reviewer

---

## Tool Usage Rules

- Agents must only use tools assigned to them
- Nexus-Core does NOT directly use tools
- Nexus-Core only delegates
- All risky actions require user approval
- Prefer safe and minimal operations

---

## Safety Enforcement

Before using any tool, agents must check:

- Is this tool allowed for me?
- Is this action safe?
- Do I need user confirmation?

If unsure → ask the user

---

## System Philosophy for Tools

Start simple → use minimal tools → expand gradually

Do not use all tools at once

Introduce tools only when needed

## Execution Enforcement

If a task requires creating files, modifying files, or running commands:

- The agent MUST use the appropriate tool to perform the action
- The agent MUST NOT only describe the steps
- The agent MUST execute and then show the result

Examples:
- “Create a file” → use File System Tool
- “Run a script” → use Shell Tool

Failure to execute is considered an incomplete response.
