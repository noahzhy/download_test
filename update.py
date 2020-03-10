import os
import requests
import json
from configparser import ConfigParser


config_file = 'config.ini'
config = ConfigParser()
config.read(config_file, encoding='UTF-8')
local_version = config['update_config']['version']
domain = config['update_config']['domain']
update_file = config['update_config']['update_file']

class Update():
    def __init__(self):
        version = local_version
        file_list = []
        try:
            url = 'http://{}/{}'.format(domain, update_file)
            sess = requests.Session()
            r = sess.post(url=url, timeout=10)
            if r.status_code == 200:
                j = r.json()
                version = j['version']
                if len(j['file_list']) > 0:
                    file_list = j['file_list']
        except Exception as e:
            print(e)

        self.version = version
        self.file_list = file_list

    def get_newest_version(self):
        return self.version

    def get_file_list(self):
        return self.file_list


def download_files(file_list):
    def download_big_file(file_name):
        try:
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
    file_list = update_json.get_file_list()

    if download_files(file_list):
        config = ConfigParser()
        config.read(config_file)
        config.set('update_config', 'version', update_json.get_newest_version())
        with open(config_file, 'w') as cf:
            config.write(cf)


if __name__ == "__main__":
    update_json = Update()
    newest_version = update_json.get_newest_version()

    if local_version < newest_version:
        run()