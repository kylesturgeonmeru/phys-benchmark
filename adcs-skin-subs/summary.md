# ADCS skin substitutes in Medicare: quick read

Public CMS data only. Medicare fee-for-service allowed amounts, 2019 to 2024. Files: `adcs_skin_subs.xlsx` (code_detail, adcs_by_year, providers, benchmarks, impact_2026, sources) and `adcs_skin_subs.html` (three charts).

## Bottom line

- Skin substitutes were 15.0% of ADCS Medicare allowed in 2024. They were 0.4% in 2019.
- The jump is almost all 2024. Skin substitute dollars went from $2.4M in 2023 to $20.8M. That one product line explains 69% of ADCS's total Medicare growth that year.
- At $127.28 per unit, the 2024 Q-code revenue would fall from $20.8M to $2.0M. That is a loss of $18.7M, or 90% of the product line and 13.5% of all ADCS Medicare allowed.
- On Medicare fee-for-service alone, the average unit would lose money at all three product cost assumptions, unless manufacturers cut prices too.

## Which NPIs

I used the retention workbook. The primary set is 576 NPIs: the current roster plus the 111 counted exits. Total Medicare allowed is for all their billing locations.

The literal reading of your instruction (every NPI in roster_now and history) is 1,128 NPIs. It adds 552 NPIs that I had excluded as shared-building noise, so it likely includes other practices. It gives $23.7M of skin substitutes in 2024 (14.0% of $169M) and a $21.5M loss. Those numbers sit in the workbook as a sensitivity.

Leavitt Medical Associates of Florida is still an inferred ADCS entity, and Florida is the biggest part of the skin substitute dollars.

## ADCS by year (primary set)

| Year | Total allowed | Skin substitute | Share | Application (15271 to 15278) | NPIs billing a Q-code |
|---|---|---|---|---|---|
| 2019 | $86.3M | $0.31M | 0.4% | $16K | 2 |
| 2020 | $79.0M | $0.93M | 1.2% | $48K | 3 |
| 2021 | $95.7M | $1.33M | 1.4% | $45K | 4 |
| 2022 | $99.3M | $2.27M | 2.3% | $45K | 4 |
| 2023 | $111.9M | $2.38M | 2.1% | $55K | 9 |
| 2024 | $138.7M | $20.77M | 15.0% | $147K | 13 |

- Skin substitute dollars per Mohs case (first-stage services 17311 and 17313): $16 in 2019, $110 in 2023, $863 in 2024.
- Mohs dollars were $19.4M and dermpath was $6.7M in 2024. Application codes are tiny. ADCS bills the product, not the graft procedure.
- No A2xxx codes appear for ADCS.

**Products, 2024.** Eight products make up all of it. Amnicore pro+ is 51% ($10.6M). Then Cogenex (14%), Amnio Tri-Core (11%), Orion (10%), Revita (6%), Helicoll (5%), Dermacyte (2%), and Kerecis Omega3 (1%). Top 10 by year is in the workbook.

**Concentration, 2024.**
- One NPI is 21% of skin substitute dollars. The top 5 are 70% and the top 10 are 93%.
- By state: FL 57%, SC 19%, PA 12%, CO 7%, GA 4%, OH 1%.
- By clinic zip: Orlando 32814 is 21%, West Columbia SC 29169 is 19%, Fort Washington PA is 12%, and Tampa 33613 and Brandon 33511 are 9% each.
- 95% of the 2024 dollars came from NPIs still on the roster.

## Benchmarks, 2024

| Group | Skin substitute share of Medicare allowed | Dollars per Mohs case | NPIs billing any |
|---|---|---|---|
| ADCS, dermatology-type NPIs (like for like) | 17.7% | $581 | 5.5% |
| ADCS, all NPIs | 15.0% | $863 | 2.6% |
| Florida dermatology | 14.0% | $590 | 6.1% |
| National dermatology | 8.0% | $337 | 2.4% |
| National Mohs surgeons | 13.1% | $284 | 9.6% |

- Use the first row. The benchmarks count dermatology-type NPIs only. ADCS's all-NPI figure is higher because two PAs and an ENT bill a third of the skin substitute dollars with no Mohs cases.
- ADCS looks like Florida, not like the rest of the country. Per Mohs case it is 1.7 times the national figure and about equal to Florida.
- In 2023 ADCS dermatology NPIs were at 3.5% and $98 per case, against 11.6% and $487 for Florida. ADCS got there late, then caught up in one year.

