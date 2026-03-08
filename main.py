from entities import UserIp, YaDiskWorks
from local_funcs import get_token_ipinfo, write_json_file, ask_tokens, \
    delete_config, get_token_yadisk, delete_json_file

def main():
    ask_tokens()  # Спрашиваем токены у пользователя
    ipinfo_token = get_token_ipinfo() # Токен ipinfo для работы
    ya_disk_token = get_token_yadisk()  # Токен ya_disk для работы

    city_response = UserIp(ipinfo_token)   # Создаем объект для получения города и ip
    city_response.get_ip_info()     # Выводим на экран информацию о полученных данных
    write_json_file(city_response)  # Записываем json файл
    data_file = 'city_by_ip.json'

    my_disk = YaDiskWorks(ya_disk_token)  # Создание объекта для работы с Яндекс Диском
    my_disk.create_folder()  # Создание папки на Яндекс диске
    ya_folder = my_disk.get_link_upload_file(data_file)  # Получение ссылки для загрузки файла
    my_disk.upload_file(ya_folder, data_file)  # Загрузка файла

    delete_json_file(data_file)  # Удаление локального json файла
    delete_config()  # Удаление config.ini

main()