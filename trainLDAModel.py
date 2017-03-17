import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities


# load corpus/dict from files
#training_corpus = corpora.MmCorpus('train_corpus_40.mm')
training_corpus = corpora.MmCorpus('train_corpus_40_norarewords.mm')
#dictionary = corpora.Dictionary.load('dictionary_40_docs.dict')
dictionary = corpora.Dictionary.load('dict_40_norarewords.dict')

lda_model = models.ldamodel.LdaModel(corpus=training_corpus, id2word=dictionary, num_topics=15, update_every=1, chunksize=10, passes=10)
#print lda_model.print_topics(5)

_ = lda_model.print_topics(-1)

lda_model.save('lda_40_docs.model') # this one is 15 topics

'''
text = "A blood cell, also called a hematocyte, is a cell produced by hematopoiesis and normally found in blood."

# transform text into the bag-of-words space
bow_vector = id2word_wiki.doc2bow(tokenize(text))
print([(id2word_wiki[id], count) for id, count in bow_vector])
[(u'blood', 2), (u'normally', 1), (u'produced', 1), (u'cell', 2)]

# transform into LDA space
lda_vector = lda_model[bow_vector]       # unpack this a bit--did he make a function for this or something
print(lda_vector)
# print the document's single most prominent LDA topic
print(lda_model.print_topic(max(lda_vector, key=lambda item: item[1])[0]))
'''