import mysql.connector as connector
from mysql.connector import Error


class WorkWithDB:

    def __init__(self, **kwargs):
        super(WorkWithDB, self).__init__()
        self.__params = kwargs
        self.__connect = None
        self.__cursor = None
        self._init_()

    def _init_(self):
        self.__connect_db()
        self.__get_cursor()

    def __connect_db(self):
        """
        This function is used to connect database
        :return: connector
        """
        if not self.__connect:
            try:
                self.__connect = connector.connect(host="localhost",
                                                   port="3306",
                                                   user="root",
                                                   password="",
                                                   db="bap_intern_ai")
            except Error as e:
                print("Connection failed: ", e)
            finally:
                print("Connected")
                return self.__connect

    def __get_cursor(self):
        """
        this method is used to create cursor
        :return: cursor
        """
        if not self.__cursor:
            if not self.__connect:
                self.__connect_db()
            self.__cursor = self.__connect.cursor()
        return self.__cursor

    def __execute(self, sql, params: tuple = None):
        """
        This method is used to execute a query
        :param sql: the sql statement to execute
        :param params: data to work with statement
        :return:
        """
        if params:
            self.__cursor.execute(sql, params)
        else:
            self.__cursor.execute(sql)

    def __execute_many(self, sql, seq_params):
        """
        This method is used to execute a query that effect on multi records
        :param sql: the sql statement to execute
        :param seq_params: sequence of dataset to work with statement
        :return:
        """
        self.__cursor.executemany(sql, seq_params)

    def __commit(self):
        """
        This method is used to commit the current transaction
        :return:
        """
        self.__connect.commit()

    def __fetchall(self):
        """
        The method fetches all (or all remaining) rows of a query result set and returns a list of tuples
        :return: list of tuples
        """
        results = self.__cursor.fetchall()
        return results if len(results) else []

    def select(self, sql):
        """
        This method is used to get all of records
        :param sql: the sql statement to execute
        :return: list of tuples
        """
        self.__execute(sql)
        results = self.__fetchall()
        return results

    def insert(self, sql, params):
        """
        This method is used to insert new record
        :param sql: the sql statement to execute
        :param params: data to work with statement
        :return:
        """
        self.__execute(sql, params)
        self.__commit()
        print("Inserted Successfully")

    def insert_list(self, sql, seq_params):
        """
        This method is used to insert multi records into table
        :param sql: the sql statement to execute
        :param seq_params: sequence of dataset to work with statement
        :return:
        """
        self.__execute_many(sql, seq_params)
        self.__commit()
        print("Inserted List Successfully")

    def update(self, sql, params):
        """
        This method is used to update record by id
        :param sql: the sql statement to execute
        :param params: data to work with statement
        :return:
        """
        self.__execute(sql, params)
        self.__commit()
        print("Updated Successfully")

    def update_list(self, sql, seq_params):
        """
        This method is used to update multi records by id
        :param sql: the sql statement to execute
        :param seq_params: sequence of dataset to work with statement
        :return:
        """
        self.__execute_many(sql, seq_params)
        self.__commit()
        print("Updated Multi Records Successfully")

    def delete(self, sql):
        """
        This method is used to delete record by id
        :param sql: the sql statement to execute
        :return:
        """
        self.__execute(sql)
        self.__commit()
        print("Deleted Successfully")

    def __close_connect(self):
        """
        this method is used to close connect
        :return:
        """
        if self.__connect.is_connected():
            if self.__cursor:
                self.__cursor.close()
            self.__connect.close()
            print("Connection Closed")
        self.__connect = None
        self.__cursor = None
