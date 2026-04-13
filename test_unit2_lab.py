"""
Unified test file for Unit 2 Lab.
Automatically detects the student's tier (bronze, silver, gold) from the
filename and runs the appropriate tests.

Usage:
    pytest test_unit2_lab.py
"""

import ast
import glob
import importlib
import os
import sys

import pytest

# ── discover the student file and tier ─────────────────────────────────────────

_TIER_ORDER = ["gold", "silver", "bronze"]
_student_file = None
_tier = None

for t in _TIER_ORDER:
    pattern = os.path.join(os.path.dirname(__file__) or ".", f"unit2_lab_{t}.py")
    matches = glob.glob(pattern)
    if matches:
        _student_file = matches[0]
        _tier = t
        break

if _student_file is None:
    pytest.exit(
        "No student file found. Expected a file named "
        "unit2_lab_bronze.py, unit2_lab_silver.py, or unit2_lab_gold.py "
        "in the same directory as this test file.",
        returncode=1,
    )

_module_name = f"unit2_lab_{_tier}"

# ── import the student module ──────────────────────────────────────────────────

_mod = importlib.import_module(_module_name)


# ── AST helpers ────────────────────────────────────────────────────────────────

def _source() -> str:
    with open(_student_file, encoding="utf-8") as f:
        return f.read()


def _tree() -> ast.Module:
    return ast.parse(_source())


def _module_docstring() -> str:
    return ast.get_docstring(_tree()) or ""


def _func_node(func_name: str) -> ast.FunctionDef | None:
    for node in ast.walk(_tree()):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return node
    return None


def _func_docstring(func_name: str) -> str:
    node = _func_node(func_name)
    return ast.get_docstring(node) or "" if node else ""


def _func_source(func_name: str) -> str:
    node = _func_node(func_name)
    return ast.get_source_segment(_source(), node) or "" if node else ""


def _annotation_str(annotation) -> str:
    if annotation is None:
        return ""
    return ast.unparse(annotation)


# ── helpers for conditional tier tests ─────────────────────────────────────────

def _is_tier(*tiers: str) -> bool:
    return _tier in tiers


def _skip_unless(*tiers: str):
    return pytest.mark.skipif(
        not _is_tier(*tiers),
        reason=f"Only runs for tier(s): {', '.join(tiers)}",
    )


# ── header comment tests ──────────────────────────────────────────────────────

class TestHeaderComments:

    def test_header_exists(self):
        assert _module_docstring().strip(), (
            f"Missing module-level header comment. Add a triple-quoted string at "
            f"the top of {_module_name}.py with author, date, and a short description."
        )

    def test_header_has_author(self):
        assert "author" in _module_docstring().lower(), (
            "Header comment is missing an 'author' line.  Example:  author: Your Name"
        )

    def test_header_has_date(self):
        assert "date" in _module_docstring().lower(), (
            "Header comment is missing a 'date' line.  Example:  date: April 10, 2026"
        )

    def test_header_has_description(self):
        lines = [
            ln.strip()
            for ln in _module_docstring().splitlines()
            if ln.strip() and not ln.lower().lstrip().startswith(("author", "date"))
        ]
        assert lines, (
            "Header comment should include a short description of the file."
        )


# ── Bronze docstring tests (students write their own) ─────────────────────────

_BRONZE_FUNCS = ["total_time", "slowest_solve", "fastest_solve"]


@_skip_unless("bronze", "silver", "gold")
class TestBronzeDocstrings:

    @pytest.mark.parametrize("func_name", _BRONZE_FUNCS)
    def test_docstring_exists(self, func_name):
        ds = _func_docstring(func_name).strip()
        assert ds, (
            f"'{func_name}' is missing a docstring. Add a triple-quoted string "
            "as the very first statement of the function."
        )

    @pytest.mark.parametrize("func_name", _BRONZE_FUNCS)
    def test_docstring_not_empty(self, func_name):
        ds = _func_docstring(func_name).strip()
        assert len(ds) > 20, (
            f"'{func_name}' docstring is too short. Include a description, "
            "Args, Returns, and Example sections."
        )

    def test_main_docstring_exists(self):
        assert _func_docstring("main").strip(), (
            "main() is missing a docstring."
        )

    @pytest.mark.parametrize("func_name", _BRONZE_FUNCS)
    def test_docstring_has_description(self, func_name):
        ds = _func_docstring(func_name)
        first_line = next((ln.strip() for ln in ds.splitlines() if ln.strip()), "")
        assert first_line and first_line.lower() not in ("args:", "returns:", "example:", "examples:"), (
            f"'{func_name}' docstring should start with a plain-English description "
            "of what the function does before listing Args/Returns/Example."
        )

    @pytest.mark.parametrize("func_name", _BRONZE_FUNCS)
    def test_docstring_has_args_section(self, func_name):
        ds = _func_docstring(func_name).lower()
        assert "args:" in ds or "arguments:" in ds or "parameters:" in ds, (
            f"'{func_name}' docstring is missing an 'Args:' section."
        )

    @pytest.mark.parametrize("func_name", _BRONZE_FUNCS)
    def test_docstring_has_returns_section(self, func_name):
        ds = _func_docstring(func_name).lower()
        assert "returns:" in ds or "return:" in ds, (
            f"'{func_name}' docstring is missing a 'Returns:' section."
        )

    @pytest.mark.parametrize("func_name", _BRONZE_FUNCS)
    def test_docstring_has_example_section(self, func_name):
        ds = _func_docstring(func_name).lower()
        assert "example" in ds, (
            f"'{func_name}' docstring is missing an 'Example' or 'Examples:' section."
        )


