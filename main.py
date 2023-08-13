from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from chat1 import get_completion_from_messages1,collect_messages_text1
from chat2 import get_completion_from_messages2,collect_messages_text2
from chat3 import get_completion_from_messages3,collect_messages_text3
from chat4 import get_completion_from_messages4,collect_messages_text4

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Message(BaseModel):
    content: str

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat1")
async def chat1(message: Message):
    user_message = message.content
    
    response = collect_messages_text1(user_message)

    return {"message": response}

@app.post("/chat2")
async def chat2(message: Message):
    user_message = message.content
    
    response = collect_messages_text2(user_message)

    return {"message": response}

@app.post("/chat3")
async def chat3(message: Message):
    user_message = message.content
    
    response = collect_messages_text3(user_message)

    return {"message": response}

@app.post("/chat4")
async def chat4(message: Message):
    user_message = message.content
    
    response = collect_messages_text4(user_message)

    return {"message": response}


@app.post("/process_voice")
async def process_voice(voice_input: dict):
    # print(voice_input)
    text = voice_input.get('input')
    # Process the voice input as needed
    # print("Voice input:", text)
    response = collect_messages_text(text)
    # print(response)
    return {"message": response}

@app.get("/templates/hotel1.html")
def hotel1(request: Request):
    return templates.TemplateResponse("hotel1.html", {"request": request})

@app.get("/templates/hotel2.html")
def hotel1(request: Request):
    return templates.TemplateResponse("hotel2.html", {"request": request})

@app.get("/templates/hotel3.html")
def hotel1(request: Request):
    return templates.TemplateResponse("hotel3.html", {"request": request})

@app.get("/templates/hotel4.html")
def hotel1(request: Request):
    return templates.TemplateResponse("hotel4.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)


# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel
# from fastapi.staticfiles import StaticFiles
# from chat import get_completion_from_messages, collect_messages_text

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")


# class Message(BaseModel):
#     content: str
#     user_phone_number: str


# @app.get("/")
# def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# @app.post("/chat")
# async def chat(message: Message):
#     user_message = message.content
#     user_phone_number = message.user_phone_number
#     response = collect_messages_text(user_message, user_phone_number)

#     return {"message": response}


# @app.post("/process_voice")
# async def process_voice(voice_input: dict):
#     # Process the voice input as needed
#     text = voice_input.get('input')
#     # Call the function to handle the conversation
#     user_phone_number = voice_input.get('user_phone_number')
#     response = collect_messages_text(text, user_phone_number)
#     return {"message": response}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, port=8000)
