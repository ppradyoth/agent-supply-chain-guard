import os
from typing import Sequence

from .scanner import Finding


def _prompt(findings: Sequence[Finding]) -> str:
    evidence = "\n".join(f"- {f.path}:{f.line} [{f.rule}] {f.message}" for f in findings)
    return (
        "You are reviewing conservative AI-agent supply-chain scanner signals. "
        "Do not invent evidence. For each signal, explain likely impact, confidence "
        "(low/medium/high), and one safe remediation. Clearly label uncertainty.\n\n"
        f"Signals:\n{evidence}"
    )


def explain(findings: Sequence[Finding], provider: str, model: str | None = None) -> str:
    if not findings:
        return "No scanner signals were found; AI review was skipped."
    prompt = _prompt(findings)
    if provider == "openai":
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install the OpenAI extra: pip install 'agent-supply-chain-guard[openai]'") from exc
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.responses.create(
            model=model or os.environ.get("AGENT_GUARD_OPENAI_MODEL", "gpt-5-mini"),
            instructions="You are a precise application-security reviewer.",
            input=prompt,
            store=False,
        )
        return response.output_text
    if provider == "anthropic":
        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise RuntimeError("Install the Anthropic extra: pip install 'agent-supply-chain-guard[anthropic]'") from exc
        client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model=model or os.environ.get("AGENT_GUARD_ANTHROPIC_MODEL", "claude-sonnet-4-6"),
            max_tokens=1200,
            system="You are a precise application-security reviewer.",
            messages=[{"role": "user", "content": prompt}],
        )
        return "\n".join(block.text for block in response.content if hasattr(block, "text"))
    raise ValueError(f"Unsupported AI provider: {provider}")
