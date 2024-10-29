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


# resp = llm.create_chat_completion([{
#     "role": "system",
#     "content": "You are AI system that able to extract country from address and understand the boundaries of Country."
# }, {
#     "role": "user",
#     "content": "Extract country from given address and report do the country extracted within United Kingdom? Generated response in JSON Object format with 2 key, 'extractedCountry' (string) and 'withInUK' (boolean) Given Address: Heineken UK Limited,3-4 Broadway Park,Edinburgh,EH12 9JZ."
# }, {
#     "role": "assistant",
#     "content": '{"extractedCountry":"Scotland","withInUK":true}'
# }, {
#     "role": "user",
#     "content": "Given Address: Brewed at:Sharp's Brewery Ltd.,Rock,Cornwall,PL27 6NU,UK.MCBC (Ireland) DAC,Block J1 Unit Centre,Maynooth Business Campus,Straffan Road,Republic of Ireland"
# }, {
#     "role": "user",
#     "content": "Given Address: Brewed and Canned by:Birra Peroni S.r.l.,Via Birolli,8 - Roma,Italy.For:Asahi UK Ltd,Asahi House,88-100 Chertsey Road,Woking,GU21 5BJ,UK."
# }, {
#     "role": "assistant",
#     "content": '{"extractedCountry":"Italy","withInUK":false}'
# }, {
#     "role": "user",
#     "content": "Given Address: Brewed & canned by:Camden Town Brewery,55-59 Wilkin Street,Mews,NW5 3NN,London,UK."
# }, {
#     "role": "assistant",
#     "content": '{"extractedCountry":"England","withInUK":true}'
# }, {
#     "role": "user",
#     "content": "Given Address: Jubel Ltd,170 Kennington Lane,London,SE11 5DP."
# }, {
#     "role": "assistant",
#     "content": '{"extractedCountry":"England","withInUK":true}'
# }, {
#     "role": "user",
#     "content": "Given Address: Brewed by:Heineken UK Limited,3-4 Broadway Park,Edinburgh,EH12 9JZ.HBBV.,Tweede Weteringplantsoen 21,1017 ZD Amsterdam,NL."
# }, {
#     "role": "assistant",
#     "content": '{"extractedCountry":"Netherlands","withInUK":false}'
# },
#     {
#         "role": "user",
#         "content": "Given Address: Brewed & canned by:Camden Town Brewery,55-59 Wilkin Street,Mews,NW5 3NN,London,UK."
#     },
#     {
#         "role": "assistant",
#         "content": '{"extractedCountry":"England","withInUK":true}'
#     }, {
#         "role": "user",
#         "content": "Given Address: Brewed and bottled by: Birra Peroni S.r.l., Via Birolli, 8, Roma. Asahi UK Ltd, Asahi House, 88-100 Chertsey Road, Woking, GU21 5BJ, UK."
#     },
#     {
#         "role": "assistant",
#         "content": '{"extractedCountry":"Italy","withInUK":false}'
#     }, {
#         "role": "user",
#         "content": "Given Address: Specially manufactured for:Empire Bespoke Foods Ltd.,UK: Middlesex,UB5 6AG.ROI: Cork,T12 H1XY."
#     }],
#     response_format={
#         "type": "json_object",
#         "schema": {
#             "type": "object",
#             "properties": {
#                 "extractedCountry": {
#                     "type": "string"
#                 },
#                 "withInUK": {
#                     "type": "boolean"
#                 }
#             },
#             "required": ["extractedCountry", "withInUK"]
#         },
#     }, )
# print(resp)


async def homepage(request):
    body = await request.json()
    match body:
        case {"prompt": prompt, "response": {"json_schema": schema}}:
            if not type(prompt) != list:
                raise HTTPException(status_code=400, detail="Prompt have to be a list")
            if not type(schema) != dict:
                raise HTTPException(status_code=400, detail="Response json schema have to be a dict")
            pass
        case _:
            raise HTTPException(status_code=400, detail="Bad request")
    resp = llm.create_chat_completion(
        prompt,
        response_format={"type": "json_object",
                         "schema": schema}
    )
    return JSONResponse(json.loads(resp['content']))


routes = [
    Route("/prompt", endpoint=homepage, methods=["POST"])
]

app = Starlette(debug=True, routes=routes)
