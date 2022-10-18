from logging import exception
import os
import sys
import re

from inquirer import Path

try:
    import psycopg2
except:
    print('Install requirements with "pip3 install -r requirements.txt"')
    quit()

try:
    import inquirer
    from inquirer import errors
except:
    print('Install requirements with "pip3 install -r requirements.txt"')
    quit()


def ip_validation(bc_address, current):
    if not re.search(r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$", current):
        raise errors.ValidationError('', reason="Your BC-Address isn't valid!")
    return True


questions = [inquirer.Text('bc-address',
                message="Please enter the BC-Address",
                default="10.255.255.255",
                validate=ip_validation                 
                ),
            inquirer.Path('file',
                message="Where should the Data be written to?",
                path_type=Path.FILE,
                default="/group/domain.admins/Files/prowise.wol"),
            inquirer.Text('hosttag',
                message="Please enter the Hosttag",
                default="Prowise",
                )
]


answers = inquirer.prompt(questions)
bc_address = answers['bc-address']
file = answers['file']
hosttag = answers['hosttag']

class Database:
    def __init__(self) -> None:
        pass

    def get_mac(self, filepath, hosttag):
        try:
            conn = psycopg2.connect("dbname=iserv user=postgres")
            cur = conn.cursor()
            cur.execute("SELECT h.mac FROM HOSTS h LEFT JOIN host_tag_assign hta ON (h.id = hta.host) LEFT JOIN host_tag ht ON (hta.tag = ht.id) WHERE ht.name ~ %s AND mac IS NOT NULL;", [hosttag])
            rows = cur.fetchall()

            with open(filepath, 'w+') as f:
                for row in rows:
                    f.write("%s\t" % row + "%s\n" % bc_address)
                print("Done!")

        except exception as E:
            print(E)


if __name__ == "__main__":
    db = Database()
    db.get_mac(file, hosttag)