# ── Bronze type annotation tests ──────────────────────────────────────────────

@_skip_unless("bronze", "silver", "gold")
class TestBronzeTypeAnnotations:

    @pytest.mark.parametrize("func_name", _BRONZE_FUNCS)
    def test_param_annotated(self, func_name):
        node = _func_node(func_name)
        assert node, f"{func_name} function not found."
        unannotated = [
            arg.arg for arg in node.args.args if arg.annotation is None
        ]
        assert not unannotated, (
            f"'{func_name}' parameter(s) missing type annotations: {unannotated}."
        )

    @pytest.mark.parametrize("func_name", _BRONZE_FUNCS)
    def test_param_type(self, func_name):
        node = _func_node(func_name)
        assert node, f"{func_name} function not found."
        for arg in node.args.args:
            ann = _annotation_str(arg.annotation)
            assert ann == "list[int]", (
                f"Parameter '{arg.arg}' in {func_name} should be annotated as "
                f"'list[int]', got '{ann}'."
            )

    @pytest.mark.parametrize("func_name", _BRONZE_FUNCS)
    def test_return_annotated(self, func_name):
        node = _func_node(func_name)
        assert node, f"{func_name} function not found."
        assert node.returns is not None, (
            f"'{func_name}' is missing a return type annotation."
        )

    @pytest.mark.parametrize("func_name", _BRONZE_FUNCS)
    def test_return_type(self, func_name):
        node = _func_node(func_name)
        assert node and node.returns is not None
        ret = _annotation_str(node.returns)
        assert ret == "int", (
            f"'{func_name}' return type should be 'int', got '{ret}'."
        )


# ── Bronze IPO comment tests ──────────────────────────────────────────────────

@_skip_unless("bronze", "silver", "gold")
class TestBronzeIPOComments:

    def test_ipo_input_comment(self):
        src = _func_source("main").lower()
        assert "# input" in src, (
            "main() is missing an '# Input' comment."
        )

    def test_ipo_output_comment(self):
        src = _func_source("main").lower()
        has_output = (
            "# output" in src
            or "processing/output" in src
            or "processing / output" in src
        )
        assert has_output, (
            "main() is missing an '# Output' or '# Processing/Output' comment."
        )


# ── Bronze functionality tests ────────────────────────────────────────────────

@_skip_unless("bronze", "silver", "gold")
class TestBronzeFunctionality:

    def test_total_time_given_list(self):
        total_time = getattr(_mod, "total_time")
        assert total_time([12, 45, 8, 23, 31, 17, 52, 9]) == 197

    def test_total_time_other_list(self):
        total_time = getattr(_mod, "total_time")
        assert total_time([5, 10, 15]) == 30

    def test_total_time_single(self):
        total_time = getattr(_mod, "total_time")
        assert total_time([42]) == 42

    def test_slowest_solve_given_list(self):
        slowest_solve = getattr(_mod, "slowest_solve")
        assert slowest_solve([12, 45, 8, 23, 31, 17, 52, 9]) == 52

    def test_slowest_solve_other_list(self):
        slowest_solve = getattr(_mod, "slowest_solve")
        assert slowest_solve([3, 7, 1]) == 7

    def test_fastest_solve_given_list(self):
        fastest_solve = getattr(_mod, "fastest_solve")
        assert fastest_solve([12, 45, 8, 23, 31, 17, 52, 9]) == 8

    def test_fastest_solve_other_list(self):
        fastest_solve = getattr(_mod, "fastest_solve")
        assert fastest_solve([3, 7, 1]) == 1


@_skip_unless("bronze")
class TestBronzeMainOutput:

    def test_main_output(self, capsys):
        main = getattr(_mod, "main")
        main()
        captured = capsys.readouterr().out
        assert "197" in captured, "main() should print the total time (197)."
        assert "52" in captured, "main() should print the slowest solve (52)."
        assert "8" in captured, "main() should print the fastest solve (8)."


