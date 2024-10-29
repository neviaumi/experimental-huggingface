from starlette.testclient import TestClient
from experimental_llama_cpp import server


def test_prompt_empty_prompt():
    client = TestClient(server.app)
    response = client.post("/prompt", json={
        "prompt": [],
        "response": {"json_schema": {}}
    })
    assert response.status_code == 400, "Empty prompt should return 400 status code."
    assert response.text == "Prompt cannot be empty", "Empty prompt should return 'Prompt cannot be empty'."


def test_prompt_not_list_prompt():
    client = TestClient(server.app)
    response = client.post("/prompt", json={
        "prompt": "This is not a list",
        "response": {"json_schema": {}}
    })
    assert response.status_code == 400, "Non-list prompt should return 400 status code."
    assert response.text == "Prompt have to be a list", "Non-list prompt should return 'Prompt have to be a list'."


def test_prompt_not_object_schema():
    client = TestClient(server.app)
    response = client.post("/prompt", json={
        "prompt": [],
        "response": {"json_schema": ""}
    })
    assert response.status_code == 400, "Non-object schema should return 400 status code."
    assert response.text == "Response json schema have to be a dict", "Non-object schema should return 'Response json schema have to be a dict'."


def test_prompt_without_system_role():
    client = TestClient(server.app)
    response = client.post("/prompt", json={
        "prompt": [{
            "role": "user",
            "content": "Given Address: Brewed & canned by:Camden Town Brewery,55-59 Wilkin Street,Mews,NW5 3NN,London,UK."
        }],
        "response": {"json_schema": {}}
    })
    assert response.status_code == 400, "Prompt without system role should return 400 status code."
    assert response.text == "First prompt item role have to be system", "Prompt without system role should return 'Prompt have to contain system role on top'."


def test_prompt_not_object_prompt_item():
    client = TestClient(server.app)
    response = client.post("/prompt", json={
        "prompt": [
            "Given Address: Brewed & canned by:Camden Town Brewery,55-59 Wilkin Street,Mews,NW5 3NN,London,UK."],
        "response": {"json_schema": {}}
    })
    assert response.status_code == 400, "Prompt without system role should return 400 status code."
    assert response.text == "Prompt message have to be dict", "Non Object prompt item should return 'Prompt message have to be dict'."


def test_prompt_missing_key_on_prompt_item():
    client = TestClient(server.app)
    response = client.post("/prompt", json={
        "prompt": [
            {
                "content": "Given Address: Brewed & canned by:Camden Town Brewery,55-59 Wilkin Street,Mews,NW5 3NN,London,UK."}],
        "response": {"json_schema": {}}
    })
    assert response.status_code == 400, "Prompt without system role should return 400 status code."
    assert response.text == "Prompt message have to contain role and content", "Missing key on prompt item should return 'Prompt message have to contain role and content'."


def test_prompt_last_item_role_is_not_user():
    client = TestClient(server.app)
    response = client.post("/prompt", json={
        "prompt": [
            {
                "role": "system",
                "content": "You are AI system that able to extract country from address and understand the boundaries of Country."
            }, {
                "role": "assistant",
                "content": '{"extractedCountry":"Netherlands","withInUK":false}'
            }],
        "response": {"json_schema": {}}
    })
    assert response.status_code == 400, "Last prompt item role isn't user should return 400 status code."
    assert response.text == "Last prompt item role have to be user", "Last prompt item role isn't user should return 'Last prompt item role have to be user'."


def test_prompt_item_should_alternating_with_user_and_assistant():
    client = TestClient(server.app)
    response = client.post("/prompt", json={
        "prompt": [{
            "role": "system",
            "content": "You are AI system that able to extract country from address and understand the boundaries of Country."
        }, {
            "role": "assistant",
            "content": '{"extractedCountry":"Scotland","withInUK":true}'
        }, {
            "role": "user",
            "content": "Extract country from given address and report do the country extracted within United Kingdom? Generated response in JSON Object format with 2 key, 'extractedCountry' (string) and 'withInUK' (boolean) Given Address: Heineken UK Limited,3-4 Broadway Park,Edinburgh,EH12 9JZ."
        },
            {
                "role": "user",
                "content": "Given Address: Brewed at:Sharp's Brewery Ltd.,Rock,Cornwall,PL27 6NU,UK.MCBC (Ireland) DAC,Block J1 Unit Centre,Maynooth Business Campus,Straffan Road,Republic of Ireland"
            }],
        "response": {"json_schema": {}}
    })
    assert response.status_code == 400, "Prompt item should isn't alternately order should return 400 status code."
    assert response.text == "Prompt item should follow alternately user and assistant"


def test_prompt_response_json():
    client = TestClient(server.app)
    response = client.post("/prompt", json={
        "prompt": [{
            "role": "system",
            "content": "You are AI system that able to extract country from address and understand the boundaries of Country."
        },
            {
                "role": "user",
                "content": "Extract country from given address and report do the country extracted within United Kingdom? Generated response in JSON Object format with 2 key, 'extractedCountry' (string) and 'withInUK' (boolean) Given Address: Heineken UK Limited,3-4 Broadway Park,Edinburgh,EH12 9JZ."
            }, {
                "role": "assistant",
                "content": '{"extractedCountry":"Scotland","withInUK":true}'
            },
            {
                "role": "user",
                "content": "Given Address: Brewed at:Sharp's Brewery Ltd.,Rock,Cornwall,PL27 6NU,UK.MCBC (Ireland) DAC,Block J1 Unit Centre,Maynooth Business Campus,Straffan Road,Republic of Ireland"
            }],
        "response": {"json_schema": {
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
        }, }
    })
    assert response.status_code == 200, "Valid prompt should return 200 status code."
    assert response.json() == {
        "extractedCountry": 'Republic of Ireland',
        "withInUK": False
    }, "Valid prompt should return JSON response."
