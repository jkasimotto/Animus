# in the tests/test_module.py file
import sys
sys.path.append("..") # For local running
sys.path.append("/Users/julianotto/Documents/Projects/jules/gfunctions/animus/") # For PyCharm

# # Print the current working directory
# import os
# x = os.getcwd()
# print(x)

# exit()
from services.action_selection import decide_actions_to_satisfy_instructions, remove_decisions_until_necessary
from models.Instruction import Instruction
from models.Conversation import Conversation

if __name__ == "__main__":
    instruction_2 = Instruction(
        tf_questions=["Did Julian speak?"],
        tf_answers=["True"],
        directions=["Begin your message with the word split."],
        directions_tf_criteria=["Did you begin your message with the word split?"],
        directions_tf_answers=["True"]
    )
    instruction_1 = Instruction(
        tf_questions=["Did Julian give a new long term instruction?"],
        tf_answers=["True"],
        directions=["Say I will record <the instruction>"],
        directions_tf_criteria=["Did you say I will record <the instruction>?"],
        directions_tf_answers=["True"]
    )

    instructions = [instruction_1, instruction_2]
    conversation = Conversation(
        ["Julian: Hello! When I use the letter t replace it with the letter j."]
    )


    print(remove_decisions_until_necessary(
        conversation, 
        [instruction_1, instruction_2],
        ["SEND Split, I will replace the letter t with the letter j"]))