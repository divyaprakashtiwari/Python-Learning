"""
Question 10: Automated Sudoku Board Validator & Backtracking Solver
Topic: Problem Solving & Competitive Programming Patterns

Key Concepts Tested:
- 9x9 Sudoku grid structure and constraint validation (row, column, 3x3 subgrid)
- Move safety verification with constraint propagation
- Recursive backtracking solver with state restoration
- ASCII board visualization formatting
- Error handling for invalid board dimensions and domain ranges
"""

from typing import List, Tuple, Optional


class SudokuEngine:
    """
    Automated engine for validating, formatting, and solving 9x9 Sudoku puzzles.
    """

    @staticmethod
    def _validate_grid(board: List[List[int]]) -> None:
        """Enforces strictly 9x9 dimensions and domain values 0..9."""
        if len(board) != 9 or any(len(row) != 9 for row in board):
            raise ValueError("Sudoku board must have exact 9x9 dimensions")
        for r in range(9):
            for c in range(9):
                if not isinstance(board[r][c], int) or not (0 <= board[r][c] <= 9):
                    raise ValueError(f"Invalid cell value at ({r}, {c}): {board[r][c]}. Must be in 0..9.")

    def is_valid_sudoku(self, board: List[List[int]]) -> bool:
        """
        Validates an initial or intermediate partially filled 9x9 grid.
        Ensures no row, column, or 3x3 box contains duplicate non-zero digits.
        """
        self._validate_grid(board)

        # 1. Check rows
        for r in range(9):
            seen = set()
            for c in range(9):
                val = board[r][c]
                if val != 0:
                    if val in seen:
                        return False
                    seen.add(val)

        # 2. Check columns
        for c in range(9):
            seen = set()
            for r in range(9):
                val = board[r][c]
                if val != 0:
                    if val in seen:
                        return False
                    seen.add(val)

        # 3. Check 3x3 subgrids
        for box_r in range(0, 9, 3):
            for box_c in range(0, 9, 3):
                seen = set()
                for r in range(box_r, box_r + 3):
                    for c in range(box_c, box_c + 3):
                        val = board[r][c]
                        if val != 0:
                            if val in seen:
                                return False
                            seen.add(val)

        return True

    @staticmethod
    def is_safe(board: List[List[int]], row: int, col: int, num: int) -> bool:
        """
        Checks whether placing num at board[row][col] is legal.
        """
        # Check row
        for c in range(9):
            if board[row][c] == num:
                return False

        # Check column
        for r in range(9):
            if board[r][col] == num:
                return False

        # Check 3x3 box
        box_r, box_c = (row // 3) * 3, (col // 3) * 3
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if board[r][c] == num:
                    return False

        return True

    def _find_mrv_empty_cell(self, board: List[List[int]]) -> Optional[Tuple[int, int]]:
        """
        Finds an empty cell, prioritizing the cell with Minimum Remaining Values (MRV).
        """
        min_candidates = 10
        best_cell = None

        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    candidates = sum(1 for num in range(1, 10) if self.is_safe(board, r, c, num))
                    if candidates < min_candidates:
                        min_candidates = candidates
                        best_cell = (r, c)
                        if min_candidates == 1:
                            return best_cell

        return best_cell

    def solve_sudoku(self, board: List[List[int]]) -> bool:
        """
        Solves the Sudoku board in-place using recursive backtracking with MRV pruning.
        Returns True if a solution is found, False otherwise.
        """
        self._validate_grid(board)

        if not self.is_valid_sudoku(board):
            return False

        cell = self._find_mrv_empty_cell(board)
        if cell is None:
            return True  # All cells filled legally

        row, col = cell
        for num in range(1, 10):
            if self.is_safe(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0  # Backtrack

        return False

    @staticmethod
    def format_board(board: List[List[int]]) -> str:
        """Renders an ASCII grid representation with subgrid borders."""
        lines = []
        border = "+-------+-------+-------+"

        for r in range(9):
            if r % 3 == 0:
                lines.append(border)
            row_str = []
            for c in range(9):
                if c % 3 == 0:
                    row_str.append("|")
                val_char = str(board[r][c]) if board[r][c] != 0 else "."
                row_str.append(f"{val_char}")
            row_str.append("|")
            # Format row tokens cleanly
            formatted_row = f"| {' '.join(row_str[1:4])} | {' '.join(row_str[5:8])} | {' '.join(row_str[9:12])} |"
            lines.append(formatted_row)
        lines.append(border)

        return "\n".join(lines)


if __name__ == "__main__":
    engine = SudokuEngine()

    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    print("=== 1. Board Validation ===")
    is_initial_valid = engine.is_valid_sudoku(puzzle)
    print(f"Initial Board Valid: {is_initial_valid}")

    print("\n=== 2. Solving with Recursive Backtracking ===")
    solved = engine.solve_sudoku(puzzle)
    print(f"Puzzle Solved Successfully: {solved}")
    print(f"Solved Board First Row:  {puzzle[0]}")
    print(f"Solved Board Middle Row: {puzzle[4]}")
    print(f"Solved Board Last Row:   {puzzle[8]}")

    print("\n=== 3. ASCII Formatted Solved Grid ===")
    board_str = engine.format_board(puzzle)
    print(board_str)

    print("\n=== 4. Edge Cases: Invalid Board Dimensions ===")
    try:
        engine.solve_sudoku([[1, 2], [3, 4]])
    except ValueError as err:
        print(f"Caught dimension error: {err}")
