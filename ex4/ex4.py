from gensim import corpora
from gensim import models
import glob
from sklearn import svm
from sklearn.externals import joblib
import numpy as np
from sklearn import metrics




def get_words(filename):
    ignores = [
        # 'artist',
        # 'mathematician',
        # 'novelist',
        # 'physicist',
        # 'physics',
        # 'art',
        # 'mathematics',
        # 'novel'
    ]
    words = []
    for line in open(filename):
        for w in line.strip().split(' '):
            w = w.replace(',','')
            w = w.replace('.','')
            w = w.lower()
            if w:
                if w in ignores:
                    pass
                else:
                    words.append(w)
    
    return words

    

class Classifier:
    def __init__(self):
        
        self.types = [
            'artist',
            'mathematician',
            'novelist',
            'physicist'
        ]

    def load(self):
        self.dic = corpora.Dictionary.load_from_text('./dic')
        self.lsi = models.LsiModel.load('lsi_model.model')
        self.clf = joblib.load('svm.pkl.cmp')
    
    def create_lsi(self):
        documents = []
        for t in self.types:        
            for filename in glob.glob('./wiki/'+t+'/train/*'):
                words = get_words(filename)

                documents.append(words)

        self.dic = corpora.Dictionary(documents)

        self.dic.filter_extremes(no_below=10, no_above=0.3)

        bow_corpus = [self.dic.doc2bow(d) for d in documents]

        self.dic.save_as_text('./dic')

        tfidf_model = models.TfidfModel(bow_corpus)

        tfidf_corpus = tfidf_model[bow_corpus]

        tfidf_model.save('tfidf_model.model')

        self.lsi = models.LsiModel(tfidf_corpus, id2word= self.dic, num_topics= 100)
        
        lsi_corpus = self.lsi[tfidf_corpus]

        self.lsi.save('lsi_model.model')

    def dump_lsi(self):
        print(self.lsi.print_topics())
    
    def calc(self, filename):
        words = get_words(filename)
        bow = self.dic.doc2bow(words)
        
        l = [l[1] for l in self.lsi[bow]]

        return l

    def train(self):
        print('train start')
        data = []
        labels = []

        for t in self.types:        
            for filename in glob.glob('./wiki/'+t+'/train/*'):
                
                
                data.append(self.calc(filename))
                labels.append(t)


        
        self.clf = svm.SVC(C=4, gamma = 0.1, kernel='rbf')
        self.clf.fit(data, labels)
        joblib.dump(self.clf, 'svm.pkl.cmp')

    def predict(self):
        test = []
        labels = []
        names = []
        for t in self.types:
            for filename in glob.glob('./wiki/'+t+'/test/*'):
                test.append(self.calc(filename))
                names.append(filename)
                labels.append(t)
        
        pre = self.clf.predict(test)
        for z in zip(names, pre):
            print(z)

        co_mat = metrics.confusion_matrix(labels, pre)
        print(self.types)
        print(co_mat)

    
import sys

if __name__ == '__main__':
    clf = Classifier()

    if len(sys.argv) > 1:
        clf.create_lsi()
        clf.train()
    else:
        clf.load()
    
    clf.dump_lsi()
    clf.predict()

