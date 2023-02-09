
import time


def search_memory(weaviate, query: str):
    print("QUERY:", query)
    results = weaviate.query._query(
        "Question",
        ["question", "answeredBy {... on Memory {_additional {id} }}"],
        near_text={
            "concepts": [query],
            "distance": 0.7
        },
        additional_properties=[
            "id",
            "distance",
        ]
    )
    # The properties are stored in result['data']['Get']['Memory'].
    results = results['data']['Get']['Question']
    # The ids of the Memory objects are stored in result['answeredBy']['_additional']['id'].
    memory_uuids = [result['answeredBy'][0]['_additional']['id'] for result in results]
    # Generate a where_filter
    where_filter = {
        "operator": "Or",
        "operands": [
            {
                "path": ["id"],
                "operator": "Equal",
                "valueString": memory_uuid
            } for memory_uuid in memory_uuids
        ]
    }
    
    results = weaviate.query._query(
        "Memory",
        ["title", "summary", "conversation", "questions"],
        filter_condition=where_filter,
        near_text={
            "concepts": [query],
            "distance": 0.3
        },
        additional_properties=["id", "distance"]
    )
    return results['data']['Get']['Memory']


def search_test_memory(weaviate, query: str):
    results = weaviate.query._query(
        "TestQuestion",
        ["question", "answeredBy {... on TestMemory {_additional {id} }}"],
        near_text={
            "concepts": [query],
            "distance": 0.2
        },
        additional_properties=[
            "id",
            "distance",
        ]
    )
    # The properties are stored in result['data']['Get']['Memory'].
    results = results['data']['Get']['TestQuestion']
    # The ids of the TestMemory objects are stored in result['answeredBy']['_additional']['id'].
    memory_uuids = [result['answeredBy'][0]['_additional']['id'] for result in results]
    # Generate a where_filter
    where_filter = {
        "operator": "Or",
        "operands": [
            {
                "path": ["id"],
                "operator": "Equal",
                "valueString": memory_uuid
            } for memory_uuid in memory_uuids
        ]
    }
    
    results = weaviate.query._query(
        "TestMemory",
        ["title", "summary", "conversation", "questions"],
        filter_condition=where_filter,
        near_text={
            "concepts": [query],
            "distance": 0.3
        },
        additional_properties=["id", "distance"]
    )
    return results['data']['Get']['TestMemory']
