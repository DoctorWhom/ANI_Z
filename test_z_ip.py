# -*- coding: utf-8 -*-
"""
+--------------------------------------------------------------------+
|            ___         ____    ___    ___                          |
|           /   \       |    \  |   |  |   |                         |
|          /  .  \      |     \ |   |  |   |   Seminar               |
|         /  /_\  \     |      \|   |  |   |                         |
|        /   ___   \    |   |\      |  |   |   Angewandte            |
|       /   /   \   \   |   | \     |  |   |   Neuroinformatik       |
|      /___/     \___\  |___|  \____|  |___|                         |
|                                                                    |
+--------------------------------------------------------------------+
|             Checksummen                |    Zusatzaufgabe 1 & 2    |   
+--------------------------------------------------------------------+

Funktionen zur Überprüfung der Lösung auf Korrektheit. 
"""

from evaluation import check_results
import numpy as np

def loesung_z1(result):
    desired_values = check_results.Result([0x183a8e6d, 0x1e8d2a01],
            [0x75a21ab5, 0xaed9c753, 0x8c365bc6, 0x180f2d33])
    mail = check_results.MailContent("markus.eisenbach@tu-ilmenau.de",
            "ANI 2017 Zusatzaufgabe 1", "ani_z.ipynb")
    check_results.check_and_send(result, desired_values, mail)

def loesung_z2(result):
    desired_values = check_results.Result([0xfaa6674, 0x89c8cca3],
            [0xadd2d83d, 0x52a76510, 0xb16d6c2d, 0x5e8643c4])
    mail = check_results.MailContent("markus.eisenbach@tu-ilmenau.de",
            "ANI 2017 Zusatzaufgabe 2", "ani_z.ipynb")
    check_results.check_and_send(result, desired_values, mail)

def loesung_z3(result):
    desired_values = check_results.Result([0x75fe5d72, 0x8feb0be2],
            [0x2631153c, 0x930adb4f, 0xc236bed6, 0x7927943b])
    mail = check_results.MailContent("markus.eisenbach@tu-ilmenau.de",
            "ANI 2017 Zusatzaufgabe 3", "ani_z.ipynb")
    check_results.check_and_send(result, desired_values, mail)

def loesung_z4(result):
    desired_values = check_results.Result([0x49f91e6d, 0x2dd691e],
            [0xd23b9ebc, 0x2123f243, 0xa250a782, 0x79c38da2])
    mail = check_results.MailContent("markus.eisenbach@tu-ilmenau.de",
            "ANI 2017 Zusatzaufgabe 4", "ani_z.ipynb")
    check_results.check_and_send(result, desired_values, mail)

def loesung_z5(result):
    desired_values = check_results.Result([0x2bac15b7, 0x18445ef9],
            [0xcefce918, 0xdd437d27, 0x1612197, 0x170cd9c1])
    mail = check_results.MailContent("markus.eisenbach@tu-ilmenau.de",
            "ANI 2017 Zusatzaufgabe 5", "ani_z.ipynb")
    check_results.check_and_send(result, desired_values, mail)

def loesung_z6(result):
    disired1 = check_results.Result([0xf49bfad1, 0x85877776], None)
    disired2 = check_results.Result([0xf483a444, 0x8664cbd5], None)
    result = np.round(result, decimals=2)
    hash_values1 = check_results.get_hash_values(np.matrix(result[0, 0]), 2)
    is_correct1 = disired1.check(hash_values1[:2])
    hash_values2 = check_results.get_hash_values(np.matrix(result[0, 1]), 2)
    is_correct2 = disired2.check(hash_values2[:2])
    if is_correct1:
        print("I(x_0; y) ist korrekt.")
    else:
        print("I(x_0; y) ist falsch.")
    if is_correct2:
        print("I(x_0; x_1) ist korrekt.")
    else:
        print("I(x_0; x_1) ist falsch.")
    desired_values = check_results.Result([0xca0e9b02, 0x3b5c9132],
            [0x60079d27, 0x9e21da13, 0x8f25f2c1, 0x3d25bffd])
    mail = check_results.MailContent("markus.eisenbach@tu-ilmenau.de",
            "ANI 2017 Zusatzaufgabe 6", "ani_z.ipynb")
    check_results.check_and_send(result, desired_values, mail)

def loesung_z7(result):
    desired_values = check_results.Result([0xb043debd, 0x8741d49f],
            [0x54fd3dfe, 0x4b68e473, 0x4f776f69, 0xae26cfc1])
    mail = check_results.MailContent("markus.eisenbach@tu-ilmenau.de",
            "ANI 2017 Zusatzaufgabe 7", "ani_z.ipynb")
    check_results.check_and_send(result, desired_values, mail)

def loesung_z8(result):
    desired_values = check_results.Result([0xa4fd74a0, 0xf5e80f73],
            [0xf9c7402b, 0xfa20c81, 0x59b62ed0, 0x6c37af2c])
    mail = check_results.MailContent("markus.eisenbach@tu-ilmenau.de",
            "ANI 2017 Zusatzaufgabe 8", "ani_z.ipynb")
    check_results.check_and_send(result, desired_values, mail)

def loesung_z9(result):
    desired_values = check_results.Result([0x5d2ece70, 0xcef285ed],
            [0x525a5ac9, 0x41326c0e, 0x7fd3381, 0xf658cbfc])
    mail = check_results.MailContent("markus.eisenbach@tu-ilmenau.de",
            "ANI 2017 Zusatzaufgabe 9", "ani_z.ipynb")
    check_results.check_and_send(result, desired_values, mail)
