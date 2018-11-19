import crawl_rm, update_price, queries

import mysql.connector
from config import MYSQL
from date import today

if __name__ == '__main__':
    today_date = today()

    url_list = crawl_rm.make_url_list(test=0, index_no=0, url_list=[])
    id_list_total = crawl_rm.get_id_list(url_list)

    cnx = mysql.connector.connect(**MYSQL)
    cursor = cnx.cursor()

    update_price.update_column(cursor=cursor, today_date=today_date)
    existed_id_list = update_price.read_property_id(cursor)

    for i in id_list_total:
        if not str(i) in existed_id_list:
            specific_link = crawl_rm.make_property_link(i)
            infos = crawl_rm.get_info(specific_link)
            data = (i, str(infos['title']), str(infos['address']), infos['price'])
            query = queries.insert_info_query(today_date)
            print(data)
            cursor.execute(query, data)
        elif str(i) in existed_id_list:
            specific_link = crawl_rm.make_property_link(i)
            updated = crawl_rm.get_price(specific_link)
            data = (today_date, updated, i)
            query = queries.update_price_query(data)
            print(query)
            cursor.execute(query)
    cnx.commit()




