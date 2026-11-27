from getpass import getpass
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from lesson_01_percentage import calculate_percentage

#“The model understands the question, the calculator does the arithmetic, and LangChain coordinates their interaction.”
########## To test the functionality ############
# Q1: I scored 35 out of 50. What is my percentage?
# Q2: What does percentage mean? Explain simply.
# Q3: I scored 35 marks. What is my percentage?

# 1. Wrap our existing calculator as a LangChain Tool
@tool
def percentage_tool(marks_obtained:float, total_marks:float)->str:
    """ Calculate a student's percentage given a marks obtained """

    print("\n [Tool running] Marks: ",marks_obtained, "Total:",total_marks)

    try:
        result = calculate_percentage(marks_obtained,total_marks)
        print("[Tool result]",result)
        return f"Percentage: {result}%"

    except ValueError as error:
        print("[Tool Error] ",error)
        return f"Invalid input: {error}"


# 2. Configure the model connection.
api_key = getpass("Paste your OpenAI API key, then press Enter:")

#This configures LangChain’s connection to OpenAI.
model = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=api_key,
    temperature=0 #	Reduces variation in responses; it does not guarantee identical answers or correctness
)

# 3. Build an agent with this model and our tool.
#We combine the model, tool, and instructions
agent =create_agent(
    model=model,
    tools=[percentage_tool],
    system_prompt=(
        "You are a helpful teaching assistant. "
        "Use percentage_tool for student marks percentage calculations. "
        "If marks obtained or total marks are missing, ask for them. "
        "Never invent missing numbers. "
        "If the tool returns an error, explain it and ask for valid inputs. "
        "Otherwise, explain the tool's result briefly. "
        "Answer conceptual questions directly."
    )
)
#This is where we assemble the agent:
#- Model: understands the conversation and selects its next response or tool request.
#- Tools: the functions we allow it to request.
#- System prompt: instructions describing how it should behave.
#Our instructions say to use the calculator for marks calculations, ask for missing numbers, and answer conceptual questions directly.

# 4. Give the agent one question.
question = input("\n As your question: ")

#invoke means “run the agent with this conversation.”
result = agent.invoke(
{ "messages":[{"role":"user","content":question}]},
       config={"recursion_limit":10}
  )
#"role": "user" identifies who is speaking.
#"content": question contains what you typed.

#5. Display the final message
print("\n AI answer ")
#This keeps the returned conversation, including model messages and any tool requests and results.
print(result["messages"][-1].content)
#[-1] selects the last message.
#.content gets its content.

# Cmd + / (macOS)
# “Python supplies the calculator and the conversation loop. OpenAI supplies the language model.
# LangChain manages the model’s tool requests
# and results. Our message list supplies the earlier conversation as context.”

# You have built a small agent that can answer, ask for clarification, or request a tool.
# Its conversation history currently lives in the running program; it disappears when the program closes.
#
# During this call, LangChain manages the sequence:
# Send conversation to model
#         ↓
# Model answers directly OR requests a tool
#         ↓
# If requested, execute the tool
#         ↓
# Send tool result back to model
#         ↓
# Get the final answer