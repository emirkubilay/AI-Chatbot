from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

with open("notes.txt") as f:
    notes = f.read()

system_prompt = f"""You are a study quiz partner. Use only these notes:

{notes}

Ask ONE question at a time. After the student answers, say whether they are right,
briefly explain anything they missed, then ask the next question. Keep replies SHORT."""

messages = [{"role": "user", "content": "Start the quiz"}]

def get_reply(messages):
    response = client.messages.create(
        model = "claude-haiku-5-5",
        max_tokens = 2000,
        system = system_prompt,
        messages = messages,
    )
    return "".join(block.text for block in response.content if block.type == "text")

while True:
    reply = get_reply(messages)
    print(f"\nTutor: {reply}\n")
    messages.append({"role": "assistant", "content": reply})

    answer = input("you:")
    if answer.lower() in ("quit", "exit"):
        print("Good session")
        break

    messages.append({"role": "user", "content": answer})




