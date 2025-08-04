import secrets
import string
import re


def slugify(text):
    """
    Converte um texto em um slug seguro para URLs.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


def random_slug(k=8):
    """
    Gera um slug aleatório com letras minúsculas e números.
    """
    chars = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(k))
