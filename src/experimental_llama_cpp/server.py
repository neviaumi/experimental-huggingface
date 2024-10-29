import json
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException

from llama_cpp import Llama
import os

llm = Llama(
    model_path=os.path.join(os.getcwd(), ".models", "phi-3.5", "Phi-3.5-mini-instruct-Q4_K_M.gguf"),
    n_ctx=8192,
)


async def homepage(request):
    body = await request.json()
    match body:
        case {"prompt": prompt, "response": {"json_schema": schema}}:
            if type(prompt) != list:
                raise HTTPException(status_code=400, detail="Prompt have to be a list")
            if type(schema) != dict:
                raise HTTPException(status_code=400, detail="Response json schema have to be a dict")
            if len(prompt) == 0:
                raise HTTPException(status_code=400, detail="Prompt cannot be empty")

            def parse_message(message):
                if type(message) != dict:
                    raise HTTPException(status_code=400, detail="Prompt message have to be dict")
                try:
                    return {"content": message["content"], "role": message["role"]}
                except KeyError:
                    raise HTTPException(status_code=400, detail="Prompt message have to contain role and content")

            [systemPrompt, *prompts] = prompt
            if parse_message(systemPrompt)['role'] != "system":
                raise HTTPException(status_code=400, detail="First prompt item role have to be system")
            if parse_message(prompts[-1])['role'] != 'user':
                raise HTTPException(status_code=400, detail="Last prompt item role have to be user")
            for index, p in enumerate(prompts):
                expected_role = "user" if index % 2 == 0 else "assistant"
                if parse_message(p)['role'] != expected_role:
                    raise HTTPException(status_code=400,
                                        detail="Prompt item should follow alternately user and assistant")
            pass
        case _:
            raise HTTPException(status_code=400, detail="Bad request")
    resp = llm.create_chat_completion(
        prompt,
        response_format={"type": "json_object",
                         "schema": schema}
    )
    resp_message = resp['choices'][0]['message']['content']
    return JSONResponse(json.loads(resp_message))


routes = [
    Route("/prompt", endpoint=homepage, methods=["POST"])
]

app = Starlette(debug=True, routes=routes)
