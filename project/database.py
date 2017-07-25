import MySQLdb as mdb
import logging
import project.config as cfg

class DatabaseException(Exception):
    pass


class Database():
    """
    Class to handle all database interactions.
    """

    def __init__(self):
        """
        Setup the connection and initialize the database.
        """
        self.log = logging.getLogger('DATABASE')
        self.con = mdb.connect(host=cfg.server, user=cfg.username,
                               passwd=cfg.password, db=cfg.database,
                               charset='utf8', use_unicode=True)
        self.cur = self.con.cursor(mdb.cursors.DictCursor)
        self.cur.execute("SET NAMES utf8mb4;")
        self.cur.execute("SET CHARACTER SET utf8mb4;")
        self.cur.execute("SET character_set_connection=utf8mb4;")

    def __del__(self):
        """
        Clean up the database connection if it exists.
        """
        if self.con is not None:
            self.con.close()

    def execute_sql(self, stmt, args=None, commit=True):
        """
        Execute an SQL statement.

        Attempt to execute an SQL statement and log any errors. Return True if
        successful and false if not.
        """
        self.log.debug('Executing {0} with args {1}.'.format(stmt, args))

        try:
            if args is None:
                self.cur.execute(stmt)
            else:
                self.cur.execute(stmt, args)

            if commit is True:
                self.con.commit()

            return True

        except mdb.Error as e:
            self.log.debug(e)
            return False


class EndpointDatabase(Database):
    """
    Class to handle endpoint data.
    """
    def __init__(self):
        Database.__init__(self)
 
    def find(self, arg1, arg2):
        self.log.debug('Searching for endpoint data.')

        stmt = "SELECT * FROM database WHERE val1=%s AND val2=%s"

        if self.execute_sql(stmt, (arg1, arg2)) is True:
            results = list(self.cur.fetchall())
            return results
        else:
            return []

