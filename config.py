import os


class Config:
    DATA_PATH = '/tmp'
    DATABASE_HOST = 'localhost'
    DATABASE_NAME = 'legal_entities_open_data'
    DATABASE_USERNAME = 'root'
    DATABASE_PASSWORD = 'Legal_entities_password11.'
    BANKRUPTCY_DATASET_SQL_PATH = 'sql/bankruptcy_dataset.sql'

class Production(Config):
    pass

class Development(Config):
    pass


def get_config():
    env = os.environ.get('legal-entities-env', None)

    if env is None:
        return Development()
    elif env == 'production':
        return Production()
    
    return Development()

config = get_config()