import argparse
import json
from pathlib import Path
from .ai import explain
from .scanner import scan


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan AI-agent supply-chain content for security signals")
    sub = parser.add_subparsers(dest="command", required=True)
    target = sub.add_parser("scan")
    target.add_argument("path", type=Path)
    target.add_argument("--format", choices=("text", "json"), default="text")
    target.add_argument("--quiet", action="store_true", help="Only set the exit status")
    target.add_argument("--ai-provider", choices=("openai", "anthropic"), help="Add an optional AI review")
    target.add_argument("--model", help="Override the provider model")
    sub.add_parser("examples")
    args = parser.parse_args()
    if args.command == "examples":
        print("Try: agent-supply-chain-guard scan .")
        return 0
    findings = scan(args.path)
    if not args.quiet and args.format == "json":
        print(json.dumps([finding.__dict__ for finding in findings], indent=2))
    elif not args.quiet:
        for finding in findings:
            print(f"{finding.path}:{finding.line}: [{finding.rule}] {finding.message}")
        print(f"{len(findings)} finding(s)")
        if args.ai_provider:
            print(f"\nAI review ({args.ai_provider}):\n{explain(findings, args.ai_provider, args.model)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
