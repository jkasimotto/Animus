import os
from config import WEAVIATE_URL
import weaviate
from typing import List

EQUAL = "Equal"
OR = "Or"


class Weaviate:
    def __init__(self):
        self.url = os.environ.get("WEAVIATE_URL")
        self.url = WEAVIATE_URL
        self.username = os.environ.get("WEAVIATE_USERNAME")
        self.password = os.environ.get("WEAVIATE_PASSWORD")
        self.client = self._create_client()
        self.query = Query(self.client)

    def _create_client(self):
        additional_headers = {
            'X-OpenAI-Api-Key': os.getenv('OPENAI_API_KEY')
        }
        return weaviate.Client(self.url, additional_headers=additional_headers)

    def create_schema(self):
        self.client.schema.create_class({
            "class": "Memory",
            "description": "A memory of the assistant",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text",
                    "vectorizeClassName": True
                }
            },
            "properties": [
                {
                    "name": "title",
                    "dataType": ["string"],
                    "description": "The title of the memory",
                    "moduleConfig": {
                            "text2vec-openai": {
                                "skip": True,
                                "vectorizePropertyName": False
                            }
                    },
                },
                {
                    "name": "summary",
                    "dataType": ["string"],
                    "description": "The important information from the conversation",
                    "moduleConfig": {
                            "text2vec-openai": {
                                "skip": False,
                                "vectorizePropertyName": False
                            }
                    },
                },
                {
                    "name": "conversation",
                    "dataType": ["string"],
                    "description": "The conversation that led to the memory",
                    "moduleConfig": {
                            "text2vec-openai": {
                                "skip": True,
                            }
                    },
                },
                {
                    "name": "user_id",
                    "dataType": ["string"],
                    "description": "The user id in Firebase",
                    "moduleConfig": {
                            "text2vec-openai": {
                                "skip": True,
                            }
                    },
                },
                {
                    "name": "questions",
                    "dataType": ["string"],
                    "description": "Questions this memory can answer",
                    "moduleConfig": {
                            "text2vec-openai": {
                                "skip": True,
                                "vectorizePropertyName": False
                            }
                    },
                }
            ]
        }
        )
        self.client.schema.create_class(
            {
                "class": "Question",
                "description": "A question that can be answered with a memory",
                "vectorizer": "text2vec-openai",
                "moduleConfig": {
                    "text2vec-openai": {
                        "model": "ada",
                        "modelVersion": "002",
                        "type": "text",
                        "vectorizeClassName": False
                    }
                },
                "properties": [
                    {
                        "name": "answeredBy",
                        "dataType": ["Memory"],
                        "description": "Memories that answers this question",
                    },
                    {
                        "name": "question",
                        "dataType": ["string"],
                        "description": "The question",
                        "moduleConfig": {
                            "text2vec-openai": {
                                "skip": False,
                                "vectorizePropertyName": False
                            }
                        },
                    },
                    {
                        "name": "user_id",
                        "dataType": ["string"],
                        "description": "The user id in Firebase",
                        "moduleConfig": {
                            "text2vec-openai": {
                                "skip": True,
                            }
                        },
                    },
                ]
            }
        )
        self.client.schema.create_class({
            "class": "Instruction",
            "description": "Instructions the user has given to the assistant",
            "properties": [
                {
                    "name": "user_id",
                    "dataType": ["string"],
                    "description": "The user id in Firebase"
                },
                {
                    "name": "name",
                    "dataType": ["string"],
                    "description": "The name of the instruction"
                },
                # TODO
            ]
        })

    def create_test_schema(self):
        self.client.schema.create_class(
            {
                "class": "TestMemory",
                "description": "A memory of the assistant",
                "vectorizer": "text2vec-openai",
                "moduleConfig": {
                    "text2vec-openai": {
                        "model": "ada",
                        "modelVersion": "002",
                        "type": "text",
                        "vectorizeClassName": True
                    }
                },
                "properties": [
                    {
                        "name": "title",
                        "dataType": ["string"],
                        "description": "The title of the memory",
                        "moduleConfig": {
                            "text2vec-openai": {
                                "skip": True,
                                "vectorizePropertyName": False
                            }
                        },
                    },
                    {
                        "name": "summary",
                        "dataType": ["string"],
                        "description": "The important information from the conversation",
                        "moduleConfig": {
                            "text2vec-openai": {
                                "skip": False,
                                "vectorizePropertyName": False
                            }
                        },
                    },
                    {
                        "name": "conversation",
                        "dataType": ["string"],
                        "description": "The conversation that led to the memory",
                        "moduleConfig": {
                            "text2vec-openai": {
                                "skip": True,
                            }
                        },
                    },
                    {
                        "name": "user_id",
                        "dataType": ["string"],
                        "description": "The user id in Firebase",
                        "moduleConfig": {
                            "text2vec-openai": {
                                "skip": True,
                            }
                        },
                    },
                    {
                        "name": "questions",
                        "dataType": ["string"],
                        "description": "Questions this memory can answer",
                        "moduleConfig": {
                            "text2vec-openai": {
                                "skip": True,
                                "vectorizePropertyName": False
                            }
                        },
                    }
                ]
            }
        )
        self.client.schema.create_class(
            {
                "class": "TestQuestion",
                "description": "A question that can be answered with a memory",
                "vectorizer": "text2vec-openai",
                "moduleConfig": {
                    "text2vec-openai": {
                        "model": "ada",
                        "modelVersion": "002",
                        "type": "text",
                        "vectorizeClassName": False
                    }
                },
                "properties": [
                    {
                        "name": "answeredBy",
                        "dataType": ["TestMemory"],
                        "description": "Memories that answers this question",
                    },
                    {
                        "name": "question",
                        "dataType": ["string"],
                        "description": "The question",
                        "moduleConfig": {
                            "text2vec-openai": {
                                "skip": False,
                                "vectorizePropertyName": False
                            }
                        },
                    },
                    {
                        "name": "user_id",
                        "dataType": ["string"],
                        "description": "The user id in Firebase",
                        "moduleConfig": {
                            "text2vec-openai": {
                                "skip": True,
                            }
                        },
                    },
                ]
            }
        )
        self.client.schema.create_class({
            "class": "TestInstruction",
            "description": "Instructions the user has given to the assistant",
            "properties": [
                {
                    "name": "user_id",
                    "dataType": ["string"],
                    "description": "The user id in Firebase"
                },
                {
                    "name": "name",
                    "dataType": ["string"],
                    "description": "The name of the instruction"
                },
                # TODO
            ]
        })

    def create_memory(self, title: str, conversation: str, summary: str, user_id: str, questions: str):
        return self.client.data_object.create(
            {
                "title": title,
                "summary": summary,
                "conversation": conversation,
                "user_id": user_id,
                "questions": questions
            },
            "Memory"
        )

    def create_question(self, question: str, user_id: str):
        return self.client.data_object.create(
            {
                "question": question,
                "user_id": user_id,
            },
            "Question"
        )

    def create_test_memory(self, title: str, conversation: str, summary: str, user_id: str, questions: str):
        data_uuid = self.client.data_object.create(
            {
                "title": title,
                "summary": summary,
                "conversation": conversation,
                "user_id": user_id,
                "questions": questions
            },
            "TestMemory"
        )
        return data_uuid

    def create_test_question(self, question: str, user_id: str):
        data_uuid = self.client.data_object.create(
            {
                "question": question,
                "user_id": user_id,
            },
            "TestQuestion"
        )
        return data_uuid

    def delete_test_schema(self):
        if self.client.schema.get("TestQuestion"):
            self.client.schema.delete_class("TestQuestion")
        if self.client.schema.get("TestMemory"):
            self.client.schema.delete_class("TestMemory")
        if self.client.schema.get("TestInstruction"):
            self.client.schema.delete_class("TestInstruction")


class Query:
    def __init__(self, client):
        self.client = client

    def _query(self,
               class_name,
               properties,
               additional_properties=None,
               filter_condition=None,
               near_text=None,
               return_dict=False,
               object_type=None):
        """
        filter_condition: The filter condition to query the data
        class_name: The class name of the data to query
        properties: The properties to return
        return_dict: If true, it will return the raw dict, otherwise it will return the object
        object_type: The object type to return
        near_text: The near text to query (only for documents)
        """
        query_result = (
            self.client.query
            .get(class_name, properties)
        )
        if filter_condition:
            query_result = query_result.with_where(filter_condition)
        if additional_properties:
            query_result = query_result.with_additional(additional_properties)
        if near_text:
            query_result = query_result.with_near_text(near_text)
        query_result = query_result.do()
        if return_dict:
            return query_result['data']['Get']
        elif object_type:
            return [object_type.from_query_result(data) for data in query_result['data']['Get'][class_name]]
        else:
            return query_result
