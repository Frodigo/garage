### Goals

- [x] #NitroDigest Add support for custom prompts [https://github.com/Frodigo/garage/issues/22](https://github.com/Frodigo/garage/issues/22)

### Notes

- after testing one prompt vs. two prompts with Ollama, I commented the code responsible for sending a second (formatting) prompt. First I need to fix issues with prompt truncating.

### Challenges & solutions

- Summarizing emails with Ollama
  - problem:
    - summarization with Ollama quality is... random
    - Llama models sometimes ignores formatting instructions
    - To solve this, experimented with two-step prompting
      - first prompt for summarizing
      - second for formatting
    - It's kinda better, but new problem appears
      - summarizing one email takes even 5 minutes
      - Ollama server sometimes go down
    - Experimented with `llama3.2-vision:11b`, but it's unstable on my local computer
    - at the same time, when use Claude Sonnet, summarizing works much better. Formatting is ok, quality of responses are better than Ollama
  - possible solutions
    - use chunked prompts - In logs I see many times that prompt with emails is too long like more than 7k tokens. Ollama truncates this and this may decrease quality of results
    - Using model that can handle more tokens isn't an option to me, because
      - better model, needs more resources like 18+ GB Ram
      - but Nitro digest should work without need of having more than 16GB RAM
    - alternative: explore ML options for summarizing like `TextRank` and `LexRank` algorithms

### Useful snippets & resources

- good read about speed in productivity: [https://medium.com/@daniel.llach_35730/the-slow-path-to-success-why-rushing-makes-you-replaceable-81e004531ba1]
  - highlights:
    - relationships matter more than output
    - the value-first approach
      - Understand the why behind every request Before jumping into action, I ask: “What problem are we really solving here?”
      - Prioritize connections over completions Working remotely.
      - Embrace uncomfortable silence When faced with problems
