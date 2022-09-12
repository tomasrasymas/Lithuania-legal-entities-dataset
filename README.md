# Tools for importing open data of Lithuania's legal entities 

Tools provided here allow you to download open data provided by the center of registers (Registrų centras) and Sodra, store that data in the MySQL database and perform further analyses. 

I used this tool to create a dataset that could be used for training ML models to calculate legal entity probability of bankruptcy. 

## Sources used:
* [Lithuania's center of registers](https://www.registrucentras.lt/p/1094)
* [Sodra](https://atvira.sodra.lt/imones/rinkiniai/index.html)

## Collect open data of the legal entities 
1. Run `docker-compose up`, this command spins up the local MySQL database, where all legal entities' data will be stored
2. Execute `pip install requirements.txt` to install libraries needed for importing the legal entities' data 
3. Run import by executing `python import_open_data.py`

### Database structure 
| Table name  | Description  |
|---|---|
| stg_legal_entities_addresses  | Addresses of legal entities registered in the center of registers  |
| stg_legal_entities_authorized_capital  | Authorized capital of registered legal entities |
| stg_legal_entities_balance_sheets  | Balance sheets provided by legal entities by finance year |
| stg_legal_entities_management  | Information on the management of registered legal entities  |
| stg_legal_entities_profit_loss_statements  | Profit loss statements provided by legal entities by finance year  |
| stg_registered_legal_entities  | Legal entities currently registered in the center of registers  |
| stg_unregistered_legal_entities  | Legal entities currently registered in center of registers |
| stg_sodra_monthly  | Monthly legal entities data provided for Sodra (average salaries, employees count, social security debt, etc.)  |

## Generate bankruptcy dataset
1. Perform steps listed [here](#how-to-collect-data)
2. Execute dataset generation by executing `python generate_bankruptcy_dataset.py`

Basic EDA of dataset could be find [here](bankruptcy_dataset.ipynb)

### Bankruptcy dataset fields description
| Field  | Description  |
|---|---|
| registration_date  | Company registration date (company creation date), e.g. `2021-01-27` |
| legal_form_name  | Name of company legal form, e.g. `Small Partnership`,  `Private Limited Liability Company` |
| status_name  | Legal status of the company (latest status, not the one that was on a particular year), e.g. `Bankrupt`, `Under Reorganization` |
| finance_year_start_date  | Start of the financial year for which information is registered, e.g. `2019-01-01` |
| finance_year_end_date  | End of the financial year for which information is registered, e.g. `2019-12-31` 
| document_registration_date  | Date when finance documents were registered, e.g. `2020-06-01` |
| equity  | Equity of the company |
| liabilities  | Liabilities of the company |
| long_term_financial_assets  | Long-term financial assets of the company |
| short_term_financial_assets  | Short-term financial assets of the company |
| profit_before_taxes  | Profit before taxes of the company |
| net_profit  | Company net profit |
| sales_revenue  | Sales revenue of the company |
| idx_eq_lia_ratio  | Radio of equity / liabilities |
| idx_lia_fin_as_ratio  | Ratio liabilities / (long term + short term financial assets) |
| idx_sh_fin_as_lia_ratio  | Ratio short term financial assets / liabilities |
| idx_fin_as_eq_ratio  | Ratio (long term + short term financial assets) / equity |
| idx_fin_as_lia_ratio  | Ratio (long term + short term financial assets) / liabilities |
| idx_n_prof_fin_as_ratio  | Ratio net profit / (long term + short term financial assets)  |
| idx_s_rev_fin_as_ratio  | Ratio sales revenue / (long term + short term financial assets) |
| idx_prof_tax_eq_ratio  | Ratio profit before taxes / equity |
| idx_prof_tax_fin_as_ratio  | Ratio profit before taxes / (long term + short term financial assets) |


`null` - indicates that data was not provided in finance year balance sheets or profit/loss statements 

Statuses `Under Restructuring`, `Going Bankrupt`, `Bankrupt`, `Liquidation due to bankruptcy` were used as bankruptcy indicators. 

Two different bankruptcy labels are created:
1. `is_bankrupted_last_year` - when only the last financial years of the company being active are labeled as bankrupted 
2. `is_bankrupted_all_years` - when all companies' financial years (despite the company went bankrupt only during the last years) are marked as bankrupted

Sample of `is_bankrupted_last_year` and `is_bankrupted_all_years`
| code  | finance_year_start_date  | ...  | is_bankrupted_last_year  | is_bankrupted_all_years  |
|---|---|---|---|---|
| 11111  | 2018-01-01 | ... | 0 | 1 |
| 11111  | 2019-01-01 | ... | 0 | 1 |
| 11111  | 2020-01-01 | ... | 0 | 1 |
| 11111  | 2021-01-01 | ... | 1 | 1 |

### Bankruptcy data cleaning
For the preparation of the dataset some raw data were removed:
1. Removed rows where finance year start and financial year end were equal
2. Removed rows that did not had matching in balance and profit-loss tables when using registration code and finance year start date fields