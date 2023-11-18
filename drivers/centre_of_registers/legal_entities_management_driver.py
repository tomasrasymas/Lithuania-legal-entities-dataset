from drivers.driver import Driver
import pandas as pd


class LegalEntitiesManagementDriver(Driver):
    urls = ['https://www.registrucentras.lt/aduomenys/?byla=JAR_VALDYMAS.csv']
    file_names = ['jar_valdymas.csv']
    # ja_kodas | ja_pavadinimas | vadovas | vad_data_nuo | valdyba | vald_data_nuo | taryba | tary_data_nuo | kiti_organai | formavimo_data
    columns_mapping = {
        'ja_kodas': 'code',
        'ja_pavadinimas': 'name',
        'vadovas': 'manager',
        'vad_data_nuo': 'manager_from_date',
        'valdyba': 'board',
        'vald_data_nuo': 'board_from_date',
        'taryba': 'council',
        'tary_data_nuo': 'council_from_date',
        'kiti_organai': 'other',
        'formavimo_data': 'data_refresh_date'
    }
    table_name = 'stg_legal_entities_management'

    def __init__(self) -> None:
        super().__init__()

    def download(self, url, file_path) -> str:
        return super().download(url=url, file_path=file_path)

    def load(self, file_path, separator="|") -> pd.DataFrame:
        return super().load(file_path=file_path, separator="|")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(df=df)

        df = df.rename(columns=self.columns_mapping)

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
