import logging
import time
import argparse
import json
import matplotlib.pyplot as plt
from enumeration import enumerate_number_card
from file_functions import read_data_txt, write_data_txt, read_statistics, write_statistics
from luhn_algorithm import algorithm_luhn

logger = logging.getLogger()
logger.setLevel('INFO')

def read_settings(file_with_settings: str = 'settings.json') -> dict:
    """
    Фукнция считывает настройки из файла
    :param file_with_settings: Путь к файлу с настройками
    :return: Настройки
    """
    settings = None
    try:
        with open(file_with_settings, 'r') as f:
            settings = json.load(f)
        logging.info("Настройки успешно считаны")
    except OSError as err:
        logging.warning(f"{err} Не удалось считать настройки")
    return settings

def create_png_with_statistics(statistics: dict) -> None:
    """
    Функция создает гистограмму со статистикой и сохраняет ее как png файл
    :param statistics: Статистика
    :return: Функция ничего не возвращает
    """
    fig = plt.figure(figsize=(30, 5))
    plt.ylabel('time')
    plt.xlabel('processes')
    plt.title('statistics')
    x = statistics.keys()
    y = statistics.values()
    plt.bar(x, y, color='blue', width=0.5)
    plt.savefig("files/visualization.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-cus', '--custom', type=str,
                        help='Использует пользовательсткий файл с настройками, необходимо указать путь к файлу')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-crd', '--card_number_enumeration', type=int,
                       help='Ищет номер карты с помощью хеша, необходимо указать количество процессов')
    group.add_argument('-sta', '--statistics',
                       help='Получается статистику подбирая номер карты на разном количестве процессов')
    group.add_argument('-lun', '--lunh_algorithm', help='Проверяет валидность номера карты с помощью алгоритма Луна')
    group.add_argument('-vis', '--visualize_statistics', help='Создает гистограмму по имеющейся статистике')
    args = parser.parse_args()
    if args.custom:
        settings = read_settings(args.custom)
    else:
        settings = read_settings()
    if settings:
        if args.card_number_enumeration:
            card_number = enumerate_number_card(settings['hash_file'], settings['bins_file'], settings['last_numbers_file'], args.card_number_enumeration)
            if card_number:
                logging.info(f"Номер карты успешно найден: {card_number}")
                write_data_txt(str(card_number), settings['card_number_file'])
            else:
                logging.info("Не удалось найти номер карты")
        elif args.statistics:
            for i in range(1, 15):
                t1 = time.time()
                enumerate_number_card(settings['hash_file'], settings['bins_file'], settings['last_numbers_file'], i)
                t2 = time.time()
                write_statistics(i, t2 - t1, settings['statistic_file'])
            logging.info("Статистика успешно посчитана")
        elif args.lunh_algorithm:
            card_number = read_data_txt(settings['card_number_file'])
            if algorithm_luhn(card_number):
                logging.info("Номер карты действителен")
            else:
                logging.info("Номер карты не действителен")
        elif args.visualize_statistics:
            create_png_with_statistics(read_statistics(settings['statistic_file']))
            logging.info("Гистограмма успешно создана")