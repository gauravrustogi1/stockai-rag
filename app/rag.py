from .vectorstore import queryDB
import ollama

def getAnswer(question, debugMode=False):
    queryResponse = queryDB(question, 20)
    contextChunks = queryResponse['documents'][0]
    context = "\n\n---\n\n".join(contextChunks)
    prompt = buildPrompt(context)
    llmResponse = getLLMResponse(prompt, question)
    returnValue = cleanLLMResponse(llmResponse, queryResponse, debugMode)
    return returnValue


def cleanLLMResponse(llmResponse, queryResponse, debugMode):
    returnValue = {
        "answer": llmResponse,
        "debugChunks": [
            {
                "type": queryResponse['metadatas'][0][i]['type'],
                "symbol": queryResponse['metadatas'][0][i]['symbol'],
                "distance": queryResponse['distances'][0][i],
                "text": queryResponse['documents'][0][i][:200]
            }
            for i in range(len(queryResponse['documents'][0]))
        ] if debugMode else []
    }
    return returnValue

def getLLMResponse(prompt, question):
    returnValue = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ]
    )
    return returnValue['message']['content']

def buildPrompt(context):
    systemPrompt = f"""You are a financial data analyst assistant. Your job is to analyze 
the provided financial data and answer questions about it factually.
You are NOT giving personal investment advice. You are reading data and 
reporting what it shows — like a research analyst writing a report.
Always answer based on the data provided. Never refuse to analyze the data.
If the data supports a conclusion, state it clearly with the numbers.

    Context:
    {context}
    """
    return systemPrompt
