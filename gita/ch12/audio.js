window.CH12_AUDIO = {
  "src": "recitation.mp3",
  "reciter": "P R Iyer",
  "attribution": "Bhagavad Gītā — All 18 chapters, audio by P R Iyer, https://archive.org/details/bhagavad-gita_pri , CC BY-NC-ND 4.0; re-encoded to 64 kbps mono (format shift only).",
  "licence": "CC BY-NC-ND 4.0",
  "source_url": "https://archive.org/details/bhagavad-gita_pri",
  "timing_status": "provisional",
  "method": {
    "primary": {
      "name": "torchaudio.pipelines.MMS_FA",
      "model": "MMS forced aligner (wav2vec2, uroman vocabulary)",
      "torchaudio": "2.8.0",
      "torch": "2.8.0",
      "licence": "CC BY-NC 4.0 (model weights)",
      "transcript": "BORI IAST romanised with uroman 1.3.1.1"
    },
    "secondary": {
      "name": "Harveenchadha/vakyansh-wav2vec2-sanskrit-sam-60",
      "revision": "28c2078678b3674c2a29734d2e473c1e9325c295",
      "model": "wav2vec2 CTC fine-tuned for Sanskrit (Vakyansh / Open-Speech-EkStep)",
      "licence": "MIT (Open-Speech-EkStep/vakyansh-models LICENSE); no licence field on the Hugging Face card",
      "transcript": "BORI text in Devanāgarī (packet verses[].devanagari)",
      "framework": "transformers 4.57.6, torchaudio.functional.forced_align"
    },
    "vad": {
      "name": "silero-vad",
      "version": "6.2.3",
      "licence": "MIT",
      "min_silence_ms": 300,
      "speech_pad_ms": 100
    },
    "boundary_rule": "start = start of the VAD speech region containing the first token onset (shift <= 0.6 s); end = end of the region containing the last token onset, measured from the last token end (shift <= 1.0 s; CTC marks the onset of the final character, the chanted final vowel runs to the region end)",
    "corroboration_rule": "both aligners snapped into the same VAD gap and within 0.25 s, for start and end",
    "untranscribed_speech_rule": "VAD regions whose greedy decode matches the transcript below 0.4 in a global character alignment are masked to blank before forced alignment",
    "optional_units_rule": "speaker lines kept when the forced-path log-likelihood with the unit exceeds the one without",
    "boundary_source": "primary aligner",
    "text_edition": {
      "path": "vedanta-timeline/data/sources/sanskrit/vedanta/bhagavadgita_mula_bori.txt",
      "edition": "BORI critical edition of the Mahābhārata (Tokunaga et al., rev. John Smith; GRETIL)",
      "script": "IAST"
    },
    "device": "cpu",
    "generated": "2026-11-08"
  },
  "corroboration": {
    "verses_total": 20,
    "corroborated": 20,
    "disagreements": []
  },
  "verses": [
    {
      "locus": "12.1",
      "start": 11.1,
      "end": 23.8
    },
    {
      "locus": "12.2",
      "start": 27.1,
      "end": 39.5
    },
    {
      "locus": "12.3",
      "start": 40.0,
      "end": 51.4
    },
    {
      "locus": "12.4",
      "start": 52.0,
      "end": 63.6
    },
    {
      "locus": "12.5",
      "start": 64.1,
      "end": 75.8
    },
    {
      "locus": "12.6",
      "start": 76.2,
      "end": 88.3
    },
    {
      "locus": "12.7",
      "start": 88.9,
      "end": 101.5
    },
    {
      "locus": "12.8",
      "start": 102.1,
      "end": 114.9
    },
    {
      "locus": "12.9",
      "start": 115.7,
      "end": 127.1
    },
    {
      "locus": "12.10",
      "start": 127.5,
      "end": 139.2
    },
    {
      "locus": "12.11",
      "start": 145.9,
      "end": 158.0
    },
    {
      "locus": "12.12",
      "start": 158.6,
      "end": 171.5
    },
    {
      "locus": "12.13",
      "start": 172.5,
      "end": 184.5
    },
    {
      "locus": "12.14",
      "start": 185.0,
      "end": 197.8
    },
    {
      "locus": "12.15",
      "start": 199.0,
      "end": 212.5
    },
    {
      "locus": "12.16",
      "start": 213.1,
      "end": 226.4
    },
    {
      "locus": "12.17",
      "start": 227.3,
      "end": 239.6
    },
    {
      "locus": "12.18",
      "start": 240.4,
      "end": 253.0
    },
    {
      "locus": "12.19",
      "start": 253.9,
      "end": 266.9
    },
    {
      "locus": "12.20",
      "start": 267.5,
      "end": 281.3
    }
  ]
};
