import numpy as np
np.random.seed(23)
from sklearn.datasets import fetch_20newsgroups
import gensim
from preprocess import Preprocess
import visualize
newsgroups_train = fetch_20newsgroups(subset='train', shuffle = True)
newsgroups_test = fetch_20newsgroups(subset='test', shuffle = True)



 

processed_docs = Preprocess().transform(newsgroups_train.data)


dictionary = gensim.corpora.Dictionary(processed_docs)

dictionary.filter_extremes(no_below=10, no_above=0.1, keep_n= 100000)

bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]


lda_model = gensim.models.LdaModel(bow_corpus, 
                                   num_topics = 10, 
                                   id2word = dictionary,                                    
                                   passes = 50)

for i, topic in lda_model.print_topics(-1):
    print("Topic Number: {} \n Representative Words: {}".format(i, topic ))
    print("\n") 


visualize.generate_html_vis(lda_model=lda_model, bow_corpus=bow_corpus)
