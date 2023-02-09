from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from utils.prompt_utils import format_multiline_string, bulletpoint_str_to_list
from models.Instruction import Instruction
from instruction_filtering import nested_list_to_nested_numbered_str

def get_edited_questions(formatted_question_str: str, formatted_edits_str: str):
    return LLMChain(
        prompt=PromptTemplate(
            template=format_multiline_string(f"""
            Edit the questions according to the edits. Write as a bulletpoint list.
            Questions:
            - Did Julian eat a banana?
            - Do you need to store the conversation.
            Edits:
            Get rid of the second question.
            Edited Questions:
            - Did Julian eat a banana?

            Edit the questions according to the edits. Write as a bulletpoint list.
            Questions: 
            {{questions}}
            Edits:
            {{edits}}
            Edited Questions:
            """),
            input_variables=["questions", "edits"]
        ),
        llm=OpenAI(temperature=0.0),
        verbose=True
    ).predict(
        questions=formatted_question_str,
        edits=formatted_edits_str
    )
