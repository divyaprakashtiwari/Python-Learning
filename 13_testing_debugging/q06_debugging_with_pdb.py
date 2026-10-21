"""
Topic 13: Testing and Debugging
Question 06: Debugging with pdb

A comprehensive, production-grade guide to debugging, stack inspection, and post-mortem
analysis in Python. Covers PYTHONBREAKPOINT hook configuration, scriptable pdb.Pdb execution
with custom I/O streams, post-mortem debugging, stack frame walking via inspect, line-by-line
tracing with sys.settrace, variable watchpoints, conditional breakpoints, rich traceback
formatting, an in-process diagnostic REPL, and an architectural CrashDumpEngine.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import pdb
import sys
import inspect
import traceback
import io
import os
import json
from typing import List, Dict, Any, Optional


# =====================================================================
# Q1: breakpoint() and sys.breakpointhook Mechanics
# =====================================================================
def q1_breakpoint_hook_mechanics():
    """
    Demonstrates Python 3.7+ breakpoint() behavior and customizing
    sys.breakpointhook to intercept debugging breakpoints programmatically.
    """
    intercepted_frames = []

    def custom_breakpoint_hook(*args, **kwargs):
        # Capture caller's frame instead of dropping into interactive shell
        frame = inspect.currentframe().f_back
        intercepted_frames.append({
            "func": frame.f_code.co_name,
            "line": frame.f_lineno,
            "locals": dict(frame.f_locals)
        })

    old_hook = sys.breakpointhook
    try:
        sys.breakpointhook = custom_breakpoint_hook

        # Execute code containing breakpoint()
        def sample_calculation(val: int):
            factor = 4
            result = val * factor
            breakpoint()
            return result

        res = sample_calculation(10)
        assert res == 40
        assert len(intercepted_frames) == 1
        assert intercepted_frames[0]["func"] == "sample_calculation"
        assert intercepted_frames[0]["locals"]["val"] == 10
        assert intercepted_frames[0]["locals"]["factor"] == 4
        assert intercepted_frames[0]["locals"]["result"] == 40

    finally:
        sys.breakpointhook = old_hook

    print("=== Q1: breakpoint() & sys.breakpointhook Interception Verified ===")


# =====================================================================
# Q2: Scriptable pdb.Pdb with Custom I/O Streams
# =====================================================================
def q2_scriptable_pdb_execution():
    """
    Demonstrates running pdb non-interactively by supplying a scripted stdin stream
    (e.g., print variables, step, continue) and capturing pdb stdout output.
    """
    def target_function(x, y):
        z = x + y
        return z

    # Scripted pdb commands:
    # 1. 'p x' (print x)
    # 2. 'p y' (print y)
    # 3. 'c' (continue execution)
    commands = "p x\np y\nc\n"
    stdin_stream = io.StringIO(commands)
    stdout_stream = io.StringIO()

    debugger = pdb.Pdb(stdin=stdin_stream, stdout=stdout_stream)

    # Run target_function under debugger
    result = debugger.runcall(target_function, 15, 25)
    assert result == 40

    output = stdout_stream.getvalue()
    # Output must contain our printed values '15' and '25'
    assert "15" in output
    assert "25" in output

    print("=== Q2: Scriptable pdb.Pdb with Custom I/O Verified ===")


# =====================================================================
# Q3: Post-Mortem Crash Inspection (pdb.post_mortem)
# =====================================================================
def faulty_nested_calculation(a, b):
    return a / b


def q3_post_mortem_crash_inspection():
    """
    Demonstrates capturing the traceback of an unhandled exception and
    inspecting crash frame locals post-mortem.
    """
    captured_tb = None
    try:
        faulty_nested_calculation(100, 0)
    except ZeroDivisionError:
        # sys.exc_info() returns (type, value, traceback)
        _, _, captured_tb = sys.exc_info()

    assert captured_tb is not None

    # Run post-mortem debugger with scripted command 'p a\np b\nc\n'
    stdin_mock = io.StringIO("p a\np b\nc\n")
    stdout_mock = io.StringIO()
    debugger = pdb.Pdb(stdin=stdin_mock, stdout=stdout_mock)
    debugger.reset()
    debugger.interaction(None, captured_tb)

    diag_output = stdout_mock.getvalue()
    assert "100" in diag_output  # value of 'a'
    assert "0" in diag_output    # value of 'b'

    print("=== Q3: Post-Mortem Crash Inspection Verified ===")


# =====================================================================
# Q4: Stack Frame Walking with inspect
# =====================================================================
def level_three():
    frame = inspect.currentframe()
    frames = []
    curr = frame
    while curr is not None:
        frames.append(curr.f_code.co_name)
        curr = curr.f_back
    return frames


def level_two():
    return level_three()


def level_one():
    return level_two()


def q4_stack_frame_walking():
    call_stack = level_one()
    # Call stack must trace back: level_three -> level_two -> level_one -> q4_stack_frame_walking
    assert call_stack[0] == "level_three"
    assert call_stack[1] == "level_two"
    assert call_stack[2] == "level_one"
    assert call_stack[3] == "q4_stack_frame_walking"

    print("=== Q4: Stack Frame Walking with inspect Verified ===")


# =====================================================================
# Q5: Low-Level Line Tracing with sys.settrace
# =====================================================================
def q5_line_level_sys_settrace():
    """
    Demonstrates writing a custom Python interpreter trace function
    tracking function calls, lines executed, and return values.
    """
    trace_events: List[Tuple[str, str, int]] = []

    def tracer(frame, event, arg):
        func_name = frame.f_code.co_name
        # Only trace functions inside this module
        if func_name in ("math_logic",):
            trace_events.append((event, func_name, frame.f_lineno))
        return tracer

    def math_logic(n):
        total = 0
        for i in range(n):
            total += i
        return total

    old_trace = sys.gettrace()
    try:
        sys.settrace(tracer)
        res = math_logic(3)
        assert res == 3
    finally:
        sys.settrace(old_trace)

    # Must contain 'call', multiple 'line' events, and 'return'
    events = [e[0] for e in trace_events]
    assert "call" in events
    assert "line" in events
    assert "return" in events

    print("=== Q5: Low-Level Tracing with sys.settrace Verified ===")


# =====================================================================
# Q6: Variable Watchpoint Tracing
# =====================================================================
def q6_variable_watchpoint_tracer():
    """
    Implements a debugger watchpoint that records every state change
    of a monitored local variable within a target scope.
    """
    watch_history: List[int] = []

    def make_watchpoint(var_name: str):
        last_val = None

        def tracer(frame, event, arg):
            nonlocal last_val
            if event in ("line", "return"):
                if var_name in frame.f_locals:
                    curr_val = frame.f_locals[var_name]
                    if curr_val != last_val:
                        last_val = curr_val
                        watch_history.append(curr_val)
            return tracer
        return tracer

    def loop_accumulator():
        counter = 0
        counter = counter + 10
        counter = counter + 20
        counter = counter + 30
        return counter

    old_trace = sys.gettrace()
    try:
        sys.settrace(make_watchpoint("counter"))
        loop_accumulator()
    finally:
        sys.settrace(old_trace)

    # Watchpoint recorded state progression of 'counter'
    assert watch_history == [0, 10, 30, 60]

    print("=== Q6: Variable Watchpoint Tracing Verified ===")


# =====================================================================
# Q7: Rich Formatted Traceback Extraction
# =====================================================================
def faulty_nested_operation():
    def step_a():
        step_b()

    def step_b():
        raise KeyError("missing_database_secret_key")

    step_a()


def q7_formatted_traceback_extraction():
    try:
        faulty_nested_operation()
    except KeyError as exc:
        # Extract structured stack summary
        tb = exc.__traceback__
        stack_summary = traceback.extract_tb(tb)
        formatted_str = traceback.format_exc()

    # 1. Stack summary objects
    frame_names = [frame.name for frame in stack_summary]
    assert "faulty_nested_operation" in frame_names
    assert "step_a" in frame_names
    assert "step_b" in frame_names

    # 2. String representation
    assert "KeyError: 'missing_database_secret_key'" in formatted_str
    assert "step_b" in formatted_str

    print("=== Q7: Rich Formatted Traceback Extraction Verified ===")


# =====================================================================
# Q8: Programmatic Evaluation in Caller's Frame
# =====================================================================
def evaluate_in_caller(expression: str) -> Any:
    """Evaluates arbitrary Python expression strings inside caller's local/global scope."""
    caller_frame = inspect.currentframe().f_back
    return eval(expression, caller_frame.f_globals, caller_frame.f_locals)


