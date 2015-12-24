# -*- coding: utf-8 -*-

from fabric.api import *

# the user to use for the remote commands
env.user = 'probiche'
# the servers where the commands are executed
env.hosts = ['webarch.cs.prv']

project_root = '/srv/nts_projects/2015/inplace'
app_dir = '%s/app' % project_root
config_dir = '%s/config' % project_root
project_repo = 'https://github.com/DrDoodlez/InPlace.git'
deploy_branch = 'deploy'
uwsgi_config = '/etc/uwsgi/vassals/inplace.ini'

def bootstrap():
    # Создать каталог проекта
    run('mkdir %s' % project_root)

    # Создать каталог для приложения
    run('mkdir %s' % app_dir)
    
    # Создать каталог для конфигов
    run('mkdir %s' % config_dir)
    
    # Развернуть deploy-ветку репозитория в каталоге приложения
    run('git clone -b %s %s %s' % (deploy_branch, project_repo, app_dir))

    # Инициализировать virtualenv в каталоге проекта
    with cd(app_dir):
        run('virtualenv venv')

def deploy():
    # Скопировать конфиг приложения на сервер
    put('config/production.cfg', config_dir)

    # В каталоге приложения
    with cd(app_dir):
        # Получить свежее состояние репозитория
        run('git pull')

        # Убедиться что находимся на ветке deploy
        run('git checkout %s' % deploy_branch)

        with shell_env(INPLACE_SETTINGS='%s/production.cfg' % config_dir):
            with prefix('source venv/bin/activate'):
                # Установить новую версию проекта
                run('python setup.py install')
            
                # Применить новые миграции БД
                run('alembic upgrade head')

    # Скопировать конфиг uwsgi на сервер
    put('config/uwsgi.ini', uwsgi_config)
    
