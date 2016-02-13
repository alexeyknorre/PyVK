# -*- coding: utf-8 -*-

"""
Script for downloading and parsing public userdata from VK.com.
Make sure you have created your own application ID and access token before usage.

Alexey Knorre, 13.02.2016

V.2
*Changelog*

- refactoring, now it all in functions
- created cooldown for API, profiles are queried in chunks
- dicts inside list are now unzipped

*External dependencies*:
vkontakte (installing in cmd: "pip install vkontakte". Make sure
you are using Anaconda Python distribution, otherwise pip won't be working.)

*TODO*
- replace aliases in fields (f.e., 1 for Moscow or 2 for SPb in field "city")
by collecting such aliases and then quering VK API for their meaning (see 
VK API docs for exact query)

"""

import csv
import random
import time

import vkontakte

# Input variables

token = "YOUR_TOKEN"

basic_parameters=["uid","first_name","last_name"]
parameters = "nickname, sex, bdate, country, city, home_town, deactivated, has_mobile, site, education, universities, schools, status, occupation, relatives, relations, personal, career, military"
result_file = "./results.csv"

# Main commands 

# For particular accounts -- write down ids inside the list:
#ids = [1, 2, 3]

# For random accounts
ids = random_ids(500)


response = get_data(ids)
save_data(response)

### CODE


# Selecting random ids to parse
def random_ids(n):
    ids=[]
    for i in range(1,n+1):
        ids.append(random.randint(1,327633900))
    return ids

# Getting data from server. Chunk query with cooldown is implemented
def get_data(ids, parameters=parameters, threshold = 100, wait_time = 2):
    print "Quering VK API..."
    vk = vkontakte.API(token=token)
    str_ids = ""
    count = 0
    response = []
    if len(ids) > threshold:
        for i in ids:
            str_ids += str(i) + ","
            count += 1
            if count % threshold == 0 or count == len(ids):
    
                response += vk.users.get(user_ids = str_ids[:-1], fields = parameters)
                print "Got "+ str(count) + " profiles..."            
                time.sleep(wait_time)
                str_ids = ""
        return response
    else:
        return vk.users.get(user_ids = str(ids).strip('[]'), fields = parameters)

# Function for flattening nested dictionaries.
# isInstance checks whether the data structure of a particular type
# Heavy if-else usage here is because of complicated situations when there is 
# dictionary inside list inside dictionary

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        if v and isinstance(v, list):
            count = 1
            for i in v:
                new_key = parent_key + k + sep + str(count)
                if isinstance(i, dict):
                    items.extend(flatten_dict(i, new_key, sep=sep).items())
                else:
                    items.append((new_key, i))
                count += 1
        else:
            items.append((new_key, v))
    return dict(items)


# Constructing headers for CSV

def construct_header(response, basic_parameters=basic_parameters):
    header = []
    for person in response:
        header += list(set(flatten_dict(person)) - set(header))
    
    header = list(set(header) - set(basic_parameters))
    header = basic_parameters + sorted(header)
    
    return header

# Parsing data and saving in CSV file

def save_data(response, result_file=result_file):
    print "Preparing headers..."    
    fieldnames = construct_header(response)
    print "Saving data into CSV..."
    with open(result_file, "wb") as output:
        writer = csv.writer(output, quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(fieldnames)
        for person in response:
            person = flatten_dict(person)
            person_data=[]
            for item in fieldnames:
                if item in person:
                    if isinstance(person[item],basestring):
                        person_data.append(person[item].encode("utf-8"))
                    else:
                        person_data.append(str(person[item]))
                else:
                    person_data.append('')
            writer.writerow(person_data)
    print "Successfully saved."
