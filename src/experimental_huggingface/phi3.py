import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import accelerate

torch.random.manual_seed(0)

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3.5-mini-instruct",
    # attn_implementation="eager",
    torch_dtype="auto",
    # device_map={"": "cpu"},
    device_map="auto",
    trust_remote_code=True,
)
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3.5-mini-instruct")
print("Model and tokenizer loaded successfully.")
messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "Can you provide ways to eat combinations of bananas and dragonfruits?"},
    {"role": "assistant", "content": "Sure! Here are some ways to eat bananas and dragonfruits together: 1. Banana and dragonfruit smoothie: Blend bananas and dragonfruits together with some milk and honey. 2. Banana and dragonfruit salad: Mix sliced bananas and dragonfruits together with some lemon juice and honey."},
    {"role": "user", "content": "What about solving an 2x + 3 = 7 equation?"},
]

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)

generation_args = {
    "max_new_tokens": 100,
    "return_full_text": False,
    "do_sample": False,
}
print("Generating response...")
output = pipe(messages, **generation_args)
print(output[0]['generated_text'])
