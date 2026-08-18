# Audio and timing standard

Audio is optional for a reader. Its absence must never block a source-grounded
text, and its presence must not weaken textual or rights standards.

## Minimum supported reader contract

When a reader includes recitation audio, it must provide:

- a lawful public or explicitly approved audio witness with performer/source
  attribution;
- a timing manifest keyed by the reader's stable unit locus;
- start/end seconds for each timed unit, in ascending non-overlapping order;
- global play/pause, keyboard-operable seeking, per-unit playback, and a clear
  active-unit state; and
- an honest `timing_status` describing whether the timings were manually
  checked, source-supplied, or only provisional.

The current Gita reader supports **verse-level** timing only. A verse range may
not be represented as word-, pada-, or commentary-level alignment.

## Alignment workflow

1. Record the audio witness, rights basis, performer, edition/URL, and the text
   edition to which it is aligned.
2. Produce a draft timing manifest from a permitted alignment process. An
   automated transcript or forced alignment is a draft aid, not proof.
3. Compare every boundary against the audible recitation and the displayed
   source text; correct sandhi, refrain, pause, and chant-introduction offsets.
4. Mark the manifest `timing_status: "verified"` only after this comparison.
   Otherwise use `provisional` and do not promise precise unit seeking.
5. Keep the timing manifest separate from translation data. A timing does not
   establish a Sanskrit reading, translation, or grammatical analysis.

## Word and pada synchronization

Do not create word/pada highlighting from evenly divided verse duration,
language-model guesses, or inferred token count. It requires a source-aligned
word sequence and manually reviewed word boundaries. Until that exists, the UI
must highlight only the verified verse/unit.

## Current repository status

The repository has verse-level manifests for the existing Gita readings and
song-specific karaoke timings. It has **no configured OpenRouter,
transcription, forced-alignment, or timestamp-generation pipeline**. Any future
integration must document its model/provider, consent and rights basis, draft
status, manual-review step, and output schema before it is used in publication.
