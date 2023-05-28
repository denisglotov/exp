#!/usr/bin/env python3
#
# Restore ECDSA private key from two signatures with same r component
# https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm#Signature_generation_algorithm
#
# Code inspired by
# https://github.com/andreacorbellini/ecc/blob/master/scripts/ecdsa.py
# https://andrea.corbellini.name/2015/05/17/elliptic-curve-cryptography-a-gentle-introduction
# https://habr.com/ru/articles/335906

import collections

EllipticCurve = collections.namedtuple('EllipticCurve', 'name p a b g n h')

curve = EllipticCurve(
    'secp256k1',
    # Field characteristic.
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    # Curve coefficients.
    a=0,
    b=7,
    # Base point.
    g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
       0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    # Subgroup order.
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    # Subgroup cofactor.
    h=1,
)


# Modular arithmetic ##########################################################

def inverse_mod(k, p):
    """Returns the inverse of k modulo p.

    This function returns the only integer x such that (x * k) % p == 1.

    k must be non-zero and p must be a prime.
    """
    if k == 0:
        raise ZeroDivisionError('division by zero')

    if k < 0:
        # k ** -1 = p - (-k) ** -1  (mod p)
        return p - inverse_mod(-k, p)

    # Extended Euclidean algorithm.
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, k

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    gcd, x, y = old_r, old_s, old_t

    assert gcd == 1
    assert (k * x) % p == 1

    return x % p


# Functions that work on curve points #########################################

def is_on_curve(point):
    """Returns True if the given point lies on the elliptic curve."""
    if point is None:
        # None represents the point at infinity.
        return True

    x, y = point

    return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0


def point_neg(point):
    """Returns -point."""
    assert is_on_curve(point)

    if point is None:
        # -0 = 0
        return None

    x, y = point
    result = (x, -y % curve.p)

    assert is_on_curve(result)

    return result


def point_add(point1, point2):
    """Returns the result of point1 + point2 according to the group law."""
    assert is_on_curve(point1)
    assert is_on_curve(point2)

    if point1 is None:
        # 0 + point2 = point2
        return point2
    if point2 is None:
        # point1 + 0 = point1
        return point1

    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2 and y1 != y2:
        # point1 + (-point1) = 0
        return None

    if x1 == x2:
        # This is the case point1 == point2.
        m = (3 * x1 * x1 + curve.a) * inverse_mod(2 * y1, curve.p)
    else:
        # This is the case point1 != point2.
        m = (y1 - y2) * inverse_mod(x1 - x2, curve.p)

    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = (x3 % curve.p,
              -y3 % curve.p)

    assert is_on_curve(result)

    return result


def scalar_mult(k, point):
    """Returns k * point computed using the double and point_add algorithm."""
    assert is_on_curve(point)

    if k % curve.n == 0 or point is None:
        return None

    if k < 0:
        # k * point = -k * (-point)
        return scalar_mult(-k, point_neg(point))

    result = None
    addend = point

    while k:
        if k & 1:
            # Add.
            result = point_add(result, addend)

        # Double.
        addend = point_add(addend, addend)

        k >>= 1

    assert is_on_curve(result)

    return result


# Restore arithmetic ##########################################################
# Signature 1 is (v, r, s) for hash z
# Signature 2 is (v2, r, s2) for hash z2

# Hashes
z = 0xe21147eaadd6f5b9439ebee73487f91963f71c2e5b67accf93661063bb41336a
z2 = 0x25c1050314a89c7d6a9c227984efcff0ebd77c7c1ef51ce05a6725c8dad2424f
delta_z = z - z2
assert(delta_z < curve.n)

# Signatures s components
s = 0x52c7a64295a40df7c76452ecd3ab3244a5242947140f8899568e3e111a773baa
s2 = 0x15ce61a661c6fcb7ea0f319028b89fa0630913ec6f19e9ad103664877de44c16
delta_s = s - s2
assert(delta_s < curve.n)

# Signature r component
r = 0x4d3dcf1e3ba2082e34b8b00332fb514af03430b9544eef450afebd27c3330a30

inv_delta_s = inverse_mod(delta_s, curve.n)
assert(inv_delta_s * delta_s % curve.n == 1);

k = (delta_z * inv_delta_s) % curve.n;
print("k = ", hex(k));

# pt = scalar_mult(k, curve.g)
# r = pt[0] % curve.n
# print("r = ", hex(r))

inv_r = inverse_mod(r, curve.n)
n = (s * k) % curve.n
assert(curve.n + n > z);

priv = (curve.n + n - z) * inv_r % curve.n
print("priv = ", hex(priv))
