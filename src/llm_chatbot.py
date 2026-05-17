from transformers import pipeline

chatbot = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-1.5B-Instruct"
)

def get_llm_response(user_input: str) -> str:
    """Send a user message to the LLM and return the assistant reply."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input},
    ]

    response = chatbot(
        messages,
        max_new_tokens=150,
        do_sample=True,
        temperature=0.7,
    )

    output = response[0]["generated_text"]
    if isinstance(output, list):
        for msg in reversed(output):
            if msg.get("role") == "assistant":
                return msg["content"].strip()

    if "Assistant:" in str(output):
        return str(output).split("Assistant:")[-1].strip()

    return str(output).strip()


if __name__ == "__main__":
    print("Modern AI Chatbot (Qwen2.5-1.5B-Instruct)")
    print("Type 'quit' to stop.\n")

    while True:
        user = input("You: ").strip()
        if not user:
            continue
        if user.lower() == "quit":
            print("Bot: Goodbye!")
            break
        print("Bot:", get_llm_response(user), "\n")