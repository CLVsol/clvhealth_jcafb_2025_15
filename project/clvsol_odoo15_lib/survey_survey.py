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

    survey_survey_fields = ['id', 'title', 'code', 'description', 'access_token', 'phase_id',
                            'users_login_required', 'is_attempts_limited', 'attempts_limit', 'users_can_go_back',
                            'questions_layout', 'color', 'questions_selection', 'access_mode', 'session_code',
                            'active']

    common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
    user_id = common.authenticate(db_name, username, password, {})
    models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

    if user_id:

        search_domain = []
        survey_survey_objects = models.execute_kw(
            db_name, user_id, password,
            'survey.survey', 'search_read',
            [search_domain, survey_survey_fields],
            {}
        )
        survey_survey = pd.DataFrame(survey_survey_objects)
        survey_survey.insert(survey_survey.columns.get_loc("phase_id") + 1, 'phase', None)

        for i, row in survey_survey.iterrows():

            if row['phase_id']:
                survey_survey['phase_id'].values[i] = row['phase_id'][0]
                survey_survey['phase'].values[i] = row['phase_id'][1]
            else:
                survey_survey['phase_id'].values[i] = None

        conn = sqlite3.connect('data/jcafb_2025.db')

        if initialize:

            survey_survey.to_sql('survey_survey', conn, if_exists='replace', index=False)

        else:

            cur = conn.cursor()
            cur.execute('DELETE FROM survey_survey')
            conn.commit()

            survey_survey.to_sql('survey_survey', conn, if_exists='append', index=False)

        conn.close()

    _logger.info(u'%s %s %s %s', '-->', 'Execution time:', secondsToStr(time() - start), '\n')

    return survey_survey
