import os
from typing import Dict, List
from abc import ABCMeta, abstractmethod
from drivers.helpers import download_file, unzip_file
import pandas as pd
import zipfile
from sqlalchemy import create_engine
from config import config
import logging

logging.getLogger().setLevel(logging.INFO)


class Driver(metaclass=ABCMeta):
    urls: List[str]
    file_names: List[str]
    columns_mapping: Dict[str, str]
    table_name: str

    def __init__(self) -> None:
        self.engine = create_engine('mysql+mysqlconnector://%s:%s@%s/%s' % (
            config.DATABASE_USERNAME,
            config.DATABASE_PASSWORD,
            config.DATABASE_HOST,
            config.DATABASE_NAME))

    @abstractmethod
    def download(self, url, file_path) -> str:
        logging.info('Downloading %s to %s' % (url, file_path))

        file_path = download_file(url, file_path)
        if not file_path:
            raise Exception('File %s not downloaded' % url)

        if zipfile.is_zipfile(file_path):
            extracted_files = unzip_file(file_path)

            assert len(extracted_files) == 1

            file_path = extracted_files[0]

        return file_path

    @abstractmethod
    def load(self, file_path, separator=',') -> pd.DataFrame:
        logging.info('Loading file %s' % file_path)

        assert os.path.exists(file_path)

        df = pd.read_csv(file_path, sep=separator, on_bad_lines='skip')
        return df

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info('Performing transformation')
        return df

    @abstractmethod
    def store(self, df: pd.DataFrame) -> int:
        logging.info('Storing the data')

        with self.engine.begin() as connection:
            rows_effected = df.to_sql(self.table_name,
                                      con=connection,
                                      if_exists='append',
                                      chunksize=500,
                                      index=False,
                                      method='multi')

        assert rows_effected

        return rows_effected

    @abstractmethod
    def post_execute(self):
        with self.engine.begin() as connection:
            connection.execute('alter table `%s` add index `%s` (`%s`)' % (self.table_name,
                                                                           'idx_' + self.table_name + '_code',
                                                                           'code'))

    @abstractmethod
    def pre_execute(self):
        with self.engine.begin() as connection:
            connection.execute('drop table if exists `%s`;' % self.table_name)

    def execute(self, data_path) -> bool:
        logging.info('Executing %s' % data_path)

        self.pre_execute()

        for idx, url in enumerate(self.urls):
            file_path = os.path.join(data_path, self.file_names[idx])

            if not os.path.exists(file_path):
                file_path = self.download(url, file_path)
            df = self.load(file_path)
            df = self.transform(df)
            self.store(df)

        self.post_execute()
        return True
