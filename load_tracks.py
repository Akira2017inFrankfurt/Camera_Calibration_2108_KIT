# get the list of tracing points
import json
# file_path of the data

file_name = '/Users/Haruki/Desktop/txt.txt'
content = open(file_name, 'r')

# better to use read
# get all the data independently
str_list = []
line = content.read()
list = line.split(',')
for value in list:
    # here need more consideration
    if value == ',' or value == '\n':
        continue
    str_list.append(value)

temp_list_1 = []
temp_list_2 = []

for index in range(len(str_list)):
    if index > 0 and index % 3 == 0:
        temp_list_2.append(temp_list_1)
        temp_list_1 = []
    temp_list_1.append(str_list[index])

print temp_list_2



content.close()
