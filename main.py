import os
import dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from Data.conv import conversation

dotenv.load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

running_conversations: Dict[str, conversation] = {}


@app.get('/')
async def llm_home():
    return {'status': f'success'}


@app.get('/start-conversation')
async def llm_start_conversation():
    try:
        id_conv = os.urandom(15).hex()

        running_conversations[id_conv] = conversation()
        return {'status': 'success', 'id': id_conv}
    except Exception as e:
        print(running_conversations)
        print(e)
        return {'status': 'error'}


class stop_model(BaseModel):
    id_conv: str


@app.delete('/close-conversation')
async def llm_stop_conversation(model: stop_model):
    try:
        del running_conversations[model.id_conv]
        return {'status': 'success'}
    except Exception as e:
        print(running_conversations)
        return {'status': 'error'}


class response_model(BaseModel):
    id_conv: str
    message: str


@app.post('/response')
def llm_response(model: response_model):
    if model.id_conv not in running_conversations:
        return {'status': 'error', 'auth': 'invalid'}

    ai = running_conversations[model.id_conv]
    ai.chat.add_message({"role": "user", "content": model.message})
    return StreamingResponse(ai.chat.generate_completion(), media_type="text/event-stream")
