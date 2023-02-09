from utils.llm_utils import make_llm_call
from utils.prompt_utils import bulletpoint_str_to_list


def store_conversation_in_memory(weaviate, conversation, test=False):

    title, summary = make_llm_call(
        prompt_template=f"""
        Write a title for the conversation and then underneath convert the conversation into a concise summary in the third person about Julian. DO NOT reduce the amount of information.
        Use the format
        Title: 
        <title>
        Summary:
        <summary>

        Conversation:
        {{conversation}}

        Title:
        """,
        input_variables=[
            'conversation'
        ],
        formatted_inputs={
            'conversation': conversation.formatted_conversation
        },
        output_fn=extract_title_summary
    )

    questions = make_llm_call(
        prompt_template=f"""
        Write a list of questions that Julian can ask the assistant to answer using this memory. Write as a bulletpoint list using the specified format for each question. Try to write each question by 'masking' one or more words in the summary. For example, if the summary is 'Julian went for a run with Blake this morning', you could write a question like 'What did Julian do this morning?' or 'Who did Julian go for a run with this morning?'.

        Memory: Julian went for a run with Blake this morning.
        Questions:
        - What did Julian do this morning?
        - What did Julian do with Blake this morning?
        - Who did Julian go for a run with this morning?
        - Who did Julian see this morning?

        Memory: Julian asked what he ate for breakfast this morning.
        Questions:
        - What has Julian asked me?

        Memory: Julian wanted to know who we saw recently.
        Questions:
        - What has Julian asked me?

        Memory: Julian worked on Animus. He implemented a test suite to test the search capabilities of Weaviate.
        Questions:
        - What has Julian worked on?
        - What did Julian do for Animus?
        - What has Julian done with Weaviate?

        Memory: {{memory}}
        Questions:
        """,
        input_variables=["memory"],
        formatted_inputs={"memory": summary},
        output_fn=bulletpoint_str_to_list
    )

    user_id = ""

    if test:
        memory_uuid = weaviate.create_test_memory(
            title, conversation.formatted_conversation, summary, user_id, "" 
        )
        for question in questions:
            question_uuid = weaviate.create_test_question(
                question, user_id)
            weaviate.client.data_object.reference.add(
                question_uuid, "answeredBy", memory_uuid, from_class_name="TestQuestion", to_class_name="TestMemory"
            )
    else:
        memory_uuid = weaviate.create_memory(
            title, conversation.formatted_conversation, summary, user_id, "" 
        )
        print("UUID", memory_uuid)
        for question in questions:
            question_uuid = weaviate.create_question(
                question, user_id)
            weaviate.client.data_object.reference.add(
                question_uuid, "answeredBy", memory_uuid, from_class_name="Question", to_class_name="Memory"
            )


def extract_title_summary(text):
    summary_start = text.index("Summary:")
    title = text[:summary_start]
    summary = text[summary_start + 9:]
    return (title, summary)
