from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils.prompt_utils import format_multiline_string, bulletpoint_str_to_list
from models.Instruction import Instruction


def create_instruction(formatted_instruction_str: str):
    formatted_question_str = get_tf_questions(formatted_instruction_str)
    formatted_answer_str = get_tf_answers(
        formatted_instruction_str, formatted_question_str)
    formatted_direct_instructions_str = get_direct_instructions(
        formatted_instruction_str)
    formatted_direct_questions_str = get_direct_instruction_tf_questions(
        formatted_instruction_str)
    formatted_direct_answers_str = get_direct_instruction_tf_answers(
        formatted_direct_instructions_str, formatted_direct_questions_str)

    questions = parse_questions(formatted_question_str)
    answers = parse_answers(formatted_answer_str)
    direct_instructions = parse_direct_instructions(
        formatted_direct_instructions_str)
    direct_instructions_questions = parse_direct_questions(
        formatted_direct_questions_str)
    direct_instructions_answers = parse_direct_answers(
        formatted_direct_answers_str)
    return Instruction(
        questions,
        answers,
        direct_instructions,
        direct_instructions_questions,
        direct_instructions_answers)


def get_tf_questions(formatted_instruction_str: str):
    """
    Turn an instruction into TF questions for a six-year-old.
    """
    return LLMChain(
        prompt=PromptTemplate(
            template=format_multiline_string(f"""

            Below is text of someone giving an instruction. Turn the instruction condition into a list of True/False questions. 
            Julian: When I say I saw someone and it's not clear what we spoke about, ask me.
            - Did Julian say he saw someone?
            - Do we know what they spoke about?

            Below is text of someone giving an instruction. Turn the instruction condition into a list of True/False questions. 
            Julian: When I say the word banana begin your reply with the word split. 
            - Did Julian say the word banana? 

            Below is text of someone giving an instruction. Turn the instruction condition into a list of True/False questions. 
            Julian: When I take an instruction as a character in my DnD game, ask me to roll a dice.
            - Did Julian take an instruction as a character in his DnD game?

            Below is text of someone giving an instruction. Turn the instruction condition into a list of True/False questions. 
            {{instruction_str}}
            """),
            input_variables=["instruction_str"]
        ),
        llm=OpenAI(temperature=0.0),
        verbose=True
    ).predict(
        instruction_str=formatted_instruction_str
    )


def get_tf_answers(formatted_instruction_str: str, formatted_question_str: str):
    """
    Answer TF questions for a six-year-old.
    """
    return LLMChain(
        prompt=PromptTemplate(
            template=format_multiline_string(f"""
            Below is text of someone giving an instruction. Give the answers that make the entire instruction true 

            Julian: When I say I saw someone and it's not clear what we spoke about, ask me.
            - Did Julian say he saw someone?
            - Do we know what they spoke about?
            - True
            - False

            Julian: When I say the word banana begin your reply with the word split. 
            - Did Julian say the word banana? 
            - True

            {{instruction_str}}
            {{question_str}}
            """),
            input_variables=["instruction_str", "question_str"]
        ),
        llm=OpenAI(temperature=0.0),
        verbose=True
    ).predict(
        instruction_str=formatted_instruction_str,
        question_str=formatted_question_str
    )


def get_direct_instructions(formatted_instruction_str: str):
    """
    Turn an instruction into direct instruction for a six-year-old.
    """
    return LLMChain(
        prompt=PromptTemplate(
            template=format_multiline_string(f"""
            Turn the instruction into a list of direct (second person) and concise instructions that could be executed by someone dumb. 

            Julian: When I say I saw someone and it's not clear what we spoke about, ask me.
            - Ask Julian what they spoke about.

            Julian: When I say the word banana begin your reply with the word split. 
            - Begin your reply with the word 'split'.

            Julian: When I say I worked on Animus, record the conversation.
            - Record the conversation.

            {{instruction_str}}
            """),
            input_variables=["instruction_str"]
        ),
        llm=OpenAI(temperature=0.0),
        verbose=True
    ).predict(
        instruction_str=formatted_instruction_str
    )


def get_direct_instruction_tf_questions(formatted_instructions_str: str):
    return LLMChain(
        prompt=PromptTemplate(
            template=format_multiline_string(f"""
            For each direct instruction write a True/False question to ask a 6 year old whether the instruction has been completed or not.

            - Ask Julian what they spoke about.
            - Did you ask Julian what they spoke about?

            - Begin your reply with the word 'split'.
            - Did you begin your reply with the word 'split'?

            {{instructions_str}}
            """),
            input_variables=["instructions_str"]
        ),
        llm=OpenAI(temperature=0.0),
        verbose=True
    ).predict(
        instructions_str=formatted_instructions_str
    )


def get_direct_instruction_tf_answers(formatted_instructions_str: str, formatted_question_str: str):
    return LLMChain(
        prompt=PromptTemplate(
            template=format_multiline_string(f"""
            For each direct instruction write the True/False answer to the questions that make the instruction True.

            - Ask Julian what they spoke about.
            - Did you ask Julian what they spoke about?
            - True

            - Don't ask Julian what they spoke about.
            - Did you ask Julian what they spoke about?
            - False

            - Begin your reply with the word 'split'.
            - Did you begin your reply with the word 'split'?
            - True

            {{instructions_str}}
            {{question_str}}
            """),
            input_variables=["instructions_str", "question_str"]
        ),
        llm=OpenAI(temperature=0.0),
        verbose=True
    ).predict(
        instructions_str=formatted_instructions_str,
        question_str=formatted_question_str
    )


def parse_questions(formatted_question_str: str):
    return bulletpoint_str_to_list(formatted_question_str)


def parse_answers(formatted_answer_str: str):
    return bulletpoint_str_to_list(formatted_answer_str)


def parse_direct_instructions(formatted_direct_instruction_str: str):
    return bulletpoint_str_to_list(formatted_direct_instruction_str)


def parse_direct_questions(formatted_direct_instruction_tf_question_str: str):
    return bulletpoint_str_to_list(formatted_direct_instruction_tf_question_str)


def parse_direct_answers(formatted_direct_instruction_tf_answer_str: str):
    return bulletpoint_str_to_list(formatted_direct_instruction_tf_answer_str)
