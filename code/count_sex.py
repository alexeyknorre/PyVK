# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 13:12:34 2017

@author: HOME
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 12:52:59 2017

@author: HOME
"""

import pandas as pd
import numpy as np
import matplotlib.pylab as plt

profiles_csv = "../results/profiles_friends.csv"
friends_folder = "../results/friends/"
count_sex_csv = "../results/sex.csv"
mean_fill = "../results/mean_fill.csv"

friends_fields = pd.read_csv(mean_fill)
friends_fields.number_of_friends



profiles = pd.read_csv(profiles_csv)

#count_sex

#обращение к столбцу
profiles.number_of_friends
profiles["sex"].value_counts()

profiles.personal_political
profiles["personal_political"].value_counts()

profiles.groupby('personal_political').sum()
#profiles.groupby(['sex']).get_group('personal_political')

fig = plt.figure()
ax = plt.subplot(111)
friends_fields.plot(x='number_of_friends',y='mean_fill',ax=ax, kind='scatter')
ax.set_xlim(0,1000)
plt.show()

"""
#поиск id по значению
#profiles.loc[profiles['sex'] == -1]
"""





