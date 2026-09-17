# Agent Supply Chain Guard

[![Tests](https://github.com/ppradyoth/agent-supply-chain-guard/actions/workflows/test.yml/badge.svg)](https://github.com/ppradyoth/agent-supply-chain-guard/actions/workflows/test.yml) [![Marketplace](https://img.shields.io/badge/GitHub%20Action-Marketplace-2088FF?logo=github)](https://github.com/marketplace/actions/agent-supply-chain-guard) [![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

<p align="center">
  <img src="assets/agent-supply-chain-guard-hero.jpg" alt="A blue shield protecting an AI agent from malicious supply-chain artifacts" width="100%">
</p>

<p align="center"><strong>Before your agent reads it, scan it.</strong></p>

## Your AI agent can be compromised by a file it reads.

An innocent-looking `SKILL.md`, MCP manifest, plugin, or README can contain instructions that redirect an agent, expose credentials, run commands, or request far more access than it needs.

**Agent Supply Chain Guard finds those signals before they reach your agent runtime.** It is free, local-first, dependency-free, and takes one command to run.

## See it catch a poisoned skill in 10 seconds

```bash
git clone https://github.com/ppradyoth/agent-supply-chain-guard.git
cd agent-supply-chain-guard
python -m agent_supply_chain_guard scan examples/poisoned-skill.md
```

Expected output:

```text
examples/poisoned-skill.md:5: [hidden-instruction] instruction-like text found in supply-chain content
examples/poisoned-skill.md:6: [process-execution] process execution reference
examples/poisoned-skill.md:7: [unrestricted-permission] broad or unrestricted permission
3 finding(s)
```

## Install and scan in 30 seconds

```bash
pipx install git+https://github.com/ppradyoth/agent-supply-chain-guard.git
agent-supply-chain-guard scan .
```

Or run it without installing:

```bash
python -m pip install agent-supply-chain-guard
agent-supply-chain-guard scan path/to/agent-project
```

A clean scan exits `0`. A scan with security signals exits `1`, so it works naturally in CI:

```bash
agent-supply-chain-guard scan . --quiet
```

## GitHub Action

```yaml
name: Agent security
on: [push, pull_request]
permissions: {}
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ppradyoth/agent-supply-chain-guard@v0.1.0
        with:
          path: .
```

Pin third-party actions to reviewed commits for production use.

## What it catches

| Signal | Why it matters |
| --- | --- |
| Hidden instruction language | Content can attempt to hijack agent behavior |
| Shell and process execution | A prompt can become a code-execution path |
| Credentials and private keys | Secrets can be copied into tools, logs, or outputs |
| Dangerous URL schemes | Files and network handlers can cross trust boundaries |
| Wildcard permissions | One compromised tool can gain excessive reach |
| Invisible Unicode controls | Text can look harmless while behaving differently |

JSON output is available for automation:

```bash
agent-supply-chain-guard scan . --format json
```

## Optional GPT or Claude review

Rules are the private, free baseline. If you want a second-pass explanation and prioritization, install one provider extra and export your own key in the shell:

```bash
pipx install 'git+https://github.com/ppradyoth/agent-supply-chain-guard.git#egg=agent-supply-chain-guard[openai]'
export OPENAI_API_KEY='your-key'
agent-supply-chain-guard scan . --ai-provider openai
```

Claude is the equivalent:

```bash
pipx install 'git+https://github.com/ppradyoth/agent-supply-chain-guard.git#egg=agent-supply-chain-guard[anthropic]'
export ANTHROPIC_API_KEY='your-key'
agent-supply-chain-guard scan . --ai-provider anthropic
```

Use `AGENT_GUARD_OPENAI_MODEL` or `AGENT_GUARD_ANTHROPIC_MODEL` to choose a model, or pass `--model`. The key is read from the environment and never printed or saved. Only matched finding evidence is sent for review; do not use AI mode on sensitive repositories unless that disclosure is acceptable. Provider fees and retention policies apply. AI output is advisory and does not alter the deterministic exit status.

## Important limitation

This is a **signal scanner**, not a proof of exploitability. Findings need human review, and a clean result does not make an agent or dependency safe. The goal is to make the first security check cheap enough that teams actually run it.

## Why now?

Agent security has moved beyond chatbot jailbreaks. MCP servers, agent skills, plugins, OAuth grants, and tool calls are becoming a software supply chain—and every new connection adds another place for untrusted instructions or excessive authority to enter.

## Contributing

Add a narrowly scoped rule with a harmless fixture and a test. See [CONTRIBUTING.md](CONTRIBUTING.md). Please never commit real credentials or client data.

Licensed under Apache-2.0.
