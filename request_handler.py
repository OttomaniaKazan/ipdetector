import time
import requests
from requests import HTTPError
from requests.exceptions import RequestException, Timeout


class SafeRequest:
    """
        Общий класс для обработки исключений
        при работе с библиотекой requests
    """

    def __init__(self, url, method, params=None, max_retries=5):
        if params is None:
            params = {}
        self.url = url
        self.method = method
        self.params = params
        self.max_retries = max_retries

    def request_handler(self):
        """ Метод для обработки запроса объекта класса """
        backoff_factor = 0.5
        retries = 0
        while retries <= self.max_retries:
            try:
                response = requests.request(self.method, self.url,
                                            params=self.params, timeout=20)
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
                if e.response.status_code >= 500:
                    # Серверные ошибки
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

    def return_json(self):
        return self.request_handler().json()