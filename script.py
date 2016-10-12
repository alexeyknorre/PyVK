from code import vk2csv, fields2network

#vk2csv.vk2csv("sex,bdate,music,movies,books,interests,personal,country,city,home_town,career,education,universities, schools", 10000)

fields2network.csv2pajek(fields='music', minimum_occurences=1)



