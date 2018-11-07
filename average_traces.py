"""
average_traces.py

Francisco José Juaan Quintanilla, Jan-2018
See LICENSE.md in the root of the repository
"""

import re

#Settings
log_path = "/home/quinta/Desktop/traza-pppx1-pppy2.txt" #Path of the log
key_word = "Encoding & Streaming:" #Keyword that precedes the data

###############################
#Start of the script
###############################

re_float = re.compile("[+-]?([0-9]*[.])?[0-9]+")

print("Taking logs from", log_path)
print("Searching the string ->  ", key_word,)
file = open(log_path, "r")
acumulator = 0.0
found_counter = 0
for line in file:

    index = line.find(key_word)
    if index > 0:
        index += len(key_word) 
        number = line[index:]
        number = number.lstrip(' ')

        m = re_float.match(number)

        if m:
            acumulator += float(m.group(0))
            found_counter += 1

print("Found", found_counter, "matches, resulting an average of", acumulator/found_counter)
