# -*- coding: utf-8 -*-
"""

Pandas analysis routine for VK data

*External dependencies*:
pandas >= 0.17 (check in cmd: "pip install pandas --upgrade". Make sure
you are using Anaconda Python distribution, otherwise pip won't be working.)
"""
import pandas as pd
import numpy as np
import matplotlib

import matplotlib.pyplot as plt


# Vars

matplotlib.rc('font', family='Verdana')
matplotlib.rcParams.update({'font.size': 12})

columns = ["uid", "first_name", "last_name", "bdate", "sex", "city",
                "deactivated", "personal_alcohol",
                "personal_life_main", "personal_religion", "personal_smoking", 
                "personal_political", "personal_inspired_by",
                "personal_people_main","career_1_position", "career_1_company",
                "occupation_name", "occupation_type", "relatives_1_type",
                "status", 
                "status_audio_artist", "universities_1_name", 
                "universities_1_faculty_name", "universities_1_graduation",
                "schools_1_year_graduated", "about", "activities", "books",
                "country", "facebook", "games", "instagram", "interests", 
                "last_seen_time", "mobile_phone", "movies", "music",
                "personallangs_1", "personallangs_2", "personallangs_3", 
                "quotes", "relation", "relation_partner_id", "site", "tv",
                "twitter", "skype", "livejournal", "wall_comments"]

csv = 'C:/Users/Alexey/Documents/VK analysis/results.csv'
freqs = "C:/Users/Alexey/Documents/VK analysis/freqs.txt"
results = 'C:/Users/Alexey/Documents/VK analysis/pics/'
## Preprocessing

# Read data

df = pd.read_csv(csv, nrows= 1000000, na_values = ["[]"], 
                 usecols = columns, encoding="utf-8")

# Fill missings 

df["deactivated"].fillna("ok", inplace=True)

# Lowercasing

for i in ["personal_religion", "personal_inspired_by", "career_1_position",
          "career_1_company", "activities", "books", "games", "interests",
          "movies", "music", "quotes", "site", "tv", "status"]:
    df[i] = df[i].str.lower()

# Labeling

df["sex"] = df["sex"].replace([0,1,2], [None,"Female", "Male"])
df.city = df.city.replace([0,1,2,314,49,60,183,99,282,280],[None,"Moscow",
"Saint-Petersburg", "Kiev", "Ekaterinburg", "Kazan'", "Novosibirsk", "Almaty", "Minsk", "Kharkiv"])
df["personal_smoking"] = df["personal_smoking"].replace([1,2,3,4,5],
                                                        ["Резко негативное",
                                                         "Негативное",
                                                         "Нейтральное",
                                                         "Компромиссное",
                                                         "Положительное"])
                                                         
df["personal_alcohol"] = df["personal_alcohol"].replace([1,2,3,4,5],
                                                        ["Резко негативное",
                                                         "Негативное",
                                                         "Нейтральное",
                                                         "Компромиссное",
                                                         "Положительное"])                                                         


df.relation = df.relation.replace([1,2,3,4,5,6,7,0],["Не женат/не замужем", 
                                  "Есть друг/подруга", "Помолвлен(а)", 
                                  "Женат/замужем", "Всё сложно", 
                                  "В активном поиске", "Влюблен(а)", None])
                                  
df.personal_political = df.personal_political.replace([1,2,3,4,5,6,7,8,9],
                                                      ["Коммунистические",
                                                       "Социалистические",
                                                       "Умеренные",
                                                       "Либеральные",
                                                       "Консервативные",
                                                       "Монархические",
                                                       "Ультраконсервативные",
                                                       "Индиффирентные",
                                                       "Либертарианские"])
                                  
df.personal_people_main = df.personal_people_main.replace([1,2,3,4,5,6],
                                                          ["Ум и креативность",
                                                          "Доброта и честность",
                                                          "Красота и здоровье",
                                                          "Власть и богатство",
                                                          "Смелость и упорство",
                                                          "Юмор и жизнелюбие"])
                                                          
df.personal_life_main = df.personal_life_main.replace([1,2,3,4,5,6,7,8],
                                                      ["Семья и дети",
                                                       "Карьера и деньги",
                                                       "Развлечения и отдых",
                                                       "Наука и исследования",
                                                       "Совершенствование мира",
                                                       "Саморазвитие",
                                                       "Красота и искусство",
                                                       "Слава и влияние"])                                                          

# Reconstruct birthyear
print "Всего дат рождения:", df.bdate.count()

df["byear"] = df.bdate[df.bdate.str.len()>5].str[-4:]
df["byear"] = pd.to_numeric(df.byear)

columns.append("byear")

print "Из них аккаунтов, указавших год рождения:", df.byear.count()

#df.bday = df.bdate[df.bdate.str.len()<6]
#print "Аккаунтов с датой, но без года рождения: ", df.bday.count()

