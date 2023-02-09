I definitely need to get the user to verify the Instruction when creating. Case in point is the following. It's meant to be throughout the day, not after 6pm...
```
Turn the instruction into a list of direct (second person) instructions you could give to your six-year-old brother. 

Julian: When I say I saw someone and it's not clear what we spoke about, ask me.
- Ask Julian what they spoke about.

Julian: When I say the word banana begin your reply with the word split. 
- Begin your reply with the word 'split'.

Julian: When it's after 6pm and you don't know what I've eaten, ask me what I've eaten that day.

> Finished chain.
>>> x.direct_instructions                                                                              
['Ask Julian what he has eaten that day after 6pm.']
```

20230202-1212
Sometimes if your LLM outputs aren't working simply adding more examples helps.

20230202-1412
The agent in Langchain isn't robust. See this example:
```
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


I need to store the instruction and then reply to the conversation.
Action: Store new instruction
Action Input: Ask what they spoke about. Begin your reply with the word 'split'.
Observation: I am storing a new instruction!
Thought: I now need to reply to the conversation.
Action: Reply
Action Input: Hi Julian, split what did you two talk about?
Observation: I am replying!
```