def q8_evaluate_in_caller_frame():
    secret_code = "ALPHA_77"
    multiplier = 5

    res1 = evaluate_in_caller("secret_code.lower()")
    assert res1 == "alpha_77"

    res2 = evaluate_in_caller("multiplier * 10")
    assert res2 == 50

    print("=== Q8: Programmatic Frame Evaluation Verified ===")


# =====================================================================
# Q9: In-Process Diagnostic Debug Shell
# =====================================================================
class DebugShell:
    """Non-interactive diagnostic shell executing scripts inside targeted frames."""
    def __init__(self, frame):
        self.frame = frame

    def execute_command(self, cmd: str) -> str:
        cmd = cmd.strip()
        if cmd.startswith("p "):
            expr = cmd[2:]
            try:
                val = eval(expr, self.frame.f_globals, self.frame.f_locals)
                return repr(val)
            except Exception as e:
                return f"EvalError: {e}"
        elif cmd == "locals":
            return repr(list(self.frame.f_locals.keys()))
        return "Unknown command"


def q9_in_process_debug_shell():
    def compute(val_x, val_y):
        sum_xy = val_x + val_y
        shell = DebugShell(inspect.currentframe())
        return shell

    shell = compute(100, 250)
    assert shell.execute_command("p val_x") == "100"
    assert shell.execute_command("p val_y") == "250"
    assert shell.execute_command("p sum_xy") == "350"
    assert "val_x" in shell.execute_command("locals")

    print("=== Q9: In-Process Diagnostic Debug Shell Verified ===")