# Black voodoo magic, god forgive me
#df["1"] = df.bdate[df.bdate.str.len()>5].str[:-5]
#df["2"] = df.bdate[df.bdate.str.len()<6]
#df["3"] = df["1"].map(str) + df["2"].map(str)
#df["3"] = df["3"].map(lambda x: x.lstrip('nan').rstrip('nan'))
##df.bday = df["3"].replace("",np.nan)
#
#df = df.drop('1', 1)
#df = df.drop('2', 1)
#df = df.drop('3', 1)

#print "Всего дат (день, месяц) рождения:", df.bday.count()

# TODO: complete converting dbay to datetime format

## Analysis

# Births

# Births
df["byear"] = df["byear"][df["byear"] > 1900]
plot_byear = df[df.deactivated == "ok"].byear.hist(bins=100, figsize=(20,10))
plot_byear.set_xlabel(u"Пользователей")
plot_byear.set_title(u"Возрастное распределение")
plot_byear.set_xlabel(u"Год рождения")
plot_byear.figure.savefig('C:/Users/Alexey/Documents/VK analysis/plot_byear.png', dpi = 200)


# UIDs and deactivation

print "Всего аккаунтов: ", len(df)

deact = df['deactivated'].value_counts()
print "Активные аккаунты: ", deact["ok"],"|", int(deact["ok"]/float(len(df))*100), "%"
print "Удалённые аккаунты: ", deact["deleted"],"|", int(deact["deleted"]/float(len(df))*100), "%"
print "Забаненные аккаунты: ", deact["banned"],"|", int(deact["banned"]/float(len(df))*100), "%"

temp_df = pd.DataFrame()
temp_df["uid"] = df['uid']
temp_df["deactivated"] = df["deactivated"]
temp_df = pd.get_dummies(temp_df)

sub_df = temp_df.groupby(pd.cut(temp_df["uid"], np.arange(0, 330000000, 2500000))).sum()
sub_df = sub_df.drop('uid', 1)
sub_plot = sub_df.plot(kind='bar',stacked=True, figsize=(20,10), title=u"Распределение деактивированных аккаунтов",
            sort_columns=True, use_index=False, width=1, xticks=[100,200,300])
sub_plot.legend([u"Забаненные",u"Удалённые",u"Активные"], loc=9,ncol=4)

n = 10

ticks = sub_plot.xaxis.get_ticklocs()
ticklabels = [l.get_text() for l in sub_plot.xaxis.get_ticklabels()]
lst = []
for i in ticklabels:
    lst.append(unicode(int(int(i)*2.5))+u" млн.")
ticklabels = lst
sub_plot.xaxis.set_ticks(ticks[::n])
sub_plot.xaxis.set_ticklabels(ticklabels[::n])

sub_plot.figure.show()
plt.savefig('C:/Users/Alexey/Documents/VK analysis/plot_users_deactivated.png', dpi = 200)

#temp_df.groupby(pd.cut(temp_df["uid"], np.arange(0, 327623848, 10000000)).sum())

#
#for i in ["ok", "deleted", "banned"]:
#    plot_users  = temp_df[temp_df["deactivated"]==i].hist(bins=33, figsize=(20,10))
##    plot_users.set_xlabel(u"Распределение ID")
##    plot_users.set_title(i)
#    plt.savefig('C:/Users/Alexey/Documents/VK analysis/plot_users_'+i+'.png', dpi = 200)
#

# DROP DEACTIVATED AND BANNED

df = df[df.deactivated == "ok"]

# Частотки по всем

with open(freqs, 'w') as f:
    for i in columns:
        f.write(str("##### "+ i + "\n" + str(df[i].value_counts().head(10)) + "\n\n\n"))


columns.remove("uid")
columns.remove("first_name")
columns.remove("last_name")
columns.remove("deactivated")
columns.remove("wall_comments")
columns.remove("last_seen_time")
columns.remove("country")


# Заполненность профилей вообще

filling = [len(df) - df[item].isnull().sum() for item in columns ]
perc = [item / float(len(df)) * 100 for item in filling]
fill_df = pd.DataFrame(perc, index=columns, columns=["Percentage"])
fill_df.sort_values("Percentage").plot(kind="barh", figsize=(10,10))

# Заполненность по годам

#temp_df = df
##temp_df = df.drop(['uid','first_name', "last_name", "deactivated",
##                   "wall_comments", "last_seen_time", "country"], axis=1)
#
#temp_df["fill_count"] = len(temp_df.columns) - temp_df.isnull().sum(axis=1)
#
#fill_years = range(1900,2002)
#for i in fill_years:
#    print i ,temp_df["fill_count"][temp_df["byear"] == i].quantile([0.25,0.5,0.75])
#temp2_df = pd.DataFrame(index=fill_years)
#
#for i in temp2_df.index:
#    temp2_df["q1"][i] = temp_df["fill_count"][temp_df["byear"] == i].quantile(0.25)
#    temp2_df["median"][i] = temp_df["fill_count"][temp_df["byear"] == i].quantile(0.5)
#    temp2_df["q3"][i] = temp_df["fill_count"][temp_df["byear"] == i].quantile(0.75)

# Заполненность профилей по полу

