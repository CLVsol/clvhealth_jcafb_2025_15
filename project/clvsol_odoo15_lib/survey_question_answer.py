# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from xmlrpc import client
import pandas as pd
import sqlite3
from time import time
from datetime import timedelta

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return str(timedelta(seconds=t))


def get_sqlite(server_url, db_name, username, password, initialize=False):

    start = time()

    _logger.info(u'%s %s %s %s', '-->', 'get_sqlite', server_url, db_name)

    survey_question_answer_fields = ['id', 'question_id', 'matrix_question_id', 'sequence', 'value', 'code',
                                     'is_correct', 'answer_score']

    common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
    user_id = common.authenticate(db_name, username, password, {})
    models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

    if user_id:

        search_domain = []
        survey_question_answer_objects = models.execute_kw(
            db_name, user_id, password,
            'survey.question.answer', 'search_read',
            [search_domain, survey_question_answer_fields],
            {}
        )
        survey_question_answer = pd.DataFrame(survey_question_answer_objects)
        survey_question_answer.insert(survey_question_answer.columns.get_loc("question_id") + 1, 'question', None)
        survey_question_answer.insert(survey_question_answer.columns.get_loc("matrix_question_id") + 1, 'matrix_question', None)

        for i, row in survey_question_answer.iterrows():

            if row['question_id']:
                survey_question_answer['question_id'].values[i] = row['question_id'][0]
                survey_question_answer['question'].values[i] = row['question_id'][1]
            else:
                survey_question_answer['question_id'].values[i] = None

            if row['matrix_question_id']:
                survey_question_answer['matrix_question_id'].values[i] = row['matrix_question_id'][0]
                survey_question_answer['matrix_question'].values[i] = row['matrix_question_id'][1]
            else:
                survey_question_answer['matrix_question_id'].values[i] = None

        conn = sqlite3.connect('data/jcafb_2025.db')

        if initialize:

            survey_question_answer.to_sql('survey_question_answer', conn, if_exists='replace', index=False)

        else:

            cur = conn.cursor()
            cur.execute('DELETE FROM survey_question_answer')
            conn.commit()

            survey_question_answer.to_sql('survey_question_answer', conn, if_exists='append', index=False)

        sql = '''
            UPDATE survey_question_answer
            SET is_correct = NULL
            WHERE is_correct = 0;
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_question_answer
            SET answer_score = NULL
            WHERE answer_score = 0;
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        conn.close()

    _logger.info(u'%s %s %s %s', '-->', 'Execution time:', secondsToStr(time() - start), '\n')

    return survey_question_answer
