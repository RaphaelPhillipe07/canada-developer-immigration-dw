# Canada DW research extract

## Sources preserved without modification

- `raw/98100307-eng.zip` — Statistics Canada, table 98-10-0307-01, downloaded from `https://www150.statcan.gc.ca/n1/en/tbl/csv/98100307-eng.zip`. Census reference year: 2021.
- `raw/job_bank_wages_2025.csv` — Government of Canada / ESDC Job Bank, 2025 Wages resource from dataset `adad580f-76b0-4502-bd05-20c125de9116`. Dataset revision date: 2025-11-19.
- `raw/job_bank_wages_package_metadata.json` — official Open Government dataset metadata, including resource URLs and yearly releases.

The Statistics Canada ZIP is 383 MB and exceeds GitHub's normal Git object limit. The private repository stores it as a release asset, while the local copy remains at the path above. Its SHA-256 checksum is recorded in the project handoff.

## Transformations

- `filtered/statcan_98100307_brazil_provinces_territories.csv` selects the 13 province/territory DGUIDs, `Age (8D) = Total - Age`, `Gender (3) = Total - Gender`, and `Place of birth (290)` in {`Brazil`, `Total – Place of birth`}. Brazil rows retain all published immigration-period measures.
- `filtered/job_bank_wages_2025_all_regions_noc_21232.csv` contains every 2025 Job Bank record with `NOC_CNP = NOC_21232`.
- `filtered/job_bank_wages_2025_noc_21232.csv` retains only provincial-level NOC 21232 records. The original `Annual_Wage_Flag_Salaire_annuel = 0`, so populated wages are CAD/hour.
- `canada_provinces_brazil_software_developer_wages.csv` is a left join from the 13 Statistics Canada province/territory rows to the Job Bank provincial wage rows by normalized English province name. `N/A` is preserved where Job Bank publishes no province-level record.

## Field lineage

Statistics Canada input fields: `REF_DATE`, `GEO`, `DGUID`, `Age (8D)`, `Gender (3)`, `Place of birth (290)`, and the following measures: `Immigrants[3]`, `Before 1980[4]`, `1980 to 1990[5]`, `1991 to 2000[6]`, `2001 to 2010[7]`, and `2011 to 2021[8]`. `Total – Place of birth` with `Immigrants[3]` supplies `total_immigrants_2021`.

Job Bank input fields: `NOC_CNP`, `NOC_Title_eng`, `prov`, `ER_Code_Code_RE`, `ER_Name`, `Low_Wage_Salaire_Minium`, `Median_Wage_Salaire_Median`, `High_Wage_Salaire_Maximal`, `Source2025_NHQ`, `Data_Source_E`, `Reference_Period`, `Revision_Date_Date_revision`, and `Annual_Wage_Flag_Salaire_annuel`.

## Geographic treatment and limitations

Statistics Canada identifies provinces/territories with Census DGUIDs (e.g. Ontario `2021A000235`). Job Bank uses two-letter `prov` codes and economic-region codes (`ER...`), neither of which is a DGUID. English province name is the crosswalk key in the final file. Quebec is `Quebec` in the English Job Bank field and in the English Statistics Canada extract; the French Job Bank field is `Québec` and is not used.

Job Bank 2025 contains provincial NOC 21232 wage records for NL, NS, NB, QC, ON, MB, SK, AB, and BC. Prince Edward Island appears only as the ER-level `ER1110` record, not a province aggregate; it and Yukon, Northwest Territories, and Nunavut are therefore `N/A` in the province-level wage columns. No regional wage was substituted. Statistics Canada is Census 2021 (a stock/count reference), while the Job Bank release is 2025 with wage reference period 2023–2024; those time bases differ and must be stated in analysis.
