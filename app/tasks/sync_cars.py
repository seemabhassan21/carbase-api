import json
import requests
from flask import current_app
from app.models import db, Car
from run import celery  # safer than importing from celery_worker

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

            if total_saved:
                db.session.commit()

        except Exception as e:
            current_app.logger.error(f"Error syncing year {year}: {str(e)}")

    current_app.logger.info(f"Sync complete: {total_saved} new cars added.")
