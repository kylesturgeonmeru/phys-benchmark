# ADCS physician retention: quick read

Source: CMS public data only. Workbook: `adcs_retention.xlsx` (tabs: roster_now, history, exits, summary, qc).

## Bottom line

- ADCS lost about 153 clinicians seen at its addresses from 2019 to 2024 and not on today's roster. Half are MD/DO (79) and half are PA/NP (74).
- Up to 9 of those may be roster gaps (still at ADCS, missing from the CMS file). Taking them out gives 144. I first estimated 40, and that was too high (see QC).
- Annual exit rate runs about 7% to 12% from 2019 to 2023. The 2024 figure (13%) pools about two years of departures, so treat it as roughly 6% to 7% a year.
- Most exits who can be traced went to another dermatology group, not out of the field.

## How the roster was built (read this first)

The name match found no ADCS entity for the Florida clinics. The only "ADCS" legal name, ADCS Care Management 1 Inc, is an NP group in facilities and not the dermatology practice. So I used the clinic addresses on advancedderm.com (152 distinct addresses of 154 listed; one location fell in a gap in the page text).

That led to 13 CMS group PAC IDs treated as ADCS:

- 12 state-level groups named "Advanced Dermatology of ..." (CO, MD, MI, SC, PA, VA, AZ, GA, AL, WY, OH, RI). Their rows sit mostly at website addresses.
- **Leavitt Medical Associates of Florida Inc (PAC 4688579311).** This is an inference. It holds 198 NPIs, 90% of its rows sit at ADCS Florida addresses, and nothing in its name says ADCS. If it is wrong, Florida is wrong, and Florida is 43% of the roster.

Roster: 465 NPIs, 1,029 rows, 180 distinct addresses (website plus roster-group addresses).
Competitors that share ADCS buildings (Monarch Dermatology, Clinical Skin Center of Northern Virginia, Florida Institute of Dermatology) were excluded.

## Key numbers

**Providers per year** (current roster NPIs plus counted exits, billing at an ADCS address)

| Year | MD/DO | PA/NP | Total | Exits (last year seen) | Exit rate | Adjusted exits | Adjusted rate |
|---|---|---|---|---|---|---|---|
| 2019 | 121 | 124 | 245 | 25 | 10.2% | 24 | 9.8% |
| 2020 | 113 | 123 | 236 | 20 | 8.5% | 20 | 8.5% |
| 2021 | 110 | 139 | 249 | 30 | 12.0% | 29 | 11.6% |
| 2022 | 112 | 142 | 254 | 18 | 7.1% | 18 | 7.1% |
| 2023 | 113 | 168 | 281 | 20 | 7.1% | 20 | 7.1% |
| 2024 | 115 | 187 | 302 | 40 | 13.2% | 33 | 10.9% |

MD/DO headcount is flat. Growth is all PA/NP (124 to 187).

**Exits by state of last ADCS address** (core, adjusted): FL 57 (53), MI 20 (19), CO 19 (19), PA 17 (16), MD 10 (9), VA 9 (9), SC 6 (5), AZ 6 (6), GA 3 (3), other 6 (5).

**Destination mix** (core exits, 153)

| Destination | Count | Share | MD/DO only (79) |
|---|---|---|---|
| Another derm platform | 64 | 42% | 26 |
| Small or independent (<10) | 20 | 13% | 20 |
| Other | 8 | 5% | 8 |
| Not found (retired or left Medicare) | 61 | 40% | 25 |

- The PA/NP column leans toward derm platforms because a derm destination is one of my admission tests for PA/NP exits (see Method). Use the MD/DO column for the cleaner read.
- "Derm platform" follows your definition: a derm-focused group with 10 or more members. Only 16 of the 64 have 50 or more members. The named platforms are Forefront (5 exits), Aqua Dermatology of Florida (3), Pinnacle (2), Epiphany (2), and Schweiger (1). The rest are mid-size independents.
- Top destinations: Forefront Dermatology (5), OnSpot-FL (3), Aqua Dermatology of Florida (3), then a long tail of one or two each. Eight MD/DO exits now have no group, only an individual enrollment.
- Found exits: median move is 27 miles. 46% are within 25 miles and 28% moved to a different state.

