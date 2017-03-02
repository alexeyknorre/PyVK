# -*- coding: utf-8 -*-


"""
Script for downloading, parsing and saving to CSV public user data from VK.com.


"""
import os
import csv
import random
import requests
import ast

# Input variables

basic_parameters = ["uid", "first_name", "last_name"]
result_file = "../results/profiles.csv"

response_file = "../results/response.txt"

#parameters = ""
parameters = "sex, bdate, country, city, deactivated, last_seen, has_mobile, site, education, universities, schools, status, relatives, relations, personal, career, contacts, exports, relation, connections, exports, wall_comments, activities, interests, music, movies, tv, books, games, about, quotes, has_photo, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, followers_count"


### CODE

# Main functions

def vk2csv(number_of_ids, result_file=result_file, parameters = parameters,
           response_file=response_file, delete_response=False):
    if isinstance(number_of_ids, list):
        ids = number_of_ids
    else:
        ids = random_ids(number_of_ids)
        with open("../results/ids.txt", 'w') as f:
            f.write(str(ids))
            
        
    get_data(ids, parameters, response_file)
    process_data(result_file, response_file, delete_response)


# Selecting random ids to parse

def random_ids(n):
    ids = []
    for i in range(1, n + 1):
        ids.append(random.randint(1, 327633900))
    # removing duplicates
    ids = list(set(ids))
    return ids


# Getting data from server. Chunk query with cooldown and repeat in case of SSL fail are implemented
def get_data(ids, parameters, response_file, threshold=200):
    def query(response):
        try:
            response = requests.get("https://api.vk.com/method/users.get?user_ids=" + str_ids[:-1] +
                                    "&fields=" + parameters).json()
        except:
            print("Got error on " + str(count) + " profiles, repeating...")
            response = query(response)
        return response

    #print("Quering VK API...")
    str_ids = ""
    count = 0
    response = []

    for i in ids:
        str_ids += str(i) + ","
        count += 1
        if count % threshold == 0 or count == len(ids):
            response = query(response)
            save_response(response, response_file)
            str_ids = ""
            print("Got " + str(count) + " profiles...")
            response = []
    #print("Data acquired.")

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

def save_response(response,response_file):
    with open(response_file, 'a') as f:
        for s in response["response"]:
            s = str(s).encode('utf-8') + str("\n").encode("utf-8")
            f.write(str(s))
            # with open(output, "a") as output:
            #    output.write(response)


def process_data(result_file, response_file, delete_response):
    #print "Loading response into memory..."
    response = []
    with open(response_file, 'r') as f:
        for line in f:
            response.append(ast.literal_eval(line.rstrip('\n')))
    # response = ast.literal_eval(response)
    #print "Preparing headers..."
    fieldnames = construct_header(response)
    #print "Saving data into CSV..."
    with open(result_file, "wb") as output:
        writer = csv.writer(output, quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(fieldnames)
        for person in response:
            person = flatten_dict(person)
            person_data = []
            for item in fieldnames:
                if item in person:
                    if isinstance(person[item], basestring):
                        person_data.append(person[item].encode("utf-8"))
                    else:
                        person_data.append(str(person[item]))
                else:
                    person_data.append('')
            writer.writerow(person_data)
    if delete_response:
        os.remove(response_file)
    #print "Successfully saved."
