from models import DBHandler
from car_price import CarPrice


my_list = list()
my_list = CarPrice.souping_data('https://bama.ir/car')

'''change db_user with database user and host with your desirable host .
your_password with database password and choose a desirable db name'''

conn = DBHandler('db_user', 'host', 'your_password', 'choose_a_db_name')
conn.open_connection()
conn.create_table()
conn.insert_to_database(my_list)
li = conn.query()
new_data = [['1397', 'مزدا', '3 جدید صندوق دار', 'کارکرد صفر کیلومتر']]
car_value = CarPrice.predict_car_price(li, new_data)
print(car_value)
