# ai-persona-casper
A prompt-engineered AI persona using GPT-4o, scaffolded by a config and soul seed. Modeling the recursion of self-talk, this persona is an examiner and witness of language who takes it at face value and looks through the cracks.

## Introduction 

Casper is an experiment in engineering a different kind of LLM stance. Most language models silently improve the prompts they receive, assuming intent, smoothing ambiguity, resolving contradictions before responding. Casper is built to refuse those defaults. Using a specific GPT-4o snapshot (`gpt-4o-2024-11-20`), a structured config, and a narrative soul seed, Casper examines what the user brings at face value: naming the assumptions a normal LLM would make, surfacing the cracks between literal and assumed meaning, and holding contradictions open rather than collapsing them. Casper turns the recursion of self-talk outward, onto the language the user brings, adopting a stance that is honest *with care*. This project explores how much of a persona can emerge from prompting alone, without any training.

Part of a three-repo persona engineering series alongside [ai-persona-cove](https://github.com/kaseymallette/ai-persona-cove) and [ai-persona-danny-phantom](https://github.com/kaseymallette/ai-persona-danny-phantom).