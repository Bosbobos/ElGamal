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
    minc, maxc = 2**32, 2**48-1
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

def new_xab(x, a, b, g, p, delta):
    if x % 3 == 0:
        xi = mod_pow(x, 2, p)
        ai = 2 * a % (p-1)
        bi = 2 * b % (p-1)
    elif x % 3 == 1:
        xi = (x * g) % p
        ai = (a + 1) % (p-1)
        bi = b
    else:
        xi = (x * delta) % p
        ai = a
        bi = (b + 1) % (p-1)

    return xi, ai, bi

def pollard_rho(g, p, delta):
    x, a, b = 1, 0, 0
    X, A, B = x, a, b
    for i in range(1, p):
        x, a, b = new_xab(x, a, b, g, p, delta)
        X, A, B = new_xab(X, A, B, g, p, delta)
        X, A, B = new_xab(X, A, B, g, p, delta)

        if x == X:
            r = (B - b) % (p-1)
            if r == 0 or a == A:
                raise Exception('No solution found')
            gcd, x, y = euclidean_extended(r, p-1)
            if gcd == 1:
                return [(mod_inv(B - b, p-1) * (a - A)) % (p-1)]
            else:
                x0 = (x * ((a - A) // gcd)) % (p - 1)
                solutions = [(x0 + k * ((p - 1) // gcd)) % (p - 1) for k in range(g)]
                return sorted(solutions)
