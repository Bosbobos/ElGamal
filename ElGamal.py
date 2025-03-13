import Utils as u
import random

class ElGamal:
    def __init__(self, p, g):
        self.p = p
        self.g = g

        self.__generate_keys()

    def __generate_keys(self):
        x = random.randint(1, self.p - 1)
        h = u.mod_pow(self.g, x, self.p)

        self.__private_key = x
        self.__public_key = h

    def get_public_key(self):
        return self.__public_key

    def decrypt_message(self, c1, c2):
        m = c2 // (u.mod_pow(c1, self.__private_key, self.p)) % self.p
        return u.int_to_string(m)

    def encrypt_message(self, message, public_key):
        m = u.string_to_int(message)
        round_key = random.randint(1, self.p - 1)
        c1 = u.mod_pow(self.g, round_key, self.p)
        c2 = m * (u.mod_pow(public_key, round_key, self.p)) % self.p

        return c1, c2

p = u.get_random_prime()
g = u.get_g(p)

a = ElGamal(p, g)
b = ElGamal(p, g)

message = 'hello'
c1, c2 = a.encrypt_message(message, b.get_public_key())
decrypted = b.decrypt_message(c1, c2)
print(decrypted)