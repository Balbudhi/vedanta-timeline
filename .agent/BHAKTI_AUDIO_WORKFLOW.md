# Bhakti audio and karaoke workflow

This is the required procedure for a new Bhakti song or for repairing an
existing song. Its outcome is a verified performance order and line-onset
map; it is not merely a lyric draft.

## Non-negotiable semantics

- A `SONG_SEQUENCE` entry represents the actual sung order. Add a new entry
  whenever a line returns after another line; do not fake that return by
  enlarging an adjacent `repeats` count.
- A timing `start` is the first audible **vocal instantiation** of the
  displayed line: solo, duet, call-and-response, choir, spoken invocation,
  pickup, or any other arrangement. Do not privilege a chorus, lead, or any
  particular vocal role.
- A timing `end` is the end of that entry's final contiguous performance.
  It may cover its explicit repeated vocal performances, but never the next
  distinct line.
- The UI has one timing object for every sequence entry. Clicking a line seeks
  exactly to that entry's `start`, so an approximate or chorus-only timestamp
  is a release blocker.
- Never invent a lyric, fill an uncertain word, or silently drop an audible
  line. Mark uncertainty in the review artifact and resolve it against audio
  before changing public song data.

## Required intake

1. Start from any YouTube link with the intake command below. It collects the
   page title, uploader/channel, description, duration, and source URL before
   downloading audio only (never video). Treat that metadata as evidence to
   review, not permission to guess the singer, composer, venue, language, or
   transliteration.
2. Create the page from the established Bhakti song-page structure: local
   `audio.m4a`, local `data.js`, and `index.html` loading `data.js` before
   `../../assets/song.js`. Preserve the reader's Roman text, literal English,
   word glosses, and click/hover behavior.
3. Read `docs/SANSKRIT_TRANSLATION_STANDARD.md` before adding Sanskrit. For
   Punjabi/Hindi devotional lyrics, retain the same discipline: source text,
   careful transliteration, literal English, word-level glosses, and no
   generated completion.

## Transcription and timing gate

For an existing page, run the OpenRouter workflow from the repository root:

```sh
python3 scripts/transcribe_bhakti_openrouter.py bhakti/<song-slug> \
  --model '~google/gemini-flash-latest' --passes 2
```

It sends short, overlapping audio-only chunks and the current line catalogue
to Gemini Flash through OpenRouter. It is arrangement- and language-agnostic:
it identifies each first vocal instantiation without assuming a lead, chorus,
or call-and-response structure. It does **not** install a package, save a copy
of the audio, or expose the API key. The machine-readable results are local,
ignored files in `bhakti/<song-slug>/.transcription/`.

For a new YouTube song, use:

```sh
python3 scripts/intake_bhakti_youtube.py '<youtube-url>' bhakti/<song-slug>
```

The command uses the installed `yta`/`yt-dlp` audio path, writes `audio.m4a`,
captures page metadata into the ignored review directory, and produces a
catalogue-free raw transcription audit. After reviewing the raw evidence,
create the exact lyrics, translation, word glosses, and initial `data.js`;
then rerun `transcribe_bhakti_openrouter.py` with that catalogue to check every
line, order, and timing. Never turn title/description metadata or a model draft
into an asserted public credit without checking the actual source.

Before editing `data.js`, inspect all passes and resolve every item reported
by `review.json`:

- unmatched or uncertain sung text;
- a sequence-order mismatch;
- a possible missing first vocal pickup or response;
- a timestamp disagreement between passes; and
- an uncovered time range.

Generate a deduplicated candidate timeline with:

```sh
python3 scripts/summarize_bhakti_timing_candidates.py bhakti/<song-slug>
```

It only clusters the independent API reports and groups adjacent matching lyric
instances; it does not modify the public page. Its `timeline-candidates.json`
is a structured checklist for the final audio spot-check.

Run the third, audio-backed reconciliation pass against those two reports:

```sh
python3 scripts/reconcile_bhakti_audio.py bhakti/<song-slug>
```

It asks the model to find missing instances, wrong order, wrong first-vocal
onsets, and non-song material at the beginning/end. It emits review evidence
only. Do not trim or replace `audio.m4a` automatically: accept a proposed
trim only after checking the candidate boundary against the audio, then retain
the untrimmed source outside the published path with its provenance.

Then update both `SONG_SEQUENCE` and `SONG_TIMINGS`, keeping one timing object
per sequence item. Listen/inspect around every proposed transition (especially
the opening and each returning refrain), then test: click every line and
confirm it seeks to the first vocal onset. Do not publish on a model-only
assertion of exactness.

## Shared credential

The Dev-wide credential contract is documented in
`/Users/eeshan/Dev/AGENTS.md`. Use its supported environment variable or
key-file path; never source Quant's `.quant/env.sh`, print a secret, or commit
a `.env`/key file.