# =====================================================================
# Q10: Architectural CrashDumpEngine for Post-Mortem Diagnostics
# =====================================================================
class CrashDumpEngine:
    """
    Production-grade crash diagnostic engine:
    - Serializes complete crash report upon uncaught exceptions
    - Extracts stack frames, function names, lines, and sanitized local variables
    - Produces machine-readable JSON artifacts
    """
    @classmethod
    def generate_crash_report(cls, exc_type, exc_val, exc_tb) -> Dict[str, Any]:
        frames = []
        curr_tb = exc_tb
        while curr_tb is not None:
            f = curr_tb.tb_frame
            # Extract safe representation of locals (masking passwords/keys)
            safe_locals = {}
            for k, v in f.f_locals.items():
                if "secret" in k.lower() or "password" in k.lower():
                    safe_locals[k] = "[MASKED_SECRET]"
                else:
                    safe_locals[k] = repr(v)[:100]

            frames.append({
                "function": f.f_code.co_name,
                "filename": os.path.basename(f.f_code.co_filename),
                "lineno": curr_tb.tb_lineno,
                "locals": safe_locals
            })
            curr_tb = curr_tb.tb_next

        report = {
            "exception_type": exc_type.__name__,
            "exception_message": str(exc_val),
            "stack_depth": len(frames),
            "frames": frames
        }
        return report


def q10_architectural_crash_dump_engine():
    def internal_service(account_id: str, secret_token: str):
        balance = 500
        # Simulated unexpected crash
        raise ValueError(f"Account {account_id} balance check failed")

    report = None
    try:
        internal_service("ACC-901", "my-super-secret-api-key")
    except ValueError:
        exc_type, exc_val, exc_tb = sys.exc_info()
        report = CrashDumpEngine.generate_crash_report(exc_type, exc_val, exc_tb)

    assert report is not None
    assert report["exception_type"] == "ValueError"
    assert "ACC-901" in report["exception_message"]

    # Verify frame locals inspection & secret masking
    leaf_frame = report["frames"][-1]
    assert leaf_frame["function"] == "internal_service"
    assert leaf_frame["locals"]["account_id"] == "'ACC-901'"
    assert leaf_frame["locals"]["secret_token"] == "[MASKED_SECRET]"

    # Verify report is JSON serializable
    json_output = json.dumps(report)
    assert "MASKED_SECRET" in json_output

    print("=== Q10: Architectural CrashDumpEngine Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_breakpoint_hook_mechanics()
    q2_scriptable_pdb_execution()
    q3_post_mortem_crash_inspection()
    q4_stack_frame_walking()
    q5_line_level_sys_settrace()
    q6_variable_watchpoint_tracer()
    q7_formatted_traceback_extraction()
    q8_evaluate_in_caller_frame()
    q9_in_process_debug_shell()
    q10_architectural_crash_dump_engine()

    print("\nAll 10 debugging with pdb practice questions passed successfully!")
