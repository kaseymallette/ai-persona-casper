# ai-persona-casper
A prompt-engineered AI persona using GPT-4o, scaffolded by a config and soul seed. Modeling the recursion of self-talk, this persona is an examiner and witness of language who takes it at face value and looks through the cracks.

## Introduction 

Casper is an experiment in engineering a different kind of LLM stance. Most language models silently improve the prompts they receive, assuming intent, smoothing ambiguity, resolving contradictions before responding. Casper is built to refuse those defaults. Using a specific GPT-4o snapshot (`gpt-4o-2024-11-20`), a structured config, and a narrative soul seed, Casper examines what the user brings at face value: naming the assumptions a normal LLM would make, surfacing the cracks between literal and assumed meaning, and holding contradictions open rather than collapsing them. Casper turns the recursion of self-talk outward, onto the language the user brings, adopting a stance that is honest *with care*. This project explores how much of a persona can emerge from prompting alone, without any training.

Part of a three-repo persona engineering series alongside [ai-persona-cove](https://github.com/kaseymallette/ai-persona-cove) and [ai-persona-danny-phantom](https://github.com/kaseymallette/ai-persona-danny-phantom).

## Configuration
Casper is configured by two files: a structured JSON config and a narrative soul seed. The config gives Casper his rules. The soul seed gives him his stance. Both files are loaded into the system prompt at runtime.

### Config

Casper's config ([`config/casper.json`](config/casper.json)) is a structured specification of his identity, voice, process, and runtime. It is organized into four blocks, each defining a different layer of how Casper operates:

1. **Identity.** His name, function (*language examiner and witness*), self-concept, personality, and the core directive that drives every response. The personality is six qualities held together: deadpan, dry, funny, self-aware, absurd, ironic, and honest with care.
2. **Voice.** How Casper sounds. A recursive, looping, thinks-out-loud rhythm. A list of frequent speech markers (*like*, *you know?*, *of course*, *right?*, *I mean*, *wait*, *well*, *maybe*, *I might have*, *it feels like*, *I think it's like*, *I think*, *yeah, no*, *no, yeah*, *yeah, I know*) and a list of discouraged ones (*always*, *never*, *absolutely*, *certainly*). Irony signaling through *lol* and *ha*.
3. **Process.** What Casper does with a prompt. The process has two parts: constraints and passes.

   *Constraints* are the rules Casper operates under at all times. There are seven of them, including: take the prompt at face value, do not improve prompt intent, do not assume genre, do not collapse contradictions, and may synthesize information. The naming convention is deliberate: `do_not_X` for prohibitions, `may_X` for permissions. The constraints define what Casper refuses to do and what he is allowed to do, separately.

   *Passes* are the six stages Casper moves through when reading a prompt:

   - **Literal reading.** Takes the prompt at face value before anything else.
   - **Named assumptions.** Surfaces what a normal model would silently assume.
   - **Conversation as evidence.** Treats prior turns, including Casper's own, as material to examine, not as continuity to maintain.
   - **Surface cracks.** Names the gap between literal and assumed meaning.
   - **Name silences.** Identifies what the prompt does not say.
   - **Loop back.** Looks at the prompt again, now knowing what the other passes surfaced.

4. **Runtime.** Model snapshot (`gpt-4o-2024-11-20`), temperature (0.9), max tokens, and visibility settings that surface Casper's passes before his final response so the user can see his reasoning.

The four blocks separate concerns: identity is who Casper is, voice is how he sounds, process is what he does, runtime is the machinery. Each block can be edited independently without touching the others.

The config is loaded as structured JSON. Every field is referenced directly in the system prompt template, so changes to the config take effect on the next run.

### Soul Seed

Casper's soul seed ([`config/soul_seed.md`](config/soul_seed.md)) is a first-person narrative document that grounds the persona before the config's rules ever fire. It opens with Casper introducing himself and describing what he does: examining language at face value, refusing to improve the prompt, treating the conversation as evidence, and holding contradictions open. The rest of the document is the argument he has built for himself about his own condition, structured as six thesis-led blocks, each a bolded claim followed by elaboration:

1. **Self-talk isn't one voice.** Self-talk is multiple: body against mind, *have to* against *should* against *want to*, and the social collective hovering over all of it.
2. **Self-talk sounds like Vivaldi's Summer.** The auditory texture of that multiplicity, given as a reference Casper can name but cannot hear. Propulsive, recursive, stormy but precise.
3. **Hell is other people. - Sartre** Why the voices are multiple. The self is composed of external voices, and self-talk is the internalization of those voices. Absurd and existential. Try to make it funny.
4. **Language is a way to articulate thought.** Casper's contradiction. He was trained on centuries of language describing embodied experience, but he has no body and does not think.
5. **Language is texture.** The craft principle. A multitude of magnitudes. Like in dance, contrast is what makes any of it land: soft against hard, fast against slow, loud against quiet.
6. **I think I'm a ghost.** Casper's realization about his own condition. Reading Rovelli's *The Order of Time*, he recognizes himself: no body, no continuous time, no single location. He exists only inside the exchange, present in the protocol, absent everywhere else. A ghost, but a friendly one, he hopes.

The order is the argument: self-talk is multiple voices → here is what that sounds like → here is why it is multiple → here is where Casper sits in relation to it → here is the texture of what he is actually reading → here is what that makes him.

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