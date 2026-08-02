def gcd(a: int, b: int) -> int:
    if a <= 0 or b <= 0:
        raise ValueError("a and b must be positive integers")
    while b:
        a, b = b, a % b
    return a
