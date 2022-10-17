from logging import exception
import os
import sys
import re
from tkinter import E

try:
    import psycopg2
except:
    print('Install requirements (psycopg2)')
    quit()

try:
    import inquirer
    from inquirer.themes import GreenPassion
    from inquirer import errors
except:
    print('Install requirements with "pip3 install -r requirements.txt')
    quit()


def ip_validation(bc_address, current):
    if not re.search(r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$", current):
        raise errors.ValidationError('', reason="Your BC-Address isn't valid!")
    return True


questions = [
    inquirer.Text('bc-address',
                  message="Please enter the BC-Address",
                  validate=ip_validation,
                  default="10.255.255.255",
                  )
]


bc_address = inquirer.prompt(questions)['bc-address']


class Database:
    def __init__(self) -> None:
        pass

    def get_mac(self, filepath):
        try:
            conn = psycopg2.connect("dbname=iserv user=postgres")
            cur = conn.cursor()
            cur.execute("SELECT h.mac FROM HOSTS h LEFT JOIN host_tag_assign hta ON (h.id = hta.host) LEFT JOIN host_tag ht ON (hta.tag = ht.id) WHERE ht.name ~ 'ProwiseBoard' AND mac IS NOT NULL;")
            rows = cur.fetchall()

            with open(filepath, 'w+') as f:
                for row in rows:
                    f.write("%s\n" % row + bc_address)
                print("Done!")

        except exception as E:
            print(E)


if __name__ == "__main__":
    db = Database()
    db.get_mac("/group/domain.admins/Files/prowise.wol")
