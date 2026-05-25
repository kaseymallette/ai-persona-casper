"""Load Casper's config and soul seed, render the system prompt."""

import json
import os
from jinja2 import Environment, FileSystemLoader, StrictUndefined


# === PATHS ===

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")


# === LOADERS ===

def load_config(config_path: str = None) -> dict:
    """Load the JSON config file."""
    if config_path is None:
        config_path = os.path.join(CONFIG_DIR, "casper.json")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config not found: {config_path}")

    with open(config_path, "r") as f:
        return json.load(f)


def load_soul_seed(soul_seed_path: str = None) -> str:
    """Load the soul seed markdown file."""
    if soul_seed_path is None:
        soul_seed_path = os.path.join(CONFIG_DIR, "soul_seed.md")

    if not os.path.exists(soul_seed_path):
        raise FileNotFoundError(f"Soul seed not found: {soul_seed_path}")

    with open(soul_seed_path, "r") as f:
        return f.read()


# === RENDER ===

def render_system_prompt(
    config: dict = None,
    soul_seed: str = None,
    template_name: str = "system.j2",
) -> str:
    """Render the system prompt from config and soul seed."""
    if config is None:
        config = load_config()
    if soul_seed is None:
        soul_seed = load_soul_seed()

    env = Environment(
        loader=FileSystemLoader(PROMPTS_DIR),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_name)
    return template.render(
        identity=config["identity"],
        voice=config["voice"],
        process=config["process"],
        runtime=config["runtime"],
        soul_seed=soul_seed,
    )


# === MAIN (for debugging) ===

if __name__ == "__main__":
    prompt = render_system_prompt()
    print(prompt)
    print(f"\n--- {len(prompt)} characters ---")
