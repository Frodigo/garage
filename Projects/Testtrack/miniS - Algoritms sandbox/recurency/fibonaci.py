def fibonacci(n: int) -> int:
    if (n < 2):
        return 1
    else:
        return fibonacci(n - 2) + fibonacci(n - 1)


if __name__ == "__main__":
    print(fibonacci(11))
