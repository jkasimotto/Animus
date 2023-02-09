# in the tests/test_module.py file
import sys
sys.path.append("..")

from models.Instruction import Instruction
from services.instruction_filtering import filter_instructions

class Conversation:

    def __init__(self, messages) -> None:
        self.messages = messages
    
    @property
    def formatted_conversation(self):
        """
        Get a formatted conversation.
        """
        return "\n".join(self.messages)

if __name__ == "__main__":
    instruction_1 = Instruction(
        tf_questions=["Did Julian say he saw someone?", "Do we know what they spoke about?"],
        tf_answers=["True", "False"],
        direct_instructions=["Ask Julian what they spoke about."]
    )
    instruction_2 = Instruction(
        tf_questions=["Did Julian say the word banana?"],
        tf_answers=["True"],
        direct_instructions=["Begin your reply with the word split."]
    )
    instruction_3 = Instruction(
        tf_questions=["Did Julian say he worked on Animus?"],
        tf_answers=["True"],
        direct_instructions=["Ask Julian what he did.", "Store the conversation"]
    )

    instructions = [instruction_1, instruction_2, instruction_3]
    conversation = Conversation(
        ["Julian: I saw Georgie today! I ate a banana with her."]
    )

    print(filter_instructions(instructions, conversation))
