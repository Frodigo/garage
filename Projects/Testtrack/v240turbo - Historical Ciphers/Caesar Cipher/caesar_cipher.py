class CaesarCipher:
    @property
    def name(self):
        return "Caesar Cipher"

    @property
    def description(self):
        return ("The Caesar cipher is one of the earliest and simplest encryption techniques. "
                "It works by shifting each letter in the plaintext by a fixed number of positions in the alphabet.")

    def encrypt(self, text, key):
        if not text:
            return ""

        try:
            shift = int(key)
        except (ValueError, TypeError):
            raise ValueError(
                "Key must be convertible to an integer for Caesar cipher")

        result = []

        for input_char in text:
            if input_char.isalpha():
                is_lower = input_char.islower()
                base_char = ord('a') if is_lower else ord('A')

                normalized_char = (ord(input_char) - base_char + shift) % 26

                if normalized_char < 0:
                    normalized_char += 26

                result.append(chr(base_char + normalized_char))
            else:
                result.append(input_char)

        return ''.join(result)

    def decrypt(self, text, key):
        try:
            shift = int(key)
        except (ValueError, TypeError):
            raise ValueError(
                "Key must be convertible to an integer for Caesar cipher")

        return self.encrypt(text, -shift)


if __name__ == "__main__":
    cipher = CaesarCipher()

    text = "Hello World!"
    key = 3

    encrypted = cipher.encrypt(text, key)
    decrypted = cipher.decrypt(encrypted, key)

    print(f"Original: {text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
