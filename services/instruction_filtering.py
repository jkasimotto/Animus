from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.prompt_utils import format_multiline_string
from utils.instructions_utils import compare_answers, nested_list_to_nested_numbered_str, nested_numbered_str_to_nested_list
from utils.llm_utils import make_llm_call


def filter_instructions(instructions, conversation):
    """
    Filter instructions based on the conversation.
    """
    formatted_question_str = nested_list_to_nested_numbered_str(
        [instruction.tf_questions for instruction in instructions])

    formatted_answer_str = answer_questions(
        formatted_question_str, conversation.formatted_conversation)

    answer_tuples = nested_numbered_str_to_nested_list(formatted_answer_str)

    indices_to_keep = compare_answers(
        answer_tuples, [instruction.tf_answers for instruction in instructions])

    return [instructions[i] for i in indices_to_keep]


def answer_questions(formatted_question_str: str, formatted_conversation_str: str):
    return make_llm_call(
            prompt_template=f"""
            Answer the questions below based on the conversation. Answer only True or False.
            Conversation
            {{conversation}}
            Questions
            {{questions}}
            Answers:
            """,
            input_variables=[
                "conversation",
                "questions"
            ],
            formatted_inputs={
                'conversation': formatted_conversation_str,
                'questions': formatted_question_str
            },
    )