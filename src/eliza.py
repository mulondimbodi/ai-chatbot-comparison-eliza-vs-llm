import re
import random

RULES = [
    # Rule 1 – Greetings
    (r'\b(hello|hi|hey|good (morning|afternoon|evening))\b',
     [
         "Hello! How are you feeling today?",
         "Hi there. What's on your mind?",
         "Hey! What would you like to talk about?",
     ]),

    # Rule 2 – Name introduction
    (r'my name is (\w+)',
     [
         "Hello, {0}. What brings you here today?",
         "Nice to meet you, {0}. How can I help?",
         "Welcome, {0}. What would you like to discuss?",
     ]),

    # Rule 3 – Feeling statements
    (r'i (feel|am feeling|am) (.*)',
     [
         "Why do you feel {1}?",
         "How long have you been feeling {1}?",
         "Does feeling {1} bother you?",
         "Tell me more about feeling {1}.",
     ]),

    # Rule 4 – Stress / exams
    (r'\b(stressed|anxious|overwhelmed|nervous)\b',
     [
         "What is making you feel stressed?",
         "Have you tried talking to someone about your stress?",
         "Stress can be difficult. What do you think is causing it?",
     ]),

    # Rule 5 – Sleep / tiredness
    (r'\b(tired|exhausted|sleepy|need (more )?sleep)\b',
     [
         "Why are you not getting enough sleep?",
         "How many hours of sleep are you getting?",
         "What is keeping you from resting?",
     ]),

    # Rule 6 – Family references
    (r'my (mother|father|mom|dad|parents?) (.*)',
     [
         "Tell me more about your {0}.",
         "How does your {0} make you feel?",
         "What role does your {0} play in your life?",
     ]),

    # Rule 7 – "I need …" statements
    (r'i need (.*)',
     [
         "Why do you need {0}?",
         "Would getting {0} really help you?",
         "What would change if you had {0}?",
     ]),

    # Rule 8 – "Because …" follow-up 
    (r'because (.*)',
     [
         "Is that the real reason?",
         "Does that reason satisfy you?",
         "What else might explain it?",
     ]),

    # Rule 9 – "I am …" identity statements
    (r"i am (.*)",
     [
         "Why do you say you are {0}?",
         "How long have you been {0}?",
         "How do you feel about being {0}?",
     ]),

    # Rule 10 – Quit / goodbye
    (r'\b(quit|bye|goodbye|exit)\b',
     [
         "Goodbye! Take care of yourself.",
         "It was good talking with you. Goodbye!",
     ]),

    # Rule 11 – Fallback / catch-all
    (r'(.*)',
     [
         "Can you tell me more about that?",
         "Interesting. Why do you say that?",
         "I see. Please continue.",
         "How does that make you feel?",
     ]),
]


def _reflect(text: str) -> str:
    """Swap first/second person pronouns so the response sounds natural."""
    REFLECTIONS = {
        "i": "you", "me": "you", "my": "your", "mine": "yours",
        "am": "are", "i'm": "you're", "i've": "you've", "i'll": "you'll",
        "you": "I", "your": "my", "yours": "mine",
    }
    words = text.lower().split()
    return " ".join(REFLECTIONS.get(w, w) for w in words)


def get_eliza_response(user_input: str) -> str:
    """Match user input against rules and return a response."""
    text = user_input.strip().lower()

    for pattern, responses in RULES:
        match = re.search(pattern, text)
        if match:
            template = random.choice(responses)
            groups = [_reflect(g) if g else "" for g in match.groups()]
            try:
                response = template
                for i, g in enumerate(groups):
                    response = response.replace(f"{{{i}}}", g)
                return response
            except Exception:
                return template

    return "Can you tell me more about that?"


# ─────────────────────────────────────────────
# Stand-alone CLI mode
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("ELIZA Chatbot  (custom rule-based version)")
    print("Type 'quit' to stop.\n")
    while True:
        user = input("You: ").strip()
        if not user:
            continue
        reply = get_eliza_response(user)
        print(f"ELIZA: {reply}\n")
        if re.search(r'\b(quit|bye|goodbye|exit)\b', user.lower()):
            break