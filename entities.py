import requests
import ipinfo
from ipinfo.error import APIError


class UserIp:
    """ Объект класса получает IP с сайта ipify.org и
        с помощью сайта ipinfo.io может вернуть город
        по IP
    """
    __base_url = 'https://api.ipify.org/'

    def __init__(self, token):
        self.__token = token
        self.ip = self._get_ip()
        self.city = self._get_city_by_ip()

    def _get_ip(self) -> str:
        """ Получаем сведения об IP """
        params = {
            'format': 'json'
        }
        response = requests.get(self.__base_url, params=params)
        return response.json()['ip']

    def get_ip_info(self) -> None:
        print(f"Ваш IP: {self.ip}")
        print(f"Ваш город: {self.city}")

    def _get_city_by_ip(self) -> str:
        """ Возвращает название города по значению IP """
        try:
            handler = ipinfo.getHandler(self.__token)
            details = handler.getDetails(self.ip)
        except APIError:
            print("Введен неправильный токен")
            exit()
        return details.city

class YaDiskWorks:
    """ Класс для работы с Яндекс диском """
    __base_url = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        self.__headers = {'Authorization': f'OAuth {token}'}
        self.path = self._get_name_folder()

    def _get_name_folder(self):
        path = input("Введите название папки: ")
        return path

    def create_folder(self):
        """ Создание папки на Яндекс диск"""
        create_url = f'{self.__base_url}/v1/disk/resources'
        params = {
            'path': self.path
        }
        response = requests.get(create_url, params=params,
                                headers=self.__headers)
        if response.status_code == 404:
            response = requests.put(create_url, params=params,
                                    headers=self.__headers)
            if response.status_code == 201:
                print(f"Папка {self.path} создана на Я.Диске")
            else:
                print(f"Внимание! Ошибка создания папки {response.status_code}: "
                      f"{response.json()['description']}")
                exit()
        else:
            pass

    def get_link_upload_file(self, path_to_file):
        """ Загрузка файла на Яндекс диск """
        upload_url = f'{self.__base_url}/v1/disk/resources/upload'
        params = {
            'path': f'{self.path}/{path_to_file}',
            'overwrite': True
        }
        response = requests.get(upload_url, params=params,
                                headers=self.__headers)
        if response.status_code == 200:
            print('Получена ссылка для загрузки файла')
            return response.json()['href']
        else:
            print(f"Внимание! Ошибка получения ссылки {response.status_code}: "
                  f"{response.json()['description']}")
            exit()

    def upload_file(self, ya_upload_link, path_to_file):
        """ Загрузка файла на диск """
        with open(path_to_file, 'r') as f:
            headers = {
                'Content-Type': 'application/json'
            }
            data = f.read()
            response = requests.put(ya_upload_link, data=data, headers=headers)
        if response.status_code == 201:
            print('Файл успешно загружен')
        else:
            print(f"Внимание! Ошибка загрузки {response.status_code}: "
                  f"{response.json()['description']}")
            exit()