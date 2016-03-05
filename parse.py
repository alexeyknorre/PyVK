# -*- coding: utf-8 -*-

"""
Script for downloading and parsing public userdata from VK.com.
Make sure you have created your own application ID and access token before usage.

Alexey Knorre, 5.03.2016

V.3
*Changelog*

- refactoring, now it all in functions
- profiles are queried in chunks
- dicts inside list are now unzipped
- can retrieve friends count, but it is very slow

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
import ast

import vkontakte

# Input variables

token = "YOUR_TOKEN"

basic_parameters=["uid","first_name","last_name"]
parameters = "nickname, sex, bdate, country, city, home_town, deactivated, last_seen, has_mobile, site, education, universities, schools, status, occupation, relatives, relations, personal, career, military, contacts, relation, connections, exports, wall_comments, activities, interests, music, movies, tv, books, games, about, quotes"
result_file = "C:/Users/Alexey/Documents/VK analysis/results.csv"

response_file = "C:/Users/Alexey/Documents/VK analysis/response.txt"

### CODE


# Selecting random ids to parse
def random_ids(n):
    ids=[]
    for i in range(1,n+1):
        ids.append(random.randint(1,327633900))
    #removing duplicates
    ids=list(set(ids))
    return ids

# Getting data from server. Chunk query with cooldown and repeat in case of SSL fail are implemented
def get_data(ids, parameters=parameters, threshold = 200, count_friends=False):
         
    def query(response):
        try:
            response = vk.users.get(user_ids = str_ids[:-1], fields = parameters, timeout=3)           
        except:
            print "Got SSL error on " + str(count) + " profiles, repeating..."
            response = query(response)
        return response
    
    def query_friends(response):
        query_moment = time.time()                    
        try:
            count = 0
            for person in response:
                count +=1
                if "deactivated" not in person:
                    while ( time.time() - query_moment ) < 0.333:
                        time.sleep(0.02)
                    friends = vk.friends.get(user_id=person["uid"], offset=0, timeout=2)
                    query_moment = time.time()
                    person["friends_count"] = len(friends)
                    print "Got friends of ", count, " from ", len(response)

        except:
            response =  query_friends(response)
        return response
        
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
                response = query(response)
                if count_friends:
                    print "Querying number of friends..."
                    response = query_friends(response)
                save_response(response)
                str_ids = ""
                print "Got "+ str(count) + " profiles..." 
                response = []
    else:
        response = vk.users.get(user_ids = str(ids).strip('[]'), fields = parameters, timeout = 3)
        save_response(response)
        #return response
    print "Data acquired."

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

def save_response(response, output=response_file):
    with open(output, 'a') as f:
        for s in response:
            f.write(str(s) + '\n')
    #with open(output, "a") as output:
    #    output.write(response)

def process_data(response_file=response_file, result_file=result_file):
    print "Loading response into memory..."
    response = []
    with open(response_file, 'r') as f:
        for line in f:
            response.append(ast.literal_eval(line.rstrip('\n')))
    #response = ast.literal_eval(response)
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
# Main commands 

# For particular accounts -- write down ids inside the list:
#ids = [593515,1]

# For random accounts

start = time.strftime("%d %b %H:%M:%S", time.localtime())
ids = random_ids(1000000)
get_data(ids)
process_data()
end = time.strftime("%d %b %H:%M:%S", time.localtime())
print "Start", start
print "End", end
