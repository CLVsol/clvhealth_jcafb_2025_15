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

    survey_user_input_fields = ['id', 'survey_id', 'start_datetime', 'end_datetime', 'deadline', 'state',
                                'test_entry', 'last_displayed_page_id', 'access_token',
                                'invite_token', 'partner_id', 'email', 'nickname',
                                'scoring_percentage', 'scoring_total', 'scoring_success', 'is_session_answer',
                                'ref_id', 'ref_model', 'ref_name', 'ref_code',
                                'state_2', 'notes', 'parameter_1', 'parameter_2', 'parameter_3', 'parameter_4']

    common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
    user_id = common.authenticate(db_name, username, password, {})
    models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

    if user_id:

        search_domain = []
        survey_user_input_objects = models.execute_kw(
            db_name, user_id, password,
            'survey.user_input', 'search_read',
            [search_domain, survey_user_input_fields],
            {}
        )
        survey_user_input = pd.DataFrame(survey_user_input_objects)
        survey_user_input.insert(survey_user_input.columns.get_loc("survey_id") + 1, 'survey', None)
        survey_user_input.insert(survey_user_input.columns.get_loc("partner_id") + 1, 'partner', None)

        for i, row in survey_user_input.iterrows():

            if row['survey_id']:
                survey_user_input['survey_id'].values[i] = row['survey_id'][0]
                survey_user_input['survey'].values[i] = row['survey_id'][1]
            else:
                survey_user_input['survey_id'].values[i] = None

            if row['partner_id']:
                survey_user_input['partner_id'].values[i] = row['partner_id'][0]
                survey_user_input['partner'].values[i] = row['partner_id'][1]
            else:
                survey_user_input['partner_id'].values[i] = None

            if not row['start_datetime']:
                survey_user_input['start_datetime'].values[i] = None

            if not row['end_datetime']:
                survey_user_input['end_datetime'].values[i] = None

            if not row['email']:
                survey_user_input['email'].values[i] = None

            if not row['ref_id']:
                survey_user_input['ref_id'].values[i] = None

            if not row['ref_model']:
                survey_user_input['ref_model'].values[i] = None

            if not row['ref_code']:
                survey_user_input['ref_code'].values[i] = None

            if not row['notes']:
                survey_user_input['notes'].values[i] = None

            if not row['parameter_1']:
                survey_user_input['parameter_1'].values[i] = None

            if not row['parameter_2']:
                survey_user_input['parameter_2'].values[i] = None

        conn = sqlite3.connect('data/jcafb_2025.db')

        if initialize:

            survey_user_input.to_sql('survey_user_input', conn, if_exists='replace', index=False)

        else:

            cur = conn.cursor()
            cur.execute('DELETE FROM survey_user_input')
            conn.commit()

            survey_user_input.to_sql('survey_user_input', conn, if_exists='append', index=False)

        sql = '''
            UPDATE survey_user_input
            SET deadline = NULL
            WHERE deadline = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_user_input
            SET last_displayed_page_id = NULL
            WHERE last_displayed_page_id = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_user_input
            SET invite_token = NULL
            WHERE invite_token = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_user_input
            SET ref_name = NULL
            WHERE ref_name = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_user_input
            SET parameter_3 = NULL
            WHERE parameter_3 = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE survey_user_input
            SET parameter_4 = NULL
            WHERE parameter_4 = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        conn.close()

    _logger.info(u'%s %s %s %s', '-->', 'Execution time:', secondsToStr(time() - start), '\n')

    return survey_user_input
