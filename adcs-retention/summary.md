# ADCS physician retention: quick read

Source: CMS public data only, plus a hand check of the ADCS provider directory and a few web searches for 9 names. Workbook: `adcs_retention.xlsx` (tabs: roster_now, history, exits, summary, qc).

## Bottom line

- 111 clinicians seen at ADCS addresses from 2019 to 2024 are not on today's roster. 65 are MD/DO and 46 are PA/NP.
- Address-only matching gives 153. The difference is 42 clinicians who billed from a different suite in the same building, which means a different practice. Treat 111 as the main number and 153 as the ceiling.
- Annual exit rate runs about 5% to 11% from 2019 to 2023. The 2024 figure (9.7%) pools about two years of departures, so treat it as roughly 5% a year.
- Of the 74 exits found in the current CMS file, 54 (73%) went to another dermatology group.
- A third of exits (37) are not in the current CMS file. I cannot tell whether they retired, left Medicare, or are just missing.

## How the roster was built (read this first)

The name match found no ADCS entity for the Florida clinics. The only "ADCS" legal name, ADCS Care Management 1 Inc, is an NP group in facilities and not the dermatology practice. So I used the clinic addresses on advancedderm.com (152 distinct addresses of 154 listed; one location fell in a gap in the page text).

That led to 13 CMS group PAC IDs treated as ADCS:

- 12 state-level groups named "Advanced Dermatology of ..." (CO, MD, MI, SC, PA, VA, AZ, GA, AL, WY, OH, RI). Their rows sit mostly at website addresses.
- **Leavitt Medical Associates of Florida Inc (PAC 4688579311).** This is an inference. It holds 198 NPIs, 90% of its rows sit at ADCS Florida addresses, and nothing in its name says ADCS. If it is wrong, Florida is wrong, and Florida is 43% of the roster.

Roster: 465 NPIs, 1,029 rows, 180 distinct addresses (website plus roster-group addresses).
Competitors that share ADCS buildings (Monarch Dermatology, Clinical Skin Center of Northern Virginia, Florida Institute of Dermatology) were excluded.

## Key numbers

**Providers per year** (current roster NPIs plus counted exits, billing at an ADCS address)

| Year | MD/DO | PA/NP | Total | Exits (last year seen) | Exit rate | Exits before suite check |
|---|---|---|---|---|---|---|
| 2019 | 113 | 107 | 220 | 14 | 6.4% | 25 |
| 2020 | 107 | 114 | 221 | 15 | 6.8% | 20 |
| 2021 | 104 | 131 | 235 | 25 | 10.6% | 30 |
| 2022 | 102 | 139 | 241 | 15 | 6.2% | 18 |
| 2023 | 106 | 162 | 268 | 14 | 5.2% | 20 |
| 2024 | 108 | 182 | 290 | 28 | 9.7% | 40 |

MD/DO headcount is flat at about 105. Growth is all PA/NP (107 to 182). MD/DO exits run 8 to 14 a year, roughly 7% to 13% of MD/DO headcount.

**Exits by state of last ADCS address:** FL 46, CO 16, PA 12, MI 11, SC 5, MD 4, AZ 4, VA 4, GA 3, other 6. Florida is 41% of exits and 43% of the roster, so there is no sign it loses people faster than the rest.

**Destination mix** (111 exits)

| Destination | All | Share | MD/DO (65) | PA/NP (46) |
|---|---|---|---|---|
| Another derm platform | 54 | 49% | 20 | 34 |
| Small or independent (<10) | 15 | 14% | 15 | 0 |
| Other | 5 | 5% | 5 | 0 |
| Not found (retired or left Medicare) | 37 | 33% | 25 | 12 |

- The PA/NP column leans toward derm platforms because a derm destination is one of my admission tests for PA/NP exits (see Method). Use the MD/DO column for the cleaner read.
- "Derm platform" follows your definition: a derm-focused group with 10 or more members. Only 15 of the 54 have 50 or more members. The named platforms are Forefront (5 exits), Aqua Dermatology of Florida (3), Pinnacle (2), and Schweiger (1). The rest are mid-size independents.
- Top destinations: Forefront Dermatology (5), OnSpot-FL (3), Aqua Dermatology of Florida (3), then a long tail of one or two each. Six MD/DO exits now have no group, only an individual enrollment.
- Found exits: median move is 30 miles. 46% are within 25 miles and 27% moved to a different state.

**Medicare allowed amount of exits in their last ADCS year:** $13.8M ($10.4M MD/DO, $3.4M PA/NP). These are nominal dollars for one year each, not annualized. 2024 exits account for $5.5M of the total.

**Top 25 current providers** are on the summary tab (2024 allowed amount, all billing locations). #1 is a Mohs surgeon in West Columbia, SC at $5.5M. The 25th is at $0.9M. 11 of the 25 belong to the Florida (Leavitt) group.

