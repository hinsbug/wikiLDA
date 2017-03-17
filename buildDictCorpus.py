import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import re
import csv
import gensim
from gensim import corpora, models, similarities
from gensim.parsing.preprocessing import STOPWORDS

"""
    Processes out the unuseful bits of wikipedia article at the end.
"""
def processSectionsOut(content):
    content = content.replace('\n', ' ') # just makes things easier to read for me!
    blocks = content.split('==')
    a = 999 # this is a janky solution and will not work for v large articles I guess
    b = 999
    c = 999
    d = 999
    i = 0
    for block in blocks:
        if " Footnotes" in block: # sorta janky way to do this (may get buggy)
            a = i

        if " References" in block:
            b = i

        if " Further reading" in block:
            c = i

        if " External links" in block:
            d = i
        i = i + 1 # iterate the count

    # if a b c or d are not inital val: test whichever one is smallest
    if(a<999 or b<999 or c<999 or d<999):
        lastGoodBlock = min([a,b,c,d])
        newContent = "".join(blocks[0:lastGoodBlock])
    else:
        newContent = content
    # either way return newContent
    return newContent


# ok here's where the actual program starts
sci_list = []
contentNoSections = [] # list of content with unnecessary sections processed out

# read docs out of a file & put them in sci_list
with open('unseen_docs_men.csv') as file:
    namereader = csv.reader(file, delimiter=',')
    for line in enumerate(namereader):
        content = line[1]
        sci_list.append(content[0])

#print sci_list
#print len(sci_list)

# take out "== x ==" sections I don't want
for scientist in sci_list:
    contentNoSections.append(processSectionsOut(scientist))

# remove common words - this gives you a list of the individual words in "texts"
#stoplist = set('for a an of the and but to in was is are on at'.split())
    # oh but does STOPWORDS include she/he? I should check
# split by all punctuation including space
# technically this splits words like "Taiwan's" into "taiwan" "s" but that's actually fine!
texts = [[word for word in
          filter(None, re.split("[('\((.*)\)'), .!?:\"]+", document.lower()))
          if word not in STOPWORDS]
         for document in contentNoSections]

#print texts

# remove words that appear only once - for now don't do this. try it later if necessary
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
         for text in texts]

'''
# COMMENT OUT FROM HERE to do unseen documents
# make a dictionary
dictionary = corpora.Dictionary(texts)
# save ya dictionary
dictionary.save('dict_60_norarewords.dict')
# make the corpus

training_corpus = [dictionary.doc2bow(text) for text in texts]
# save the corpus -->
corpora.MmCorpus.serialize('train_corpus_60_norarewords.mm', training_corpus)
# COMMENT OUT TO HERE


# ----For modeling unseen documents----
# ----Comment this whole part if you're just training a model----
'''
# load stuff you made before--the model and the dictionary
dictionary = corpora.Dictionary.load('dict_40_norarewords.dict')
lda_40 = gensim.models.LdaModel.load('lda_40_docs.model')


# turn unseen women into a list of vectors(?)
unseen_men = [dictionary.doc2bow(text) for text in texts]

for person in unseen_men:
    # transform into LDA space
    lda_vector = lda_40[person]
    # print the topic numbers + how significant they are. **it would be awesome to order these by signif!
    print(lda_vector)
    # print the document's single most prominent LDA topic
    # **how to get this to print the topic number not the topic words.....
    print(lda_40.print_topic(max(lda_vector, key=lambda item: item[1])[0]))
