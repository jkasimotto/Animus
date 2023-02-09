from utils.prompt_utils import format_multiline_string
from models.Instruction import Instruction
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from services.action_selection import decide_actions_to_satisfy_instructions
from services.instruction_filtering import filter_instructions
from services.memory_storage import store_conversation_in_memory
from services.memory_search import search_memory
from utils.llm_utils import make_llm_call


class Animus:

    def __init__(self, firestore, weaviate, conversation) -> None:
        self.firestore = firestore
        self.weaviate = weaviate
        self.conversation = conversation
        # Get entity instructions from weaviate
        self.instructions = self.get_instructions()

    def main(self):
        relevant_instructions = filter_instructions(self.instructions, self.conversation)
        relevant_actions = decide_actions_to_satisfy_instructions(
            self.conversation,
            relevant_instructions,
            None
        )
        for action in relevant_actions:
            # Get the first word
            operator = action.split(" ")[0].strip().replace(" ", "").lower()
            if operator == "send":
                memories = None
                self.conversation.messages.append(action)
                return self.conversation, [], [], []
            elif operator == "store":
                memories = None
                store_conversation_in_memory(self.weaviate, self.conversation)
                self.conversation.messages.append("I STORED the conversation in memory.")
            elif operator == "instruction":
                memories = None
                self.conversation.messages.append(f"I STORED INSTRUCTION {action}.")
            elif operator == "search":
                memories = search_memory(self.weaviate, ' '.join(action.split(" ")[1:]))
                reply = make_llm_call(
                    prompt_template=f"""
                        You are Julian's digital assistant. Think carefully about the conversation and what is required. Use the RELEVANT (so not all) information in your memory. Use chain of thought reasoning to craft a response.
                        Conversation:
                        {{conversation}}
                        Memories:
                        {{memories}}
                        Reply:
                    """,
                    input_variables=['conversation', 'memories'],
                    formatted_inputs={
                        'conversation': self.conversation.formatted_conversation,
                        'memories': "\n- ".join([memory['summary'] for memory in memories])
                    },
                )
                self.conversation.messages.append(f"AI: {reply}")
        return self.conversation, relevant_instructions, relevant_actions, memories

    
    def send(self, text):
        self.conversation.messages.append(text)
    
    def store(self):
        pass

    def get_instructions(self):
        return [
            Instruction(
                tf_questions=[
                    "Did Julian say he was with someone?",
                    "Do you know what they spoke about?",
                    "Is Julian's last response a direct question of you?",
                ],
                tf_answers=[
                    "True",
                    "False",
                    "False"
                ],
                directions=[
                    "Ask Julian what they spoke about."
                ],
                directions_tf_criteria=[
                    "Did you ask Julian what they spoke about?"
                ],
                directions_tf_answers=[
                    "True"
                ]
            ),
            Instruction(
                tf_questions=[
                    "Did Julian talk about an event or activity he did?",
                    "Is Julian's last response a direct question of you?"
                ],
                tf_answers=[
                    "True",
                    "False"
                ],
                directions=[
                    "Store the converastion"
                ],
                directions_tf_criteria=[
                    "Did you store the conversation?"
                ],
                directions_tf_answers=[
                    "True"
                ]
            ),
            Instruction(
                tf_questions=[
                    "Did Julian give a new long term instruction?"
                ],
                tf_answers=[
                    "True"
                ],
                directions=[
                    "Remember the instruction"
                ],
                directions_tf_criteria=[
                    "Did you remember the instruction?"
                ],
                directions_tf_answers=[
                    "True"
                ]
            ),
            Instruction(
                tf_questions=[
                    "Did Julian ask you a question about himself or his past?"
                ],
                tf_answers=[
                    "True"
                ],
                directions=[
                    "Search your memory for an answer",
                    "Write QUESTION <the question>"
                ],
                directions_tf_criteria=[
                    "Under Assistant decisions, the decision with the format SEARCH <question>. Is the question a fully formed standalone question?",
                    "Did you write QUESTION followed by the question?"
                ],
                directions_tf_answers=[
                    "True",
                    "True"
                ]
            ),
        ]
        # return self.weaviate.get_entity_instructions()