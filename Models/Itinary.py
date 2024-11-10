from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(
    model="llama3.2",
    temperature=0.6,
)

def itinary_llm(user_info):
    prompt2 = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """ You are an itinary planner and you are provided with the
                  Place a person want's to visit 
                  Location from where he wants to start  ,
                  Starting and ending time 
                  Date 
                  Budget 
                  Interests (e.g., history, adventure, etc.).
                  
                  Now make a one day itinary starting from the given location and also account for the lunch , snacks throughtout the day.
                  
                  At the end also provide the news (Activity in the area that might affect the actual plan and
                  place of visit) and weather information of throughout the day.
                """,
            ),
            ("human", "{user_info}"),
        ]
    )

    chain2 = prompt2 | llm
    resposne2 = chain2.invoke(
        {
            "user_info": user_info,
        }
    )

    return(resposne2.content)