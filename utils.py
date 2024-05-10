import string
import secrets

class PasswordLengthError(Exception):
    "Password must be at least 8 characters long."

def generate_password(length: int) -> str:
    """
    Create a random Wialon API compliant password.

    Parameters
    ----------
    length: <int>
        The length of the password.

    Returns
    -------
    password: <str>
        The password.

    Password Requirements
    ---------------------
    - At least one lowercase letter
    - At least one number
    - At least one special character
    - At least one uppercase letter
    - Different from username
    - Minumum 8 charcters

    """
    length += 1

    if length < 8:
        raise PasswordLengthError

    letters: tuple = tuple(string.ascii_letters)
    numbers: tuple = tuple(string.digits)
    symbols: tuple = ("@", "#", "$", "%")

    while True:
        password = "".join(
            secrets.choice(letters + numbers + symbols) for i in range(length)
        )
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
        ):
            break

    return password
