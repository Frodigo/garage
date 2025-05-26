class VigenereCipher:
    @property
    def name(self):
        return "Vigenère"

    @property
    def description(self):
        return "A polyalphabetic substitution cipher that uses a keyword to determine shifting."

    def encrypt(self, text, key):
        return self._process_text(text, str(key), True)

    def decrypt(self, text, key):
        return self._process_text(text, str(key), False)

    def _process_text(self, text, key, encrypt):
        if not text or not key:
            return ""

        result = []
        key_index = 0

        for i in range(len(text)):
            text_char = text[i]

            if not text_char.isalpha():
                result.append(text_char)
                continue

            key_char = key[key_index % len(key)]
            key_index += 1

            shift = ord(key_char.upper()) - ord('A')

            if not encrypt:
                shift = -shift

            base_char = ord('A') if text_char.isupper() else ord('a')

            shifted_char = chr(
                ((ord(text_char) - base_char + shift + 26) % 26) + base_char)
            result.append(shifted_char)

        return ''.join(result)


if __name__ == "__main__":
    cipher = VigenereCipher()

    text = "Hello World!"
    key = "KEY"

    encrypted = cipher.encrypt(text, key)
    decrypted = cipher.decrypt(encrypted, key)

    print(f"Original: {text}")
    print(f"Key: {key}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")

    print("\n=== Another Example ===")
    text2 = "ATTACKATDAWN"
    key2 = "LEMON"

    encrypted2 = cipher.encrypt(text2, key2)
    decrypted2 = cipher.decrypt(encrypted2, key2)

    print(f"Original: {text2}")
    print(f"Key: {key2}")
    print(f"Encrypted: {encrypted2}")
    print(f"Decrypted: {decrypted2}")
