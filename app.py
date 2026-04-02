import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.openaillm import OpenAILLM
import os
from dotenv import load_dotenv

load_dotenv()

app= FastAPI()

os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")


@app.post("/blogs")
async def create_blogs(request:Request):
    data= await request.json()
    topic= data.get("topic","")
    language= data.get("current_language","")

    # Initalize the LLM
    openai_llm_obj= OpenAILLM()
    llm= openai_llm_obj.get_llm()
    # Initialize the Graph
    graph_obj= GraphBuilder(llm)

    if topic and language:
        graph= graph_obj.setup_graph(usecase="language")
        state= graph.invoke({"topic":topic, "current_language":language})
    elif topic:
        graph= graph_obj.setup_graph(usecase="topic")
        state= graph.invoke({"topic":topic})
    
    return {"data": state}


if __name__=="__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)
