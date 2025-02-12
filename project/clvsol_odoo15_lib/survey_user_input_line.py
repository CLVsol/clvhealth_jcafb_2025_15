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


def get_sqlite(server_url, db_name, username, password, search_domain, clear_table=True, initialize=False):

    start = time()

    _logger.info(u'%s %s %s', '-->', 'search_domain:', search_domain)

    _logger.info(u'%s %s %s %s', '-->', 'get_sqlite', server_url, db_name)

    survey_user_input_line_fields = ['id', 'user_input_id', 'survey_id', 'question_id', 'question_sequence', 'skipped',
                                     'answer_type', 'value_char_box', 'value_numerical_box',
                                     'value_date', 'value_datetime', 'value_text_box',
                                     'suggested_answer_id', 'matrix_row_id', 'answer_score', 'answer_is_correct']

    common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
    user_id = common.authenticate(db_name, username, password, {})
    models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

    if user_id:

        # search_domain = []
        survey_user_input_line_objects = models.execute_kw(
            db_name, user_id, password,
            'survey.user_input.line', 'search_read',
            [search_domain, survey_user_input_line_fields],
            {}
        )
        survey_user_input_line = pd.DataFrame(survey_user_input_line_objects)

        survey_user_input_line.insert(survey_user_input_line.columns.get_loc("user_input_id") + 1, 'user_input', None)
        survey_user_input_line.insert(survey_user_input_line.columns.get_loc("survey_id") + 1, 'survey', None)
        survey_user_input_line.insert(survey_user_input_line.columns.get_loc("question_id") + 1, 'question', None)
        survey_user_input_line.insert(
            survey_user_input_line.columns.get_loc("suggested_answer_id") + 1, 'suggested_answer', None)
        survey_user_input_line.insert(survey_user_input_line.columns.get_loc("matrix_row_id") + 1, 'matrix_row', None)

        for i, row in survey_user_input_line.iterrows():

            if row['user_input_id']:
                survey_user_input_line['user_input_id'].values[i] = row['user_input_id'][0]
                survey_user_input_line['user_input'].values[i] = row['user_input_id'][1]
            else:
                survey_user_input_line['user_input_id'].values[i] = None

            if row['survey_id']:
                survey_user_input_line['survey_id'].values[i] = row['survey_id'][0]
                survey_user_input_line['survey'].values[i] = row['survey_id'][1]
            else:
                survey_user_input_line['survey_id'].values[i] = None

            if row['question_id']:
                survey_user_input_line['question_id'].values[i] = row['question_id'][0]
                survey_user_input_line['question'].values[i] = row['question_id'][1]
            else:
                survey_user_input_line['question_id'].values[i] = None

            if row['suggested_answer_id']:
                survey_user_input_line['suggested_answer_id'].values[i] = row['suggested_answer_id'][0]
                survey_user_input_line['suggested_answer'].values[i] = row['suggested_answer_id'][1]
            else:
                survey_user_input_line['suggested_answer_id'].values[i] = None

            if row['matrix_row_id']:
                survey_user_input_line['matrix_row_id'].values[i] = row['matrix_row_id'][0]
                survey_user_input_line['matrix_row'].values[i] = row['matrix_row_id'][1]
            else:
                survey_user_input_line['matrix_row_id'].values[i] = None

            if not row['answer_type']:
                survey_user_input_line['answer_type'].values[i] = None

            if not row['value_char_box']:
                survey_user_input_line['value_char_box'].values[i] = None

            if row['value_numerical_box'] == 0.0:
                survey_user_input_line['value_numerical_box'].values[i] = None

            if not row['value_date']:
                survey_user_input_line['value_date'].values[i] = None

            if not row['value_datetime']:
                survey_user_input_line['value_datetime'].values[i] = None

            if not row['value_text_box']:
                survey_user_input_line['value_text_box'].values[i] = None

            if row['value_numerical_box'] == 0.0:
                survey_user_input_line['value_numerical_box'].values[i] = None

        conn = sqlite3.connect('data/jcafb_2025.db')

        if initialize:

            survey_user_input_line.to_sql('survey_user_input_line', conn, if_exists='replace', index=False)

        else:

            if clear_table:
                cur = conn.cursor()
                cur.execute('DELETE FROM survey_user_input_line')
                conn.commit()

            survey_user_input_line.to_sql('survey_user_input_line', conn, if_exists='append', index=False)

        sql = '''
            UPDATE survey_user_input_line
            SET matrix_row_id = NULL
            WHERE matrix_row_id = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_user_input_line
            SET value_text_box = NULL
            WHERE value_text_box = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_user_input_line
            SET value_text_box = NULL
            WHERE value_text_box = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_user_input_line
            SET value_datetime = NULL
            WHERE value_datetime = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        conn.close()

    _logger.info(u'%s %s %s', '-->', 'Execution time:', secondsToStr(time() - start))
    _logger.info(u'%s %s %s %s', '-->', 'DataFrame Shape:', str(survey_user_input_line.shape), '\n')

    # return survey_user_input_line
    return
