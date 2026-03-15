import time
import requests
import ipinfo
from ipinfo.error import APIError
from requests import RequestException, HTTPError, Timeout
from request_handler import SafeRequest

class UserIp:
    """
        Объект класса получает IP с сайта ipify.org
    """
    __base_url = 'https://api.ipify.org/'

    def __init__(self):
        self.ip = self._get_ip()

    def _get_ip(self) -> SafeRequest | None:
        """ Получаем сведения об IP """
        params = {
            'format': 'json'
        }
        response = SafeRequest(self.__base_url, 'GET', params)
        if response.request_handler():
            return response
        else:
            return None

    def show_ip(self):
        ip = self._get_ip()
        if ip:
            print(f"Ваш IP: {ip.return_json()['ip']}")
        else:
            print('Невозможно получить информацию об IP')

    def return_ip(self):
        ip = self._get_ip()
        if ip:
            return ip.return_json()['ip']
        else:
            return None

class CityByIp:
    """ Класс для определения города по IP"""
    def __init__(self, token, ip):
        self.__token = token
        self.ip = ip

    def get_city_by_ip(self) -> str:
        """ Возвращает название города по значению IP """
        try:
            handler = ipinfo.getHandler(self.__token)
            details = handler.getDetails(self.ip)
        except APIError:
            print("Введен неправильный токен")
            raise SystemExit()
        return details.city

    def show_city(self):
        print(f"Ваш город: {self.get_city_by_ip()}")

class YaDiskWorks:
    """ Класс для работы с Яндекс диском """
    __base_url = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        self.__headers = {'Authorization': f'OAuth {token}'}
        self.path = self._get_name_folder()

    def _get_name_folder(self):
        path = input("Введите название папки: ")
        return path

    def create_folder(self) -> None:
        """ Создание папки на Яндекс диск"""
        create_url = f'{self.__base_url}/v1/disk/resources'
        params = {
            'path': self.path
        }
        safe_request = YDUploadFile(create_url, 'PUT', None,
                                    self.__headers, params)
        response = safe_request.request_handler()
        if response:
            print(f"Папка {self.path} создана на Я.Диске")

    def get_link_upload_file(self, path_to_file) -> str | None:
        """ Загрузка файла на Яндекс диск """
        upload_url = f'{self.__base_url}/v1/disk/resources/upload'
        params = {
            'path': f'{self.path}/{path_to_file}',
            'overwrite': True
        }
        safe_request = YDUploadFile(upload_url, 'GET', None,
                                    self.__headers, params)
        response = safe_request.request_handler()
        if response.status_code == 200:
            print('Получена ссылка для загрузки файла')
            return response.json()['href']
        else:
            return None

    def upload_file(self, ya_upload_link, path_to_file):
        """ Загрузка файла на диск """
        with open(path_to_file, 'r') as f:
            headers = {
                'Content-Type': 'application/json'
            }
            data = f.read()
            safe_request = YDUploadFile(ya_upload_link, 'PUT', data,
                                    headers, None)
            response = safe_request.request_handler()
        if response.status_code == 201:
            print('Файл успешно загружен')
        else:
            print('Не удалось загрузить файл')


class YDUploadFile(SafeRequest):
    """ Наследный класс для загрузки файла на Яндекс Диск"""

    def __init__(self, url, method, data, headers, params, max_retries=5):
        super().__init__(url, method, params, max_retries)
        self.data = data
        self.headers = headers

    def request_handler(self):
        """ Метод для обработки запроса объекта класса """
        backoff_factor = 0.5
        retries = 0
        while retries <= self.max_retries:
            try:
                response = requests.request(self.method, self.url, data=self.data,
                                            headers=self.headers, params=self.params, timeout=20)
                response.raise_for_status()
                return response
            except (Timeout, ConnectionError) as e:
                # Ошибки тайм-аута и соединения
                retries += 1
                if retries >= self.max_retries:
                    raise SystemExit()
                sleep_time = backoff_factor * (2 ** (retries - 1))
                time.sleep(sleep_time)
                print(f"Попыток {retries}/{self.max_retries} после ошибки {e}")
            except HTTPError as e:
                # Серверные ошибки
                if e.response.status_code >= 500:
                    retries += 1
                    if retries > self.max_retries:
                        raise SystemExit()
                elif 400 <= e.response.status_code < 500:
                    # Клиентская ошибка
                    print(f"Ошибка на стороне клиента: {e}")
                    raise SystemExit()
                sleep_time = backoff_factor * (2 ** (retries - 1))
                time.sleep(sleep_time)
                print(f"Попыток {retries}/{self.max_retries} после ошибки "
                      f"на сервере {e}")
            except RequestException as e:
                # Другие ошибки обработки
                retries += 1
                if retries >= self.max_retries:
                    raise SystemExit()
                sleep_time = backoff_factor * (2 ** (retries - 1))
                time.sleep(sleep_time)
                print(f"Попыток {retries}/{self.max_retries} после ошибки {e}")
        return None