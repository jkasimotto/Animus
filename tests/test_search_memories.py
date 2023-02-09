# in the tests/test_module.py file
import sys
sys.path.append("..")
sys.path.append("/Users/julianotto/Documents/Projects/jules/gfunctions/animus/") # For PyCharm


from models.Conversation import Conversation
from typing import Tuple
import unittest
from db.Weaviate import Weaviate
from services.memory_storage import store_conversation_in_memory
from services.memory_search import search_test_memory

EVENT_CONVERSATIONS = [
    Conversation(
        messages=[
            "Julian: I saw Georgie today! I ate a banana with her.",
        ]
    ),
    Conversation(
        messages=[
            "Julian: I went for a run with Blake this morning. I felt great then I went home and began working on Animus.",
        ]
    ),
    Conversation(
        messages=[
            "Julian: I felt really annoyed by the dogs this morning... They needed so much attention."
        ]
    ),
    Conversation(
        messages=[
            "Julian: I went to the beach yesterday with my friends. The water was so warm and we had a great time playing in the waves.",
        ]
    ),
    Conversation(
        messages=[
            "Julian: I had a job interview today. I was so nervous but it went well. I'm hoping to hear back from them soon.",
        ]
    ),
    Conversation(
        messages=[
            "Julian: I just finished reading a great book. It was a mystery and I couldn't put it down. I'm excited to start the next one.",
        ]
    ),
    Conversation(
        messages=[
            "Julian: I went to the museum today. There was a new exhibition and it was amazing. I learned so much about art and history.",
        ]
    ),
    Conversation(
        messages=[
            "Julian: I had a picnic with my family today. The weather was perfect and the food was delicious. We had such a great time.",
        ]
    ),
    Conversation(
        messages=[
            "Julian: I went shopping today and found some great deals. I bought a new shirt and a pair of shoes. I'm so excited to wear them.",
        ]
    ),
    Conversation(
        messages=[
            "Julian: I had a busy day today. I had a lot of work to do, but I was able to get everything done. I'm feeling accomplished.",
        ]
    ),
    Conversation(
        messages=[
            "Julian: I went to the park today and played basketball with my friends. It was a great way to get some exercise and have fun.",
        ]
    ),
    Conversation(
        messages=[
            "Julian: I went to a concert last night. The music was incredible and the energy was amazing. I had such a great time.",
        ]
    ),
    Conversation(
        messages=[
            "Julian: I went on a hike today. The scenery was breathtaking and I felt so connected to nature. I can't wait to go again.",
        ]
    )
]
QUESTION_CONVERSATIONS = [
    Conversation(
        messages=[
            "Julian: When did I last go rock climbing?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: How did I feel on Tuesday?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: Can you get me a list of how I felt the last week?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: What do I need to do for Animus?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: What did I do yesterday for Animus?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: Where does Blake live?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: Who can I go and do some rock climbing with?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: I've got 20 minutes. What can I do on my phone to be productive?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: When was the last time I cleaned my room?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: What did I have for breakfast yesterday?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: When was the last time I went to the gym?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: Who did I go to the museum with last week?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: What did I do over the weekend?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: When was the last time I went to the park?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: Who did I go shopping with last month?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: When was the last time I had a job interview?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: What was the last book I read?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: Who did I go to the concert with last night?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: When was the last time I went on a hike?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: Who did I go to the beach with yesterday?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: What did I do last night?",
        ]
    ),
    Conversation(
        messages=[
            "Julian: When was the last time I had a picnic?",
        ]
    ),
]

CONVERSATIONS = EVENT_CONVERSATIONS + QUESTION_CONVERSATIONS


class TestSearchMemory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.weaviate = Weaviate()
        # cls.weaviate.delete_test_schema()
        # cls.weaviate.create_test_schema()

        # Add the conversations to the database
        # for conversation in CONVERSATIONS:
        #     store_conversation_in_memory(cls.weaviate, conversation, test=True)

    def test_search_last_time_saw_Blake(self):
        query = "When did I last see Blake?"
        results = search_test_memory(self.weaviate, query)
        print_results(query, results)
        # self.assertTrue(len(results) > 0)

    def test_search_questions_asked(self):
        query = "What sort of questions have I asked you?"
        results = search_test_memory(self.weaviate, query)
        print_results(query, results)
        # self.assertTrue(len(results) > 0)

    def test_search_questions_about_food(self):
        query = "What questions have I asked you about food?"
        results = search_test_memory(self.weaviate, query)
        print_results(query, results)
        # self.assertTrue(len(results) > 0)

    def test_search_what_to_do_today(self):
        query = "What can I do today?"
        results = search_test_memory(self.weaviate, query)
        print_results(query, results)
        # self.assertTrue(len(results) > 0)

    # Add 6 more test cases here with different queries

def print_results(query, results):
    print("====================================")
    print("Results for query '{}':".format(query))
    print("======")
    for i, result in enumerate(results):
        # print(result)
        print(result['conversation'])
        print(result['_additional']['distance'])
        print()
        if i == 9:
            break
if __name__ == '__main__':
    unittest.main()
