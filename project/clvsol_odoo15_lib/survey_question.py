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

    survey_question_fields = ['id', 'title', 'code', 'description', 'parameter', 'survey_id', 'sequence',
                              'is_page', 'page_id', 'question_type',
                              'matrix_subtype', 'column_nb', 'comments_allowed', 'comments_message', 'comment_count_as_answer',
                              'validation_required', 'validation_email', 'validation_length_min', 'validation_length_max',
                              'validation_min_float_value', 'validation_max_float_value',
                              'validation_min_date', 'validation_max_date',
                              'validation_min_datetime', 'validation_max_datetime',
                              'validation_error_msg', 'constr_mandatory', 'constr_error_msg',
                              'is_conditional', 'triggering_question_id', 'triggering_answer_id']

    common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
    user_id = common.authenticate(db_name, username, password, {})
    models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

    if user_id:

        search_domain = []
        survey_question_objects = models.execute_kw(
            db_name, user_id, password,
            'survey.question', 'search_read',
            [search_domain, survey_question_fields],
            {}
        )
        survey_question = pd.DataFrame(survey_question_objects)
        survey_question.insert(survey_question.columns.get_loc("survey_id") + 1, 'survey', None)
        survey_question.insert(survey_question.columns.get_loc("page_id") + 1, 'page', None)
        survey_question.insert(survey_question.columns.get_loc("triggering_question_id") + 1, 'triggering_question', None)
        survey_question.insert(survey_question.columns.get_loc("triggering_answer_id") + 1, 'triggering_answer', None)

        for i, row in survey_question.iterrows():

            if row['survey_id']:
                survey_question['survey_id'].values[i] = row['survey_id'][0]
                survey_question['survey'].values[i] = row['survey_id'][1]
            else:
                survey_question['survey_id'].values[i] = None

            if row['page_id']:
                survey_question['page_id'].values[i] = row['page_id'][0]
                survey_question['page'].values[i] = row['page_id'][1]
            else:
                survey_question['page_id'].values[i] = None

            if row['triggering_question_id']:
                survey_question['triggering_question_id'].values[i] = row['triggering_question_id'][0]
                survey_question['triggering_question'].values[i] = row['triggering_question_id'][1]
            else:
                survey_question['triggering_question_id'].values[i] = None

            if row['triggering_answer_id']:
                survey_question['triggering_answer_id'].values[i] = row['triggering_answer_id'][0]
                survey_question['triggering_answer'].values[i] = row['triggering_answer_id'][1]
            else:
                survey_question['triggering_answer_id'].values[i] = None

            if row['page_id']:
                survey_question['page_id'].values[i] = row['page_id'][0]
                survey_question['page'].values[i] = row['page_id'][1]
            else:
                survey_question['page_id'].values[i] = None

            if not row['description']:
                survey_question['description'].values[i] = None

            if not row['parameter']:
                survey_question['parameter'].values[i] = None

            if not row['question_type']:
                survey_question['question_type'].values[i] = None

            if not row['matrix_subtype']:
                survey_question['matrix_subtype'].values[i] = None

            if not row['column_nb']:
                survey_question['column_nb'].values[i] = None

            if not row['comments_message']:
                survey_question['comments_message'].values[i] = None

            if not row['validation_error_msg']:
                survey_question['validation_error_msg'].values[i] = None

            if not row['constr_error_msg']:
                survey_question['constr_error_msg'].values[i] = None

        conn = sqlite3.connect('data/jcafb_2025.db')

        if initialize:

            survey_question.to_sql('survey_question', conn, if_exists='replace', index=False)

        else:

            cur = conn.cursor()
            cur.execute('DELETE FROM survey_question')
            conn.commit()

            survey_question.to_sql('survey_question', conn, if_exists='append', index=False)

        sql = '''
            UPDATE survey_question
            SET validation_email = NULL
            WHERE validation_email = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_question
            SET validation_min_date = NULL
            WHERE validation_min_date = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_question
            SET validation_max_date = NULL
            WHERE validation_max_date = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_question
            SET validation_min_datetime = NULL
            WHERE validation_min_datetime = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_question
            SET validation_max_datetime = NULL
            WHERE validation_max_datetime = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_question
            SET triggering_question_id = NULL
            WHERE triggering_question_id = 0;
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_question
            SET triggering_answer_id = NULL
            WHERE triggering_answer_id = 0;
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        conn.close()

    _logger.info(u'%s %s %s %s', '-->', 'Execution time:', secondsToStr(time() - start), '\n')

    return survey_question
