from drivers.driver import Driver
import pandas as pd
from drivers.mappings import LEGAL_ENTITIES_FORMS_MAP, LEGAL_ENTITIES_STATUS_MAP


class LegalEntitiesBalanceSheetsDriver(Driver):

    urls = ['https://www.registrucentras.lt/aduomenys/?byla=JAR_FA_RODIKLIAI_BLNS_2022.csv',
            'https://www.registrucentras.lt/aduomenys/?byla=JAR_FA_RODIKLIAI_BLNS_2021.csv',
            'https://www.registrucentras.lt/aduomenys/?byla=JAR_FA_RODIKLIAI_BLNS_2020.csv',
            'https://www.registrucentras.lt/aduomenys/?byla=JAR_FA_RODIKLIAI_BLNS_2019.csv',
            'https://www.registrucentras.lt/aduomenys/?byla=JAR_FA_RODIKLIAI_BLNS_2018.csv',
            'https://www.registrucentras.lt/aduomenys/?byla=JAR_FA_RODIKLIAI_BLNS_2017.csv',
            'https://www.registrucentras.lt/aduomenys/?byla=JAR_FA_RODIKLIAI_BLNS_2016.csv',
            'https://www.registrucentras.lt/aduomenys/?byla=JAR_FA_RODIKLIAI_BLNS_2015.csv']
    file_names = ['jar_fa_blns_2022.csv', 
                  'jar_fa_blns_2021.csv', 
                  'jar_fa_blns_2020.csv', 
                  'jar_fa_blns_2019.csv', 
                  'jar_fa_blns_2018.csv',
                  'jar_fa_blns_2017.csv',
                  'jar_fa_blns_2016.csv',
                  'jar_fa_blns_2015.csv']
    columns_mapping = {
        'obj_kodas': 'code',
        'obj_pav': 'name',
        'form_kodas': 'legal_form_code',
        'form_pav': 'legal_form_name',
        'stat_statusas': 'status_code',
        'stat_pav': 'status_name',
        'template_id': 'template_id',
        'template_name': 'template_name',
        'standard_id': 'standard_id',
        'standard_name': 'standard_name',
        'laikotarpis_nuo': 'finance_year_start_date',
        'laikotarpis_iki': 'finance_year_end_date',
        'reg_date': 'document_registration_date',
        'nuosavas_kapitalas': 'equity',
        'mok_sumos_ir_isipareigojimai': 'liabilities',
        'ilgalaikis_turtas': 'long_term_financial_assets',
        'trumpalaikis_turtas': 'short_term_financial_assets',
        'formavimo_data': 'data_refresh_date'
    }
    table_name = 'stg_legal_entities_balance_sheets'
    
    def __init__(self) -> None:
        super().__init__()
    
    def download(self, url, file_path) -> str:
        return super().download(url=url, file_path=file_path)
    
    def load(self, file_path) -> pd.DataFrame:
        return super().load(file_path=file_path)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(df=df)
        
        df = df.rename(columns = self.columns_mapping)

        df['finance_year_start_date'] = pd.to_datetime(df['finance_year_start_date']).dt.date
        df['finance_year_end_date'] = pd.to_datetime(df['finance_year_end_date']).dt.date
        df['document_registration_date'] = pd.to_datetime(df['document_registration_date']).dt.date
        df['data_refresh_date'] = pd.to_datetime(df['data_refresh_date']).dt.date

        df['legal_form_name'] = df['legal_form_name'].map(lambda x: LEGAL_ENTITIES_FORMS_MAP.get(x))
        df['status_name'] = df['status_name'].map(lambda x: LEGAL_ENTITIES_STATUS_MAP.get(x))

        return df

    def pre_execute(self):
        return super().pre_execute()
    
    def post_execute(self):
        with self.engine.begin() as connection:
            connection.execute('alter table `%s` add index `%s` (`%s`)' % (self.table_name,
                                                                           'idx_' + self.table_name + '_code',
                                                                           'code'))

            connection.execute('alter table `%s` add index `%s` (`%s`)' % (self.table_name,
                                                                           'idx_' + self.table_name + '_fin_year_str',
                                                                           'finance_year_start_date'))

    def store(self, df: pd.DataFrame) -> int:
        df = super().store(df=df)

        return df
