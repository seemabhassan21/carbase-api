import json
import requests
from app.models import db, Car
from flask import current_app
from celery_worker import celery

@celery.task
def sync_cars():
    url = current_app.config['CAR_API_URL']
    headers = current_app.config['CAR_API_HEADERS']

    total_saved = 0

    for year in range(2012, 2023):
        query = json.dumps({"Year": year})
        response = requests.get(url, headers=headers, params={"where": query})

        if response.status_code != 200:
            print(f"Failed to fetch data for year {year}: {response.status_code}")
            continue

        cars = response.json().get('results', [])

        for c in cars:
            if not Car.query.filter_by(make=c['Make'], model=c['Model'], year=c['Year']).first():
                db.session.add(Car(make=c['Make'], model=c['Model'], year=c['Year']))
                total_saved += 1

        db.session.commit()

    print(f" Sync complete: {total_saved} new cars added.")
