import json
import requests
from flask import current_app
from app.extensions import db
from app.models import Car
from .celery_worker import celery

@celery.task(name="sync_cars")
def sync_cars():
    url = current_app.config['CAR_API_URL']
    headers = current_app.config['CAR_API_HEADERS']
    total_saved = 0

    for year in range(2012, 2023):
        try:
            query = json.dumps({"Year": year})
            response = requests.get(url, headers=headers, params={"where": query})

            if response.status_code != 200:
                current_app.logger.warning(f"Failed to fetch data for year {year}: {response.status_code}")
                continue

            cars = response.json().get('results', [])

            for c in cars:
                if not Car.query.filter_by(make=c['Make'], model=c['Model'], year=c['Year']).first():
                    db.session.add(Car(make=c['Make'], model=c['Model'], year=c['Year']))
                    total_saved += 1

        except Exception as e:
            current_app.logger.error(f"Error syncing year {year}: {str(e)}")
            db.session.rollback()

    try:
        if total_saved > 0:
            db.session.commit()
        current_app.logger.info(f"Sync complete: {total_saved} new cars added.")
    except Exception as e:
        current_app.logger.error(f"Failed to commit changes: {str(e)}")
        db.session.rollback()
