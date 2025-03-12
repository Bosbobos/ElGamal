import random

def get_g(p: int):
    phi = p - 1
    i = 2
    prime_divisors = set()
    while i * i <= phi:
        if phi % i == 0:
            prime_divisors.add(i)
            prime_divisors.add(phi // i)
        i += 1
    g = int(phi**0.5)
    while g >= 2:
        if all(pow(g, phi // d, p) != 1 for d in prime_divisors):
            return g
        g -= 1
    return None

def ferma_prime_test(n: int, k=12):
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
        if pow(a, n - 1, n) != 1:
            return False
    return True

def get_random_prime():
    candidate = random.randint(2**32, 2**48-1)
    while not ferma_prime_test(candidate):
        candidate = random.randint(2**32, 2**48-1)

    return candidate

p = get_random_prime()
g = get_g(p)
print(p, g)