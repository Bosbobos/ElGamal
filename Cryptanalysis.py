import Utils as u
from ElGamal import ElGamal
from math import ceil


class Cryptanalysis(ElGamal):
    def __init__(self, p, g, public_key):
        self.p = p
        self.g = g
        self._ElGamal__public_key = public_key
        self._ElGamal__private_key = u.pollard_rho(self.g, self.p, self._ElGamal__public_key)

    def decrypt_message(self, encrypted):
        possible_messages = []
        for possible_key in self._ElGamal__private_key:
            message = ''
            for c1, c2 in encrypted:
                m = c2 * u.mod_inv(u.mod_pow(c1, possible_key, self.p), self.p) % self.p
                bin_m = bin(m)[2:]
                message += u.binary_to_string(bin_m.zfill(ceil(len(bin_m) / 8) * 8))
            possible_messages.append(message)
        return possible_messages
