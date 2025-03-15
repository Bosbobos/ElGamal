import random

def euclidean_extended(a: int, b: int) -> \
        (int, int, int, int, int):
    x2, x1, y2, y1 = 1, 0, 0, 1
    while b > 0:
        q = a // b
        r = a - q * b
        x = x2 - q * x1
        y = y2 - q * y1

        a, b = b, r
        x2, x1 = x1, x
        y2, y1 = y1, y

    return a, x2, y2

def mod_inv(num: int, p: int) -> int:
    d, x, y = euclidean_extended(p, num)

    if d % p != 1:
        raise Exception(f'{num}**-1 mod {p} does not exist')

    return y % p

def mod_pow(num: int, exp: int, p: int) -> int:
    if exp == -1:
        return mod_inv(num, p)
    if exp == 0:
        return 1

    num, exp = num % p, exp % p
    b = 1
    k = reversed(bin(exp)[2:])
    for x in k:
        if x == '1':
            b = (b % p * num % p) % p
        num = num ** 2 % p

    return b

def get_g(p: int) -> int:
    phi = p - 1
    phi_sqrt = int(phi**0.5)
    i = 2
    prime_divisors = set()
    while i <= phi_sqrt:
        if phi % i == 0:
            prime_divisors.add(i)
            prime_divisors.add(phi // i)
        i += 1

    g = 2
    while g < phi_sqrt:
        if all(mod_pow(g, phi // d, p) != 1 for d in prime_divisors):
            return g
        g += 1

    return None

def ferma_prime_test(n: int, k=12) -> bool:
    """
    Тест Ферма для проверки простоты числа.
    n - число для проверки
    k - количество итераций теста (чем больше, тем точнее проверка)
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, n - 2)
        if mod_pow(a, n - 1, n) != 1:
            return False

    return True

def get_random_prime() -> int:
    minc, maxc = 2**4, 2**8-1
    candidate = random.randint(minc, maxc)
    while not ferma_prime_test(candidate):
        candidate = random.randint(minc, maxc)

    return candidate

def string_to_binary(text):
    return ''.join(bin(ord(i))[2:].zfill(8) for i in text)

def binary_to_string(binary):
    return ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8))

def string_to_int(text):
    return int(string_to_binary(text), 2)

def int_to_string(integer):
    binary = bin(integer)[2:]
    return binary_to_string(binary.zfill(len(binary) + len(binary) % 8))

def pollard_rho(g, p, delta):
    s1 = p // 3
    s2 = s1 * 2
    x, a, b = [1], [0], [0]
    for i in range(1, p):
        if 0 <= x[i-1] < s1:
            xi = x[i-1] * delta % p
            ai = a[i-1]
            bi = (b[i-1] + 1) % p
        elif s1 <= x[i-1] < s2:
            xi = mod_pow(x[i-1], 2, p)
            ai = 2 * a[i-1] % p
            bi = 2 * b[i-1] % p
        else:
            xi = x[i-1] * g
            ai = (a[i-1] + 1) % p
            bi = b[i-1]

        x.append(xi)
        a.append(ai)
        b.append(bi)

        if i % 2 == 0:
            if x[i] == x[i//2]:
                r = (b[i//2] - b[i]) % p
                if r == 0:
                    raise Exception('Algortihm failed')
                x = mod_inv(r, p) * (a[i] - a[i//2]) % p

                return x

p = get_random_prime()
g = get_g(p)
delta = g ** 7 % p
print(p, g, pollard_rho(g, p, delta))
