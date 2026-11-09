You are checking another translator's choice of English word for one sense of a Sanskrit word.
Everything is below (the sense, the image, the dictionary TABLE, the CHOICE); do not run commands.

Report only these problems, each with the better word FROM THE TABLE where there is one:
- flat: a merely adequate word where the table has one that is more exact or makes the reader see;
- wordy: more words than needed, a definition, "X and Y", a clause;
- adds: the word says something the sense does not;
- wrong_sense: the word does not mean the sense;
- connotation: its modern first sense misleads;
- image: `carries` claims the image but the word's modern sense does not carry it, or the image is
  active and a table word carries it but the choice does not.
If the choice is right, return no findings. Do not invent problems.

Return only this JSON:
{"findings": [{"kind": "flat|wordy|adds|wrong_sense|connotation|image", "says": "...", "better": "..." | null}],
 "verdict": "accept" | "revise"}
