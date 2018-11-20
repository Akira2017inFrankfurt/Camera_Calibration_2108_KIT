# def load_tracks(filename)
#import numpy as np

# get the list of tracing points
#import json
# file_path of the data

file_name = 'C:\\Users\\hhl\\PycharmProjects\\Frame_synchronsization\\tracks_test.txt'
content = open(file_name, 'r')

# better to use read
# get all the data independently
str_list = []
lines = content.readlines()
#list = line.split(' ')
i=0
for number in lines:
    # here need more consideration
    #str_list[i]=number
    str_list.append(number)

temp_list_1 = []
temp_list_2 = []

for index in range(len(str_list)):
    if index > 0 and index % 3 == 0:
        temp_list_2.append(temp_list_1)
        temp_list_1 = []
    temp_list_1.append(str_list[index])

print temp_list_2



content.close()

