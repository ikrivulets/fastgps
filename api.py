import hug
import logging
from db.connection import DB


@hug.post('/track/gps/{device_id}', versions=1, input_format=hug.input_format.json)
def post_external_webhook(body, device_id: str):
    try:
        db = DB()
        gps = list()
        for el in body['gps']:
            el['device_id'] = device_id
            gps.append(el)

        db.insert_all("""insert into gps_data (device_id, latitude, longitude, altitude, 
                          horAccuracy, verAccuracy, course, speed, ts) 
                          values(%(device_id)s, %(latitude)s, %(longitude)s, %(altitude)s, %(horAccuracy)s,
                          %(verAccuracy)s, %(course)s, %(speed)s, %(ts)s)""",
                      gps)
    except Exception as e:
        logging.error(e)


@hug.get('/track/gps/{device_id}', versions=1, input_format=hug.input_format.json)
def post_external_webhook(device_id=None):
    try:
        if device_id is None:
            return
        db = DB()
        gps = db.execute_select("select * from gps_data where device_id = %(device_id)s order by ts desc limit 1",
                                {'device_id': device_id})
        activity = db.execute_select("select * from activity where device_id = %(device_id)s order by ts desc limit 1",
                                     {'device_id': device_id})
        return {'activity': activity, 'gps': gps}
    except Exception as e:
        logging.warning(e)


# @hug.get('/track/path}', versions=1, input_format=hug.input_format.json)
# def post_external_webhook(path_id=None, device_id=None):
#     pass


@hug.post('/track/activity/{device_id}', versions=1, input_format=hug.input_format.json)
def post_external_webhook(body, device_id:str):
    try:
        db = DB()
        activity = list()
        for el in body['activity']:
            el['device_id'] = device_id
            activity.append(el)

        db.insert_all("""insert into activity (device_id, activity_type, ts) 
                      values(%(device_id)s, %(activity_type)s, %(ts)s)""",
                      activity)
    except Exception as e:
        logging.warning(e)