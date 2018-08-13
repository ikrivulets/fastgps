import hug
import logging
from db.connection import DB

logging.basicConfig(level=logging.DEBUG)


@hug.post('/track/gps/{device_id}', versions=1, input_format=hug.input_format.json)
def post_track_gps(body, device_id: str):
    try:
        logging.debug(body)
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
def get_track_gps(device_id=None):
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
        logging.error(e)


@hug.post('/path/', versions=1, input_format=hug.input_format.json)
def post_track_path(body):
    if body is None:
        return {"No parameters are entered"}
    if body.get('device_id') is None or body.get('start_ts') is None:
        return {"device_id and start_ts should be populated"}
    db = DB()
    device_id = str(body.get('device_id'))
    start_ts = int(body.get('start_ts'))
    finish_ts = int(body.get('finish_ts')) if body.get('finish_ts') is not None else None
    path_id = db.execute_select("""insert into paths (device_id, start_ts, finish_ts) 
                                values(%(device_id)s, %(start_ts)s, %(finish_ts)s) returning id;""",
                                {'device_id': device_id, 'start_ts': start_ts, 'finish_ts': finish_ts})
    return {'path_id': path_id[0]['id']}


@hug.put('/path/{path_id}', versions=1, input_format=hug.input_format.json)
def post_track_path(body, path_id: str):
    db = DB()
    if body is None:
        return {"No parameters are entered"}
    finish_ts = body.get('finish_ts')
    if path_id is None or finish_ts is None:
        return {"path_id and finish_ts should be populated"}
    path_id = int(path_id)
    finish_ts = int(finish_ts)
    path = db.execute_select("select * from paths where id = %(path_id)s",
                             {'path_id': path_id})
    if not path:
        return {'path id {} is absent'.format(path_id)}
    db.execute_crud("update paths set finish_ts = %(finish_ts)s where id = %(path_id)s",
                    {'finish_ts': finish_ts, 'path_id': path_id})
    return {'finish_ts is updated for path id {}'.format(path_id)}


@hug.post('/track/activity/{device_id}', versions=1, input_format=hug.input_format.json)
def post_track_activiy(body, device_id: str):
    try:
        logging.debug(body)
        db = DB()
        activity = list()
        for el in body['activity']:
            el['device_id'] = device_id
            activity.append(el)

        db.insert_all("""insert into activity (device_id, activity_type, ts) 
                      values(%(device_id)s, %(activity_type)s, %(ts)s)""",
                      activity)
    except Exception as e:
        logging.error(e)
