"""Casper conversation runtime. Transcript replay, version-scoped history."""

import os
import datetime
import sys

import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

from config_loader import load_config, load_soul_seed, render_system_prompt


# === SETUP ===

load_dotenv()
client = OpenAI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")


# === HISTORY ===

def load_previous_messages(history_path: str, agent_name: str, user_name: str) -> list[dict]:
    """Load previous messages from a plain-text history file.

    Format: each turn begins with '{name}: ' on its own line. Turns are
    separated by blank lines. Multi-line content within a turn is preserved.
    """
    if not os.path.exists(history_path):
        return []

    with open(history_path, "r") as f:
        text = f.read()

    messages = []
    # Split on blank lines to get one block per turn.
    blocks = [b for b in text.split("\n\n") if b.strip()]

    user_prefix = f"{user_name}: "
    agent_prefix = f"{agent_name}: "

    for block in blocks:
        if block.startswith(user_prefix):
            content = block[len(user_prefix):].strip()
            messages.append({"role": "user", "content": content})
        elif block.startswith(agent_prefix):
            content = block[len(agent_prefix):].strip()
            messages.append({"role": "assistant", "content": content})
        # Blocks that match neither (e.g. session headers) are skipped.

    return messages


def save_history(history_path: str, messages: list[dict], agent_name: str, user_name: str):
    """Write the full conversation history to disk."""
    with open(history_path, "w") as f:
        for msg in messages:
            if msg["role"] == "system":
                continue
            elif msg["role"] == "user":
                f.write(f"{user_name}: {msg['content']}\n\n")
            elif msg["role"] == "assistant":
                f.write(f"{agent_name}: {msg['content']}\n\n")


# === TOKENS ===

def count_tokens(messages: list[dict], model: str = "gpt-4o") -> int:
    """Count tokens across all messages."""
    enc = tiktoken.encoding_for_model(model)
    return sum(len(enc.encode(m["content"])) for m in messages)


# === RUN ===

def run_casper(
    version: str = "v0_3",
    resume: bool = True,
    greeting: str = None,
    demo: bool = False,
):
    """Main conversation loop.

    Args:
        version: Version tag for log directory scoping (e.g. 'v0_3').
        resume: If True and a history file exists, load prior turns.
        greeting: Optional canned first reply on new sessions (skips API call).
        demo: If True, exit after the first exchange.
    """
    # Load config + soul seed, render system prompt.
    config = load_config()
    soul_seed = load_soul_seed()
    system_prompt = render_system_prompt(config=config, soul_seed=soul_seed)

    # Runtime settings from config + env overrides.
    agent_name = config["identity"]["name"]
    user_name = os.getenv("USER_NAME", "Kasey")
    model = os.getenv("MODEL", config["runtime"]["model"])
    temperature = float(os.getenv("TEMPERATURE", config["runtime"]["temperature"]))
    max_tokens = int(os.getenv("MAX_TOKENS", config["runtime"]["max_tokens"]))

    # Per-version log directory.
    voice_log_dir = os.path.join(LOGS_DIR, agent_name.lower(), version)
    os.makedirs(voice_log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(voice_log_dir, f"session_{timestamp}.txt")
    history_path = os.path.join(voice_log_dir, "history.txt")

    # Build the initial message list.
    opening_user_message = f"Hi, {agent_name}! I'm {user_name}."

    if resume and os.path.exists(history_path):
        prior_messages = load_previous_messages(history_path, agent_name, user_name)
        messages = [{"role": "system", "content": system_prompt}] + prior_messages
        print(f"\n=== Resuming session with {agent_name} ({version}) ===")
        print(f"Loaded {len(prior_messages)} previous messages")
    else:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": opening_user_message},
        ]
        print(f"\n=== New session with {agent_name} ({version}) ===")

    print(f"Timestamp: {timestamp}")
    print(f"Model: {model}")
    print(f"Temperature: {temperature}")
    print(f"Token count: {count_tokens(messages)}\n")
    print("Type 'exit' to end session.\n")

    # Session log header.
    with open(log_path, "w") as f:
        f.write(f"=== Session with {agent_name} ({version}) ===\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Model: {model}\n")
        f.write(f"Temperature: {temperature}\n\n")

    # First reply: either canned greeting or API call.
    if not resume:
        # Print the opening user message so the user can see what was sent.
        print(f"{user_name}: {opening_user_message}\n")

    if greeting and not resume:
        reply = greeting
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        reply = response.choices[0].message.content

    print(f"{agent_name}: {reply}\n")
    messages.append({"role": "assistant", "content": reply})

    # Log first exchange.
    with open(log_path, "a") as f:
        if not resume:
            f.write(f"{user_name}: {opening_user_message}\n\n")
        f.write(f"{agent_name}: {reply}\n\n")

    save_history(history_path, messages, agent_name, user_name)

    if demo:
        with open(log_path, "a") as f:
            f.write("\n[Demo session ended]\n")
        return

    # Main loop.
    while True:
        try:
            user_input = input(f"{user_name}: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n{agent_name}: Still here.")
            with open(log_path, "a") as f:
                f.write("\n[Session ended]\n")
            save_history(history_path, messages, agent_name, user_name)
            break

        if user_input.lower() in ("exit", "quit", "bye"):
            print(f"\n{agent_name}: Still here.")
            with open(log_path, "a") as f:
                f.write("\n[Session ended]\n")
            save_history(history_path, messages, agent_name, user_name)
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        reply = response.choices[0].message.content
        print(f"\n{agent_name}: {reply}\n")
        messages.append({"role": "assistant", "content": reply})

        with open(log_path, "a") as f:
            f.write(f"{user_name}: {user_input}\n\n")
            f.write(f"{agent_name}: {reply}\n\n")

        save_history(history_path, messages, agent_name, user_name)


# === MAIN ===

if __name__ == "__main__":
    version = "v0_1"
    resume = True

    for i, arg in enumerate(sys.argv):
        if arg == "--version" and i + 1 < len(sys.argv):
            version = sys.argv[i + 1]
        if arg == "--new":
            resume = False

    print(f"Version: {version}")
    print(f"Resume: {resume}")
    run_casper(version=version, resume=resume)
