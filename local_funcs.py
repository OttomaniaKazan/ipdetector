import configparser
import json
import os

from entities import UserIp

def ask_tokens():
    """" Получение и сохранение токенов сайта в файл конфигурации """
    config = configparser.ConfigParser()
    if not os.path.exists('config.ini'):
        ask_ipinfo_token()
        ask_ya_disk_token()
    else:
        with open('config.ini', 'r', encoding='utf-8') as f:
            config.read_file(f)
        all_sections = config.sections()
        if 'ipinfo.io' not in all_sections:
            ask_ipinfo_token()
        if 'ya_disk' not in all_sections:
            ask_ya_disk_token()

    return print("Настройки доступов получены")

def ask_ipinfo_token():
    """ Диалоговая функция для записи ipinfo токена """
    config = configparser.ConfigParser()
    print("===== Для первоначальной настройки зарегистрируйтесь на "
          "сайте https://ipinfo.io/ ======")
    token_ipinfo = input("Введите API Token со "
                         "страницы https://ipinfo.io/dashboard: ")
    config['ipinfo.io'] = {}
    config['ipinfo.io']['token'] = token_ipinfo
    with open('config.ini', 'a', encoding='utf-8') as f:
        config.write(f)

def ask_ya_disk_token():
    """ Диалоговая функция для записи ya_disk токена """
    config = configparser.ConfigParser()
    print("===== Зарегистрируйтесь и получите OAuth-токен "
          "на https://yandex.ru/dev/disk/poligon/ ======")
    token_yadisk = input("Введите ваш OAuth-токен: ")
    config['ya_disk'] = {}
    config['ya_disk']['token'] = token_yadisk
    with open('config.ini', 'a', encoding='utf-8') as f:
        config.write(f)

def delete_config():
    """ Удаление файла config.ini """
    delete_cfg = input('Хотите удалить токены доступа?(y/n): ')
    while delete_cfg != 'y' or delete_cfg != 'n':
        if delete_cfg == 'y':
            if os.path.exists('config.ini'):
                os.remove('config.ini')
            exit()
        elif delete_cfg == 'n':
            print('Файл config.ini сохранен. '
                  'Не публикуйте его в открытый доступ!')
            exit()
        else:
            print('Можно ввести только y или n, попробуйте еще раз')

def delete_json_file(data_file):
    os.remove(data_file)

def get_token_ipinfo():
    """ Получение токена ipinfo из файла config.ini """
    config = configparser.ConfigParser()
    with open('config.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)

    if 'ipinfo.io' in config:
        return config['ipinfo.io']['token']
    else:
        return None

def get_token_yadisk():
    """ Получение токена ya_disk из файла config.ini """
    config = configparser.ConfigParser()
    with open('config.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)

    if 'ya_disk' in config:
        return config['ya_disk']['token']
    else:
        return None

def write_json_file(city_by_ip: UserIp):
    """ Запись в json файл ip(ключ) и город(значение) пользователя"""
    json_data = {
        city_by_ip.ip: city_by_ip.city
    }

    with open('city_by_ip.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False)