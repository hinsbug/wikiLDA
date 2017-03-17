import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import wikipedia
import re
import csv
import gensim
from gensim import corpora, models, similarities

# ok here's where the actual program starts
namelist = []


# read names file
with open('unseen_names_women.csv') as file:
    namereader = csv.reader(file, delimiter=',')
    for line in enumerate(namereader):
        name = line[1]
        namelist.append(name)

#namelist = ["Ethel Shakespear","Audrey Tang","Ming C. Lin"]

# write to CSV
with open('unseen_docs_women.csv', 'wb') as file: # perhaps I want txt here?
    writer = csv.writer(file)
    for row in namelist:
        pg = wikipedia.page([row])
        cont = pg.content
        cont = cont.encode('utf-8')
        writer.writerow([cont]) # row not rows that's important. also the brackets
