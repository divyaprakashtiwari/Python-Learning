"""
Topic 02 - Control Flow
Practice Question 4 Solution: Collatz Conjecture (3n + 1) Trajectory Analyzer

Problem Statement:
Simulates and analyzes the Collatz Conjecture using a while loop for a given starting integer:
1. While n > 1:
   - if n is even: n = n // 2
   - if n is odd: n = 3 * n + 1
2. Records: sequence, total steps (stopping time), peak value.
3. Guards against infinite loops with max_iterations = 5000 safety threshold.
"""


def analyze_collatz(starting_number: int, max_iterations: int = 5000) -> dict[str, object]:
    """Generates the Collatz trajectory and computes stopping time and peak value."""
    if not isinstance(starting_number, int) or starting_number < 1:
        raise ValueError("Starting number must be an integer >= 1.")

    current = starting_number
    trajectory = [current]
    steps = 0
    peak = current
    safety_triggered = False

    while current > 1:
        if steps >= max_iterations:
            safety_triggered = True
            break

        if current % 2 == 0:
            current = current // 2
        else:
            current = 3 * current + 1

        trajectory.append(current)
        steps += 1
        if current > peak:
            peak = current

    return {
        "starting_number": starting_number,
        "steps": steps,
        "peak": peak,
        "trajectory": trajectory,
        "safety_triggered": safety_triggered,
    }


def main() -> None:
    start_val = 27
    res = analyze_collatz(start_val)

    print(f"Starting Value: {res['starting_number']}")
    print(f"Total Stopping Time (Steps): {res['steps']}")
    print(f"Peak Trajectory Value: {res['peak']}")

    traj = res["trajectory"]
    first_5 = traj[:5]
    last_5 = traj[-5:] if len(traj) >= 5 else traj
    print(f"First 5 Values: {first_5}")
    print(f"Last 5 Values: {last_5}")
    print(f"Safety Limit Triggered: {res['safety_triggered']}")


if __name__ == "__main__":
    main()
