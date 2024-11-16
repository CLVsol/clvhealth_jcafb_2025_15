# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import images

from odoo_client.cli import *
from odoo_client.db import *


class CLVhealthJCAFB(object):

    def __init__(
        self,

        server='http://localhost:8069',

        CompanyName='CLVhealth-JCAFB',
        Company_image=images.Company_image,
        website='https://github.com/CLVsol',

        admin_user_pw='admin',
        admin_user_email='admin@clvsol.com',
        Administrator_image=images.Administrator_image,

        # demo_user_name='Demo User',
        # demo_user='demo',
        # demo_user_pw='demo',
        # demo_user_email='demo.user@clvsol.com',
        # Demo_User_image=images.Demo_User_image,

        data_admin_user_name='Data Administrator',
        data_admin_user='data.admin',
        data_admin_user_pw='data.admin',
        data_admin_user_email='data.admin@clvsol.com',
        DataAdministrator_image=images.DataAdministrator_image,

        dbname='clvhealth_jcafb',

        lang='pt_BR',
        tz='America/Sao_Paulo',

        demo_data=False,
        upgrade_all=False,
        modules_to_upgrade=[],
    ):

        self.server = server

        self.CompanyName = CompanyName
        self.Company_image = Company_image
        self.website = website

        self.admin_user_pw = admin_user_pw
        self.admin_user_email = admin_user_email
        self.Administrator_image = Administrator_image

        # self.demo_user_name = demo_user_name
        # self.demo_user = demo_user
        # self.demo_user_pw = demo_user_pw
        # self.demo_user_email = demo_user_email
        # self.Demo_User_image = Demo_User_image

        self.data_admin_user_name = data_admin_user_name
        self.data_admin_user = data_admin_user
        self.data_admin_user_pw = data_admin_user_pw
        self.data_admin_user_email = data_admin_user_email
        self.DataAdministrator_image = DataAdministrator_image

        self.dbname = dbname

        self.lang = lang
        self.tz = tz

        self.demo_data = demo_data
        self.upgrade_all = upgrade_all
        self.modules_to_upgrade = modules_to_upgrade

    def install_upgrade_module(self, module, upgrade, group_name_list=[]):

        print('\n%s%s' % ('--> ', module))
        if module in self.modules_to_upgrade:
            new_module = db.module_install_upgrade(module, True)
        else:
            new_module = db.module_install_upgrade(module, upgrade)

        return new_module

    def install(self):

        global upgrade

        print('--> create_database()')
        newDB = db.create()
        if newDB:

            print('\n--> newDB: ', newDB)
            print('\n--> my_company_setup()')
            db.my_company_setup(self.CompanyName, self.website, self.Company_image)
            print('\n--> Administrator()')
            db.administrator_setup(self.admin_user_email, self.Administrator_image)
            # print('\n--> demo_user_setup()')
            # db.demo_user_setup(
            #     self.demo_user_name, self.demo_user_email, self.CompanyName,
            #     self.demo_user, self.demo_user_pw, self.Demo_User_image
            # )
            print('\n--> data_administrator_user_setup()')
            db.data_administrator_user_setup(
                self.data_admin_user_name, self.data_admin_user_email, self.CompanyName,
                self.data_admin_user, self.data_admin_user_pw, self.DataAdministrator_image
            )

        else:

            print('\n--> newDB: ', newDB)
            print('\n--> my_company_setup()')
            db.my_company_setup(self.CompanyName, self.website, self.Company_image)
            print('\n--> Administrator()')
            db.administrator_setup(self.admin_user_email, self.Administrator_image)
            # print('\n--> demo_user_setup()')
            # db.demo_user_setup(
            #     self.demo_user_name, self.demo_user_email, self.CompanyName,
            #     self.demo_user, self.demo_user_pw, self.Demo_User_image
            # )
            print('\n--> data_administrator_user_setup()')
            db.data_administrator_user_setup(
                self.data_admin_user_name, self.data_admin_user_email, self.CompanyName,
                self.data_admin_user, self.data_admin_user_pw, self.DataAdministrator_image
            )

            print('\n--> newDB: ', newDB)
            client = erppeek.Client(
                server=self.server,
                db=self.dbname,
                user='admin',
                password=self.admin_user_pw
            )
            print('\n--> Update Modules List"')
            IrModuleModule = client.model('ir.module.module')
            IrModuleModule.update_list()

        group_names = []

        # ############################################################################################
        #
        # Odoo Addons
        #
        # ############################################################################################

        self.install_upgrade_module('mail', False, group_names)

        self.install_upgrade_module('hr', False, group_names)

        self.install_upgrade_module('contacts', False, group_names)

        # self.install_upgrade_module('base_address_city', False, group_names)

        self.install_upgrade_module('base_address_extended', False, group_names)

        self.install_upgrade_module('survey', False, group_names)

        # ############################################################################################
        #
        # CLVsol l10n-brazil
        #
        # ############################################################################################

        self.install_upgrade_module('l10n_br_base', self.upgrade_all, group_names)

        self.install_upgrade_module('l10n_br_zip', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons
        # #
        # # ############################################################################################

        # # group_names = [
        # #     'User (Base)',
        # #     'Super User (Base)',
        # #     'Annotation User (Base)',
        # #     'Register User (Base)',
        # #     'Log User (Base)',
        # #     'Manager (Base)',
        # #     'Super Manager (Base)',
        # # ]
        # self.install_upgrade_module('clv_base', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_phase', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_file_system', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_global_tag', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_set', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_pool', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_employee', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_employee_history', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_survey', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_event', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_document', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_document_survey', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_lab_test', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_lab_test_survey', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_partner_entity', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_residence', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_residence_history', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_history', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_aux', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_rec', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_community', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_residence_community', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_history', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_residence_history_community', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_family', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_family_history', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_relation', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_community', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_history', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_history_community', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_aux', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_aux', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - Brazilian Localization
        # #
        # # ############################################################################################

        # self.install_upgrade_module('clv_partner_entity_l10n_br', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_residence_l10n_br', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_l10n_br', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_aux_l10n_br', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_rec_l10n_br', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_l10n_br', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_family_l10n_br', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_l10n_br', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_aux_l10n_br', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_aux_l10n_br', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - JCAFB customizations
        # #
        # # ############################################################################################

        # self.install_upgrade_module('clv_base_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_employee_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_event_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_document_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_document_pool_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_lab_test_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_lab_test_pool_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_residence_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_residence_pool_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_pool_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_aux_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_rec_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_residence_community_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_family_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_community_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_aux_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_aux_jcafb', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - Log
        # #
        # # ############################################################################################

        # self.install_upgrade_module('clv_global_log', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - Log - JCAFB customizations
        # #
        # # ############################################################################################

        # # # self.install_upgrade_module('clv_phase_log_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_global_tag_log_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_document_log_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_lab_test_log_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_partner_entity_log_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_residence_log_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_log_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_aux_log_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_rec_log_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_community_log_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_log_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_family_log_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_log_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_aux_log_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_aux_log_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_processing_log_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_external_sync_log_jcafb', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - Summary
        # #
        # # ############################################################################################

        # self.install_upgrade_module('clv_summary', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - Summary - JCAFB customizations
        # #
        # # ############################################################################################

        # self.install_upgrade_module('clv_summary_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_employee_summary_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_summary_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_family_summary_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_summary_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_aux_summary_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_residence_summary_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_summary_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_aux_summary_jcafb', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - Verification
        # #
        # # ############################################################################################

        # self.install_upgrade_module('clv_verification', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - Verification - JCAFB customizations
        # #
        # # ############################################################################################

        # self.install_upgrade_module('clv_verification_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_verification_log_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_partner_entity_verification_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_rec_verification_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_residence_verification_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_verification_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_aux_verification_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_lab_test_verification_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_verification_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_residence_community_verification_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_family_verification_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_verification_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_community_verification_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_aux_verification_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_aux_verification_jcafb', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - Export
        # #
        # # ############################################################################################

        # self.install_upgrade_module('clv_export', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_document_export', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_lab_test_export', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_export', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_export', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - Export - JCAFB customizations
        # #
        # # ############################################################################################

        # self.install_upgrade_module('clv_export_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_document_export_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_lab_test_export_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_export_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_export_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_community_export_jcafb', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - Process
        # #
        # # ############################################################################################

        # self.install_upgrade_module('clv_processing', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_survey_process', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - Process - JCAFB customizations
        # #
        # # ############################################################################################

        # self.install_upgrade_module('clv_processing_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_survey_process', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - Sync
        # #
        # # ############################################################################################

        # self.install_upgrade_module('clv_external_sync', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_base_sync', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_phase_sync', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_file_system_sync', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_global_tag_sync', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_set_sync', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_employee_sync', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_employee_history_sync', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_survey_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_event_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_document_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_document_survey_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_lab_test_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_lab_test_survey_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_partner_entity_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_residence_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_residence_history_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_history_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_aux_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_residence_community_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_history_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_residence_history_community_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_family_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_family_history_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_relation_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_community_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_history_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_history_community_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_aux_sync', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_aux_sync', self.upgrade_all, group_names)

        # # ############################################################################################
        # #
        # # CLVsol Odoo Addons - Sync - JCAFB customizations
        # #
        # # ############################################################################################

        # self.install_upgrade_module('clv_external_sync_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_phase_log_sync_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_global_tag_log_sync_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_employee_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_event_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_document_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_document_log_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_lab_test_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_lab_test_log_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_lab_test_verification_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_residence_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_residence_log_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_residence_verification_sync_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_residence_history_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_log_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_verification_sync_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_patient_history_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_aux_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_aux_log_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_aux_verification_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_log_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_verification_sync_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_address_history_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_family_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_family_log_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_family_verification_sync_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_family_history_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_sync_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_person_relation_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_log_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_verification_sync_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_person_history_sync_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_address_aux_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_aux_log_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_address_aux_verification_sync_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_person_aux_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_aux_log_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_person_aux_verification_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_verification_sync_jcafb', self.upgrade_all, group_names)

        # # # # self.install_upgrade_module('clv_export_sync_jcafb', self.upgrade_all, group_names)

        # # # ############################################################################################
        # # #
        # # # CLVsol Odoo Addons - Report
        # # #
        # # # ############################################################################################

        # # # self.install_upgrade_module('clv_report', self.upgrade_all, group_names)

        # # # ############################################################################################
        # # #
        # # # CLVsol Odoo Addons - Report - JCAFB customizations
        # # #
        # # # ############################################################################################

        # # # self.install_upgrade_module('clv_report_jcafb', self.upgrade_all, group_names)


if __name__ == '__main__':

    from time import time

    cli = CLI(
        super_user_pw='*',
        admin_user_pw='*',
        # data_admin_user_pw='*',
        dbname='*',
        demo_data=False,
        lang='pt_BR',
        tz='America/Sao_Paulo',
    )
    cli.argparse_db_setup()

    clvhealth_jcafb = CLVhealthJCAFB(
        # super_user_pw=cli.super_user_pw,
        dbname=cli.dbname,
        admin_user_pw=cli.admin_user_pw,
        # demo_user_pw='demo',
        # data_admin_user_pw=cli.data_admin_user_pw,
        demo_data=cli.demo_data,
        upgrade_all=cli.upgrade_all,
        modules_to_upgrade=cli.modules_to_upgrade,
        lang=cli.lang,
        tz=cli.tz
    )

    db = DB(
        server=cli.server,
        super_user_pw=cli.super_user_pw,
        admin_user_pw=cli.admin_user_pw,
        # data_admin_user_pw=cli.data_admin_user_pw,
        dbname=cli.dbname,
        demo_data=cli.demo_data,
        lang=cli.lang,
        tz=cli.tz
    )

    start = time()

    print('--> Executing install.py...\n')

    print('--> Executing install()...\n')
    clvhealth_jcafb.install()

    print('\n--> install.py')
    print('--> Execution time:', secondsToStr(time() - start), '\n')
