from drivers.driver import Driver
import pandas as pd
from drivers.mappings import LEGAL_ENTITIES_FORMS_MAP, LEGAL_ENTITIES_STATUS_MAP


class RegisteredLegalEntitiesDriver(Driver):

    urls = ['https://www.registrucentras.lt/aduomenys/?byla=JAR_IREGISTRUOTI.csv']
    file_names = ['jar_iregistruoti.csv']
    columns_mapping = {
        'JA_kodas': 'code',
        'JA_pavadinimas': 'name',
        'adresas': 'address',
        'reg_data': 'registration_date',
        'form_kodas': 'legal_form_code',
        'form_pavadinimas': 'legal_form_name',
        'status_kodas': 'status_code',
        'stat_pavadinimas': 'status_name',
        'stat_data_nuo': 'status_from_date',
        'formavimo_data': 'data_refresh_date'
    }
    table_name = 'stg_registered_legal_entities'
    
    def __init__(self) -> None:
        super().__init__()
    
    def download(self, url, file_path) -> str:
        return super().download(url=url, file_path=file_path)
    
    def load(self, file_path) -> pd.DataFrame:
        return super().load(file_path=file_path)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(df=df)
        
        df = df.rename(columns = self.columns_mapping)

        df['registration_date'] = pd.to_datetime(df['registration_date']).dt.date
        df['status_from_date'] = pd.to_datetime(df['status_from_date']).dt.date
        df['data_refresh_date'] = pd.to_datetime(df['data_refresh_date']).dt.date

        df['legal_form_name'] = df['legal_form_name'].map(lambda x: LEGAL_ENTITIES_FORMS_MAP.get(x))
        df['status_name'] = df['status_name'].map(lambda x: LEGAL_ENTITIES_STATUS_MAP.get(x))

        return df

    def pre_execute(self):
        return super().pre_execute()
    
    def post_execute(self):
        return super().post_execute()

    def store(self, df: pd.DataFrame) -> int:
        df = super().store(df=df)

        return df
