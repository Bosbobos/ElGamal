import Utils as u
import random
from math import floor, ceil

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

    def decrypt_message(self, encrypted):
        message = ''
        for c1, c2 in encrypted:
            m = c2 // (u.mod_pow(c1, self.__private_key, self.p)) % self.p
            bin_m = bin(m)[2:]
            message += u.binary_to_string(bin_m.zfill(ceil(len(bin_m))*8))
        return message

    def encrypt_message(self, message, public_key):
        res = []
        bin_msg = u.string_to_binary(message)
        bytes_in_block = floor(self.p / 255)
        block_num = ceil(len(bin_msg) / 8 / bytes_in_block)
        for i in range(block_num):
            block = bin_msg[i * 8 * bytes_in_block:(i+1) * 8 * bytes_in_block]
            m = int(block, 2)
            round_key = random.randint(1, self.p - 1)
            c1 = u.mod_pow(self.g, round_key, self.p)
            c2 = m * (u.mod_pow(public_key, round_key, self.p)) % self.p
            res.append([c1, c2])

        return res

p = u.get_random_prime()
g = u.get_g(p)

a = ElGamal(p, g)
b = ElGamal(p, g)

message = 'hello'
encrypted = a.encrypt_message(message, b.get_public_key())
decrypted = b.decrypt_message(encrypted)
print(decrypted)