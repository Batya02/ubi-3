import sqlite3
from random import randint

sql = sqlite3.connect("UBI.sqlite")
cursor = sql.cursor()

cursor.execute("SELECT created FROM phone_all_orders")

dates = cursor.fetchall()

for i, date in enumerate(dates):
    if date[0] == "None":
        print(date[0])
    else:
        old_date = date[0]
        date, time = old_date.split(" ")
        
        date_arr = date.split("-")
        date_arr.reverse()

        date = "-".join([d for d in date_arr])
        
        random_values = "".join([str(randint(0, x)) for x in range(1, 7)])

        print(date, f"{time}.{random_values}")