# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 17:34:29 2016

@author: f
"""
import os
import vk2csv
import friends2csv
import friends_of_friends

for folder in ["../results","../results/friends"]:
    if not os.path.exists(folder):
        os.makedirs(folder)


#vk2csv.vk2csv(number_of_ids = 10000)
#friends2csv.add_friends_to_csv()
friends_of_friends.get_numbers_of_friends()

# Count friends for user's friends


"""
import ast

with open('../results/ids.txt', 'r') as txt:
    ids_to_load = ast.literal_eval(txt.read())

vk2csv.vk2csv(number_of_ids = ids_to_load)
"""