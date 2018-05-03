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
| Copyright (c) 2015,                                                |
|     Neuroinformatics and Cognitive Robotics Labs                   |
|     at TU Ilmenau, Germany                                         |
|                                                                    |
| All rights reserved.                                               |
|                                                                    |
| Copying, resale, or redistribution, with or without modification,  |
| is strictly prohibited.                                            |
|                                                                    |
| THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBU-   |
| TORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT |
| NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FIT- |
| NESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL    |
| THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, IN-  |
| DIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES,  |
| EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                 |
+--------------------------------------------------------------------+

Content:
General purpose and application specific hash-functions.

@author: Markus Eisenbach
@date:   2015/03/18
"""

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import numpy
import math


def js_hash_update(hash_, value_8bit):
    """
    Update of JS hash function
    """
    hash2 = numpy.uint32(hash_ << 5)    # left shift
    hash3 = hash_ >> 2    # right shift
    hash5 = numpy.uint32(hash2 + value_8bit + hash3)    # sum with overflow
    hash_updated = hash_ ^ hash5    # bitwise xor
    return hash_updated


def js_hash(something):
    """
    General purpose JS hash function
    """
    # constants
    UINT16_SCALE_FACTOR = 0xFFFF
    BYTE_MASK = 0xFF
    INITIAL_HASH = 0x4E67C6A7

    matrix = something

    # check type
    is_string_type = False
    if isinstance(matrix, (list, tuple)):
        matrix = numpy.array(matrix)
    if isinstance(matrix, str):
        is_string_type = True
        # convert to ascii values
        matrix = numpy.array([[ord(c) for c in matrix]])

    # get shape of matrix
    if len(matrix.shape) == 1:
        matrix = numpy.array([matrix.tolist()])
    sx, sy = matrix.shape
    n = sx * sy

    # make it a vector (quantizize using 16 bits)
    array_uint16 = None
    if is_string_type:
        n_half = n // 2
        if (n % 2) == 1:    # odd
            matrix = numpy.concatenate((matrix, [[0]]), axis=1)
            n_half = (n + 1) // 2
        reshaped_matrix = numpy.reshape(matrix, (2, n_half))
        ls_bytes = reshaped_matrix[0, :]
        ms_bytes = numpy.multiply(reshaped_matrix[1, :], 0x100)
        array_uint16 = numpy.add(ls_bytes, ms_bytes)
        array_uint16 = numpy.concatenate((array_uint16, [n]))
    else:
        reshaped_matrix = numpy.reshape(matrix, n)
        min_value = numpy.min(reshaped_matrix)
        max_value = numpy.max(reshaped_matrix)
        dif = max_value - min_value
        descriptor_dif = 0
        magnitute_dif = 0
        if dif > 0:
            magnitute_dif = math.ceil(math.log10(dif))
            base_dif = 10 ** magnitute_dif
            descriptor_dif = numpy.round((float(dif) / float(base_dif)) *
                                         0x7FFF) + 0x7FFF
            magnitute_dif += 0x7FFF
        else:
            dif = 1
        descriptor_max = 0
        magnitute_max = 0
        if max_value > 0:
            magnitute_max = math.ceil(math.log10(max_value))
            base_max = 10 ** magnitute_max
            descriptor_max = numpy.round((float(max_value) / float(base_max)) *
                                         0x7FFF)
            magnitute_max += 0x7FFF
        elif max_value < 0:
            max_value_inv = -max_value
            magnitute_max = math.ceil(math.log10(max_value_inv))
            base_max = 10 ** magnitute_max
            descriptor_max = numpy.round(
                (float(max_value_inv) / float(base_max)) * 0x7FFF) + 0x7FFF
            magnitute_max += 0x7FFF
        min_sub = numpy.subtract(reshaped_matrix, min_value)
        normalized_mat = numpy.divide(min_sub, float(dif))
        uint16_scaled = numpy.multiply(normalized_mat, UINT16_SCALE_FACTOR)
        matrix_uint16 = numpy.round(uint16_scaled)
        array_uint16 = numpy.squeeze(numpy.asarray(matrix_uint16))
        if n == 1:
            array_uint16 = [array_uint16]
        descr = [n, sx, sy, descriptor_dif, magnitute_dif,
                 descriptor_max, magnitute_max]
        array_uint16 = numpy.concatenate((array_uint16, descr))

    # initialize hash value
    init = numpy.uint32(INITIAL_HASH)
    hash_ = init

    for element in array_uint16:
        # convert to integer type
        value = numpy.uint32(element)
        # update hash value with most significant 8 bits of 16bit element
        value_most_significant_byte = value >> 8    # right shift
        hash_ = js_hash_update(hash_, value_most_significant_byte)
        # update hash value with least significant 8 bits of 16bit element
        value_least_significant_byte = value & BYTE_MASK    # bitwise and
        hash_ = js_hash_update(hash_, value_least_significant_byte)

    return hash_


def hash_matrikelnummer(matrikelnummer):
    # constants
    BYTE_MASK = 0xFF
    UINT32_MASK = 0xFFFFFFFF
    UINT32_CORRECTION = 0x100000000
    INITIAL_HASH = 0x4E67C6A7

    # preprocessing to get many differences for small changes
    # optimized for range from 10000 to 150000 (= range of matrikel)
    # additional benefit: makes inversion a bit harder
    v1 = float(matrikelnummer) * 180.0 / math.pi
    v2 = (float(matrikelnummer) - 10.0) * 180.0 / math.pi
    v3 = (float(matrikelnummer) / 3.0 - 100.0) * 180.0 / math.pi
    v4 = (float(matrikelnummer) / 2.0 - 33.0) * 180.0 / math.pi
    val = numpy.round((math.sin(v1) + math.sin(v2) + math.cos(v3) -
                      math.cos(v4) + 2.5) * (179.0 ** 4.0))
    # bring val into uint32 range
    while val < 0:
        val += UINT32_CORRECTION
    while val > UINT32_MASK:
        val -= UINT32_CORRECTION
    # convert to uint32
    nr = numpy.uint32(val)

    # divide nr into 4 bytes
    b1 = nr & BYTE_MASK
    b2 = (nr >> 8) & BYTE_MASK
    b3 = (nr >> 16) & BYTE_MASK
    b4 = (nr >> 24) & BYTE_MASK

    # initialize hash value
    init = numpy.uint32(INITIAL_HASH)
    hash_ = init ^ nr    # bitwise xor

    # update hash value for all 4 bytes
    hash_ = js_hash_update(hash_, b1)
    hash_ = js_hash_update(hash_, b2)
    hash_ = js_hash_update(hash_, b3)
    hash_ = js_hash_update(hash_, b4)

    # optimize hash for displaying only last 3 digits
    # try to get equal distribution for all 3-digit-suffixes (101 - 998)
    hash_matrikel = ((hash_ // 898) % 4000000) * 1000 + (hash_ % 898) + 101

    return hash_matrikel


def main():
    """
    Examples, test cases
    """
    print("Test cases for hash functions")

    # matrix
    mat = numpy.matrix([[1, 2], [3, 4]])
    mat2 = numpy.matrix([[2, 3], [4, 5]])
    # one value of mat3 has noticable difference to mat
    # thus it should get a different hash
    mat3 = numpy.matrix([[1, 2.001], [3, 4]])
    # mat4 is similar to mat except small differences (e.g. rounding errors)
    # thus it should get the same hash
    mat4 = numpy.matrix([[0.999999, 2.0000001], [2.999999, 4.000001]])
    print("====== numpy.matrix ======")
    print("Matrix = ", mat)
    print("HASH(Matrix) = ", js_hash(mat))
    print("HASH(Matrix.T) = ", js_hash(mat.T))
    print("Matrix2 = ", mat2)
    print("HASH(Matrix2) = ", js_hash(mat2))
    print("HASH(Matrix2.T) = ", js_hash(mat2.T))
    print("Matrix3 = ", mat3)
    print("HASH(Matrix3) = ", js_hash(mat3))
    print("HASH(Matrix3.T) = ", js_hash(mat3.T))
    print("cos(Matrix) = ", numpy.cos(mat))
    print("HASH(cos(Matrix)) = ", js_hash(numpy.cos(mat)))
    print("Matrix4 = ", mat4)
    print("HASH(Matrix4) = ", js_hash(mat4))
    print("HASH(Matrix4.T) = ", js_hash(mat4.T))
    # --- test cases ---
    print("TEST A01 [HASH(Matrix) != HASH(Matrix.T)] successfull = ",
          js_hash(mat) != js_hash(mat.T))
    print("TEST A02 [HASH(Matrix) != HASH(Matrix2)] successfull = ",
          js_hash(mat) != js_hash(mat2))
    print("TEST A03 [HASH(Matrix) != HASH(Matrix2.T)] successfull = ",
          js_hash(mat) != js_hash(mat2.T))
    print("TEST A04 [HASH(Matrix.T) != HASH(Matrix2)] successfull = ",
          js_hash(mat.T) != js_hash(mat2))
    print("TEST A05 [HASH(Matrix.T) != HASH(Matrix2.T)] successfull = ",
          js_hash(mat.T) != js_hash(mat2.T))
    print("TEST A06 [HASH(Matrix) != HASH(Matrix3)] successfull = ",
          js_hash(mat) != js_hash(mat3))
    print("TEST A07 [HASH(Matrix) != HASH(Matrix3.T)] successfull = ",
          js_hash(mat) != js_hash(mat3.T))
    print("TEST A08 [HASH(Matrix.T) != HASH(Matrix3)] successfull = ",
          js_hash(mat.T) != js_hash(mat3))
    print("TEST A09 [HASH(Matrix.T) != HASH(Matrix3.T)] successfull = ",
          js_hash(mat.T) != js_hash(mat3.T))
    print("TEST A10 [HASH(Matrix) != HASH(cos(Matrix))] successfull = ",
          js_hash(mat) != js_hash(numpy.cos(mat)))
    print("TEST A11 [HASH(Matrix) == HASH(Matrix4)] successfull = ",
          js_hash(mat) == js_hash(mat4))
    print("TEST A12 [HASH(Matrix.T) == HASH(Matrix4.T)] successfull = ",
          js_hash(mat.T) == js_hash(mat4.T))

    # array
    arr = numpy.array([[1, 2], [3, 4]])
    print("====== numpy.array ======")
    print("Array = ", arr)
    print("HASH(Array) = ", js_hash(arr))
    print("HASH(Array.T) = ", js_hash(arr.T))
    # --- test cases ---
    print("TEST B01 [HASH(Array) != HASH(Array.T)] successfull = ",
          js_hash(arr) != js_hash(arr.T))
    print("TEST B02 [HASH(Matrix) == HASH(Array)] successfull = ",
          js_hash(mat) == js_hash(arr))
    print("TEST B03 [HASH(Matrix.T) == HASH(Array.T)] successfull = ",
          js_hash(mat.T) == js_hash(arr.T))

    # list
    lis = [[1, 2], [3, 4]]
    lis_transpose = [[1, 3], [2, 4]]
    print("====== list ======")
    print("List = ", lis)
    print("HASH(List) = ", js_hash(lis))
    print("HASH(List.T) = ", js_hash(lis_transpose))
    # --- test cases ---
    print("TEST C01 [HASH(List) != HASH(List.T)] successfull = ",
          js_hash(lis) != js_hash(lis_transpose))
    print("TEST C02 [HASH(Matrix) == HASH(List)] successfull = ",
          js_hash(mat) == js_hash(lis))
    print("TEST C03 [HASH(Matrix.T) == HASH(List.T)] successfull = ",
          js_hash(mat.T) == js_hash(lis_transpose))

    # tuple
    tup = ((1, 2), (3, 4))
    tup_transpose = ((1, 3), (2, 4))
    print("====== tuple ======")
    print("Tuple = ", tup)
    print("HASH(Tuple) = ", js_hash(tup))
    print("HASH(Tuple.T) = ", js_hash(tup_transpose))
    # --- test cases ---
    print("TEST D01 [HASH(Tuple) != HASH(Tuple.T)] successfull = ",
          js_hash(tup) != js_hash(tup_transpose))
    print("TEST D01 [HASH(Matrix) == HASH(Tuple)] successfull = ",
          js_hash(mat) == js_hash(tup))
    print("TEST D01 [HASH(Matrix.T) == HASH(Tuple.T)] successfull = ",
          js_hash(mat.T) == js_hash(tup_transpose))

    # string
    string = "test"
    string_capital_letter = "Test"
    string_space = "test "
    print("====== str ======")
    print("String = ", string)
    print("HASH(String) = ", js_hash(string))
    print("String2 = ", string_capital_letter)
    print("HASH(String2) = ", js_hash(string_capital_letter))
    print("String3 = ", string_space)
    print("HASH(String3) = ", js_hash(string_space))
    # --- test cases ---
    print("TEST E01 [HASH(String) != HASH(String2)] successfull = ",
          js_hash(string) != js_hash(string_capital_letter))
    print("TEST E02 [HASH(String) != HASH(String3)] successfull = ",
          js_hash(string) != js_hash(string_space))
    print("TEST E03 [HASH(String2) != HASH(String3)] successfull = ",
          js_hash(string_capital_letter) != js_hash(string_space))

    # matrikelnummer
    matrikel_nr1 = 12345
    matrikel_nr2 = 12346
    print("M.-Nr.1 = ", matrikel_nr1)
    print("HASH(M.-Nr.1) = ", hash_matrikelnummer(matrikel_nr1))
    print("M.-Nr.2 = ", matrikel_nr2)
    print("HASH(M.-Nr.2) = ", hash_matrikelnummer(matrikel_nr2))
    print("TEST F01 [HASH(M.-Nr.1) != HASH(M.-Nr.2)] successfull = ",
          (hash_matrikelnummer(matrikel_nr1) !=
           hash_matrikelnummer(matrikel_nr2)))
    dif_bitwise = (hash_matrikelnummer(matrikel_nr1) ^
                   hash_matrikelnummer(matrikel_nr2))    # bitwise xor
    sum_dif = 0
    for i in range(32):
        bit = (dif_bitwise >> i) & 0x1
        sum_dif += bit
    print("Bit-Differences(HASH(M.-Nr.1), HASH(M.-Nr.2)) = ", sum_dif)
    print("TEST F02 [sum(bit-differences) > 10] successfull = ",
          sum_dif > 10)
    # count conflicts in matrikelnummer range
    print("check conflicts in relevant ranges")
    print("check if conflict probability in last 3 digits" +
          " for seminar participants is very low")
    for i in range(1, 15):
        offset = i * 10000
        hash_list = []
        hash_suffix_list = []
        total_conflicts = 0
        total_conflicts_suffix = 0
        total_combinations = 20000 ** 2
        total_participants = 30
        seminar_combinations = total_participants ** 2
        for mnr in range(offset, offset + 20000):
            hash_ = hash_matrikelnummer(mnr)
            if hash_ in hash_list:
                total_conflicts += 1
            else:
                hash_list.append(hash_)
            suffix_3digits = hash_ % 10000
            if suffix_3digits in hash_suffix_list:
                total_conflicts_suffix += 1
            else:
                hash_suffix_list.append(suffix_3digits)
        print("#Conflicts in range [%s, %s) = " % (offset, offset + 20000),
              total_conflicts)
        print("TEST F%s [#Conflicts == 0] successfull = " % (2*i+1),
              total_conflicts == 0)
        conflict_probability = float(total_conflicts_suffix) * \
            float(seminar_combinations) / float(total_combinations)
        print("P(Confl.(3dig.) in seminar) in range [%s, %s) = " %
              (offset, offset + 20000), conflict_probability)
        print("TEST F%s [P(Confl.(3dig.)) < 0.05] successfull = " % (2*i+2),
              conflict_probability < 0.05)

if __name__ == "__main__":
    main()
