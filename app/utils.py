from passlib.context import CryptContext

pass_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_pass(password):
    return pass_context.hash(password)


def verify_pass(password, hashed_pass):
    return pass_context.verify(password, hashed_pass)
