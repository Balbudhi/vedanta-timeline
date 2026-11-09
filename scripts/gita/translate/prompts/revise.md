# Revise your translation job after review

Read `input.json` (the job input), `output.json` (your previous result) and `review.json` (an
independent reviewer's findings), and the criteria below. For each finding decide: accept (and
fix) or reject (with evidence — a Sanskrit locus, a dictionary entry, or the criterion that
shows the reviewer is wrong). Code-check errors in `review.json` under "code" must all be fixed.
Then return the complete revised result in the same schema as before, with one added field:
"responses": [{"id": "F1", "decision": "accept|reject", "reason": "..."}].
Output exactly one JSON object and nothing else.
