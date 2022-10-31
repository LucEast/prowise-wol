# WoL Prowise-Boards within IServ

This code interactively select all Prowise-Boards from the IServ `HOSTS` table and write their MAC and the broadcast address in a file.\
Then it creates/append a cronjob where the file with the MAC-addresses and bc-address will be called with the command `wakeonlan -f` every weekday at 4am.

## Script setup

```
# Install Requirements
pip3 install -r requirements.txt
```

The script can now simply be called like this:

```
python3 prowise-wol.py
```