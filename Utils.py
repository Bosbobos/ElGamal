import numpy as np

def find_g(p: np.uint64):
    phi = p - 1
    i = 2
    prime_divisors = set()
    while i * i <= phi:
        if phi % i == 0:
            prime_divisors.add(i)
            prime_divisors.add(phi // i)
        i += 1
    g = 2
    while g * g <= phi:
        if all(pow(g, phi // d, p) != 1 for d in prime_divisors):
            return g
    return None

def ferma_prime_test(n: np.uint64, k=12):
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
        a = np.random.randint(2, n - 2, dtype=np.uint64)
        if np.power(a, n - 1, n) != 1:
            return False
    return True

def get_random_prime():
    candidate = np.random.randint(2**32, 2**64-1, dtype=np.uint64)
    while not ferma_prime_test(candidate):
        candidate = np.random.randint(2**32, 2**64-1, dtype=np.uint64)

    return candidate

print(get_random_prime())