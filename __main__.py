from ElGamal import ElGamal
from Cryptanalysis import Cryptanalysis
import Utils as u

p = u.get_random_prime()
g = u.get_g(p)

a = ElGamal(p, g)
b = ElGamal(p, g)

message = 'hello! how are you doing today? hope everything\'s ok!'
encrypted = a.encrypt_message(message, b.get_public_key())
decrypted = b.decrypt_message(encrypted)
print(decrypted)
hacker = Cryptanalysis(p, g, b.get_public_key())
hacked = hacker.decrypt_message(encrypted)
print(hacked)
