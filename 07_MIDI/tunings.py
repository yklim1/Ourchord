#!/usr/bin/env python

from fractions import Fraction as F

notes = "C C# D D# E F F# G G# A A# B".split()

pythagoras = [F(1,1), F(2187,2048), F(9,8), F(32,27), F(81,64), F(4,3),
              F(729,512), F(3,2), F(6561,4096), F(27,16), F(16,9), F(243,128)]


just_intonation = [F(1,1), F(16,15), F(9,8), F(6,5), F(5,4), F(4,3),
                   F(7,5), F(3,2), F(8,5), F(5,3), F(9,5), F(15,8)]


kirnberger = [F(1,1), F(256,243), F(9,8), F(32,27), F(5,4), F(4,3),
              F(45,32), F(3,2), F(128,81), F(5,3), F(16,9), F(15,8)]


def scale_freqs(name, base_freq=440):
    return [float(x * base_freq) for x in name]


def harmonic_series(n, fundamental):
    return [fundamental * (x + 1) for x in range(n)]


def gen_csound(freqs):
    print("f1   0    4096 10 1")
    print("i1   0    1    90     {0}".format(freqs[0]))

    for item in freqs[1:]:
        print("i1   +    .    90     {0}".format(item))
