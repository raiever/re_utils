import crawl_rm 

import mysql.connector
from config import MYSQL

if __name__ == '__main__':
    url_list = crawl_rm.make_url_list(test=1, index_no=0, url_list=[])
    id_list_total = crawl_rm.get_id_list(url_list)

    
