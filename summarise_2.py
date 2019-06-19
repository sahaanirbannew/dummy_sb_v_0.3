import summarise
from summarizer import summarize
import random
import g_

link = 'http://www.anirbansaha.com/aerosol-arena-wall-arts-in-magdeburg/'

text = summarise.get_text_from_link(link)
title = "finding birds in magdeburg"

x = random.randint(1, 7)
description_set = summarize(title, text, count=x)
description = ''
count = 0
max_count = len(description_set)
while count < max_count:
    description = description + description_set[count] + '\n'
    count = count + 1

print("---------------------\n")
print("Method 2:\n")
print(description)
print("\n---------------------\n")
print("Method 1:\n")
description2 = summarise.get_summary_description(link, 'fb')
print(description2)
