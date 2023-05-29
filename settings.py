import json

settings = {
    'hash_file': '7dbbccf1e06c2ea6c7f7711cb90b08eee16d1476fa0e75067d84a642494589149eba75ba396ad3ccbb9ca9d2fc5340cf',
    'last_numbers_file': '6302',
    'bins_file': ['220015'],
    'card_number_file': 'files/card_number_file.txt',
    'statistic_file': 'files/statistic_file.csv'
}

if __name__ == "__main__":
    with open('settings.json', 'w') as fp:
        json.dump(settings, fp)