# ── Silver docstring tests ────────────────────────────────────────────────────

@_skip_unless("silver", "gold")
class TestSilverDocstrings:

    def test_apply_penalty_docstring_exists(self):
        ds = _func_docstring("apply_penalty").strip()
        assert ds, "'apply_penalty' is missing a docstring."

    def test_main_docstring_exists(self):
        assert _func_docstring("main").strip(), "main() is missing a docstring."


# ── Silver type annotation tests ──────────────────────────────────────────────

@_skip_unless("silver", "gold")
class TestSilverTypeAnnotations:

    def test_apply_penalty_param_annotated(self):
        node = _func_node("apply_penalty")
        assert node, "apply_penalty function not found."
        unannotated = [
            arg.arg for arg in node.args.args if arg.annotation is None
        ]
        assert not unannotated, (
            f"apply_penalty parameter(s) missing type annotations: {unannotated}."
        )

    def test_apply_penalty_param_type(self):
        node = _func_node("apply_penalty")
        assert node, "apply_penalty function not found."
        for arg in node.args.args:
            ann = _annotation_str(arg.annotation)
            assert ann == "int", (
                f"Parameter '{arg.arg}' in apply_penalty should be annotated as "
                f"'int', got '{ann}'."
            )

    def test_apply_penalty_return_annotated(self):
        node = _func_node("apply_penalty")
        assert node, "apply_penalty function not found."
        assert node.returns is not None, (
            "apply_penalty is missing a return type annotation."
        )

    def test_apply_penalty_return_type(self):
        node = _func_node("apply_penalty")
        assert node and node.returns is not None
        ret = _annotation_str(node.returns)
        assert ret == "int", (
            f"apply_penalty return type should be 'int', got '{ret}'."
        )


# ── Silver IPO comment tests ──────────────────────────────────────────────────

@_skip_unless("silver", "gold")
class TestSilverIPOComments:

    def test_ipo_input_comment(self):
        src = _func_source("main").lower()
        assert "# input" in src, "main() is missing an '# Input' comment."

    def test_ipo_processing_comment(self):
        src = _func_source("main").lower()
        assert "# processing" in src, "main() is missing a '# Processing' comment."

    def test_ipo_output_comment(self):
        src = _func_source("main").lower()
        has_output = (
            "# output" in src
            or "processing/output" in src
            or "processing / output" in src
        )
        assert has_output, (
            "main() is missing an '# Output' or '# Processing/Output' comment."
        )


# ── Silver functionality tests ────────────────────────────────────────────────

@_skip_unless("silver", "gold")
class TestSilverFunctionality:

    def test_apply_penalty_below_threshold(self):
        apply_penalty = getattr(_mod, "apply_penalty")
        assert apply_penalty(8) == 8, (
            "apply_penalty(8) should return 8 (below 15, no penalty)."
        )

    def test_apply_penalty_at_threshold(self):
        apply_penalty = getattr(_mod, "apply_penalty")
        assert apply_penalty(15) == 30, (
            "apply_penalty(15) should return 30 (15 or more gets doubled)."
        )

    def test_apply_penalty_above_threshold(self):
        apply_penalty = getattr(_mod, "apply_penalty")
        assert apply_penalty(23) == 46, "apply_penalty(23) should return 46."

    def test_apply_penalty_just_below(self):
        apply_penalty = getattr(_mod, "apply_penalty")
        assert apply_penalty(14) == 14, (
            "apply_penalty(14) should return 14 (below 15, no penalty)."
        )

    def test_apply_penalty_large(self):
        apply_penalty = getattr(_mod, "apply_penalty")
        assert apply_penalty(52) == 104, "apply_penalty(52) should return 104."


@_skip_unless("silver")
class TestSilverMainOutput:

    def test_main_output(self, capsys):
        main = getattr(_mod, "main")
        main()
        captured = capsys.readouterr().out
        assert "197" in captured, "main() should print the original total time (197)."
        assert "52" in captured, "main() should print the slowest solve (52)."
        assert "8" in captured, "main() should print the fastest solve (8)."
        assert "365" in captured, "main() should print the penalized total time (365)."


# ── Gold docstring tests ──────────────────────────────────────────────────────

@_skip_unless("gold")
class TestGoldDocstrings:

    def test_calculate_power_docstring_exists(self):
        ds = _func_docstring("calculate_power").strip()
        assert ds, "'calculate_power' is missing a docstring."

    def test_main_docstring_exists(self):
        assert _func_docstring("main").strip(), "main() is missing a docstring."


# ── Gold type annotation tests ────────────────────────────────────────────────

