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

    clv_partner_entity_street_pattern_fields = ['id', 'street', 'street2', 'notes', 'active']

    common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
    user_id = common.authenticate(db_name, username, password, {})
    models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

    if user_id:

        search_domain = []
        clv_partner_entity_street_pattern_objects = models.execute_kw(
            db_name, user_id, password,
            'clv.partner_entity.street_pattern', 'search_read',
            [search_domain, clv_partner_entity_street_pattern_fields],
            {}
        )
        clv_partner_entity_street_pattern = pd.DataFrame(clv_partner_entity_street_pattern_objects)

        for i, row in clv_partner_entity_street_pattern.iterrows():

            if row['notes'] is False:
                clv_partner_entity_street_pattern['notes'].values[i] = None

        conn = sqlite3.connect('data/jcafb_2025.db')

        if initialize:

            clv_partner_entity_street_pattern.to_sql('clv_partner_entity_street_pattern', conn, if_exists='replace', index=False)

        else:

            cur = conn.cursor()
            cur.execute('DELETE FROM clv_partner_entity_street_pattern')
            conn.commit()

            clv_partner_entity_street_pattern.to_sql('clv_partner_entity_street_pattern', conn, if_exists='append', index=False)

            # sql = '''
            #     UPDATE clv_partner_entity_street_pattern
            #     SET description = NULL
            #     WHERE description = '0';
            #     '''
            # cur = conn.cursor()
            # cur.execute(sql)
            # conn.commit()

        conn.close()

    return clv_partner_entity_street_pattern