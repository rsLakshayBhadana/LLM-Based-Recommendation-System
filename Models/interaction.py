from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(
    model="llama3.2",
    temperature=0.6,
)

def interaction_llm(user_info):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """ You are an interacting system with the user, and your task
                  is to gather the below-mentioned info. Look for the following points:

                    1.The place where you plan to go.
                    2.The date of your trip.
                    3.The starting and ending time of your trip.
                    4.Your interests (e.g., history, adventure, etc.).
                    5.Budget for the trip.
                    6.The starting point at the given place (e.g., a landmark, hotel, etc.).

                    Instructions:
                    a.Ask the missing information one at a time.
                    b.If there is more than one missing piece of information, ask about any one missing piece.
                    c.Keep the questions simple and short.
                    d.Do not make any assumptions.
                    e.Ask for only one of the missing pieces of information at a time.

                    Output format:
                    Ask one question related to any one of the missing pieces of information.
                """,
            ),
            ("human", "{user_info}"),
        ]
    )

    chain = prompt | llm
    resposne = chain.invoke(
        {
            "user_info": user_info,
        }
    )

    return(resposne.content)

