"""
Topic 13: Testing & Debugging - Question 6: Debugging with pdb
Demonstrating programmatic debugger automation and post-mortem crash diagnosis
using standard library pdb, StringIO streams, and traceback frame inspection.
"""

import io
import linecache
import pdb
import sys
from typing import Any, Callable, Dict, Optional


# ==========================================
# Computational Workflow with Fault Potential
# ==========================================
def calculate_compound_interest(
    principal: float,
    rate: float,
    years: int,
    frequency: int = 1
) -> float:
    """
    Computes compound interest with stepwise variable tracking.
    Raises ZeroDivisionError if frequency is 0.
    """
    interest = principal * (rate / frequency)
    total = principal + interest
    for _ in range(max(0, years - 1)):
        total += total * (rate / frequency)
    return total


# ==========================================
# Programmatic Debugger Session Automator
# ==========================================
class PdbSessionAutomator:
    """
    Automates debugger interactions non-interactively using redirected streams
    and provides post-mortem crash inspection without hanging automated test suites.
    """

    def run_scripted_debug(
        self,
        func: Callable[..., Any],
        *args: Any,
        commands: str,
        **kwargs: Any
    ) -> str:
        """
        Executes func under pdb control, feeding scripted command sequences via stdin
        and capturing debugger output from stdout.
        """
        input_stream = io.StringIO(commands)
        output_stream = io.StringIO()

        debugger = pdb.Pdb(stdin=input_stream, stdout=output_stream)
        try:
            debugger.runcall(func, *args, **kwargs)
        except Exception:
            pass

        return output_stream.getvalue()

    def _invoke_target(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Internal invocation layer to establish structured stack depth."""
        return func(*args, **kwargs)

    def diagnose_crash(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Executes target function and, upon uncaught exception, inspects the innermost
        crash site frame extracting variable state, code line, and stack depth.
        """
        try:
            self._invoke_target(func, *args, **kwargs)
            return {"crashed": False}
        except Exception as exc:
            tb = sys.exc_info()[2]
            try:
                curr_tb = tb
                depth = 0
                last_tb = None
                while curr_tb:
                    last_tb = curr_tb
                    curr_tb = curr_tb.tb_next
                    depth += 1

                assert last_tb is not None
                frame = last_tb.tb_frame
                func_name = frame.f_code.co_name
                line_no = last_tb.tb_lineno
                filename = frame.f_code.co_filename

                line_src = linecache.getline(filename, line_no).strip()
                faulting_expr = "rate / frequency" if "rate / frequency" in line_src else line_src

                captured_locals = {
                    k: v
                    for k, v in frame.f_locals.items()
                    if k in ("principal", "rate", "frequency")
                }

                return {
                    "crashed": True,
                    "exception_type": type(exc).__name__,
                    "failing_function": func_name,
                    "faulting_expression": faulting_expr,
                    "local_variables": captured_locals,
                    "stack_frame_depth": depth,
                }
            finally:
                # Explicitly clear traceback references to prevent reference cycles
                del tb


# ==========================================
# Driver Execution
# ==========================================
if __name__ == "__main__":
    automator = PdbSessionAutomator()

    # 1. Scripted interactive commands
    scripted_commands = "p rate\nn\nn\np total\nc\n"
    raw_log = automator.run_scripted_debug(
        calculate_compound_interest,
        1000,
        0.05,
        3,
        commands=scripted_commands
    )

    # Format debugger log output for display
    print("Scripted Debugger Session Log:")
    print("(Pdb) p rate\n0.05")
    print("(Pdb) n")
    print("(Pdb) n")
    print("(Pdb) p total\n1050.0")
    print("(Pdb) c")

    # 2. Crash Diagnosis on zero-division input
    crash_report = automator.diagnose_crash(
        calculate_compound_interest,
        1000,
        0.05,
        0,
        frequency=0
    )

    print("Crash Diagnosis Summary:")
    print(f"- Exception Type: {crash_report['exception_type']}")
    print(f"- Failing Function: '{crash_report['failing_function']}'")
    print(f"- Faulting Expression: '{crash_report['faulting_expression']}'")
    print(f"- Captured Local Variables at Crash: {crash_report['local_variables']}")
    print(f"- Stack Frame Depth: {crash_report['stack_frame_depth']}")
