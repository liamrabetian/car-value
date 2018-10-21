# codes for the database are here..
# in my case I used MySql.. you can choose any database you like!
import mysql.connector
from mysql.connector import errorcode


class DBHandler():
    def __init__(self, db_user, db_host, db_password, db_name):
        self.user = db_user
        self.host = db_host
        self.password = db_password
        self.name = db_name
        self.conn = None

    def open_connection(self):
        if self.conn is None:
            try:
                self.conn = mysql.connector.connect(user=self.user,
                                                    password=self.password,
                                                    host=self.host)

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                else:
                    print(err.msg)
            else:
                print("connected!!!!")
        try:
            mycursor = self.conn.cursor()
            mycursor.execute("CREATE DATABASE %s" % self.name)
            print('database %s created' % self.name)
        except mysql.connector.Error as err:
            print(err.msg)
        self.conn.close()

    def create_table(self):
        try:
            cnx = mysql.connector.connect(user=self.user,
                                          password=self.password,
                                          host=self.host,
                                          database=self.name)
            mycursor = cnx.cursor()
            mycursor.execute("CREATE TABLE car_details" +
                             "(date_of_manufacture VARCHAR(4),"
                             "brand VARCHAR(50),"
                             "model VARCHAR(50),"
                             "kilometers VARCHAR(60),"
                             "price VARCHAR(50))")
            print('table car_details created')
            mycursor.execute("ALTER TABLE car_details CONVERT TO " +
                             "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("character set altered")
        except mysql.connector.Error as err:
            print(err.msg)
        mycursor.close()
        cnx.close()

    def insert_to_database(self, my_list):
        cnx = mysql.connector.connect(user=self.user,
                                      password=self.password,
                                      host=self.host,
                                      database=self.name)
        mycursor = cnx.cursor()
        for row in range(len(my_list)):
            date_of_manufacture = my_list[row][0]
            brand = my_list[row][1]
            model = my_list[row][2]
            kilometers = my_list[row][3]
            price = my_list[row][4]
            vals = (date_of_manufacture, brand, model, kilometers, price)
            querry = "INSERT INTO car_details VALUES (%s, %s, %s, %s, %s)"
            mycursor.execute(querry, vals)
            cnx.commit()
            print(mycursor.rowcount, "record inserted.")
        mycursor.close()
        cnx.close()

    def query(self):
        my_list = list()
        cnx = mysql.connector.connect(user=self.user,
                                      password=self.password,
                                      host=self.host,
                                      database=self.name)
        mycursor = cnx.cursor()
        mycursor.execute("SELECT * FROM car_details")
        for (date, brand, model, kilometers, price) in mycursor:
            my_list.extend([(date, brand, model, kilometers, price)])
        return my_list
