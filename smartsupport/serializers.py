import unicodedata

import nltk
import six
import re

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from rest_framework import serializers
from .models import Record
from .metrics import Metrics

from bm25 import BM25


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Record
        #fields = ('id', 'name')
        fields = '__all__'

    def main(self, sentence):

        #Okapi BM25
        messageQuestions = []
        messageAnswers = []
        idAnswers = []
        questions = []
        answers = []
        messageOrder = []
        scoreTotal = []
        cursor = Record().get_knowledgebases()
        for row in cursor.fetchall():
            idAnswers.append(row[0])
            messageQuestions.append(self.to_unicode(row[1],'latin1'))
            messageAnswers.append(self.to_unicode(row[2],'latin1'))
            tokensQuestion = self.normalize_terms(self.to_unicode(row[1],'latin1'))
            tokensAnswer = self.normalize_terms(self.to_unicode(row[2],'latin1'))
            questions.append(tokensQuestion)
            answers.append(tokensAnswer)

        bm25Questions = BM25(questions)
        bm25Answers = BM25(answers)
        
        query = self.normalize_terms(self.to_unicode(sentence,'latin1'))
        
        for position, index in enumerate(bm25Questions.ranked(query, 5)):

            scoreQuestion = bm25Questions._get_scores(query)[index]
            scoreAnswer = bm25Answers._get_scores(query)[index]
            print 'ScoreQuestion: ',scoreQuestion
            print 'ScoreAnswer: ',scoreAnswer,'\n'
            avr = (scoreQuestion + scoreAnswer) / 2 if (scoreQuestion + scoreAnswer) > 0 else 0
            #avr = (scoreQuestion + scoreAnswer) / 2
            scoreTotal.append((index,avr))
            scoreTotal.sort(key=lambda x: x[1], reverse=True)
            ind, scr = zip(*scoreTotal)

        for index, score in zip(ind,scr):
            result = score,idAnswers[index],messageAnswers[index]
            messageOrder.append(result)
            print messageQuestions[index],'\n-',questions[index],'\n-',idAnswers[index],' - ',messageAnswers[index],'\n-',score,'\n'

        return messageOrder


    def normalize_terms(self, terms):

        #Remove Numerals
        terms = self.remove_numerals(terms)

        #Remove Punctuation and tokenize
        terms = self.remove_punctuation(terms)

        #Remove StopWords
        filtered_words = [word for word in terms if word not in stopwords.words('portuguese')]

        #Stemming
        st = nltk.stem.RSLPStemmer()
        #sno = nltk.stem.SnowballStemmer('portuguese')
        filtered_stem = [st.stem(filtered_word) for filtered_word in filtered_words]

        return [self.remove_accents(term).lower() for term in filtered_stem]


    def remove_diacritics(self, text, encoding='latin1'): #utf8
        """Remove diacritics from bytestring or unicode, returning an unicode string"""
        nfkd_form = unicodedata.normalize('NFKD', to_unicode(text, encoding))
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return only_ascii.decode(encoding)


    def to_unicode(self, text, encoding):
        """Convert a string (bytestring in `encoding` or unicode), to unicode."""
        if isinstance(text, six.text_type):
            return text
        return text.decode(encoding)

    def remove_numerals(self, text):
        """Remove numerals"""
        filtered_num = re.sub(r'\d+', '', text)
        return filtered_num

    def remove_accents(self, term):
        return unicodedata.normalize('NFKD', term).encode('ASCII','ignore').decode('ASCII')

    def remove_punctuation(self, term):
        """Remove Punctuation and tokenize"""
        tokenizer = RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(term)

    def set_update(self):
        cursor = Record().get_knowledge_validation()
        for row in cursor.fetchall():
            id_question = self.main(row[3])
            scr, idAws, ind = zip(*id_question)
            print 'idAws: ',idAws[0],' - ','id_base: ',row[0],'\n'
            Record().set_update(idAws[0], row[0])

        return self.get_metrics()
        #return 'metrics'

    def get_metrics(self):
        arrTrue = []
        arrPred = []
        cursor = Record().get_knowledge_validation()
        for row in cursor.fetchall():
            arrTrue.append(row[1])
            arrPred.append(row[2])

        accuracy = Metrics(arrTrue, arrPred).accuracy()
        f1Score = Metrics(arrTrue, arrPred).f1_score()

        print 'accuracy: ',accuracy
        print 'f1Score: ',f1Score
        return 'Accuracy: ',accuracy,'f1Score: ',f1Score