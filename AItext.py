from transformers import GPT2Tokenizer, GPT2LMHeadModel

def generate_summary(text, summary_length=100):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    input_ids = tokenizer.encode(text, return_tensors="pt")
    max_length = len(input_ids[0]) + summary_length
    output = model.generate(input_ids, max_length=max_length, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return summary

# User input for the text to be summarized
text = input("Enter the text to be summarized: ")

summary = generate_summary(text, summary_length=100)
print(summary)

