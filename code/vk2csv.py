# -*- coding: utf-8 -*-


"""
Script for downloading, parsing and saving to CSV public user data from VK.com.


"""


import csv
import random
import requests
import ast

# Input variables

basic_parameters=["uid","first_name","last_name"]
result_file = "./results/profiles.csv"

response_file = "./results/response.txt"

### CODE

# Main function 

def vk2csv(parameters, number_of_ids):
	ids = random_ids(number_of_ids)
	get_data(ids,parameters)
	process_data()

# Selecting random ids to parse



def random_ids(n):
    ids=[]
    for i in range(1,n+1):
        ids.append(random.randint(1,327633900))
    #removing duplicates
    ids=list(set(ids))
    return ids

# Getting data from server. Chunk query with cooldown and repeat in case of SSL fail are implemented
def get_data(ids, parameters, threshold = 400, count_friends=False):
         
    def query(response):
        try:
            response = requests.get("https://api.vk.com/method/users.get?user_ids="+str_ids[:-1]+
                                    "&fields="+parameters).json()
        except:
            pass#print("Got error on " + str(count) + " profiles, repeating...")
            #response = query(response)
        return response
        
    print("Quering VK API...")
    str_ids = ""
    count = 0
    response = []
        
    for i in ids:
        str_ids += str(i) + ","
        count += 1
        if count % threshold == 0 or count == len(ids):
            response = query(response)
            save_response(response)
            str_ids = ""
            print("Got "+ str(count) + " profiles..." )
            response = []
    print("Data acquired.")

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
        for s in response["response"]:
            s = str(s).encode('utf-8') + str("\n").encode("utf-8")
            f.write(str(s))
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


