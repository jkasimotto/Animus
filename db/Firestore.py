from google.cloud import firestore
from config import FIRESTORE_PROJECT_ID
from models.Instruction import Instruction


class Firestore:
    """
    A class for interacting with the Firestore database.
    """

    def __init__(self):
        self.client = firestore.Client(
            project=FIRESTORE_PROJECT_ID)  # TODO: Make env var?

    def get_conversation(self, conversation_id):
        """
        Get a conversation from Firestore.
        """
        conversation = self.client.collection(
            u'conversations').document(conversation_id).get().to_dict()
        return conversation

    def create_instruction(self, uid: str, instruction: Instruction):
        """
        Create an instruction in Firestore in the instructions subcollection.
        """
        self.client.collection(u'users').document(uid).collection(
            u'instructions').document().set(instruction.to_dict())
