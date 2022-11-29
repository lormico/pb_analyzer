import datetime
from typing import List, Dict

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from pb_analyzer.client import JsonObject
from pb_analyzer.persistence.models import Station, Price, Metadata


def upsert_stations(session: Session, stations: Dict[str, JsonObject]):
    values = list()
    for station in stations.values():
        values.append(dict(
            id=int(station['id']),
            co=station['co'],
            co_name=station['co_name'],
            lat=float(station['lat']),
            lng=float(station['lng']),
            name=station['name'],
            address=station['address'],
            zip=station['zip'],
            city=station['city_name'],
            provincia=station['provincia'],
            regione=station['regione'],
            fuels=station['fuels'],
            status=station['status'],
            insertion_date=datetime.datetime.strptime(station['insertion_date'], "%Y-%m-%d %H:%M"),
            last_updated=datetime.datetime.strptime(station['last_updated'], "%Y-%m-%d %H:%M"),
        ))

    statement = insert(Station).values(values)
    # If there's already a station with a given ID, it overwrites all the info
    statement = statement.on_conflict_do_update(index_elements=['id'], set_=statement.excluded)

    session.execute(statement)


def insert_prices(session: Session, prices: List[JsonObject]):
    values = list()
    for price in prices:
        values.append(dict(
            station=int(price['station']),
            date=datetime.datetime.strptime(price['date'], "%Y-%m-%d %H:%M:%S"),
            service=price['service'],
            fuel=price['fuel'],
            price=float(price['price']),
        ))

    statement = insert(Price).prefix_with("OR IGNORE").values(values)
    session.execute(statement)


def upsert_metadata(session: Session, metadata: Dict):
    values = [{"key": k, "value": v} for k, v in metadata.items()]
    statement = insert(Metadata).values(values)
    statement = statement.on_conflict_do_update(index_elements=['key'], set_=statement.excluded)
    session.execute(statement)
