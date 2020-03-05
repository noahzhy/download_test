import os
import requests
import json
from configparser import ConfigParser


def check_version():
    local_version, domain, update_ini = load_config(config_file='config.ini')
    def get_newest_version():
        try:
            url = 'http://{}/{}'.format(domain, update_ini)
            sess = requests.Session()
            r = sess.post(url=url)

            if r.status_code == 200:
                j = r.json()
                return j['version']

        except Exception as e:
            print(e)
            pass

    newest = get_newest_version()
    if (local_version < newest):
        return True
    else:
        return False


def load_config(config_file):
    config = ConfigParser()
    config.read(config_file, encoding='UTF-8')
    version = config['update_config']['version']
    domain = config['update_config']['domain']
    file_list = config['update_config']['file_list']
    return (version, domain, file_list)


def get_file_list(url):
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


def download_files(file_list):
    def download_big_file(domain, file_name):
        try:
            url = 'http://{}/{}'.format(domain, file_name)
            r = requests.get(url, stream=True)
            with open(file_name, "wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        pdf.write(chunk)
        except Exception as e:
            print(e)

    file_counter = 0
    _, domain, _ = load_config(config_file='config.ini')

    for i in file_list:
        print(domain, i)
        file_counter += 1
        download_big_file(domain, i)

    return True if file_counter == len(file_list) else False


def run():
    _, domain, file_list = load_config(config_file='config.ini')
    api = 'http://{}/{}'.format(domain, file_list)
    fl = get_file_list(api)
    download_files(fl)


if __name__ == "__main__":
    # run()
    if check_version():
        run()