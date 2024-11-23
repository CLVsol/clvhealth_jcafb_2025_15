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

    res_partner_fields = ['id', 'name', 'type',
                          'street_name', 'street', 'street_number', 'street_number2', 'street2', 'district', 'active'
                          ]

    common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
    user_id = common.authenticate(db_name, username, password, {})
    models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

    if user_id:

        search_domain = []
        res_partner_objects = models.execute_kw(
            db_name, user_id, password,
            'res.partner', 'search_read',
            [search_domain, res_partner_fields],
            {}
        )
        res_partner = pd.DataFrame(res_partner_objects)

        for i, row in res_partner.iterrows():

            if row['street_name'] is False:
                res_partner['street_name'].values[i] = None

            if row['street'] is False:
                res_partner['street'].values[i] = None

            if row['street_number'] is False:
                res_partner['street_number'].values[i] = None

            if row['street_number2'] is False:
                res_partner['street_number2'].values[i] = None

            if row['street2'] is False:
                res_partner['street2'].values[i] = None

            # if row['district'] is False:
            #     res_partner['district'].values[i] = None

        conn = sqlite3.connect('data/jcafb_2025.db')

        if initialize:

            res_partner.to_sql('res_partner', conn, if_exists='replace', index=False)

        else:

            cur = conn.cursor()
            cur.execute('DELETE FROM res_partner')
            conn.commit()

            res_partner.to_sql('res_partner', conn, if_exists='append', index=False)

            sql = '''
                UPDATE res_partner
                SET district = NULL
                WHERE district = '0';
                '''
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()

        conn.close()

    return res_partner
