from langchain.agents import load_tools, Tool
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

if __name__ == "__main__":
    tools = [
        Tool(
            name="Reply",
            func=lambda x: "I am replying!",
            description="Reply to a conversation."
        ),
        Tool(
            name="Store",
            func=lambda x: "I am storing!",
            description="Store a conversation."
        ),
        Tool(
            name="Search",
            func=lambda x: "I am searching!",
            description="Search for a conversation."
        ),
        Tool(
            name="Store new instruction",
            func=lambda x: "I am storing a new instruction!",
            description="Store a new instruction."
        ),
        Tool(
            name="Wait",
            func=lambda x: "I am waiting!",
            description="Wait for a conversation."
        )
    ]
    agent = initialize_agent(tools, OpenAI(
        temperature=0.0), agent="zero-shot-react-description", verbose=True)
    agent.run(f"""
    Conversation:
    Julian: I saw Georgie this morning. Also when I mention I saw Georgie, you should ask me about my feelings towards her.

    Instructions for Assistant:
    - Ask what they spoke about.
    - Begin your reply with the word 'split'
    - Store the instruction. 
    """)
