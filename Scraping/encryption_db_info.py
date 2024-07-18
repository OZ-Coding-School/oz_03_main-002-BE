from cryptography.fernet import Fernet


def encrypt_config(config_file, key_file):
    with open(key_file, "rb") as f:
        key = f.read()
    fernet = Fernet(key)

    with open(config_file, "rb") as f:
        original_config = f.read()
    encrypted_config = fernet.encrypt(original_config)

    with open(config_file + ".enc", "wb") as f:
        f.write(encrypted_config)


encrypt_config("config.json", "config.key")
encrypt_config("config_test.json", "config.key")
