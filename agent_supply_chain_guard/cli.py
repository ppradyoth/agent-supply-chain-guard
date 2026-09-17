import argparse
from pathlib import Path
from .scanner import scan


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan AI-agent supply-chain content for security signals")
    sub = parser.add_subparsers(dest="command", required=True)
    target = sub.add_parser("scan")
    target.add_argument("path", type=Path)
    sub.add_parser("examples")
    args = parser.parse_args()
    if args.command == "examples":
        print("Try: agent-supply-chain-guard scan .")
        return 0
    findings = scan(args.path)
    for finding in findings:
        print(f"{finding.path}:{finding.line}: [{finding.rule}] {finding.message}")
    print(f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
