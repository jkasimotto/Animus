# Project Specification:
## Input:
- HTTP request object, containing a message stack (series of messages between multiple users) and an executed instruction stack (series of instructions that have been executed for the AI to follow)
- Firestore database for basic user information
- Weaviate database for storing documents and instructions

## Output:
HTTP response object with headers and a status code
  - Updated message stack
  - Updated executed instruction stack
## Data Structures:
- Instruction: contains information about a specific instruction, text (text string), questions (text strings), booleans (booleans), actions (text strings), topics (text strings).
- Action: An enum that contains the order of operations (Miscellaneous, Search, Ask, Store, Update, Delete)
- MessageStack: stores the message history between multiple users.
- Message: has a user_id and text.
- Session: maintains the session state. Which entities are participating. Which messages have been passed. Which actions have been executed (and which instructions they belong to). Which actions are to be executed (and which instructions they belong to).

## Process:
1. Connect to the Firestore and Weaviate databases
2. Parse the input HTTP request object, extracting the session. 
3. Get instructions from the Weaviate database based on the entity IDs involved in the session 
4. Chunk the input text by instruction and sort the instructions by order of operations (Miscellaneous, Search, Ask, Store, Update, Delete)
5. Process the instruction queue. Some instructions have actions that require saving the session state and sending a response to the user. Some instructions produce output that is passed to a FrontendBot responsible for generating a text reply to the user. 
6. Call specific functions based on the action reached:
7. Use a large language model to generate a text reply and any additional data
8. Package the text reply, additional data, and the updated session into the HTTP response object, along with headers and a status code.
9. Send the HTTP response object back to the user, this is the last step of the process.

## Additional Notes:
The program should be able to handle errors that may occur while processing the instructions and should have a mechanism in place to save the current state of the program, including the message stack, executed instruction stack, and current instruction queue, and generate a text reply acknowledging the error and asking the user if they would like to try again.