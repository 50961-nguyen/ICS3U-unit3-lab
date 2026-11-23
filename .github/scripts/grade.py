"""Run the lab tests and report a tier-capped score out of 100."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
TIERS = (("gold", 100), ("silver", 85), ("bronze", 70))


def report(message: str) -> None:
    print(message, flush=True)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as output:
            output.write(message + "\n")


def main() -> int:
    tier = next(
        ((name, cap) for name, cap in TIERS
         if (ROOT / f"unit3_lab_{name}.py").is_file()),
        None,
    )
    if tier is None:
        report(
            "## Autograding: 0.00/100\n\n"
            "No student file found. Submit unit3_lab_bronze.py, "
            "unit3_lab_silver.py, or unit3_lab_gold.py."
        )
        return 1

    name, cap = tier
    with tempfile.TemporaryDirectory() as temp_dir:
        results = Path(temp_dir) / "pytest-results.xml"
        try:
            completed = subprocess.run(
                [
                    sys.executable, "-m", "pytest", "test_unit3_lab.py",
                    "-v", "--junitxml", str(results),
                ],
                cwd=ROOT,
                timeout=120,
                check=False,
            )
        except subprocess.TimeoutExpired:
            report(f"## Autograding: 0.00/100\n\n{name.title()} tests timed out.")
            return 1

        if completed.returncode not in (0, 1):
            report(
                f"## Autograding: 0.00/100\n\n"
                f"Pytest could not complete normally (exit code {completed.returncode})."
            )
            return 1

        try:
            cases = ET.parse(results).getroot().findall(".//testcase")
        except (OSError, ET.ParseError) as error:
            report(f"## Autograding: 0.00/100\n\nCould not read pytest results: {error}")
            return 1

    applicable = [case for case in cases if case.find("skipped") is None]
    if not applicable:
        report("## Autograding: 0.00/100\n\nNo applicable tests were run.")
        return 1

    passed = sum(
        case.find("failure") is None and case.find("error") is None
        for case in applicable
    )
    score = cap * passed / len(applicable)
    report(
        f"## Autograding: {score:.2f}/100\n\n"
        f"Tier: {name.title()} (maximum {cap}/100)  \n"
        f"Tests passed: {passed}/{len(applicable)} "
        "(skipped tests excluded)."
    )
    return 0 if completed.returncode == 0 and passed == len(applicable) else 1


if __name__ == "__main__":
    sys.exit(main())
