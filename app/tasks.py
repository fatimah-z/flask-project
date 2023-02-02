import requests
from celery.schedules import crontab
from flask import json

from app import app, db
from app.celery_app import celery
from app.models import Car

celery.conf.beat_schedule = {
    'add-everyday': {
        'task': 'test',
        'schedule': crontab(minute=0, hour=0),
    },
}
celery.conf.timezone = 'UTC'


@celery.task(name="test")
def test():
    with app.app_context():
        url = 'https://parseapi.back4app.com/classes/Carmodels_Car_Model_List?limit=10'
        headers = {
            'X-Parse-Application-Id': 'WDMOU1Qwd4krcZ8ukdFzNcgwZQjckZr8iAn6REKG',
            'X-Parse-REST-API-Key': 'FDbiA367WWEgIF7LEJjEfddu1sJ6rzykGR626EF8'
        }

        data = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))

        try:
            for item in data['results']:
                existing_car = db.session.query(Car).filter_by(objectId=item['objectId']).first()

                if not existing_car:
                    car = Car(objectId=item['objectId'],
                              createdAt=item['createdAt'],
                              updatedAt=item['updatedAt'],
                              year=item['Year'],
                              make=item['Make'],
                              category=item['Category']
                              )
                    db.session.add(car)
                    db.session.commit()
                else:
                    if existing_car.year != item['Year']:
                        existing_car.year = item['Year']
                    if existing_car.make != item['Make']:
                        existing_car.make = item['Make']
                    if existing_car.category != item['Category']:
                        existing_car.category = item['Category']
                    if existing_car.updatedAt != item['updatedAt']:
                        existing_car.updatedAt = item['updatedAt']
                    if existing_car.updatedAt != item['createdAt']:
                        existing_car.updatedAt = item['createdAt']
                    db.session.commit()

            response_object = {
                'status': 'success',
                'data': data
            }
            return json.dumps(response_object)
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': str(e)
            }
            return json.dumps(response_object)