## QC

**NPPES spot check of 15 exits.**
- Strict match (NPPES practice location equals the CMS destination city or zip): 5 of 15 confirm.
- Within 25 miles and same state: 9 of 15 confirm. Most misses are the same metro area, such as Ponte Vedra and Jacksonville.
- "Found" exits: 5 of 10 strict, 9 of 10 within 25 miles.
- "Not found" exits: 0 of 5. All five still list the ADCS address in NPPES.
- NPPES and the CMS clinician file draw on overlapping enrollment data, so this is a consistency check, not independent proof.

**Not-found bucket.** I checked all 37 against NPPES. 22 still show the ADCS address, 11 show another address, and 4 have no record (likely deactivated). In an earlier cut of this bucket, most of those NPPES records had not been updated since before 2023 and most clinicians had not billed Medicare in 2023 or 2024, so a stale NPPES address is the likelier explanation than still working there. Nothing here can confirm a retirement.

**Hand check of 9 flagged names.** These were the 9 not-found exits with a recent sign of activity. The ADCS provider directory (checked by hand) showed none of them. Web searches of non-social sites found:

- Gevoy, Ottuso, Fu: still counted as exits. Gevoy shows at a practice in Michigan. Ottuso and Fu still appear at ADCS in several directory aggregators, but those pages are often stale, and the hand check outranks them.
- Bright, Pakieser, Tafur, Ellis: different practices in the same buildings (pain medicine, family NP, family NP, and a different suite). They were never ADCS.
- Amige and Salazar de Torres: also billed from a different suite than ADCS. Amige now shows at Dermatology Partners in Philadelphia. If you know either was ADCS staff, add them back.

The four never-ADCS cases exposed the suite problem, which is why the suite check exists.

## Surprising

1. **Shared buildings inflate address-only counts badly.** 663 candidates looked like exits. 69 are still at the same address under another organization. 42 more billed from a different suite and were dropped by the suite check. Hospital and primary-care PAs make up most of the rest.
2. **The not-found bucket is murky.** It is a third of exits and none of the 5 sampled could be confirmed. Do not quote it as retirements.
3. **The address match missed 37% of the roster.** 157 of 421 roster NPIs that billed Medicare in 2024 were never seen at an ADCS address in any year. They are 73 PAs, 44 dermatologists, 21 NPs, and a few others. Billing addresses in the Medicare file differ from enrollment addresses. Real exits are likely undercounted too.
4. **Medicare allowed dollars jumped about 41% in 2024** ($61.5M to $86.5M) against 8% more providers. I did not chase the cause.
5. **The Florida group has non-derm specialties.** Top 25 includes an ENT and a pathologist. The top-25 list uses group membership, not specialty.
6. **The ADCS website state filter has no NY, NJ, or MN.** The "Advanced Dermatology" groups in those states (for example Advanced Dermatology PC in NY) were not treated as ADCS.

## Method choices

- **Match rule.** Street number, normalized street name, and 5-digit zip. A looser key (number, zip, longest street word) catches spelling variants like "Trce" and "Trail".
- **Suite check.** The ADCS suite list for each address comes from the website and from current roster rows. An exit whose last billing suite shares no token with any ADCS suite at that address is dropped. Suites are compared loosely ("S-1" equals "S1"). No suite on either side means no test, so those stay in.
- **MD/DO** (dermatology, Mohs, dermatopathology) at an ADCS address count as exits on address alone, after the suite check.
- **PA/NP** count only if they are now at a derm-focused group, or are missing from the clinician file and billed at an address where ADCS is at least 60% of derm, PA, and NP clinicians.
- **Exit year** = last year seen at an ADCS address. **Exit rate** = exits that year divided by providers billing that year.
- **Destination class.** Group size under 10, or no group, is small or independent. Derm-focused means a name starting with derm, skin, Mohs, or cosmetic, or at least 20% of members in derm or Mohs. Size 10 or more and derm-focused is a platform. Everything else found is other.
- All 663 candidates stay in the exits tab with a flag and a reason, so you can change any call.

## Caveats

- Medicare fee-for-service only. Clinicians with little FFS volume are missing or understated.
- The latest billing year is 2024 and lags about two years. Exits after 2024 appear only through the roster comparison, which is why "2024" exits pool 2025 and 2026 departures.
- Address matching misses providers who billed elsewhere (see item 3 above) and can attribute shared-building clinicians to ADCS. The suite check reduces the second problem and may overcorrect: a genuine exit who billed under an unusual suite would be dropped. The 153 figure is the ceiling.
- Leavitt Medical Associates of Florida is an inferred ADCS entity.
- Website addresses are one snapshot. Closed clinics are not listed, so older exits from closed sites may be missed.
- Distances use zip centroids from the 2020 Census gazetteer.
