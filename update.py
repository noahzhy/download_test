import os
import requests
import json
from configparser import ConfigParser


config_file = 'config.ini'

def get_newest_version():
    local_version, domain, update_file = load_config(config_file)

    try:
        url = 'http://{}/{}'.format(domain, update_file)
        sess = requests.Session()
        r = sess.post(url=url)

        if r.status_code == 200:
            j = r.json()
            return j['version']

    except Exception as e:
        print(e)
        return local_version


def load_config(config_file):
    config = ConfigParser()
    config.read(config_file, encoding='UTF-8')
    version = config['update_config']['version']
    domain = config['update_config']['domain']
    update_file = config['update_config']['update_file']
    return (version, domain, update_file)


def get_file_list():
    _, domain, file_list = load_config(config_file)
    url = 'http://{}/{}'.format(domain, file_list)
    file_list = []

    try:
        sess = requests.Session()
        r = sess.post(url=url)
        if r.status_code == 200:
            j = r.json()
            if len(j['file_list']) > 0:
                file_list = j['file_list']

    except Exception as e:
        print(e)

    return file_list


def update_or_not():
    local_version, _, _ = load_config(config_file)
    newest_version = get_newest_version()
    return True if local_version < newest_version else False


def download_files(file_list):
    def download_big_file(file_name):
        try:
            _, domain, _ = load_config(config_file)
            url = 'http://{}/{}'.format(domain, file_name)
            r = requests.get(url, stream=True)
            with open(file_name, "wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        pdf.write(chunk)
            return True
        except Exception as e:
            print(e)
            return False

    file_counter = 0

    for i in file_list:
        if download_big_file(i):
            file_counter += 1
            print(i, 'downloaded')

    return True if file_counter == len(file_list) else False


def run():
    fl = get_file_list()

    if download_files(fl):
        config = ConfigParser()
        config.read(config_file)
        config.set('update_config', 'version', get_newest_version())
        with open(config_file, 'w') as cf:
            config.write(cf)


if __name__ == "__main__":
    if update_or_not():
        run()