@_skip_unless("gold")
class TestGoldTypeAnnotations:

    def test_calculate_power_param_annotated(self):
        node = _func_node("calculate_power")
        assert node, "calculate_power function not found."
        unannotated = [
            arg.arg for arg in node.args.args if arg.annotation is None
        ]
        assert not unannotated, (
            f"calculate_power parameter(s) missing type annotations: {unannotated}."
        )

    def test_calculate_power_param_type(self):
        node = _func_node("calculate_power")
        assert node, "calculate_power function not found."
        for arg in node.args.args:
            ann = _annotation_str(arg.annotation)
            assert ann == "str", (
                f"Parameter '{arg.arg}' in calculate_power should be annotated as "
                f"'str', got '{ann}'."
            )

    def test_calculate_power_return_annotated(self):
        node = _func_node("calculate_power")
        assert node, "calculate_power function not found."
        assert node.returns is not None, (
            "calculate_power is missing a return type annotation."
        )

    def test_calculate_power_return_type(self):
        node = _func_node("calculate_power")
        assert node and node.returns is not None
        ret = _annotation_str(node.returns)
        assert ret == "int", (
            f"calculate_power return type should be 'int', got '{ret}'."
        )


# ── Gold IPO comment tests ────────────────────────────────────────────────────

@_skip_unless("gold")
class TestGoldIPOComments:

    def test_ipo_input_comment(self):
        src = _func_source("main").lower()
        assert "# input" in src, "main() is missing an '# Input' comment."

    def test_ipo_processing_comment(self):
        src = _func_source("main").lower()
        assert "# processing" in src, "main() is missing a '# Processing' comment."

    def test_ipo_output_comment(self):
        src = _func_source("main").lower()
        has_output = (
            "# output" in src
            or "processing/output" in src
            or "processing / output" in src
        )
        assert has_output, (
            "main() is missing an '# Output' or '# Processing/Output' comment."
        )


# ── Gold functionality tests ──────────────────────────────────────────────────

@_skip_unless("gold")
class TestGoldFunctionality:

    def test_calculate_power_rascal(self):
        calculate_power = getattr(_mod, "calculate_power")
        assert calculate_power("Rascal") == 3, (
            "calculate_power('Rascal') should return 3 (R + s + c)."
        )

    def test_calculate_power_lowercase_rascal(self):
        calculate_power = getattr(_mod, "calculate_power")
        assert calculate_power("rascal") == 2, (
            "calculate_power('rascal') should return 2 (s + c). "
            "Lowercase 'r' is not a power letter."
        )

    def test_calculate_power_tim(self):
        calculate_power = getattr(_mod, "calculate_power")
        assert calculate_power("Tim") == 1, (
            "calculate_power('Tim') should return 1 (T only)."
        )

    def test_calculate_power_no_power(self):
        calculate_power = getattr(_mod, "calculate_power")
        assert calculate_power("John") == 0, (
            "calculate_power('John') should return 0 (no power letters)."
        )

    def test_calculate_power_all_power(self):
        calculate_power = getattr(_mod, "calculate_power")
        assert calculate_power("cRsT") == 4, (
            "calculate_power('cRsT') should return 4 (all four are power letters)."
        )

    def test_calculate_power_case_sensitive_r(self):
        calculate_power = getattr(_mod, "calculate_power")
        assert calculate_power("R") == 1, "calculate_power('R') should return 1."
        assert calculate_power("r") == 0, (
            "calculate_power('r') should return 0 (lowercase r is not a power letter)."
        )

    def test_calculate_power_case_sensitive_t(self):
        calculate_power = getattr(_mod, "calculate_power")
        assert calculate_power("T") == 1, "calculate_power('T') should return 1."
        assert calculate_power("t") == 0, (
            "calculate_power('t') should return 0 (lowercase t is not a power letter)."
        )

    def test_calculate_power_repeated_letters(self):
        calculate_power = getattr(_mod, "calculate_power")
        assert calculate_power("ccesss") == 5, (
            "calculate_power('ccesss') should return 5 (2 c's + 3 s's)."
        )

    def test_main_collects_six_names(self, monkeypatch, capsys):
        main = getattr(_mod, "main")
        inputs = iter(["Rascal", "Tim", "John", "cRsT", "Alice", "Bob"])
        monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
        main()
        captured = capsys.readouterr().out
        # Rascal=3, Tim=1, John=0, cRsT=4, Alice=1, Bob=0 => sum=9
        assert "197" in captured, "main() should print the total time (197)."
        assert "52" in captured, "main() should print the slowest solve (52)."
        assert "8" in captured, "main() should print the fastest solve (8)."
        assert "365" in captured, "main() should print the penalized total time (365)."
        assert "9" in captured, (
            f"Expected the sum of power counts to be 9, got output: '{captured}'"
        )
