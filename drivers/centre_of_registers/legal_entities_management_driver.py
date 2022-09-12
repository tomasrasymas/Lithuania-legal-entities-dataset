from drivers.driver import Driver
import pandas as pd


class LegalEntitiesManagementDriver(Driver):

    urls = ['https://www.registrucentras.lt/aduomenys/?byla=JAR_VALDYMAS.csv']
    file_names = ['jar_valdymas.csv']
    columns_mapping = {
        'JA_kodas': 'code',
        'JA_pavadinimas': 'name',
        'vadovas': 'manager',
        'vad_org_nuo': 'manager_from_date',
        'valdyba': 'board',
        'vald_org_nuo': 'board_from_date',
        'taryba': 'council',
        'tar_org_nuo': 'council_from_date',
        'kiti_valdymo_organai': 'other',
        'formavimo_data': 'data_refresh_date'
    }
    table_name = 'stg_legal_entities_management'
    
    def __init__(self) -> None:
        super().__init__()
    
    def download(self, url, file_path) -> str:
        return super().download(url=url, file_path=file_path)
    
    def load(self, file_path) -> pd.DataFrame:
        return super().load(file_path=file_path)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(df=df)
        
        df = df.rename(columns = self.columns_mapping)

        df['manager_from_date'] = pd.to_datetime(df['manager_from_date']).dt.date
        df['board_from_date'] = pd.to_datetime(df['board_from_date']).dt.date
        df['council_from_date'] = pd.to_datetime(df['council_from_date']).dt.date
        df['data_refresh_date'] = pd.to_datetime(df['data_refresh_date']).dt.date

        return df

    def pre_execute(self):
        return super().pre_execute()
    
    def post_execute(self):
        return super().post_execute()

    def store(self, df: pd.DataFrame) -> int:
        df = super().store(df=df)

        return df
