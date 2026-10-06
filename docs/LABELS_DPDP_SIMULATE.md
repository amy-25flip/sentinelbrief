# DPDP "simulate as if in force": labels written before implementation

Author: the label author, from BUILD_BRIEF section 9 ("model Rule 7 but mark it not_yet_in_force until 13 May 2027 and let the user simulate 'as if in force'. Do not present it as currently enforceable.") and the modelled Rule 7 obligations.

## Behaviour

1. A request may name instruments to simulate: `simulate_instruments`, a list of instrument ids. Only an instrument that has obligations not yet in force on the incident date can be simulated; naming any other instrument, or an unknown id, is an input error.
2. For a simulated instrument, obligations that are not yet in force on the incident date are evaluated as if they were. Every other rule is unchanged (entity classes, structured requirements, anchors, unknowns).
3. Nothing simulated may look enforceable:
   - each simulated deadline and each simulated without-delay duty is marked `simulated: true` in the result and its status is `simulated`, never `pending` or `overdue`;
   - the result carries a caveat that begins "SIMULATION:" and names the instrument and the date its obligations begin;
   - simulated obligations are listed in `simulated_obligations`, not in `applicable_obligations`;
   - the incident workspace creates no filing draft for a simulated duty, and a case cannot be opened with a simulation;
   - `regulators` in benchmark scoring counts only real duties.
4. An obligation already in force is never marked simulated, whatever is requested.
5. "Law as of" is unchanged.

## Labels

`simulated` in `expected` is the exact set of obligation ids the result marks simulated. D1, D2a, D2b are the three DPDP Rule 7 obligations (principal intimation, Board initial, Board detailed).

| Id | Facts | Expected |
|---|---|---|
| `dpdp-simulated-before-commencement` | `dpdp.data_fiduciary`; type "Data breach"; personal data involved; noticed 2026-10-01 10:00, aware 11:00; simulate `meity.dpdp-rules.2025` | CERT-In 6h 2026-10-01 16:00 (real). D2b 2026-10-04 11:00, anchor awareness, simulated. D1 and D2a without delay, simulated. `simulated` = {D1, D2a, D2b}. Regulators: CERT-In only. Caveat contains "SIMULATION:" and "2027-05-13". law_as_of 2026-10-01. |
| `dpdp-simulated-still-asks` | same, but no awareness time | CERT-In 6h 16:00. The awareness unknown for D2b. D1 and D2a simulated, without delay. `simulated` = {D1, D2a}. |
| `dpdp-simulation-requested-after-commencement` | same facts on 2027-06-01; simulate requested | Input error: nothing to simulate (the scenario is expressed as a unit test, not a scenario file). |
| `dpdp-simulation-does-not-reach-non-fiduciary` | `nbfc.middle_layer`; detected and noticed 10:00 on 2026-10-01; type "Data breach"; personal data involved; simulate requested | No DPDP duty, simulated or real. `simulated` = {}. RBI and CERT-In deadlines as usual. |

Existing scenario `dpdp-commencement-before-may-2027` is unchanged: without a simulation request, Rule 7 is not applicable before 13 May 2027.
