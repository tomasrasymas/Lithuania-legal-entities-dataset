with broken_balance_sheets as ( 
	select 
		distinct code
	from stg_legal_entities_balance_sheets
    where
		finance_year_start_date = finance_year_end_date or
        legal_form_name is null or
        status_name is null
), broken_profit_loss_statements as ( 
	select 
		distinct code
	from stg_legal_entities_profit_loss_statements
    where
		finance_year_start_date = finance_year_end_date or
        legal_form_name is null or
        status_name is null
), legal_entities as ( 
	select 
		code,
        registration_date
	from stg_registered_legal_entities
    union
    select 
		code,
        registration_date
	from stg_unregistered_legal_entities
), balance_sheets as (
	select 
		code,
        name, 
        legal_form_name,
        status_name,
        finance_year_start_date,
		finance_year_end_date,
		document_registration_date,
        equity,
        liabilities,
        long_term_financial_assets,
        short_term_financial_assets,
        row_number() over(partition by code order by code, finance_year_start_date desc) AS row_num
	from stg_legal_entities_balance_sheets
    where
        code not in (select code from broken_balance_sheets)
), profit_loss_statements as (
	select 
		code,
        name, 
        legal_form_name,
        status_name,
        finance_year_start_date,
		finance_year_end_date,
		document_registration_date,
        profit_before_taxes,
        net_profit,
        sales_revenue
	from stg_legal_entities_profit_loss_statements
    where
        code not in (select code from broken_profit_loss_statements)
), dataset as (
	select 
		bs.code,
		le.registration_date,
		bs.legal_form_name,
		bs.status_name,
		bs.finance_year_start_date,
		bs.finance_year_end_date,
		bs.document_registration_date,
		bs.equity as equity, 
		bs.liabilities as liabilities, 
		bs.long_term_financial_assets as long_term_financial_assets, 
		bs.short_term_financial_assets as short_term_financial_assets, 
		pls.profit_before_taxes as profit_before_taxes, 
		pls.net_profit as net_profit,
		pls.sales_revenue as sales_revenue,
		bs.equity / bs.liabilities as idx_eq_lia_ratio,
		bs.liabilities / (bs.long_term_financial_assets + bs.short_term_financial_assets) as idx_lia_fin_as_ratio,
		bs.short_term_financial_assets / bs.liabilities as idx_sh_fin_as_lia_ratio,
		(bs.long_term_financial_assets + bs.short_term_financial_assets) / bs.equity as idx_fin_as_eq_ratio,
		(bs.long_term_financial_assets + bs.short_term_financial_assets) / bs.liabilities as idx_fin_as_lia_ratio,
		pls.net_profit / (bs.long_term_financial_assets + bs.short_term_financial_assets) as idx_n_prof_fin_as_ratio,
		pls.sales_revenue / (bs.long_term_financial_assets + bs.short_term_financial_assets) as idx_s_rev_fin_as_ratio,
		pls.profit_before_taxes / bs.equity as idx_prof_tax_eq_ratio,
		pls.profit_before_taxes / (bs.long_term_financial_assets + bs.short_term_financial_assets) as idx_prof_tax_fin_as_ratio,
        case
			when bs.status_name in ("Under Restructuring", "Going Bankrupt", "Bankrupt", "Liquidation due to bankruptcy") and
				 bs.row_num = 1 then 1
			else 0
		end as is_bankrupted_last_year,
		case
			when bs.status_name in ("Under Restructuring", "Going Bankrupt", "Bankrupt", "Liquidation due to bankruptcy") then 1
			else 0
		end as is_bankrupted_all_years
	from balance_sheets bs
	left join legal_entities le on bs.code = le.code
	left join profit_loss_statements pls on bs.code = pls.code and
											bs.finance_year_start_date = pls.finance_year_start_date
	order by
		bs.code,
        bs.finance_year_start_date,
        bs.document_registration_date
)

select 
	* 
from dataset