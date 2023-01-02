import hashlib
import logging

log = logging.getLogger("password_algo")
log.setLevel('INFO')

def generate_hashed_password(username, password, application):
    password_bytes = str(password).encode()

    # todo get salt from secrets manager
    salt = "3242423m23423l423432424352dddd!4"

    log.warning(f'SECURTY_WARNING: Hard-coded salt.  be sure to add this to secrets manager!')

    # add a little something special to the salt to make sure it's unique per user
    salt = f"{salt}{application}{username}"
    salt_version = "v1.0"
    hashed = hashlib.sha384(str(f'{password}{salt}').encode())
    hashed_password = hashed.hexdigest()

    return hashed_password