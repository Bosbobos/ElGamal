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

#TODO: добавить операцию ввода приватного ключа вместо генерации нового
operations = ('Выберите операцию:\n'
              '0: Смена p и g\n'
              '1: Смена g\n'
              '2: Зашифрование сообщения\n'
              '3: Расшифрование сообщения от лица законного пользователя\n'
              '4: Расшифрование сообщения от лица злоумышленника\n'
              '5: Выход\n')

def input_p():
    messages = message_p
    while True:
        key = input(messages[0])
        if key == '0':
            key = u.get_random_prime()
            print(f'{messages[1]} {key}')
            return key
        elif u.ferma_prime_test(int(key)):
            return key
        else:
            print(messages[3])

def input_g(p: int):
    messages = message_g
    while True:
        key = input(messages[0])
        if key == '0':
            key = u.get_g(p)
            print(f'{messages[1]} {key}')
            return key
        elif u.check_g(p, int(key)):
            return key
        else:
            print(messages[3])

def create_elgamal(p: int, g: int) -> ElGamal:
    elgamal = ElGamal(p, g)
    print(f'Схема Эль-Гамаля успешно инициализирована, открытый ключ: {elgamal.get_public_key()}')

    return elgamal

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
    p = input_p()
    g = input_g(p)
    elgamal = create_elgamal(p, g)

    op = input(operations)
    while op != '5':
        if op == '0':
            p = input_p()
            g = input_g(p)
            elgamal = create_elgamal(p, g)
        elif op == '1':
            g = input_g(p)
            elgamal = create_elgamal(p, g)
        elif op == '2':
            public_key = int(input('Введите открытый ключ: '))
            message = input('Введите сообщение: ')
            print(elgamal.encrypt_message(message, public_key))
        elif op == '3':
            message = parse_nested_list(input('Введите шифротекст: '))
            print(elgamal.decrypt_message(message))
        elif op == '4':
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
