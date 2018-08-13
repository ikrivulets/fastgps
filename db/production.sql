CREATE TABLE IF NOT EXISTS gps_data
(
  device_id VARCHAR(120),
  latitude float8,
  longitude float8,
  altitude float8,
  horAccuracy integer,
  verAccuracy integer,
  course integer,
  speed integer,
  ts integer
);


CREATE TABLE IF NOT EXISTS activity
(
  device_id VARCHAR(120),
  activity_type varchar(50),
  ts integer
);


CREATE TABLE IF NOT EXISTS paths
(
  id SERIAL,
  device_id VARCHAR(120),
  start_ts integer,
  finish_ts integer
);
