
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from chat import get_completion_from_messages
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from chat import get_completion_from_messages

app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")

class Message(BaseModel):
    message: str

@app.get("/")
def main():
    with open("templates/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# @app.post("/completion")
# async def chat_completion(message: str) -> str:
#     response = get_completion_from_messages([message])
#     return response

@app.post("/completion")
async def chat_completion(message: Message) -> str:
    messages = [m.content for m in message.messages]
    print(messages)
    response = get_completion_from_messages(messages)
    return {"choices": [{"message": {"content": response}}]}