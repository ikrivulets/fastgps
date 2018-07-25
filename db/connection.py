import psycopg2
import logging
import psycopg2.pool
import psycopg2.extras
from utils import configuration


class DB:
    """ Class encapsulating essential operations with DB """

    pool = None

    def __init__(self):
        if self.pool is None:
            config = configuration.load()
            self.build_connection_pool(config['database'])

    @staticmethod
    def build_connection_pool(config):
        if not DB.check_configuration(config):
            raise ValueError('Invalid database configuration.')
        if DB.pool is None:
            try:
                DB.pool = psycopg2.pool.ThreadedConnectionPool(1, config['pool'], host=config['hostname'],
                                                               database=config['database'], user=config['username'],
                                                               password=config['password'], port=config['port'])
            except Exception as e:
                logging.error('Unable to connect to database: {}'.format(repr(e)))

    @staticmethod
    def check_configuration(config):
        required_keys = ['pool', 'hostname', 'database', 'username', 'password', 'port']
        if set(required_keys).issubset(list(config)):
            valid_config = True
        else:
            valid_config = False
        return valid_config

    @staticmethod
    def execute_crud(sql, data=None):
        rowcount = 0

        try:
            conn = DB.pool.getconn()
            curs = conn.cursor()
            curs.execute(sql, data)
            conn.commit()
            rowcount = curs.rowcount
            DB.pool.putconn(conn)
        except Exception as e:
            logging.error("Execute CRUD: {}".format(repr(e)))
            conn.rollback()
        return rowcount

    @staticmethod
    def execute_select(sql, data=None):
        result = None
        try:
            conn = DB.pool.getconn()
            curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            curs.execute(sql, data)
            conn.commit()
            result = curs.fetchall()
            DB.pool.putconn(conn)
        except Exception as e:
            logging.error("Execute SELECT: {}".format(repr(e)))
        return result

    @staticmethod
    def insert_all(sql, data=None):
        if data is None:
            return

        try:
            conn = DB.pool.getconn()
            curs = conn.cursor()
            curs.executemany(sql, data)
            conn.commit()
            DB.pool.putconn(conn)
        except Exception as e:
            logging.error("Execute INSERT: {}".format(repr(e)))
            conn.rollback()

    @staticmethod
    def get_connection():
        return DB.pool.getconn()

    @staticmethod
    def put_connection(connection):
        DB.pool.putconn(connection)
