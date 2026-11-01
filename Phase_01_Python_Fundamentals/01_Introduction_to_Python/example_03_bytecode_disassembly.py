"""
Topic 01: Introduction to Python
Example 03: How Python Executes Code (Source Code -> Bytecode -> PVM)

Demonstrates that Python compiles human-readable source code into intermediate
bytecode instructions before the Python Virtual Machine (PVM) executes them.
"""

import dis


def calculate_rectangle_area(length: int, width: int) -> int:
    """Return the area of a rectangle."""
    area = length * width
    return area


def main() -> None:
    length = 12
    width = 5
    result = calculate_rectangle_area(length, width)

    print(f"Rectangle Dimensions : {length} x {width}")
    print(f"Calculated Area      : {result}")
    print("\n=== Compiled Bytecode Instructions (Code Object) ===")
    code_obj = calculate_rectangle_area.__code__
    print(f"Function Name        : {code_obj.co_name}")
    print(f"Local Variables      : {code_obj.co_varnames}")
    print(f"Bytecode Instruction Count: {len( list(dis.get_instructions(calculate_rectangle_area)) )}")
    print("\nInstruction Listing:")
    for instr in dis.get_instructions(calculate_rectangle_area):
        print(f"  Offset {instr.offset:>2}: {instr.opname:<18} {instr.argrepr}")


if __name__ == "__main__":
    main()
