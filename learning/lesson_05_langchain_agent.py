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
model = ChatOpenAI(
    model="gpt-4.1-mini",
    api_key=api_key,
    temperature=0
)

# 3. Build an agent with this model and our tool.
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

# 4. Give the agent one question.
question = input("\n As your question: ")

result = agent.invoke(
{ "messages":[{"role":"user","content":question}]},
       config={"recursion_limit":10}
  )

#5. Display the final message
print("\n AI answer ")
print(result["messages"][-1].content)