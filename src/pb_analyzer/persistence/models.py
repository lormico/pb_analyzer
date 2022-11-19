from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

ShortDateTime = DATETIME(storage_format="%(year)04d-%(month)02d-%(day)02d "
                                        "%(hour)02d:%(minute)02d:%(second)02d",
                         regexp=r"(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)")


class Station(Base):
    __tablename__ = "station"
    id = Column(Integer, primary_key=True)
    co = Column(String)
    co_name = Column(String)
    lat = Column(Numeric)
    lng = Column(Numeric)
    name = Column(String)
    address = Column(String)
    zip = Column(String)
    city = Column(String)
    city_name = Column(String)
    provincia = Column(String)
    regione = Column(String)
    fuels = Column(String)
    status = Column(String)
    insertion_date = Column(ShortDateTime)
    last_updated = Column(ShortDateTime)


class Price(Base):
    __tablename__ = "price"
    station = Column(Integer, ForeignKey("station.id"), primary_key=True)
    date = Column(ShortDateTime, primary_key=True)
    service = Column(String, primary_key=True)
    fuel = Column(String, primary_key=True)
    price = Column(Numeric, primary_key=True)


class Metadata(Base):
    __tablename__ = "metadata"
    key = Column(String, primary_key=True)
    value = Column(String)
