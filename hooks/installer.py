import logging
from os import path
from os.path import join
from subprocess import check_output

from syncloudlib import fs, linux, gen, logger
from syncloudlib.application import paths, urls, storage, service

APP_NAME = 'grocy'
USER_NAME = APP_NAME
CRON_USER = APP_NAME

SYSTEMD_NGINX = '{0}.nginx'.format(APP_NAME)
SYSTEMD_PHP_FPM = '{0}.php-fpm'.format(APP_NAME)

class Installer:
    def __init__(self):
        if not logger.factory_instance:
            logger.init(logging.DEBUG, True)

        self.log = logger.get_logger('grocy_installer')
        self.app_dir = paths.get_app_dir(APP_NAME)
        self.common_dir = paths.get_data_dir(APP_NAME)
        self.data_dir = join('/var/snap', APP_NAME, 'current')
        self.config_dir = join(self.data_dir, 'config')
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

    def pre_refresh(self):
        pass

    def post_refresh(self):
        self.install_config()

    def configure(self):
        
        if path.isfile(self.install_file):
            self.upgrade()
        else:
            self.initialize()
        
        app_storage_dir = storage.init_storage(APP_NAME, USER_NAME)
        
        self.on_domain_change()

    def upgrade(self):
        self.prepare_storage()

    def initialize(self):
        self.prepare_storage()
        app_storage_dir = storage.init_storage(APP_NAME, USER_NAME)
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

