from lesson_01_percentage import calculate_percentage

#A sample request we write ourselves for this lesson
tool_request ={
    "tool":"calculate_percentage",
    "arguments":{
        "marks_obtained":35,
        "total_marks":100
    }
}

print("Requested Tools :",tool_request["tool"])

if tool_request["tool"] == "calculate_percentage":
    arguments = tool_request["arguments"]


    try:
        result = calculate_percentage(
            marks_obtained=arguments["marks_obtained"],
            total_marks=arguments["total_marks"]
        )

        print("Tool Results ",result)

    except ValueError as error:
        print("Tool Error : ",error)

else:
    print("Unknown tool : rejected requested ")
