import os
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

config_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../config.yml")

with open(config_path) as yml_file:
    config = yaml.load(yml_file)

db_config = config["database"]

connection_string = 'mysql+pymysql://{user}:{password}@{host}:3306/{db_name}?charset=utf8' \
    .format(
    user=db_config["db_user"],
    password=db_config["db_password"],
    host=db_config["db_host"],
    db_name=db_config["db_name"]
)

engine = create_engine(
    connection_string,
    pool_size=5,
    pool_recycle=3600
)

db = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
