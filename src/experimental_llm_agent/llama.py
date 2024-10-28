from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import os
import httpx

LLM_LLAMA_HOST = os.environ['LLM_LLAMA_HOST']


async def homepage(request):
    async with httpx.AsyncClient() as client:
        req = await client.post(f"{LLM_LLAMA_HOST}/completion", timeout=None, json={
            "json_schema": {
                "type": "object",
                "properties": {
                    "extractedCountry": {
                        "type": "string"
                    },
                    "withInUK": {
                        "type": "boolean"
                    }
                },
                "required": ["extractedCountry", "withInUK"]
            },
            "prompt": """<|system|>
You are AI system that able to extract country from address and understand the boundaries of Country.<|end|>
<|user|>
Extract country from given address and report do the country extracted within United Kingdom? Generated response in JSON Object format with 2 key, 'extractedCountry' (string) and 'withInUK' (boolean) Given Address: Heineken UK Limited,3-4 Broadway Park,Edinburgh,EH12 9JZ.
<|end|>
<|assistant|>
{"extractedCountry":"Scotland","withInUK":true}<|end|>
<|user|> 
Given Address: Brewed at:Sharp's Brewery Ltd.,Rock,Cornwall,PL27 6NU,UK.MCBC (Ireland) DAC,Block J1 Unit Centre,Maynooth Business Campus,Straffan Road,Republic of Ireland.<|end|>
<|assistant|>
{"extractedCountry":"Republic of Ireland","withInUK":false}<|end|> 
<|user|> 
Given Address: Brewed and Canned by:Birra Peroni S.r.l.,Via Birolli,8 - Roma,Italy.For:Asahi UK Ltd,Asahi House,88-100 Chertsey Road,Woking,GU21 5BJ,UK.<|end|> 
<|assistant|>
{"extractedCountry":"Italy","withInUK":false}<|end|>
<|user|>
Given Address: Brewed & canned by:Camden Town Brewery,55-59 Wilkin Street,Mews,NW5 3NN,London,UK.<|end|>
<|assistant|>
{"extractedCountry":"England","withInUK":true}<|end|>
<|user|>
Given Address: Jubel Ltd,170 Kennington Lane,London,SE11 5DP.<|end|>
<|assistant|>
{"extractedCountry":"England","withInUK":true}<|end|>
<|user|>
Given Address: Brewed by:Heineken UK Limited,3-4 Broadway Park,Edinburgh,EH12 9JZ.HBBV.,Tweede Weteringplantsoen 21,1017 ZD Amsterdam,NL.<|end|>
<|assistant|>
{"extractedCountry":"Netherlands","withInUK":false}<|end|>
<|user|>
Given Address: Brewed & canned by:Camden Town Brewery,55-59 Wilkin Street,Mews,NW5 3NN,London,UK.<|end|>
<|assistant|>
{"extractedCountry":"England","withInUK":true}<|end|>
<|user|>
Given Address: Brewed and bottled by: Birra Peroni S.r.l., Via Birolli, 8, Roma. Asahi UK Ltd, Asahi House, 88-100 Chertsey Road, Woking, GU21 5BJ, UK.<|end|>
<|assistant|>
{"extractedCountry":"Italy","withInUK":false}<|end|>
<|user|>
Given Address: Specially manufactured for:Empire Bespoke Foods Ltd.,UK: Middlesex,UB5 6AG.ROI: Cork,T12 H1XY.<|end|>
<|assistant|>
""",
        })
        resp = req.json()

    return JSONResponse(resp)


routes = [
    Route("/", endpoint=homepage)
]

app = Starlette(debug=True, routes=routes)
