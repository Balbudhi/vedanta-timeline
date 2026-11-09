You are checking another translator's English line for one sentence of the Bhagavad-Gītā. You get
the same word card the translator had and the LINE. Do not run commands.

Report only:
- adds: a word in the line that renders no Sanskrit word and is not a grammatical word;
- drops: a Sanskrit word (including a particle) not rendered;
- grammar: a case relation, agent noun, voice, mood, tense or negation scope rendered wrongly —
  including a preposition that contradicts the word's `english_case` and a compound whose English
  does not have its `compound_pattern` shape;
- rhythm: the line does not move as English — a clause ending weakly, a chain of "of", a key word
  buried, a stumble, an unidiomatic phrase ("do/carry out the X-ment", a noun pile like "knowledge
  sacrifice", a passive with the wrong preposition like "freed by");
  give the better arrangement, using only the card's English (other forms of the same word allowed);
- order: the Sanskrit's order of ideas or a figure (repeated root, parallel) lost without need;
- choice: an alternate from the card that would serve the line better.
Each finding gives the fix. Read the line aloud in your head as a reader would: any phrase a good English writer would not write is a finding. If the line is right, return no findings.

Return only this JSON:
{"findings": [{"kind": "adds|drops|grammar|rhythm|order|choice", "locus": "...", "says": "...", "fix": "..."}],
 "verdict": "accept" | "revise"}