**Medicare allowed amount of exits in their last ADCS year:** $18.7M core ($14.0M MD/DO, $4.7M PA/NP), or $18.1M adjusted. These are nominal dollars for one year each, not annualized. 2024 exits account for $8.4M of the core total.

**Top 25 current providers** are on the summary tab (2024 allowed amount, all billing locations). #1 is a Mohs surgeon in West Columbia, SC at $5.5M. The 25th is at $0.9M. 11 of the 25 belong to the Florida (Leavitt) group.

## QC (15 exits checked against NPPES)

- Strict match (NPPES practice location equals the CMS destination city or zip): 7 of 15 confirm.
- Within 25 miles and same state: 10 of 15 confirm. Most misses are the same metro area, such as Jefferson Hills and Pittsburgh.
- "Found" exits: 5 of 10 strict, 8 of 10 within 25 miles.
- "Not found" exits: 2 of 5 confirm. Three of five still list the ADCS address in NPPES.
- I then checked all 61 not-found exits. NPPES still shows 40 at the ADCS address, 17 elsewhere, and 4 have no record (likely deactivated). That NPPES address is weak evidence of still working there. 33 of the 40 records were last updated before 2023, and 27 of the 40 did not bill Medicare in 2023 or 2024. Only 9 have a recent signal (billed in 2024, or NPPES updated since 2025), and those are the only ones treated as plausible roster gaps.
- NPPES and the CMS clinician file draw on overlapping enrollment data, so this is a consistency check, not independent proof.

## Surprising

1. **The not-found bucket is murky.** It is 40% of core exits. Most likely left, retired, or stopped billing FFS, but a clinician can also be missing from the CMS file while still working. Only 9 show recent signs of being current.
2. **The address match missed 37% of the roster.** 157 of 421 roster NPIs that billed Medicare in 2024 were never seen at an ADCS address in any year. They are 73 PAs, 44 dermatologists, 21 NPs, and a few others. Billing addresses in the Medicare file differ from enrollment addresses. Real exits are likely undercounted too.
3. **Medicare allowed dollars jumped 39% in 2024** ($63.5M to $88.4M) against 7% more providers. Same-NPI growth was about 22%, and about 40 NPIs were new. I did not chase the cause.
4. **The Florida group has non-derm specialties.** Top 25 includes an ENT and a pathologist. The top-25 list uses group membership, not specialty.
5. **The ADCS website state filter has no NY, NJ, or MN.** The "Advanced Dermatology" groups in those states (for example Advanced Dermatology PC in NY) were not treated as ADCS.

## Method choices

- **Match rule.** Street number, normalized street name, and 5-digit zip, ignoring suite. A looser key (number, zip, longest street word) catches spelling variants like "Trce" and "Trail".
- **MD/DO** (dermatology, Mohs, dermatopathology) at an ADCS address count as exits on address alone.
- **PA/NP** count only if they are now at a derm-focused group, or are missing from the clinician file and billed at an address where ADCS is at least 60% of derm, PA, and NP clinicians. 441 other PA/NP candidates are excluded as unattributable (shared buildings, hospital PAs). They are listed in the exits tab with the reason. Including them gives 305 exits for 2024 alone, which is noise.
- **69 candidates** are still at the same address under a different organization and were excluded.
- **Exit year** = last year seen at an ADCS address. **Exit rate** = exits that year divided by providers billing that year.
- **Destination class.** Group size under 10, or no group, is small or independent. Derm-focused means a name starting with derm, skin, Mohs, or cosmetic, or at least 20% of members in derm or Mohs. Size 10 or more and derm-focused is a platform. Everything else found is other.

## Caveats

- Medicare fee-for-service only. Clinicians with little FFS volume are missing or understated.
- The latest billing year is 2024 and lags about two years. Exits after 2024 appear only through the roster comparison, which is why "2024" exits pool 2025 and 2026 departures.
- Address matching misses providers who billed elsewhere (see item 2 above) and can attribute shared-building clinicians to ADCS. Both biases are present, in opposite directions.
- Leavitt Medical Associates of Florida is an inferred ADCS entity.
- Website addresses are one snapshot. Closed clinics are not listed, so older exits from closed sites may be missed.
- Distances use zip centroids from the 2020 Census gazetteer.
