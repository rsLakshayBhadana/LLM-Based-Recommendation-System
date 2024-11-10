from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(
    model="llama3.2",
    temperature=0.6,
)

def check(user_info):
    prompt1 = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                    You are an evalutor and evalutes the input text by looking for the below mentioned info and if any of the 
                    information is not available you will respond "No" : otherwise , Respond with "Yes".

                    Information that needs to check:

                    1.The place where you plan to go.
                    2.The date of your trip.
                    3.The starting and ending time of your trip.
                    4.Your interests (e.g., history, adventure, etc.).
                    5.Budget for the trip.
                    6.The starting point at the given place (e.g., a landmark, hotel, etc.).

                    Strict rules : Respond "Yes" only if all the above information is available if any information if missing Respond : "No"
                    Output format : "Yes" Or "No" . not any additional information
                """,
            ),
            ("human", "{user_info}"),
        ]
    )
    
    chain1 = prompt1 | llm

    resposne1 = chain1.invoke(
        {
            "user_info": user_info,
        }
    )

    return(resposne1.content)