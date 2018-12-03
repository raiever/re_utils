from date import today

today_date = today()

def insert_info_query(today_date):
    insert_info = ("INSERT INTO property_list "
                   "(property_id, title, address, %s) " % today_date) + ("VALUES (%s, %s, %s, %s);")
    return insert_info

def update_price_query(data):
    try:
        update_price = ("UPDATE property_list "
                        "SET %s = %d "
                        "WHERE property_id = %d;" % data) # data = price_column, price, id
    except:
        print("update_error: ", data)
        pass
    return update_price