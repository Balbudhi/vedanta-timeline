# Chronology migration standard

The Academic/Traditional control is a whole-timeline feature. The initial
Śaṅkara, Rāmānuja, and Yāmunācārya variants are reference records, not a claim
that the other figures have been migrated.

## Per-visible-thinker target

Every visible thinker must eventually contain:

```json
{
  "chronology": {
    "default_variant": "academic",
    "traditional_status": "pending-evidence",
    "variants": {
      "academic": {
        "low": 700,
        "high": 750,
        "tier": "consensus-textual",
        "source_kind": "academic",
        "notes": "...",
        "evidence": []
      }
    }
  }
}
```

When the tradition actually preserves a date claim, add a `traditional`
variant with its own low/high range, tier, source kind, notes, and evidence.
When it does not, replace `pending-evidence` with one of
`not-attested`, `not-applicable`, or `insufficiently-identified` and explain
why. Do not generate a traditional date by copying a lineage, a hagiographic
episode, or an academic estimate.

## Research order

1. Start with figures whose `dates_notes` already names both academic and
   traditional placements.
2. Consult tradition-specific chronologies, guru-paramparā records, colophons,
   inscriptional claims, and transmitted biographies; record which type of
   witness is being used.
3. Preserve the academic range separately even where the site's default is a
   traditional range.
4. Mark reconstructed/citation-preserved figures carefully: a tradition may
   not attest a person-date at all, even though later texts attest a position.
5. Review each batch independently before it becomes user-visible.

## Completion gate

The timeline must not be described as having a complete Traditional view until
the coverage report shows every visible record has an academic variant and
either a traditional variant or an explicit traditional status. Until then the
UI fallback message is required and correct.
