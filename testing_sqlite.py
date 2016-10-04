import requests
import sqlite3

basic_parameters = 'uid,first_name,last_name,deactivated,hidden,deleted'
parameters="bdate,personal,music"

response = requests.get(
    "https://api.vk.com/method/users.get?user_ids=1,2,3,4,5,6,7,8,9,10,777&fields={0}".format(parameters)).json()

db_columns = basic_parameters+','+parameters
db_columns = db_columns.split(',')


db = sqlite3.connect('vk_profiles.db')
c = db.cursor()

# c.execute('''create table profiles
# (uid int primary key,
# first_name text,
# last_name text,
# deactivated int,
# hidden int,
# deleted int,
# bdate text,
# personal text,
# music text)''')


query = "insert into profiles ({0}) values ({1})"

for profile in response['response']:
    query = "insert into profiles ({0}) values ({1})"
    values = [str(i) for i in profile.values()]
    query = query.format(",".join(profile.keys()), str("?," * len(profile.keys()))[:-1])
    print query
    for a, b in profile.iteritems():
        print a, b
    c = db.cursor()
    c.execute(query,values)
    c.close()
