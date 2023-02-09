# in the tests/test_module.py file
import sys
sys.path.append("..")

from services.instruction_creation import create_instruction

def print_instruction(instruction):
    print("Questions")
    print(instruction.tf_questions)
    print("Answers")
    print(instruction.tf_answers)
    print("Direct Instructions")
    print(instruction.direct_instructions)

if __name__ == "__main__":
    instruction = create_instruction(
        "Julian: When I give you a new instruction, store it."
    )
    print_instruction(instruction)