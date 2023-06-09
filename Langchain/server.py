
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain.document_loaders import TextLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
index_creator = VectorstoreIndexCreator()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    prompt: str
    
class Context(BaseModel):
    text: str

@app.post("/generate/")
async def generate(prompt: Prompt):

    loader = TextLoader('text.txt')
    docsearch = index_creator.from_loaders([loader])
    query = prompt.prompt
    docs = docsearch.similarity_search(query)
    chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
    res = chain.run(input_documents=docs, question=query)
    return res

@app.post("/context/")
async def generate(prompt: Context):
    string_to_save = prompt.text
    with open("text.txt", "a") as file:
        file.write(string_to_save)