import mysql.connector
from config import MYSQL
from date import today

from crawl_rightmove import make_url, get_price

def read_property_id():
    id_list = []
    cnx = mysql.connector.connect(**MYSQL)
    cursor = cnx.cursor()
    query = ("SELECT property_id "
             "FROM property_list")
    cursor.execute(query)
    [id_list.append('%d' %i) for i in cursor]
    print(id_list)
    cursor.close()
    cnx.close()
    return id_list

def update_price(id_list):
    cnx = mysql.connector.connect(**MYSQL)
    cursor = cnx.cursor()
    today_date = today()
    new_column = '%s' % today_date
    alter_query = ("ALTER TABLE property_list "
                   "ADD %s INT(11);" % new_column)
    try:
        cursor.execute(alter_query)
    except Exception as e:
        print(e)
    for property_id in id_list:
        specific_link = "https://www.rightmove.co.uk/property-for-sale/property-%d.html" % int(property_id)
        print(specific_link)
        price = get_price(specific_link)
        data = (new_column, price, int(property_id))
        insert_query = ("UPDATE property_list "
                        "SET %s = %d "
                        "WHERE property_id = %d;" % data)
        print(insert_query)
        cursor.execute(insert_query)
    cnx.commit()
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    id_list = read_property_id()
    print(len(id_list))

    update_price(id_list)
