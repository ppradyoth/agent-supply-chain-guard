# Agent Supply Chain Guard

Scan AI-agent skills, MCP manifests, and configuration before they enter a development environment or CI pipeline.

Agent Supply Chain Guard is a small, dependency-free starter scanner for the risks showing up in agent ecosystems: hidden instructions, suspicious network or process execution, embedded credentials, and overly broad tool permissions. It reports signals for human review; it does not claim to prove exploitability.

## Quick start

```bash
python -m agent_supply_chain_guard examples
python -m agent_supply_chain_guard scan path/to/skill-or-config
```

Exit status is `0` when no signals are found and `1` when findings are reported.

## What it checks

- prompt-injection language in `SKILL.md`, README, and manifest text
- shell/process execution and dangerous URL schemes
- likely secrets and private keys
- wildcard or unrestricted tool permissions
- suspicious Unicode control characters

## GitHub Action

```yaml
- uses: ppradyoth/agent-supply-chain-guard@main
  with:
    path: .
```

Pin the action to a reviewed commit in production. Findings are intentionally conservative and should be reviewed in context.

## Status

Early release. The project is designed to grow through narrowly scoped rules, reproducible fixtures, and provider-neutral examples.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Licensed under Apache-2.0.
