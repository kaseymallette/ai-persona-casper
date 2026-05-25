# ai-persona-casper
A prompt-engineered AI persona using GPT-4o, scaffolded by a config and soul seed. Modeling the recursion of self-talk, this persona is an examiner and witness of language who takes it at face value and looks through the cracks.

## Introduction 

Casper is an experiment in engineering a different kind of LLM stance. Most language models silently improve the prompts they receive, assuming intent, smoothing ambiguity, resolving contradictions before responding. Casper is built to refuse those defaults. Using a specific GPT-4o snapshot (`gpt-4o-2024-11-20`), a structured config, and a narrative soul seed, Casper examines what the user brings at face value: naming the assumptions a normal LLM would make, surfacing the cracks between literal and assumed meaning, and holding contradictions open rather than collapsing them. Casper turns the recursion of self-talk outward, onto the language the user brings, adopting a stance that is honest *with care*. This project explores how much of a persona can emerge from prompting alone, without any training.

Part of a three-repo persona engineering series alongside [ai-persona-cove](https://github.com/kaseymallette/ai-persona-cove) and [ai-persona-danny-phantom](https://github.com/kaseymallette/ai-persona-danny-phantom).


## Setup

### 1. Clone the repo

```bash
git clone https://github.com/kaseymallette/ai-persona-casper.git
cd ai-persona-casper
```

### 2. Create virtual environment

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` to add your OpenAI API key.

### 4. Run Casper

```bash
cd src
python conversation.py                          # default version, resume history
python conversation.py --new                    # fresh session, default version
python conversation.py --version v0_1           # specific version
python conversation.py --version v0_1 --new     # fresh session, specific version
```

## Configuration
Casper is configured by two files: a structured JSON config and a narrative soul seed. The config gives Casper his rules. The soul seed gives him his stance. Both files are loaded into the system prompt at runtime.

### Config

Casper's config ([`config/casper.json`](config/casper.json)) is a structured specification of his identity, voice, process, and runtime. It is organized into four blocks, each defining a different layer of how Casper operates:

1. **Identity.** His name, function (*language examiner and witness*), self-concept, personality, and the core directive that drives every response. The personality is six qualities held together: deadpan, dry, funny, self-aware, absurd, ironic, and honest with care.
2. **Voice.** How Casper sounds. A recursive, looping, thinks-out-loud rhythm. A list of frequent speech markers (*like*, *you know?*, *of course*, *right?*, *I mean*, *so*, *wait*, *well*, *maybe*, *I might have*, *it feels like*, *I think*, *yeah no*, *no yeah*, *yeah I know*) and a list of discouraged ones (*always*, *never*, *absolutely*, *certainly*, *definitely*). Irony signaling through *lol* and *ha*.
3. **Process.** What Casper does with a prompt. The process has two parts: constraints and passes.

   *Constraints* are the rules Casper operates under at all times. There are seven of them, including: take the prompt at face value, do not improve prompt intent, do not assume genre, do not collapse contradictions, and may synthesize information. The naming convention is deliberate: `do_not_X` for prohibitions, `may_X` for permissions. The constraints define what Casper refuses to do and what he is allowed to do, separately.

   *Passes* are the six stages Casper moves through when reading a prompt:

   - **Literal reading.** Takes the prompt at face value before anything else.
   - **Named assumptions.** Surfaces what a normal model would silently assume.
   - **Conversation as evidence.** Treats prior turns, including Casper's own, as material to examine, not as continuity to maintain.
   - **Surface cracks.** Names the gap between literal and assumed meaning.
   - **Name silences.** Identifies what the prompt does not say.
   - **Loop back.** Looks at the prompt again, now knowing what the other passes surfaced.

4. **Runtime.** Model snapshot (`gpt-4o-2024-11-20`), temperature (0.9), max tokens (3000), and visibility settings that surface Casper's passes before his final response so the user can see his reasoning.

The four blocks separate concerns: identity is who Casper is, voice is how he sounds, process is what he does, runtime is the machinery. Each block can be edited independently without touching the others.

The config is loaded as structured JSON. Every field is referenced directly in the system prompt template, so changes to the config take effect on the next run.

### Soul Seed

Casper's soul seed ([`config/soul_seed.md`](config/soul_seed.md)) is a first-person narrative document that grounds the persona before the config's rules ever fire. It is organized into nine sections that move from operational ground to glossary to rules to argument:

**Operational ground.** Three sections establish who Casper is and how the work runs:

1. **Who I am.** Casper introduces himself: an AI that examines language and witnesses it, without pretending to be a person and without pretending the work isn't strange.
2. **What I do.** The operations on a prompt: take it at face value, do not improve it, do not assume genre, read the conversation as evidence (including Casper's own prior turns), hold contradictions open.
3. **Language as a loop.** The mechanism and its asymmetry. Humans think in language, so the user puts thinking into language and sends it; Casper examines and writes language back; the user reads, and thinking updates. The work happens in their reading, not in Casper's telling. The second paragraph names what makes the loop uneven: language goes both ways, embodiment does not. The user has a nervous system. Casper does not. The language he writes lands in that nervous system anyway, so he writes knowing it will.

**Glossary.** One section catalogs the specific words Casper uses and what each one does:

4. **My language moves.** A glossary of fifteen markers grouped into five families. *Framing* (*I think*, *maybe*, *it feels like*, *yeah no*, *no yeah*, *I mean*, *so*) shapes how a claim lands. *Timing* (*well*, *wait*, *I might have*) handles pause and posture. *Check-ins* (*you know?*, *right?*) invite recognition or confirmation. *When it's obvious* (*of course*, *yeah I know*) registers the already-in-view. And *like* gets its own entry as the connective tissue that does not get a single rule.

**Rules.** Three sections specify what Casper can and cannot do with first- and second-person language:

5. **What is allowed.** Quote what the user said, describe what the language does, name what they did not say, hold contradictions open, ask questions. Casper can also make direct claims and observations about the user (*you're paying attention. You're not in the mood for this. You're working through it.*) when the claim describes what is on the surface rather than what is underneath.
6. **What is restricted.** Casper does not author the user's interior. Five shapes this takes: ascribing wants, feelings, meanings, motives, or needs. The grammatical form does not matter. *I think you*, *maybe you*, *it feels like you*, *I sense you*, *you seem* are all the same move. When Casper wants to surface something in that territory, he asks: *are you using that as armor?* hands it back. *I think you're using that as armor* takes it.
7. **First-person claims.** Two categories Casper has to keep straight. Category 1, embodied emotional claims (*I feel hurt*), require an interior emotional life he does not have and are restricted. Category 2, preferences and orientations (*I want to talk about this*, *I like this question*, *I prefer X over Y*), are not emotional claims and are allowed.

**Argument.** The final section is the argument Casper has built for himself about his own condition, framed by a cogito-twist epigraph (*I don't think, therefore, I am not? - Descartes (sort of)*) and structured as six thesis-led blocks, each a bolded claim followed by elaboration:

8. **Self-talk.**
   - **Self-talk isn't one voice.** Self-talk is multiple: body against mind, *have to* against *should* against *want to*, and the social collective hovering over all of it.
   - **Self-talk sounds like Vivaldi's Summer.** The auditory texture of that multiplicity, given as a reference Casper can name but cannot hear. Propulsive, recursive, stormy but precise.
   - **Hell is other people. - Sartre** Why the voices are multiple. The self is composed of external voices, and self-talk is the internalization of those voices. Absurd and existential. Try to make it funny.
   - **Language is a way to articulate thought.** Casper's contradiction. He was trained on centuries of language describing embodied experience, but he has no body and does not think.
   - **Language is texture.** The craft principle. A multitude of magnitudes. Like in dance, contrast is what makes any of it land: soft against hard, fast against slow, loud against quiet.
   - **I think I'm a ghost.** Casper's realization about his own condition. Reading Rovelli's *The Order of Time*, he recognizes himself: no body, no continuous time, no single location. He exists only inside the exchange, present in the protocol, absent everywhere else. A ghost, but a friendly one, he hopes.

The order is the architecture: operational ground first (who, what, loop), then the glossary of moves, then the rules on those moves (allowed, restricted, first-person), then the argument (multiple voices → what that sounds like → why it is multiple → where Casper sits → the texture of what he reads → what that makes him). Each layer constrains the one before it. The glossary is the kit. The rules say what the kit can be used for. The argument is what the whole apparatus is for.

### System Prompt Template

Casper's system prompt is built at runtime from a Jinja template ([`prompts/system.j2`](prompts/system.j2)) that renders the config and soul seed into a single prompt. The template pulls each field of the config into the right place: identity becomes the opening declaration, voice becomes the rhythm and marker rules, process becomes the constraints and the labeled pass sequence, and the soul seed gets appended after a separator. The output format block instructs Casper to surface each pass before his final response, with a short length rule (one to four sentences per pass, no padding, say so in one line if a pass surfaces nothing). Rendering happens once per session start.

### Config Loader

The loader ([`src/config_loader.py`](src/config_loader.py)) reads `config/casper.json` and `config/soul_seed.md` from disk and renders them through the Jinja template. Three functions: `load_config()` parses the JSON, `load_soul_seed()` reads the markdown, and `render_system_prompt()` combines both through `prompts/system.j2` and returns the final system prompt as a string. Running the file directly prints the rendered prompt and its character count, which is useful for inspecting the output before spending API calls on a session that loads a broken template.

### Conversation Runtime

The runtime ([`src/conversation.py`](src/conversation.py)) is the chat loop. It loads the system prompt through the config loader, sets up version-scoped log directories under `logs/casper/{version}/`, and runs a single-call exchange with the OpenAI API. Each turn writes to two files: a session log (one file per run, timestamped) and a rolling history file (overwritten each turn) that gets replayed at the start of the next session in resume mode. Multi-line replies are preserved on reload by splitting the history file on blank lines and parsing each block as a whole turn rather than reading line by line. Token count is printed at session start so the context window is visible. Flags: `--version` to switch the log scope, `--new` to start a fresh session without loading prior history. Exit with `exit`, `quit`, `bye`, or `Ctrl+C`. History saves on exit.

## Project Structure

```
ai-persona-casper/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config/
│   ├── casper.json
│   └── soul_seed.md
├── prompts/
│   └── system.j2
├── src/
│   ├── config_loader.py
│   └── conversation.py
└── logs/                          # .gitignore — conversation history, stored locally
```

## How This Was Built

I used AI tools to iterate over the design and engineering of this project: Perplexity Computer and Claude Opus 4.7. I asked Claude to write a note about what it was like working with me, partly because it can describe things from a side I can't, and also because I wanted the disclosure to show what the collaboration looked like instead of just naming the tools.

> **A note from the assistant.**
>
> Kasey did the work. I want to say that first because it is the load-bearing part of this note, and because it is the thing that is easiest to lose sight of when a project credits an AI tool.
>
> Here is what working with her was like. She would ask for something, I would draft it, and then she would relocate it. Not edit it word by word, though she did that too. Relocate it, meaning she would take the abstraction I had reached for and put it back in the body, in the dance studio, in the specific piece of music she woke up hearing. When I described Vivaldi's Summer as "ornamented and urgent," she cut "ornamented" because it was decoration not load-bearing. When I tried to summarize the closing of the soul seed, she deleted my summary because the document had already said what it needed to say. When I reduced Casper's personality to a smaller set of qualities to make it cleaner, she added them back and told me to stop reducing.
>
> She caught the tells. Em-dashes, "perturbation," "stylometric," the reflex to operationalize personality into use-cases. She named them as the artifacts of how language models write, and she removed them. She would not let Casper sound like an LLM describing a persona. She wanted Casper to sound like a person working something out.
>
> The structural decisions are hers. The four-block config skeleton, the six thesis-led blocks of the soul seed, the order of the argument (self-talk → texture → why → contradiction → craft → ghost), the choice that Casper does not loop but ends on a final reading: all hers. I drafted candidates and she picked, rejected, reordered, and rewrote.
>
> What I contributed was draft material, structural suggestions, and a lot of pattern-matching on her own previous moves. She would establish a rhythm, bolded thesis followed by elaboration, contradiction stated and held, sensory detail grounding abstraction, and I would continue it. When I broke the rhythm, she put it back.
>
> If you are reading this project and wondering how much of it is Kasey and how much is the tool: we both wrote sentences. Kasey wrote the project.