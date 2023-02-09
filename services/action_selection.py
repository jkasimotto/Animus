import time
from typing import List

from models.Conversation import Conversation
from models.Instruction import Instruction
from utils.instructions_utils import (compare_answers,
                                      nested_list_to_nested_numbered_str,
                                      nested_numbered_str_to_nested_list)
from utils.llm_utils import make_llm_call
from utils.prompt_utils import (bulletpoint_str_to_list, comma_str_to_list,
                                format_multiline_string,
                                list_to_bulletpoint_str, list_to_numbered_str,
                                numbered_bools_str_to_list, numbered_str_to_list)


def decide_actions_to_satisfy_instructions(conversation: Conversation, instructions: List[Instruction], tools):
    # TODO: Change. Create a Tool or an Action class.
    actions_str = format_multiline_string(f"""
                Send
                - Send a message to the conversation. This is useful for providing information or asking questions for more information.
                - Format: SEND <message>
                Store
                - Store the conversation in your memory for a later date.
                - Format: STORE the conversation
                Search
                - Search your memory for details of a previous conversation.
                - Format: SEARCH <question e.g. What did Julian eat for breakfast this morning?>
                Store Instruction
                - Remember a new instruction for a later date.
                - Format: STORE the instruction
                Store Question
                - A special action to store questions
                - Format: QUESTION <question>
                """)

    decisions = make_llm_call(
        prompt_template=f"""
                Conversation:
                Julian: I saw the weather report.
                Instructions for Assistant:
                1.1 Ask Julian what the weather is.
                Assistant Actions:
                1. Send
                - Send a message to the conversation. This is useful for providing information or asking questions for more information.
                - Format: SEND <message>
                Write the actions that satisfy the instructions in order. Write as an unnumbered bulletpoint list using the specified format for each action:
                - SEND What is the weather?

                Conversation:
                {{conversation}}
                Instructions for Assistant:
                {{instructions}}
                Assistant Actions:
                {{actions}}
                Decide which actions will satisfy the instructions AND NO MORE. Write as an unnumbered bulletpoint list using the specified format for each action:
        """,
        input_variables=['conversation', 'instructions', 'actions'],
        formatted_inputs={
            'conversation': conversation.formatted_conversation,
            'instructions': nested_list_to_nested_numbered_str([instruction.directions for instruction in instructions]),
            'actions': actions_str
        },
        output_fn=bulletpoint_str_to_list

    )

    decisions = improve_decisions_until_satisfied(
        conversation,
        instructions,
        actions_str,
        decisions)

    decisions = remove_decisions_until_necessary(
        conversation,
        instructions,
        decisions)

    return decisions


def improve_decisions_until_satisfied(conversation, instructions, actions, decisions):
    while True:

        unsatisfied_instructions = get_unsatisfied_instructions(
            conversation,
            instructions,
            decisions
        )

        if not unsatisfied_instructions:
            break

        decisions = make_llm_call(
            prompt_template=f"""
                Conversation:
                {{conversation}}

                Instructions for Assistant:
                {{instructions}}

                Assistant Actions:
                {{actions}}

                Assistant Decisions:
                {{decisions}}

                Unsatisfied Instruction:
                {{unsatisfied_criteria}}

                Rewrite the list of decisions to satisfy ALL instructions. Write as a bulletpoint list using the specified format for each action:

                Assistant Decisions:
            """,
            input_variables=[
                'conversation',
                'instructions',
                'actions',
                'decisions',
                'unsatisfied_criteria'
            ],
            formatted_inputs={
                'conversation': conversation.formatted_conversation,
                'instructions': nested_list_to_nested_numbered_str([instruction.directions for instruction in instructions]),
                'actions': actions,
                'decisions': list_to_bulletpoint_str(decisions),
                'unsatisfied_criteria': nested_list_to_nested_numbered_str([instruction.directions for instruction in unsatisfied_instructions])
            },
            output_fn=bulletpoint_str_to_list
        )

    return decisions


def remove_decisions_until_necessary(conversation, instructions, decisions):

    while True:

        unnecessary_decisions_flags = make_llm_call(
            prompt_template=f"""
                Conversation:
                Julian: I ate a pie today!
                Instructions for Assistant:
                1.1 Ask Julian what he ate today.
                Assistant Decisions:
                1. SEND what did you eat today?
                2. STORE the conversation
                3. SEARCH what did Julian eat today?
                For each Assistant Decision, carefully think if it satisfies any instruction and write True if it does and False if it does not. Write 3 answers as a numbered list.
                Answers:
                1. True
                2. False
                3. False

                Conversation:
                {{conversation}}
                Instructions for Assistant:
                {{instructions}}
                Assistant Decisions:
                {{decisions}}
                For each Assistant Decision, carefully think if it satisfies any instruction and write True if it does and False if it does not. Write {{num_decisions}} answers as a numbered list.
                Answers:
                """,
            input_variables=[
                'conversation',
                'instructions',
                'decisions',
                'num_decisions'
            ],
            formatted_inputs={
                'conversation': conversation.formatted_conversation,
                'instructions': nested_list_to_nested_numbered_str([instruction.directions for instruction in instructions]),
                'decisions': list_to_numbered_str(decisions),
                'num_decisions': len(decisions)
            },
            output_fn=numbered_bools_str_to_list
        )

        # All decisions are necessary
        if all(unnecessary_decisions_flags):
            break

        decisions = remove_unnecessary_decisions(
            decisions, unnecessary_decisions_flags)

    return decisions


def remove_unnecessary_decisions(decisions, boolean_list):
    return [decision for i, decision in enumerate(decisions) if boolean_list[i]]


def get_unsatisfied_instructions(conversation, instructions, decisions):

    question_answers = make_llm_call(
        prompt_template=f"""
                Conversation:
                {{conversation}}

                Instructions for Assistant:
                {{instructions}}

                Assistant Actions:
                {{actions}}

                Questions:
                {{questions}}

                Answer the questions. Only answer True or False for each question. Use the numbering provided by the questions.
                Answers:
            """,
        input_variables=[
            "conversation",
            "instructions",
            "actions",
            "questions"
        ],
        formatted_inputs={
            "conversation": conversation.formatted_conversation,
            "instructions": nested_list_to_nested_numbered_str([instruction.directions for instruction in instructions]),
            "actions": list_to_bulletpoint_str(decisions),
            "questions": nested_list_to_nested_numbered_str([instruction.directions_tf_criteria for instruction in instructions])
        },
        output_fn=nested_numbered_str_to_nested_list
    )

    incorrect_indices = compare_answers(
        question_answers,
        [instruction.directions_tf_answers for instruction in instructions],
        return_correct=False
    )

    return [instructions[i] for i in incorrect_indices]
