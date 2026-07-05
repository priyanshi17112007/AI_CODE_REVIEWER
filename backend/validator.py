import ast
import json
import os
import subprocess


def run_deterministic_syntax_check(content: str, filename: str) -> list:
    """
    Performs a multi-pass validation sweep.

    Returns:
        List[dict]:
        [
            {
                "line": int,
                "message": str,
                "type": str
            }
        ]
    """

    ext = os.path.splitext(filename)[1].lower()
    issues = []

    # -------------------------------------------------------
    # PASS 1: Native Python AST Syntax Check
    # -------------------------------------------------------
    if ext == ".py":
        try:
            ast.parse(content)
        except SyntaxError as e:
            issues.append(
                {
                    "line": e.lineno,
                    "message": f"SyntaxError: {e.msg}",
                    "type": "Compilation Blocker",
                }
            )

    # -------------------------------------------------------
    # PASS 2: Pylint Deep Structural Analysis
    # -------------------------------------------------------
    temp_filename = f"temp_{filename}"

    with open(temp_filename, "w", encoding="utf-8") as f:
        f.write(content)

    try:
        cmd = [
            "pylint",
            temp_filename,
            "--output-format=json",
            "--disable=C,R,W",
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        if result.stdout.strip():
            linter_data = json.loads(result.stdout)

            for issue in linter_data:
                issues.append(
                    {
                        "line": issue["line"],
                        "message": issue["message"],
                        "type": issue["message-id"],
                    }
                )

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

    return issues