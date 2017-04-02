import MySQLdb

#from __future__ import unicode_literals
from django.db import models


class Record(models.Model):
    name = models.CharField(max_length=5000)
    
    class Meta:
        verbose_name = u'Record'
        verbose_name_plural = u'Records'

    def get_connection(self):
        return MySQLdb.connect(host='localhost', user='root', passwd='root',db='db_test')

    def get_knowledgebases(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT kbs.id, kbs.title, kbs.text FROM knowledge_bases kbs")
        conn.close()
        return cursor

    def get_knowledge_validation(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = '''
                SELECT kbv.id, kbv.id_answer, kbv.id_answer_label, kbv.question
                FROM knowledge_bases_validation kbv
                ORDER BY kbv.id_answer
                '''
        cursor.execute(query)
        conn.close()
        return cursor
    
    def set_update(self, id_answer, id_base):
        conn = self.get_connection()
        cursor = conn.cursor()

        query = '''
                UPDATE knowledge_bases_validation
                SET id_answer_label = "{id_answer}"
                WHERE id = "{id_base}"
                '''.format(id_answer=id_answer, id_base=id_base)

        #print 'query: ',query
        cursor.execute(query)
        conn.commit()
        conn.close()
        
    def __str__(self):
        return self.name