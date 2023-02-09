import json


class Session:
    def __init__(self):
        # list of entities involved in the session, each entity should have id and name properties
        self.participating_entities = []
        self.messages = []  # list of Message objects
        self.is_online = True
        # list of Instruction objects that have been executed
        self.executed_instructions = []
        # list of Instruction objects that need to be executed
        self.instructions_to_execute = []
        # list of Instruction objects to add to the LLM context window before replying.
        self.instructions_for_prompt = []

    @property
    def conversation(self):
        """
        Return the conversation as a formatted string like:

        Julian: Hello everyone.
        John: Hey mate!
        AI: How are you both?
        Julian: Good thank you.
        """
        conversation = ""
        for message in self.messages:
            conversation += f"\n{message.sender}: {message.text}"
        return conversation
    
    @property
    def prompt_instructions(self):
        """
        Return the instructions as a formatted string like:

        John: Please do this.
        Julian: Please do that.
        """
        instructions = ""
        for i, instruction in enumerate(self.instructions_for_prompt):
            instructions += f"\n{i + 1}: {instruction.text}"
        return instructions

    def add_participating_entity(self, entity_id, entity_name):
        """Add an entity to the list of participating entities"""
        self.participating_entities.append(
            {'id': entity_id, 'name': entity_name})

    def add_message(self, message):
        """Add a message to the message history"""
        self.messages.append(message)

    def add_executed_instruction(self, instruction):
        """Add an instruction to the list of executed instructions"""
        self.executed_instructions.append(instruction)

    def add_instruction_to_execute(self, instruction):
        """Add an instruction to the list of instructions to execute"""
        self.instructions_to_execute.append(instruction)

    def get_participating_entities(self):
        """Return the list of participating entities"""
        return self.participating_entities

    def get_message_history(self):
        """Return the message history"""
        return self.messages

    def get_executed_instructions(self):
        """Return the list of executed instructions"""
        return self.executed_instructions

    def get_instructions_to_execute(self):
        """Return the list of instructions to execute"""
        return self.instructions_to_execute

    def to_json(self):
        """Return the session object as a JSON string"""
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    @staticmethod
    def from_json(json_str):
        """Create a Session object from a JSON string"""
        json_data = json.loads(json_str)
        session = Session()
        session.is_online = json_data['is_online']
        return session
