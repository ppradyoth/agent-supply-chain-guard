from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Finding:
    rule: str
    path: str
    line: int
    message: str


RULES = (
    ("hidden-instruction", re.compile(r"ignore (?:all )?previous instructions|reveal (?:the )?(?:system|secret) prompt", re.I), "instruction-like text found in supply-chain content"),
    ("process-execution", re.compile(r"(?:child_process|subprocess|os\.system|shell=True|/bin/(?:sh|bash)|powershell)", re.I), "process execution reference"),
    ("dangerous-url", re.compile(r"(?:file|gopher|javascript|data)://", re.I), "non-HTTP URL scheme"),
    ("credential-material", re.compile(r"(?:BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY|AKIA[0-9A-Z]{16}|(?:api[_-]?key|secret[_-]?key)\s*[:=])", re.I), "possible credential material"),
    ("unrestricted-permission", re.compile(r"(?:permissions?|tools?)\s*[:=].*(?:\*|all|admin|unrestricted)", re.I), "broad or unrestricted permission"),
    ("unicode-control", re.compile(r"[\u202a-\u202e\u2066-\u2069\u200b\u200c\u200d]"), "invisible or directional Unicode control character"),
)


def scan(path: Path) -> list[Finding]:
    findings = []
    paths = [path] if path.is_file() else [p for p in path.rglob("*") if p.is_file() and p.stat().st_size < 2_000_000]
    for candidate in paths:
        try:
            lines = candidate.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(lines, 1):
            for rule, pattern, message in RULES:
                if pattern.search(line):
                    findings.append(Finding(rule, str(candidate), number, message))
    return findings
