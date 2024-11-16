# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_client.cli import *
from odoo_client.db import *

from odoo_client.host import *

from odoo_client.res_users import *

import logging

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


if __name__ == '__main__':

    from time import time

    cli = CLI2(
        remote_server='*',
        remote_admin_user_pw='*',
        remote_dbname='*',
        local_server='*',
        local_admin_user_pw='*',
        local_dbname='*',
    )
    cli.argparse()

    start = time()

    print()
    _logger.info(u'%s %s\n', '-->', 'Executing res_users_migration.py...')

    ruid, rsock, login_msg = host_login(cli.remote_server,
                                        cli.remote_dbname,
                                        'admin',
                                        cli.remote_admin_user_pw)
    _logger.info(u'%s %s %s\n', '-->', rsock, login_msg)

    luid, lsock, login_msg = host_login(cli.local_server,
                                        cli.local_dbname,
                                        'admin',
                                        cli.local_admin_user_pw)
    _logger.info(u'%s %s %s\n', '-->', lsock, login_msg)

    res_user_migrate(rsock, ruid, cli.remote_admin_user_pw, cli.remote_dbname,
                     lsock, luid, cli.local_admin_user_pw, cli.local_dbname)

    print()
    _logger.info('--> res_users_migration.py')
    _logger.info(u'%s %s\n', '--> Execution time:', secondsToStr(time() - start))
