from drivers.driver import Driver
import pandas as pd


class SodraMonthlyDriver(Driver):

    urls = ['https://atvira.sodra.lt/imones/downloads/2021/monthly-2021.csv.zip',
            'https://atvira.sodra.lt/imones/downloads/2022/monthly-2022.csv.zip']
    file_names = ['sodra_monthly_2021.csv', 'sodra_monthly_2022.csv']
    columns_mapping = {
        'Draudėjo kodas (code)': 'assurer_code',
        'Juridinių asmenų registro kodas (jarCode)': 'legal_entity_code',
        'Pavadinimas (name)': 'legal_entity_name',
        'Savivaldybė, kurioje registruota(municipality)': 'municipality',
        'Ekonominės veiklos rūšies kodas(ecoActCode)': 'eco_act_code',
        'Ekonominės veiklos rūšies pavadinimas(ecoActName)': 'eco_act_name',
        'Mėnuo (month)': 'month',
        'Vidutinis darbo užmokestis (avgWage)': 'average_salary',
        'Apdraustųjų skaičius (numInsured)': 'number_of_insured',
        'Vidutinis darbo užmokestis II (avgWage2)': 'average_salary_authorship_contract',
        'Apdraustųjų skaičius II (numInsured2)': 'number_of_insured_authorship_contract',
        'Valstybinio socialinio draudimo įmoka (tax)': 'tax'
    }
    table_name = 'stg_sodra_monthly'
    
    def __init__(self) -> None:
        super().__init__()
    
    def download(self, url, file_path) -> str:
        return super().download(url=url, file_path=file_path)
    
    def load(self, file_path) -> pd.DataFrame:
        return super().load(file_path=file_path, separator=';')

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = super().transform(df=df)
        
        df = df.rename(columns = self.columns_mapping)

        return df

    def pre_execute(self):
        return super().pre_execute()
    
    def post_execute(self):
        with self.engine.begin() as connection:
            connection.execute('alter table `%s` add index `%s` (`%s`)' % (self.table_name,
                                                                           'idx_' + self.table_name + '_legal_entity_code',
                                                                           'legal_entity_code'))

            connection.execute('''alter table `%s` 
                                  change column `legal_entity_code` `legal_entity_code` bigint null default null,
                                  change column `eco_act_code` `eco_act_code` bigint null default null;''' % self.table_name)

    def store(self, df: pd.DataFrame) -> bool:
        df = super().store(df=df)

        return df
