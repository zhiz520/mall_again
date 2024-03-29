from cryptography.fernet import Fernet
# from zhiz_mall import settings

key = b'AgTkpqEkmH0nUtUdtml-HKJ2Oeamz_B6SjPL8G6rrxA='
# print(Fernet.generate_key())


def crypt_encode(opendi, key=key):
    a = Fernet(key)
    b = a.encrypt(str(opendi).encode())
    return b


def crypt_decode(opendi, key=key):
    a = Fernet(key)
    b = a.decrypt(opendi)
    return b
