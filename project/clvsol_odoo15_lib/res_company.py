# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from xmlrpc import client
import pandas as pd
import sqlite3

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def get_sqlite(server_url, db_name, username, password, initialize=False):

    _logger.info(u'%s %s %s %s', '-->', 'get_sqlite', server_url, db_name)

    res_company_fields = ['id', 'name']

    common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
    user_id = common.authenticate(db_name, username, password, {})
    models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

    if user_id:

        search_domain = []
        res_company_objects = models.execute_kw(
            db_name, user_id, password,
            'res.company', 'search_read',
            [search_domain, res_company_fields],
            {}
        )
        res_company = pd.DataFrame(res_company_objects)

        conn = sqlite3.connect('data/jcafb_2025.db')

        if initialize:

            res_company.to_sql('res_company', conn, if_exists='replace', index=False)

        else:

            cur = conn.cursor()
            cur.execute('DELETE FROM res_company')
            conn.commit()

            res_company.to_sql('res_company', conn, if_exists='append', index=False)

        conn.close()

    return res_company