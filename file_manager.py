import os
import time
import datetime
from random import randint

import requests


class FileManager:

    def __init__(self) -> None:
        self.check_file()
        self.set_file_content()

    def check_file(self):
        """检查we_dog.txt文件信息"""
        file_path = os.path.abspath(__file__)
        self.module_path = os.path.split(file_path)[0]
        print(self.module_path)
        self.download_data_path = os.path.join(self.module_path, 'download_data')
        print(self.download_data_path)
        if not os.path.isdir(self.download_data_path):
            os.mkdir(self.download_data_path)
        self.dog_txt_path = os.path.join(self.download_data_path, 'dog.txt')
        if not os.path.isfile(self.dog_txt_path):
            self.download_file()
            return
        if self.check_version():
            self.download_file()
        return True

    def download_file(self):
        request = requests.get('http://download.kway.site/we_dog_bot/dog.txt')
        with open(self.dog_txt_path, 'wb') as f:
            f.write(request.content)

    def check_version(self):
        request = requests.get('http://download.kway.site/we_dog_bot/version.txt')
        remote_version = float(request.text)
        with open(self.dog_txt_path, 'r', encoding='utf-8') as f:
            local_version = float(f.readline().split('=')[-1])
        return remote_version != local_version

    def set_file_content(self):
        with open(self.dog_txt_path, 'r', encoding='utf-8') as f:
            content_list = f.readlines()
            content_list.pop(0)
            self.content_list = content_list

    def get_random_words(self):
        random_int = randint(0, len(self.content_list)-1)
        random_words = self.get_today_desc() + '\n' + self.content_list[random_int]
        return random_words

    def get_time_desc(self):
        today = datetime.datetime.today()
        today_str = today.strftime("%Y年%m月%d日")
        return today_str

    def get_today_desc(self):
        weathers = ['晴', '雨', '阴']
        return self.get_time_desc() + ' ' + weathers[randint(0, len(weathers) - 1)]
