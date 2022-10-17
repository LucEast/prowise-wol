import os
import sys

bc_address = "10.255.255.255"

try:
    import psycopg2
except:
    print('Install requirements (psycopg2)')
    quit()

class Database:
    def __init__(self) -> None:
        pass

    def get_mac(self):
        try:
            conn = psycopg2.connect ("dbname=iserv user=postgres")
            cur = conn.cursor()
            cur.execute("SELECT h.mac FROM HOSTS h LEFT JOIN host_tag_assign hta ON (h.id = hta.host) LEFT JOIN host_tag ht ON (hta.tag = ht.id) WHERE ht.name ~ 'ProwiseBoard' AND mac IS NOT NULL;")
            rows = cur.fetchall()

            with open(r'/group/domain.admins/Files/prowise.wol', 'w') as f:
                for row in rows:
                    f.write("%s\n" % row + bc_address)
                print("Done!")