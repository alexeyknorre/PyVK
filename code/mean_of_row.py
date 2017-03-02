# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 13:31:55 2017

@author: HOME
"""

import pandas as pd
import numpy as np

profiles_csv = "../results/profiles_friends.csv"
friends_folder = "../results/friends/"
mean_row_csv = "../results/mean_row.csv"

profiles = pd.read_csv(profiles_csv)
