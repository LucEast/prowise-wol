import os
import sys
import re


try:
    import psycopg2
except:
    print('Install requirements with "pip3 install -r requirements.txt"')
    quit()

try:
    import inquirer
    from inquirer import errors
    from inquirer import Path
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
                f.close()
                print("Done!")

        except Exception as E:
            print(E)

class cron:
    def __init__(self) -> None:
        pass

    def krz(self, filepath):
        if not os.path.exists(filepath):
            try:
                with open(filepath, 'w+') as f:
                    f.write("# Cron Jobs for KRZ\n")
                    f.write("\nSHELL=/bin/sh\n")
                    f.write("PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin\n")    
                    f.write("\n# m h d m dow   user    command\n")
                    f.write("\nWake Prowise Boards at 4am\n")
                    f.write("\n0 4 * * 1-5 root wakeonlan -f {}\n".format(file))
                    f.write(" ")
                    f.close()
                    print("Created new Cronfile")
            
            except Exception as E:
                print(E)
        else:
            with open(filepath, 'a') as f:
                f.write("Wake Prowise Boards at 4am\n")
                f.write("\n0 4 * * 1-5 root wakeonlan -f {}\n".format(file))
                f.write(" ")
                f.close()
                print("Appended to existing Cronfile")


if __name__ == "__main__":
    db = Database()
    db.get_mac(file, hosttag)
    cr = cron()
    cr.krz("/etc/cron.d/krz")