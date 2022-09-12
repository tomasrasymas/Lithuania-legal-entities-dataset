from drivers.driver import Driver
import pandas as pd


class LegalEntitiesAddressesDriver(Driver):

    urls = ['https://www.registrucentras.lt/aduomenys/?byla=JAR_ADRESAI.csv']
    file_names = ['jar_adresai.csv']
    columns_mapping = {
        'JA_kodas': 'code',
        'adresas': 'address',
        'aob_kodas': 'address_code',
        'adresas_nuo': 'address_from_date',
        'formavimo_data': 'data_refresh_date'
    }
    table_name = 'stg_legal_entities_addresses'
    
    def __init__(self) -> None:
        super().__init__()
    
    def download(self, url, file_path) -> str:
        return super().download(url=url, file_path=file_path)
    
    def load(self, file_path) -> pd.DataFrame:
        return super().load(file_path=file_path)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(df=df)
        
        df = df.rename(columns = self.columns_mapping)

        df['address_from_date'] = pd.to_datetime(df['address_from_date']).dt.date
        df['data_refresh_date'] = pd.to_datetime(df['data_refresh_date']).dt.date

        return df

    def pre_execute(self):
        return super().pre_execute()
    
    def post_execute(self):
        return super().post_execute()
                                                                           
    def store(self, df: pd.DataFrame) -> int:
        df = super().store(df=df)

        return df
