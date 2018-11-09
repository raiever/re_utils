import mysql.connector
from config import MYSQL
from date import today

from crawl_rightmove import make_url

if __name__ == '__main__':
    cnx = mysql.connector.connect(**MYSQL)
    cursor = cnx.cursor()

    query_1 = ("SELECT property_id "
               "FROM property_list")
    
    cursor.execute(query_1)
    for i in cursor:
        print(i)
