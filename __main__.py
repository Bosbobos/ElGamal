from ElGamal import ElGamal
from Cryptanalysis import Cryptanalysis
import Utils as u
import ast

welcome_message = 'Добро пожаловать в программу для работы с криптосистемой Эль-Гамаля!'
message_p = ['Пожалуйста, введите простое число, на основе которого будут производиться операции,'
               ' или 0, чтобы сгенерировать случайное: ',
               'Сгенерированное число:',
               'Введенное число не является простым. Введите простое число или 0 для генерации случайного.']

message_g = ['Пожалуйста, введите параметр домена g, являющийся примитивным корнем по модулю p,'
               ' или 0, чтобы сгенерировать случайный: ',
               'Сгенерированное число:',
               'Введенное число не является примитивным корнем. Введите примитивный корень или 0 для генерации случайного.']

message_keys = ['Введите два целых числа (открытый и закрытый ключ) через пробел, или 0 для генерации: ',
                 'Сгенерированные ключи:',
                 'Некорректный ввод. Введите два целых числа через пробел или 0 для генерации.']

#TODO: добавить операцию ввода приватного ключа вместо генерации нового
operations = ('Выберите операцию:\n'
              '0: Заново инициализировать программу\n'
              '1: Зашифрование сообщения\n'
              '2: Расшифрование сообщения от лица законного пользователя\n'
              '3: Расшифрование сообщения от лица злоумышленника\n'
              '4: Выход\n')

def input_p():
    messages = message_p
    while True:
        key = int(input(messages[0]))
        if key == 0:
            key = u.get_random_prime()
            print(f'{messages[1]} {key}')
            return key
        elif key > 100 and u.ferma_prime_test(key):
            return key
        else:
            print(messages[2])

def input_g(p: int):
    messages = message_g
    while True:
        key = input(messages[0])
        if key == '0':
            key = u.get_g(p)
            print(f'{messages[1]} {key}')
            return key
        elif u.check_g(p, int(key)):
            return int(key)
        else:
            print(messages[2])

def input_keys():
    messages = message_keys
    while True:
        keys = input(messages[0])
        if keys == '0':
            return '0'
        try:
            public_key, private_key = map(int, keys.split())
            return public_key, private_key
        except ValueError:
            print(messages[2])

def create_elgamal() -> ElGamal:
    p = input_p()
    g = input_g(p)
    keys = input_keys()
    if keys == '0':
        elgamal = ElGamal(p, g)
        print(f'Сгенерированный открытый ключ: {elgamal.get_public_key()}')
    else:
        elgamal = ElGamal(p, g, keys[0], keys[1])
    print(f'Схема Эль-Гамаля успешно инициализирована')

    return p, g, elgamal

def parse_nested_list(input_string: str):
    try:
        parsed_list = ast.literal_eval(input_string)
        if isinstance(parsed_list, list) and all(isinstance(sublist, list) for sublist in parsed_list):
            return parsed_list
        else:
            raise ValueError("Invalid format: Input must be a nested list.")
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"Invalid input format: {e}")


if __name__ == '__main__':
    print(welcome_message)
    p, g, elgamal = create_elgamal()

    op = input(operations)
    while op != '4':
        if op == '0':
            elgamal = create_elgamal()
        elif op == '1':
            public_key = int(input('Введите открытый ключ: '))
            message = input('Введите сообщение: ')
            print(elgamal.encrypt_message(message, public_key))
        elif op == '2':
            message = parse_nested_list(input('Введите шифротекст: '))
            print(elgamal.decrypt_message(message))
        elif op == '3':
            public_key = int(input('Введите открытый ключ: '))
            print('Сейчас будет произведен поиск возможных закрытых ключей, подождите...')
            hacker = Cryptanalysis(p, g, public_key)
            message = parse_nested_list(input('Введите шифротекст: '))
            decrypted = hacker.decrypt_message(message)
            for key, message in decrypted:
                print(f'{key}: {message}')
        else:
            print('Выбрана неизвестная операция.')

        op = input(operations)
