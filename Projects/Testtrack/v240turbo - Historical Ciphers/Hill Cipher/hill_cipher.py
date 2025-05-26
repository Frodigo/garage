import numpy as np


class HillCipher:
    ALPHABET_SIZE = 26
    BASE_CHAR = ord('A')
    PADDING_CHAR = 'X'

    @property
    def name(self):
        return "Hill Cipher"

    @property
    def description(self):
        return ("The Hill cipher is a polygraphic substitution cipher based on linear algebra. "
                "It encrypts blocks of letters using matrix multiplication.")

    def encrypt(self, text, key):
        if not text:
            return ""

        matrix = self._validate_and_convert_key(key)
        matrix_size = len(matrix)

        processed_text = self._prepare_text(text, matrix_size)
        result = []

        for i in range(0, len(processed_text), matrix_size):
            block = processed_text[i:i + matrix_size]
            result.append(self._process_block(block, matrix))

        return ''.join(result)

    def decrypt(self, text, key):
        if not text:
            return ""

        matrix = self._validate_and_convert_key(key)
        matrix_size = len(matrix)

        inverse_matrix = self._calculate_inverse_matrix(matrix)

        processed_text = self._prepare_text(text, matrix_size)
        result = []

        for i in range(0, len(processed_text), matrix_size):
            block = processed_text[i:i + matrix_size]
            result.append(self._process_block(block, inverse_matrix))

        return ''.join(result)

    def _process_block(self, block, matrix):
        size = len(matrix)

        block_values = [ord(char) - self.BASE_CHAR for char in block]

        result_values = []
        for row in range(size):
            value = 0
            for col in range(size):
                value += matrix[row][col] * block_values[col]
            result_values.append(
                self._modulo_positive(value, self.ALPHABET_SIZE))

        return ''.join(chr(self.BASE_CHAR + val) for val in result_values)

    def _validate_and_convert_key(self, key):
        if not isinstance(key, (list, tuple, np.ndarray)):
            raise ValueError(
                "Key must be a square matrix (list of lists) for Hill cipher")

        if isinstance(key, np.ndarray):
            key = key.tolist()

        if not all(len(row) == len(key) for row in key):
            raise ValueError("Matrix must be square for Hill cipher")

        return key

    def _prepare_text(self, text, block_size):
        text = ''.join(char.upper() for char in text if char.isalpha())

        if len(text) % block_size != 0:
            padding_needed = block_size - (len(text) % block_size)
            text += self.PADDING_CHAR * padding_needed

        return text

    def _calculate_inverse_matrix(self, matrix):
        size = len(matrix)

        if size == 1:
            value = matrix[0][0]
            inverse = self._find_modular_multiplicative_inverse(
                value, self.ALPHABET_SIZE)

            if inverse == -1:
                raise ValueError(
                    f"The matrix value {value} is not invertible modulo {self.ALPHABET_SIZE}")

            return [[inverse]]

        if size == 2:
            det = (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0])
            det = self._modulo_positive(det, self.ALPHABET_SIZE)

            det_inverse = self._find_modular_multiplicative_inverse(
                det, self.ALPHABET_SIZE)
            if det_inverse == -1:
                raise ValueError(
                    "The matrix is not invertible modulo 26. Choose a different key.")

            adj = [[matrix[1][1], -matrix[0][1]],
                   [-matrix[1][0], matrix[0][0]]]

            inverse = []
            for i in range(2):
                row = []
                for j in range(2):
                    row.append(self._modulo_positive(
                        adj[i][j] * det_inverse, self.ALPHABET_SIZE))
                inverse.append(row)

            return inverse

        if size == 3:
            a, b, c = matrix[0][0], matrix[0][1], matrix[0][2]
            d, e, f = matrix[1][0], matrix[1][1], matrix[1][2]
            g, h, i = matrix[2][0], matrix[2][1], matrix[2][2]

            det = a * (e * i - f * h) - b * \
                (d * i - f * g) + c * (d * h - e * g)
            det = self._modulo_positive(det, self.ALPHABET_SIZE)

            det_inverse = self._find_modular_multiplicative_inverse(
                det, self.ALPHABET_SIZE)
            if det_inverse == -1:
                raise ValueError(
                    "The 3x3 matrix is not invertible modulo 26. Choose a different key.")

            cofactor = [
                [e * i - f * h, -(d * i - f * g), d * h - e * g],
                [-(b * i - c * h), a * i - c * g, -(a * h - b * g)],
                [b * f - c * e, -(a * f - c * d), a * e - b * d]
            ]

            adj = [[cofactor[j][i] for j in range(3)] for i in range(3)]

            inverse = []
            for row in range(3):
                inverse_row = []
                for col in range(3):
                    inverse_row.append(self._modulo_positive(
                        adj[row][col] * det_inverse, self.ALPHABET_SIZE))
                inverse.append(inverse_row)

            return inverse

        raise NotImplementedError(
            "Matrix inversion for sizes larger than 3x3 is not implemented.")

    def _modulo_positive(self, value, modulo):
        return ((value % modulo) + modulo) % modulo

    def _find_modular_multiplicative_inverse(self, a, m):
        a = self._modulo_positive(a, m)

        m0 = m
        y = 0
        x = 1

        if m == 1:
            return 0

        while a > 1:
            q = a // m
            t = m

            m = a % m
            a = t
            t = y

            y = x - q * y
            x = t

        if x < 0:
            x += m0

        if a != 1:
            return -1

        return x


if __name__ == "__main__":
    cipher = HillCipher()

    text = "HELLO"
    key_2x2 = [[3, 2], [5, 7]]
    key_3x3 = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]

    print("=== 2x2 Matrix Example ===")
    encrypted_2x2 = cipher.encrypt(text, key_2x2)
    decrypted_2x2 = cipher.decrypt(encrypted_2x2, key_2x2)

    print(f"Original: {text}")
    print(f"Key: {key_2x2}")
    print(f"Encrypted: {encrypted_2x2}")
    print(f"Decrypted: {decrypted_2x2}")

    print("\n=== 3x3 Matrix Example ===")
    encrypted_3x3 = cipher.encrypt(text, key_3x3)
    decrypted_3x3 = cipher.decrypt(encrypted_3x3, key_3x3)

    print(f"Original: {text}")
    print(f"Key: {key_3x3}")
    print(f"Encrypted: {encrypted_3x3}")
    print(f"Decrypted: {decrypted_3x3}")
