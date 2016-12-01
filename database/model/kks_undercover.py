from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

TABLE_ARGS = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}


class WCFavorability(Base):
    __table_args__ = TABLE_ARGS
    __tablename__ = 'wc_favorability'

    name = Column(String(45), primary_key=True)
    nick_name = Column(String(45))
    score = Column(Integer)