male_filling = [len(df[df.sex == "Male"]) - df[item][df.sex == "Male"].isnull().sum() for item in columns ]
sex_fill = np.array([male_filling]).transpose()
sex_fill_df=pd.DataFrame(sex_fill, columns=["Male"], index=columns).sort_values("Male")
columns = list(reversed(list(sex_fill_df.index)))

male_filling = [len(df[df.sex == "Male"]) - df[item][df.sex == "Male"].isnull().sum() for item in columns[:len(columns)/2+1] ]
male_perc = [item / float(len(df[df.sex == "Male"])) * 100 for item in male_filling]
female_filling = [len(df[df.sex == "Female"]) - df[item][df.sex == "Female"].isnull().sum() for item in columns[:len(columns)/2+1] ]
female_perc = [item / float(len(df[df.sex == "Female"])) * 100 for item in female_filling]
sex_fill = np.array([male_perc, female_perc]).transpose()
sex_fill_df=pd.DataFrame(sex_fill, columns=["Male","Female"], index=columns[:len(columns)/2+1])
plot_sex_fill = sex_fill_df.sort_values("Male").plot(kind="barh",figsize=(20,10))
plot_sex_fill.set_xlabel(u"Процентов пользователей, заполнивших полей")
plot_sex_fill.set_title(u"Заполнение полей")
plot_sex_fill.set_ylabel(u"Поле")
plot_sex_fill.figure.savefig('C:/Users/Alexey/Documents/VK analysis/plot_sex_fill-1.png', dpi = 200)

male_filling = [len(df[df.sex == "Male"]) - df[item][df.sex == "Male"].isnull().sum() for item in columns[len(columns)/2:] ]
male_perc = [item / float(len(df[df.sex == "Male"])) * 100 for item in male_filling]
female_filling = [len(df[df.sex == "Female"]) - df[item][df.sex == "Female"].isnull().sum() for item in columns[len(columns)/2:] ]
female_perc = [item / float(len(df[df.sex == "Female"])) * 100 for item in female_filling]
sex_fill = np.array([male_perc, female_perc]).transpose()
sex_fill_df=pd.DataFrame(sex_fill, columns=["Male","Female"], index=columns[len(columns)/2:])
plot_sex_fill = sex_fill_df.sort_values("Male").plot(kind="barh",figsize=(20,10))
plot_sex_fill.set_xlabel(u"Процентов пользователей, заполнивших полей")
plot_sex_fill.set_title(u"Заполнение полей")
plot_sex_fill.set_ylabel(u"Поле")
plot_sex_fill.figure.savefig('C:/Users/Alexey/Documents/VK analysis/plot_sex_fill-2.png', dpi = 200)


# Заполняемость по семейному положению

temp_df = df
temp_df["fill_count"] = len(temp_df.columns) - temp_df.isnull().sum(axis=1)
temp_df["relation"] = temp_df["relation"].replace([-99.0],[None])
plot_fill_relation = temp_df.boxplot("fill_count", by='relation', figsize=(20,10))
plot_fill_relation.set_xlabel(u"Семейное положение")
plot_fill_relation.set_title(u"Как заполняют профиль люди с разным СП")
plot_fill_relation.set_ylabel(u"Количество заполненных полей")
plot_fill_relation.figure.savefig('C:/Users/Alexey/Documents/VK analysis/plot_fill_relation.png', dpi = 200)

# Заполненность по году рождения



# Заполненность по семейному положению и полу

#for i in ["Male","Female"]:
#    sex_df = df[df.sex == i]
#    filling = [len(sex_df) - sex_df[item].isnull().sum() for item in columns ]
#    perc = [item / float(len(sex_df)) * 100 for item in filling]
#    fill_df = pd.DataFrame(perc, index=columns, columns=["Percentage"])
#    fill_df.sort_values("Percentage").plot(kind="barh")

### FRIENDS

#columns = ["uid", "first_name", "last_name", "bdate", "sex", "city",
#                "deactivated", "personal_alcohol",
#                "personal_life_main", "personal_religion", "personal_smoking", 
#                "personal_political", "personal_inspired_by",
#                "personal_people_main","career_1_position", "career_1_company",
#                "occupation_name", "occupation_type", "relatives_1_type",
#                "status", 
#                "status_audio_artist", "universities_1_name", 
#                "universities_1_faculty_name", "universities_1_graduation",
#                "schools_1_year_graduated", "about", "activities", "books",
#                "country", "facebook", "games", "instagram", "interests", 
#                "last_seen_time", "mobile_phone", "movies", "music",
#                "personallangs_1", "personallangs_2", "personallangs_3", 
#                "quotes", "relation", "relation_partner_id", "site", "tv",
#                "twitter", "skype", "livejournal", "wall_comments", "friends_count"]
#
#csv = 'C:/Users/Alexey/Documents/VK analysis/results_with_friends.csv'
#
#df = pd.read_csv(csv, na_values = ["[]"], 
#                 usecols = columns, encoding="utf-8")
#
#df["fill_count"] = len(df.columns) - df.isnull().sum(axis=1)

