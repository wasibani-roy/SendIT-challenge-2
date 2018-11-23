"""This file handles setting up the connection to database"""
import os
import psycopg2
import psycopg2.extras as sendIT


class Database:
    """This class connects to the database"""

    def __init__(self):
        db_name = d6q5a9sklhd48a

        self.conn = psycopg2.connect(
            database=db_name, user="vyriitwrgflaqt", password="61e72d8b7c669e8f0432f0d0597a4d421841ed7c983d46c1fe78113044eeb4d0",
            host="ec2-54-163-230-178.compute-1.amazonaws.com", port="5432"
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor(cursor_factory=sendIT.RealDictCursor)

    def create_tables(self):
        """method for creating all tables"""
        create_user_table = """CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY,
                username VARCHAR NOT NULL,
                email VARCHAR NOT NULL,
                password VARCHAR NOT NULL,
                role VARCHAR NOT NULL
            )"""
        create_order_table = """CREATE TABLE IF NOT EXISTS orders(
                parcel_order_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                destination VARCHAR NOT NULL,
                receiver_name VARCHAR NOT NULL,
                parcel_name VARCHAR NOT NULL,
                location VARCHAR NOT NULL,
                status VARCHAR NOT NULL,
                deliver_status VARCHAR NULL, 
                FOREIGN KEY (user_id) REFERENCES users(user_id) 
                ON DELETE CASCADE ON UPDATE CASCADE)"""

        commands = (
            create_user_table,
            create_order_table
        )

        for command in commands:
            self.cur.execute(command)

    def drop_table(self, *table_names):
        '''Drops the tables created '''
        for table_name in table_names:
            drop_table = "DROP TABLE IF EXISTS {} CASCADE".format(table_name)
            self.cur.execute(drop_table)
