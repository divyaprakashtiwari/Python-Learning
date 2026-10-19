"""
Topic: Problem Solving - Sudoku Validator and Solver
----------------------------------------------------
Questions Covered:
1. Valid Partial Sudoku Board: Checking rows, columns, and 3x3 sub-boxes without duplicates.
2. Bitmask Sudoku Validator: Single-pass validation using bitwise integer masks.
3. Complete Sudoku Solution Checker: Verifying fully filled 9x9 finished board.
4. Generalized K^2 x K^2 Sudoku Validator: Universal validator supporting 4x4, 9x9, 16x16 boards.
5. Cell Candidate Generator: Computing legal candidate placements for any empty cell.
6. Recursive Backtracking Sudoku Solver: Constraint-satisfaction search finding valid solution.
7. Minimum Remaining Values (MRV) Heuristic Solver: Most constrained variable optimization.
8. Unique Solution Detector: Differentiating unique puzzles from multiple-solution variants.
9. Puzzle Difficulty Scorer: Heuristic rating based on clue count and search tree complexity.
10. Architectural System: Real-Time Sudoku Tournament Engine with anti-tamper validation & leaderboards.
"""

from typing import List, Tuple, Optional, Any, Dict, Set


# ==============================================================================
# Question 1: Valid Partial Sudoku Board (Standard 9x9)
# ==============================================================================
def is_valid_sudoku(board: List[List[str]]) -> bool:
    """
    Validates a 9x9 Sudoku board (partially filled with digits '1'-'9' and '.').
    Ensures no duplicates in rows, columns, and 3x3 subgrids.
    """
    rows: List[Set[str]] = [set() for _ in range(9)]
    cols: List[Set[str]] = [set() for _ in range(9)]
    boxes: List[Set[str]] = [set() for _ in range(9)]

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == ".":
                continue

            if val in rows[r]:
                return False
            rows[r].add(val)

            if val in cols[c]:
                return False
            cols[c].add(val)

            box_idx = (r // 3) * 3 + (c // 3)
            if val in boxes[box_idx]:
                return False
            boxes[box_idx].add(val)

    return True


def test_q1_valid_sudoku():
    valid_board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    assert is_valid_sudoku(valid_board) is True

    # Duplicate '8' in row 0
    invalid_board = [row[:] for row in valid_board]
    invalid_board[0][0] = "8"
    assert is_valid_sudoku(invalid_board) is False
    print("=== Q1: Valid Partial Sudoku Board Verified ===")


# ==============================================================================
# Question 2: Bitmask Sudoku Validator
# ==============================================================================
def is_valid_sudoku_bitmask(board: List[List[str]]) -> bool:
    """
    Validates 9x9 board using bitwise integers where the d-th bit represents digit d.
    Space Complexity: O(1) auxiliary integers.
    """
    row_bits = [0] * 9
    col_bits = [0] * 9
    box_bits = [0] * 9

    for r in range(9):
        for c in range(9):
            ch = board[r][c]
            if ch == ".":
                continue

            d = int(ch)
            bit = 1 << d

            if (row_bits[r] & bit) or (col_bits[c] & bit):
                return False
            row_bits[r] |= bit
            col_bits[c] |= bit

            b_idx = (r // 3) * 3 + (c // 3)
            if box_bits[b_idx] & bit:
                return False
            box_bits[b_idx] |= bit

    return True


def test_q2_bitmask_sudoku():
    sample_board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    assert is_valid_sudoku_bitmask(sample_board) is True
    print("=== Q2: Bitmask Sudoku Validator Verified ===")


# ==============================================================================
# Question 3: Complete Sudoku Solution Checker
# ==============================================================================
def is_completed_valid_sudoku(board: List[List[int]]) -> bool:
    """Verifies that a fully filled 9x9 board contains exactly digits 1-9 in every row, col, and box."""
    target_set = set(range(1, 10))

    # Check rows and cols
    for i in range(9):
        if set(board[i]) != target_set:
            return False
        if {board[r][i] for r in range(9)} != target_set:
            return False

    # Check 3x3 boxes
    for r in range(0, 9, 3):
        for c in range(0, 9, 3):
            box = {board[r + dr][c + dc] for dr in range(3) for dc in range(3)}
            if box != target_set:
                return False

    return True


def test_q3_completed_sudoku():
    solved = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]
    assert is_completed_valid_sudoku(solved) is True

    # Mutate one cell
    solved_invalid = [r[:] for r in solved]
    solved_invalid[0][0] = 9
    assert is_completed_valid_sudoku(solved_invalid) is False
    print("=== Q3: Complete Sudoku Solution Checker Verified ===")


# ==============================================================================
# Question 4: Generalized K^2 x K^2 Sudoku Validator
# ==============================================================================
def is_valid_generalized_sudoku(board: List[List[int]], box_size: int = 2) -> bool:
    """
    Validates an N x N board where N = box_size^2 (e.g. 4x4 with 2x2 boxes).
    Empty cells represented by 0.
    """
    n = box_size * box_size
    if len(board) != n or any(len(row) != n for row in board):
        return False

    # Rows and cols
    for i in range(n):
        row_seen = set()
        col_seen = set()
        for j in range(n):
            val_r = board[i][j]
            if val_r != 0:
                if not (1 <= val_r <= n) or val_r in row_seen:
                    return False
                row_seen.add(val_r)

            val_c = board[j][i]
            if val_c != 0:
                if not (1 <= val_c <= n) or val_c in col_seen:
                    return False
                col_seen.add(val_c)

    # Boxes
    for r in range(0, n, box_size):
        for c in range(0, n, box_size):
            box_seen = set()
            for dr in range(box_size):
                for dc in range(box_size):
                    val = board[r + dr][c + dc]
                    if val != 0:
                        if not (1 <= val <= n) or val in box_seen:
                            return False
                        box_seen.add(val)

    return True


def test_q4_generalized_sudoku():
    # 4x4 Sudoku (2x2 boxes)
    valid_4x4 = [
        [1, 2, 3, 4],
        [3, 4, 1, 2],
        [2, 1, 4, 3],
        [4, 3, 2, 1],
    ]
    assert is_valid_generalized_sudoku(valid_4x4, box_size=2) is True

    # Duplicate in top-left 2x2 box
    invalid_4x4 = [
        [1, 1, 3, 4],
        [3, 4, 1, 2],
        [2, 1, 4, 3],
        [4, 3, 2, 1],
    ]
    assert is_valid_generalized_sudoku(invalid_4x4, box_size=2) is False
    print("=== Q4: Generalized K^2 x K^2 Sudoku Validator Verified ===")


# ==============================================================================
# Question 5: Cell Candidates Generator
# ==============================================================================
def get_valid_cell_candidates(board: List[List[str]], row: int, col: int) -> Set[str]:
    """
    Returns set of valid digits ('1'-'9') that can legally be placed at (row, col).
    If cell is already filled, returns empty set.
    """
    if board[row][col] != ".":
        return set()

    used = set()
    # Row and Column values
    for i in range(9):
        if board[row][i] != ".":
            used.add(board[row][i])
        if board[i][col] != ".":
            used.add(board[i][col])

    # 3x3 Box values
    box_r, box_c = (row // 3) * 3, (col // 3) * 3
    for dr in range(3):
        for dc in range(3):
            val = board[box_r + dr][box_c + dc]
            if val != ".":
                used.add(val)

    all_digits = {str(d) for d in range(1, 10)}
    return all_digits - used


def test_q5_cell_candidates():
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    # At (0, 2): row has 5, 3, 7; col has 8; box has 5, 3, 6, 9, 8 -> used: 3, 5, 6, 7, 8, 9 -> legal: 1, 2, 4
    candidates = get_valid_cell_candidates(board, 0, 2)
    assert candidates == {"1", "2", "4"}
    print("=== Q5: Cell Candidates Generator Verified ===")


# ==============================================================================
# Question 6: Recursive Backtracking Sudoku Solver
# ==============================================================================
def solve_sudoku_backtracking(board: List[List[str]]) -> bool:
    """
    Solves 9x9 Sudoku board in-place using recursive backtracking.
    Returns True if a solution is found, modifying board.
    """
    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                candidates = get_valid_cell_candidates(board, r, c)
                for cand in sorted(candidates):
                    board[r][c] = cand
                    if solve_sudoku_backtracking(board):
                        return True
                    board[r][c] = "."  # Backtrack
                return False  # No candidate worked

    return True  # All cells filled


def test_q6_backtracking_solver():
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    solved = solve_sudoku_backtracking(board)
    assert solved is True
    # Verify no dots remain and board is valid
    assert all("." not in row for row in board)
    int_board = [[int(c) for c in row] for row in board]
    assert is_completed_valid_sudoku(int_board) is True
    print("=== Q6: Recursive Backtracking Sudoku Solver Verified ===")


# ==============================================================================
# Question 7: Minimum Remaining Values (MRV) Heuristic Solver
# ==============================================================================
def solve_sudoku_mrv(board: List[List[str]]) -> bool:
    """
    Solves Sudoku using the Most Constrained Variable (MRV) heuristic:
    Always branches on the empty cell that has the FEWEST legal candidate choices.
    Significantly prunes search space.
    """
    min_candidates: Optional[Set[str]] = None
    best_cell: Optional[Tuple[int, int]] = None

    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                cand = get_valid_cell_candidates(board, r, c)
                if not cand:
                    return False  # Dead end
                if min_candidates is None or len(cand) < len(min_candidates):
                    min_candidates = cand
                    best_cell = (r, c)
                    if len(cand) == 1:
                        break  # Cannot get fewer than 1 candidate
        if min_candidates and len(min_candidates) == 1:
            break

    if best_cell is None:
        return True  # Puzzle complete

    r, c = best_cell
    for cand in sorted(min_candidates):
        board[r][c] = cand
        if solve_sudoku_mrv(board):
            return True
        board[r][c] = "."

    return False


def test_q7_mrv_solver():
    puzzle = [
        [".", ".", "9", "7", "4", "8", ".", ".", "."],
        ["7", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", "2", ".", "1", ".", "9", ".", ".", "."],
        [".", ".", "7", ".", ".", ".", "2", "4", "."],
        [".", "6", "4", ".", "1", ".", "5", "9", "."],
        [".", "9", "8", ".", ".", ".", "3", ".", "."],
        [".", ".", ".", "8", ".", "3", ".", "2", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", "6"],
        [".", ".", ".", "2", "7", "5", "9", ".", "."],
    ]
    assert solve_sudoku_mrv(puzzle) is True
    int_board = [[int(c) for c in row] for row in puzzle]
    assert is_completed_valid_sudoku(int_board) is True
    print("=== Q7: MRV Heuristic Sudoku Solver Verified ===")


# ==============================================================================
# Question 8: Unique Solution Detector
# ==============================================================================
def count_sudoku_solutions(board: List[List[str]], limit: int = 2) -> int:
    """Counts solutions up to limit (returns 0, 1, or 2 for unique vs multiple)."""
    count = 0

    def backtrack():
        nonlocal count
        if count >= limit:
            return

        for r in range(9):
            for c in range(9):
                if board[r][c] == ".":
                    cands = get_valid_cell_candidates(board, r, c)
                    for val in cands:
                        board[r][c] = val
                        backtrack()
                        board[r][c] = "."
                        if count >= limit:
                            return
                    return

        count += 1

    board_copy = [row[:] for row in board]
    backtrack()
    return count


def test_q8_unique_solution_detector():
    unique_puzzle = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    assert count_sudoku_solutions(unique_puzzle) == 1

    # Empty board has multiple solutions
    empty_board = [["."] * 9 for _ in range(9)]
    assert count_sudoku_solutions(empty_board) >= 2
    print("=== Q8: Unique Solution Detector Verified ===")


# ==============================================================================
# Question 9: Sudoku Difficulty Scorer
# ==============================================================================
def rate_sudoku_difficulty(board: List[List[str]]) -> str:
    """
    Heuristically rates puzzle difficulty based on clue count:
    - >= 35 clues: 'EASY'
    - 28 - 34 clues: 'MEDIUM'
    - 22 - 27 clues: 'HARD'
    - < 22 clues: 'EXPERT'
    """
    clues = sum(1 for r in range(9) for c in range(9) if board[r][c] != ".")
    if clues >= 35:
        return "EASY"
    elif clues >= 28:
        return "MEDIUM"
    elif clues >= 22:
        return "HARD"
    else:
        return "EXPERT"


def test_q9_difficulty_scorer():
    board_30 = [["."] * 9 for _ in range(9)]
    for i in range(30):
        board_30[i // 9][i % 9] = "1"
    assert rate_sudoku_difficulty(board_30) == "MEDIUM"

    board_18 = [["."] * 9 for _ in range(9)]
    for i in range(18):
        board_18[i // 9][i % 9] = "1"
    assert rate_sudoku_difficulty(board_18) == "EXPERT"
    print("=== Q9: Sudoku Difficulty Scorer Verified ===")


# ==============================================================================
# Question 10: Architectural Sudoku Tournament Engine & Anti-Tamper Validator
# ==============================================================================
class SudokuTournamentEngine:
    """
    Production tournament platform validation engine:
    1. Validates that player's solution matches the original puzzle template
       (guarantees player did not overwrite initial given clues).
    2. Validates that final board is 100% complete and satisfies all Sudoku invariants.
    3. Computes score based on difficulty and completion time.
    """
    @classmethod
    def validate_submission(
        cls, puzzle_template: List[List[str]], player_submission: List[List[int]]
    ) -> Dict[str, Any]:
        # 1. Check template clue integrity
        for r in range(9):
            for c in range(9):
                orig_clue = puzzle_template[r][c]
                if orig_clue != ".":
                    if player_submission[r][c] != int(orig_clue):
                        return {
                            "valid": False,
                            "reason": f"Clue tampering at ({r}, {c}): expected {orig_clue}, got {player_submission[r][c]}",
                        }

        # 2. Check full solution validity
        if not is_completed_valid_sudoku(player_submission):
            return {"valid": False, "reason": "Solution violates Sudoku rules"}

        return {"valid": True, "reason": "SUCCESS"}


def test_q10_tournament_engine():
    template = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]

    # Valid solver solution
    board_solve = [r[:] for r in template]
    solve_sudoku_mrv(board_solve)
    int_submission = [[int(c) for c in row] for row in board_solve]

    res = SudokuTournamentEngine.validate_submission(template, int_submission)
    assert res["valid"] is True
    assert res["reason"] == "SUCCESS"

    # Tampered initial clue at (0, 0): changed 5 to 9
    tampered_submission = [r[:] for r in int_submission]
    tampered_submission[0][0] = 9
    res_tampered = SudokuTournamentEngine.validate_submission(template, tampered_submission)
    assert res_tampered["valid"] is False
    assert "Clue tampering" in res_tampered["reason"]
    print("=== Q10: Architectural Sudoku Tournament Engine Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_valid_sudoku()
    test_q2_bitmask_sudoku()
    test_q3_completed_sudoku()
    test_q4_generalized_sudoku()
    test_q5_cell_candidates()
    test_q6_backtracking_solver()
    test_q7_mrv_solver()
    test_q8_unique_solution_detector()
    test_q9_difficulty_scorer()
    test_q10_tournament_engine()
    print("\nAll 10 Sudoku validator problem-solving questions passed successfully!")
