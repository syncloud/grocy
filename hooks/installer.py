import logging
import shutil
import uuid
import re
from os import path
from os.path import isfile
from os.path import join
from os.path import realpath
from subprocess import check_output, CalledProcessError

from syncloudlib import fs, linux, gen, logger
from syncloudlib.application import paths, urls, storage, service

from postgres import Database

APP_NAME = 'grocy'

INSTALL_USER = 'installer'
USER_NAME = APP_NAME
DB_NAME = APP_NAME
DB_USER = APP_NAME
DB_PASSWORD = APP_NAME
LOG_PATH = 'log/{0}.log'.format(APP_NAME)
CRON_USER = APP_NAME
APP_CONFIG_PATH = '{0}/config'.format(APP_NAME)
PSQL_PORT = 5436

SYSTEMD_NGINX = '{0}.nginx'.format(APP_NAME)
SYSTEMD_PHP_FPM = '{0}.php-fpm'.format(APP_NAME)
SYSTEMD_POSTGRESQL = '{0}.postgresql'.format(APP_NAME)

class Installer:
    def __init__(self):
        if not logger.factory_instance:
            logger.init(logging.DEBUG, True)

        self.log = logger.get_logger('grocy_installer')
        self.app_dir = paths.get_app_dir(APP_NAME)
        self.common_dir = paths.get_data_dir(APP_NAME)
        self.data_dir = join('/var/snap', APP_NAME, 'current')
        self.config_dir = join(self.data_dir, 'config')
        self.db = Database(self.app_dir, self.data_dir, self.config_dir, PSQL_PORT)
        self.install_file = join(self.common_dir, 'installed')
         
    def install_config(self):

        home_folder = join('/home', USER_NAME)
        linux.useradd(USER_NAME, home_folder=home_folder)
        storage.init_storage(APP_NAME, USER_NAME)
        templates_path = join(self.app_dir, 'config')

        variables = {
            'app_dir': self.app_dir,
            'common_dir': self.common_dir,
            'data_dir': self.data_dir,
            'db_psql_port': PSQL_PORT,
            'database_dir': self.db.database_dir,
            'config_dir': self.config_dir,
            'domain': urls.get_app_domain_name(APP_NAME)
        }
        gen.generate_files(templates_path, self.config_dir, variables)

        fs.makepath(join(self.common_dir, 'log'))
        fs.makepath(join(self.common_dir, 'nginx'))
        fs.makepath(join(self.data_dir, 'data'))

        check_output('mv {0}/config.php {1}/data'.format(self.config_dir, self.data_dir), shell=True)
        self.fix_permissions()

    def install(self):
        self.install_config()
        self.db.init()
        self.db.init_config()

    def pre_refresh(self):
        self.db.backup()

    def post_refresh(self):
        self.install_config()

        self.db.remove()
        self.db.init()
        
        self.db.init_config()

    def configure(self):
        
        if path.isfile(self.install_file):
            self.upgrade()
        else:
            self.initialize()
        
        app_storage_dir = storage.init_storage(APP_NAME, USER_NAME)
        
        self.on_domain_change()

    def installed(self):
        return 'installed' in open(self.grocy_config_file).read().strip()

    def upgrade(self):
        self.db.restore()
        self.prepare_storage()

    def initialize(self):
        self.prepare_storage()
        app_storage_dir = storage.init_storage(APP_NAME, USER_NAME)
        self.db.execute('postgres', DB_USER, "ALTER USER {0} WITH PASSWORD '{1}';".format(DB_USER, DB_PASSWORD))
        self.db.execute('postgres', DB_USER, "CREATE DATABASE grocy OWNER {0} TEMPLATE template0 ENCODING 'UTF8';".format(DB_USER))
        self.db.execute('postgres', DB_USER, "GRANT CREATE ON SCHEMA public TO {0};".format(DB_USER))
        with open(self.install_file, 'w') as f:
            f.write('installed\n')


    def on_disk_change(self):
        
        self.prepare_storage()
        service.restart(SYSTEMD_PHP_FPM)
        service.restart(SYSTEMD_NGINX)

    def prepare_storage(self):
        app_storage_dir = storage.init_storage(APP_NAME, USER_NAME)
        
    def on_domain_change(self):
        app_domain = urls.get_app_domain_name(APP_NAME)

    def backup_pre_stop(self):
        self.pre_refresh()

    def restore_pre_start(self):
        self.post_refresh()

    def restore_post_start(self):
        self.configure()

    def fix_permissions(self):
        check_output('chown -R {0}.{0} {1}'.format(USER_NAME, self.common_dir), shell=True)
        check_output('chown -R {0}.{0} {1}/'.format(USER_NAME, self.data_dir), shell=True)

