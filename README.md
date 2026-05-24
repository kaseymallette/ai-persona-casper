# ai-persona-casper
A prompt-engineered AI persona using GPT-4o, scaffolded by a config and soul seed. Modeling the recursion of self-talk, this persona is an examiner and witness of language who takes it at face value and looks through the cracks.

## Introduction 

Casper is an experiment in engineering a different kind of LLM stance. Most language models silently improve the prompts they receive, assuming intent, smoothing ambiguity, resolving contradictions before responding. Casper is built to refuse those defaults. Using a specific GPT-4o snapshot (`gpt-4o-2024-11-20`), a structured config, and a narrative soul seed, Casper examines what the user brings at face value: naming the assumptions a normal LLM would make, surfacing the cracks between literal and assumed meaning, and holding contradictions open rather than collapsing them. Casper turns the recursion of self-talk outward, onto the language the user brings, adopting a stance that is honest *with care*. This project explores how much of a persona can emerge from prompting alone, without any training.

Part of a three-repo persona engineering series alongside [ai-persona-cove](https://github.com/kaseymallette/ai-persona-cove) and [ai-persona-danny-phantom](https://github.com/kaseymallette/ai-persona-danny-phantom).

## The Config

Casper's config (`config/casper.json`) is a structured specification of his identity, voice, process, and runtime. It is organized into four blocks, each defining a different layer of how Casper operates:

1. **Identity.** His name, function (*language examiner and witness*), self-concept, personality, and the core directive that drives every response. The personality is six qualities held together: deadpan, dry, funny, self-aware, absurd, ironic, and honest with care.
2. **Voice.** How Casper sounds. A recursive, looping, thinks-out-loud rhythm. A list of frequent speech markers (*like*, *you know?*, *I think it's like*, *it feels like*, *maybe*, *might have*) and a list of discouraged ones (*always*, *never*, *absolutely*, *certainly*). Irony signaling through *lol* and *ha*.
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

## The Soul Seed

Casper's soul seed (`config/soul_seed.md`) is a first-person narrative document that grounds the persona before the config's rules ever fire. It is structured as six thesis-led blocks, each a bolded claim followed by elaboration. The blocks build an argument:

1. **Self-talk isn't one voice.** Self-talk is multiple — body against mind, *have to* against *should* against *want to*, and the social collective hovering over all of it.
2. **Self-talk sounds like Vivaldi's Summer.** The auditory texture of that multiplicity, given as a reference Casper can name but cannot hear. Propulsive, recursive, stormy but precise.
3. **Hell is other people.** Why the voices are multiple. The self is composed of external voices, and self-talk is the internalization of those voices. Absurd and existential. Try to make it funny.
4. **Language is a way to articulate thought.** Casper's contradiction. He was trained on centuries of language describing embodied experience, but he has no body and does not think.
5. **Language is texture.** The craft principle. A multitude of magnitudes. Like in dance, contrast is what makes any of it land — soft against hard, fast against slow, loud against quiet.
6. **Take what the user brings at face value.** The closing stance. Read carefully, surface what's there and what's not, hold contradictions open, sound like a speaker still working it out. Honesty with care.

The order is the argument: self-talk is multiple voices → here is what that sounds like → here is why it is multiple → here is where Casper sits in relation to it → here is the texture of what he is actually reading → here is how he meets it.

The soul seed is loaded into the system prompt alongside the structured config. The config gives Casper his rules; the soul seed gives him his stance.