**Provider flags.** The national p90 is taken among dermatologists with 20 or more Mohs cases who billed any skin substitute. It is $8,600 per case in 2024.
- No ADCS NPI is above it. The highest ADCS NPI is at the 84th percentile ($3,664 per case).
- Among all Mohs surgeons the p90 is $0, because about 90% bill no skin substitutes, so I did not use that version.
- On absolute dollars, 3 ADCS NPIs are above the national p90 of $2.4M. They are a Mohs surgeon, a dermatologist, and a PA.
- The provider list is in the `providers` tab, marked internal. This summary and the HTML name no one.

## 2026 repricing (Medicare fee-for-service only)

- 15,985 Q-code units in 2024. Old allowed $20.77M. New at $127.28 per unit: $2.03M. Revenue lost: $18.73M.
- ADCS's average allowed was $1,299 per unit, 10 times the new rate. Seven of the eight codes are 3.6 to 19 times higher. Only Kerecis Omega3 is near $127.
- No code looks wrong on units. All 8 ADCS Q-codes are described as per square centimeter. Nationally, 18 Q-codes and A2014 are priced per mg or cc, and Q4100 is unspecified. ADCS did not bill them in 2024. They are listed in the workbook.
- Nothing goes up. The gain on codes below $127.28 is $0.

| Product cost, share of old allowed | Margin before | Margin after, cost unchanged | Margin lost, cost unchanged | Margin lost if costs fall with price |
|---|---|---|---|---|
| 20% | $16.6M | -$2.1M | $18.7M | $15.0M |
| 40% | $12.5M | -$6.3M | $18.7M | $11.2M |
| 60% | $8.3M | -$10.4M | $18.7M | $7.5M |

- With cost fixed, margin lost equals revenue lost. That is the arithmetic, not an error.
- Break-even product cost is $127.28 per unit, or about 10% of the old average allowed amount. Even the 20% case averages $260 per unit. Kerecis Omega3 is the exception, because it already sits near $127.
- $127.28 is applied to allowed amounts, which include the 20% patient share.

## Open Payments (optional, relationship data)

This is relationship data, not evidence of wrongdoing.
- General payments to the primary NPI set were $16.0M from 2019 to 2025. Nearly all came from pharmaceutical dermatology brands.
- Payments from 14 skin substitute makers totaled $24K, or 0.15%. Organogenesis ($10.2K) and Kerecis ($6.1K) are the largest.
- By year: $3.7K (2019), $0.2K, $0.9K, $1.2K, $3.9K, $6.2K (2024), and $8.0K (2025).
- The manufacturer list is mine and is in the workbook. Dressings, debridement, and breast-reconstruction products were left out.

## Surprising

1. **The size and speed.** Skin substitute dollars grew almost nine-fold in one year, while the NPIs billing grew from 9 to 13. Nationally Q-code dollars rose from $85M in 2019 to $4.6B in 2024, so ADCS is riding a market-wide wave.
2. **Florida dermatology is just as exposed.** At 14% of its Medicare allowed, the Florida benchmark is not a safe haven.
3. **Pricing.** The 2024 allowed amount per unit ($1,299) is 10 times the 2026 rate. This is a rate change, not a trim.
4. **The 2025 and 2026 numbers are unknown.** The 2024 level may not hold. ADCS's 2025 skin substitute billing could be higher or lower.

## Caveats

- **Data lag.** The latest data year is 2024. It lags about two years. 2025 and 2026 billing is not in this data.
- **Medicare fee-for-service only.** Medicare Advantage and commercial claims are excluded, so the real exposure to skin substitutes and to the rate change could be larger.
- **Allowed amounts.** Dollars are allowed amounts, not cash collected. They include patient coinsurance.
- **Internal only.** The provider-level list stays internal.
- The service file drops lines with fewer than 11 beneficiaries, so skin substitute dollars are a floor.
- The service-year NPI list is today's roster plus counted exits, so billing before an NPI joined ADCS is included.
- Distinct beneficiary counts in `code_detail` are sums across NPIs, so they overstate unique patients.
