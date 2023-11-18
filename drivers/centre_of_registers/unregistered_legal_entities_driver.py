from drivers.driver import Driver
import pandas as pd
from drivers.mappings import LEGAL_ENTITIES_FORMS_MAP


class UnregisteredLegalEntitiesDriver(Driver):
    urls = ['https://www.registrucentras.lt/aduomenys/?byla=JAR_ISREGISTRUOTI.csv']
    file_names = ['jar_isregistruoti.csv']
    columns_mapping = {
        'ja_kodas': 'code',
        'ja_pavadinimas': 'name',
        'adresas': 'address',
        'ja_reg_data': 'registration_date',
        'form_kodas': 'legal_form_code',
        'form_pavadinimas': 'legal_form_name',
        'isreg_data': 'unregistered_date',
        'formavimo_data': 'data_refresh_date'
    }
    table_name = 'stg_unregistered_legal_entities'

    def __init__(self) -> None:
        super().__init__()

    def download(self, url, file_path) -> str:
        return super().download(url=url, file_path=file_path)

    def load(self, file_path, separator=',') -> pd.DataFrame:
        return super().load(file_path=file_path, separator='|')

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(df=df)

        df = df.rename(columns=self.columns_mapping)

        df['registration_date'] = pd.to_datetime(df['registration_date']).dt.date
        df['unregistered_date'] = pd.to_datetime(df['unregistered_date']).dt.date
        df['data_refresh_date'] = pd.to_datetime(df['data_refresh_date']).dt.date

        df['legal_form_name'] = df['legal_form_name'].map(lambda x: LEGAL_ENTITIES_FORMS_MAP.get(x))

        return df

    def pre_execute(self):
        return super().pre_execute()

    def post_execute(self):
        return super().post_execute()

    def store(self, df: pd.DataFrame) -> int:
        df = super().store(df=df)

        return df
