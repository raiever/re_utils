from date import today

today_date = today()

insert_info = ("INSERT INTO property_list "
               "(property_id, title, address, %s)" # % today_date
               "VALUES (%s, %s, %s, %s)")