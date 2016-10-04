# -*- coding: utf-8 -*-
"""
Created on Mon Jul 04 13:44:10 2016

@author: Alexey
"""

import pandas as pd
import operator
from transliterate import translit, get_available_language_codes
import re

csv = '../results/profiles.csv'


## test
# csv = '../tests/profiles.csv'
# PAJEK_EDGELIST = '../tests/test_edgelist.net'
# field = "music"
# minimum_occurences = 25

USELESS_WORDS = u'разная|разное|разные|по настроению|под настроение|меломанка|меломан|всякая|все|всякая|нету|зависит от настроения|слушаю всё|всё|нет|_|'


def read_data(fields, csv=csv):

    columns = ["uid"] + fields.split(',')
    df = pd.read_csv(csv, na_values=["[]"],
                     usecols=columns, encoding="utf-8")
    fields = fields.split(',')
    query = '+", " + '.join('df["{0}"]'.format(field) for field in fields)
    exec("df['field'] = " + query)

    df['field'] = df['field'].str.lower()
    df = df.dropna(subset=['field'])
    return df


def clean_data(df):
    # Remove weird characters
    df = df.str.replace('[!_@#¶()]', '', case=False)
    # Remove useless words
    df = df.str.replace(USELESS_WORDS, '')
    # Remove stacks of characters like 00000000
    return df.str.replace(r'(.)\1{4,}', '')


def get_sorted_dict(df):
    music_freq = {}
    for field in df:
        elements = field.split(",")
        for element in elements:
            element = element.strip()
            if element in music_freq:
                music_freq[element] += 1
            else:
                music_freq[element] = 1
    return music_freq, sorted(music_freq.items(), key=operator.itemgetter(1), reverse=True)


def show_sorted_dict(sorted_dict, elements=50):
    for i in range(elements):
        print sorted_dict[i][0], sorted_dict[i][1]


def get_arcs(df, vertices):
    print "Getting arcs..."
    arcs = {}
    c = 0
    for field in df:
        c += 1
        if c % 1000 == 0:
            print c
        elements = []
        elements_raw = field.split(",")
        for element in elements_raw:
            elements.append(element.strip())
        for element in elements:
            if element not in vertices:
                continue
            other_elements = elements
            other_elements.remove(element)
            vertice_from = vertices.index(element)
            if other_elements != None:
                for other_element in other_elements:
                    if other_element not in vertices:
                        continue
                    vertice_to = vertices.index(other_element)
                    # Add 1 so arcs index starts with 1
                    arc = (vertice_from + 1, vertice_to + 1)
                    if arc in arcs:
                        arcs[arc] += 1
                    else:
                        arcs[arc] = 1
    return arcs


def get_vertices(sorted_dict, minimum_occurences):
    print "Getting vertices..."
    vertices = []
    for i in sorted_dict:
        if i[1] >= minimum_occurences and len(i[0]) > 2:
            vertices.append(i[0])
    return vertices


def save_edgelist(vertices, arcs, fields):
    print "Saving..."
    PAJEK_EDGELIST = '../results/'+fields+'.net'
    with open(PAJEK_EDGELIST, 'wb') as f:
        f.write("*Vertices " + str(len(vertices)) + "\r\n")
        c = 0
        for i in vertices:
            c += 1
            # Transliterate for Pajek
            i = translit(i, "ru", reversed=True)
            # Leave only literals and _ for Pajek
            i = re.sub("[\W_]+", "_", i)
            f.write(str(c) + ' "' + str(i.encode("utf-8")) + '"\r\n')
        f.write("*Arcs \r\n")
        for i in arcs.items():
            f.write(str(i[0][0]) + " " + str(i[0][1]) + " " + str(i[1]) + "\r\n")


def csv2pajek(fields, minimum_occurences):
    df = read_data(fields)
    df_clean = clean_data(df['field'])
    music_freq, srt = get_sorted_dict(df_clean)[0], get_sorted_dict(df_clean)[1]
    v = get_vertices(srt, minimum_occurences)
    arcs = get_arcs(df_clean, v)
    save_edgelist(v, arcs, fields)

