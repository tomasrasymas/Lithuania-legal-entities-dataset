from config import config
from sqlalchemy import create_engine
import csv
import os
import logging


logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    dataset_file_path = os.path.join(config.DATA_PATH, 'bankruptcy_dataset.csv')

    logging.info(f'Started dataset generation. Output file path: "{ dataset_file_path }"')

    engine = create_engine('mysql+mysqlconnector://%s:%s@%s/%s' % (config.DATABASE_USERNAME,
                                                                   config.DATABASE_PASSWORD,
                                                                   config.DATABASE_HOST,
                                                                   config.DATABASE_NAME))
    with engine.begin() as connection:
        cursor = connection.execute(open(config.BANKRUPTCY_DATASET_SQL_PATH).read())
        rows = cursor.fetchall()

        with open(dataset_file_path, 'w') as f:
            csv_out = csv.writer(f)

            csv_out.writerow(list(cursor.keys()))
            csv_out.writerows(rows)

            logging.info(f'Dataset generated, path - "{ dataset_file_path }", records count: { len(rows) }')
