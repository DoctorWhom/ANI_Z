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
Function and classes for checking correctness of results

@author: Markus Eisenbach
@date:   2015/03/19
"""

from six.moves import input

import numpy

from . import simple_gui
from . import send_mail
from . import hash_function

class Result():
    def __init__(self, hash_compare, mask_send):
        self.hash_correct_answers = hash_compare
        self.mask_send = mask_send
    
    def check(self, hash_results):
        is_correct = hash_results == self.hash_correct_answers
        return is_correct
        
    def mask(self, hash_results):
        res = []
        for i in range(len(hash_results)):
            masked = hash_results[i] ^ self.mask_send[i] # bitwise xor
            res.append(masked)
        return res

class MailContent():
    def __init__(self, receiver, description, attachements):
        self.receiver = receiver
        self.description = description
        self.attachements = attachements
        if isinstance(attachements, str):
            self.attachements = [attachements]
    
    def get_mail_zusatzaufgabe(self, inputs):
        text = self.description + "\n"
        text = text + "result = " + str(inputs[1]) + "\n"
        text = text + "name = " + inputs[3] + "; "
        text = text + "hash(m-nr) = " + str(inputs[2]) + ";\n"
        hash_values = inputs[0]
        hash_values[3] = hash_values[3] ^ inputs[2]
        text = text + "#["
        for i in range(3):
            text = text + str(hash_values[i]) + ","
        text = text + str(hash_values[3]) + "]\n"
        return self.receiver, "ANI Result", text, self.attachements
        
    def get_mail_contest(self, inputs):
        # TODO: implement this function (sending contest results)
        print(inputs)

def round_result(result, n_decimal_places):
    # convert to numpy array
    arr = result    
    if isinstance(result, (list, tuple)):
        arr = numpy.array(result)
    if isinstance(result, numpy.matrix):
        arr = numpy.array(result)
    if isinstance(result, str):
        # convert to ascii values
        arr = numpy.array([[ord(c) for c in result]])
        
    # cut decimal places
    dp_factor = 10.0 ** n_decimal_places
    arr = numpy.divide(numpy.round(numpy.multiply(arr, dp_factor)), dp_factor)
    return arr
    
def get_hash_values(result, n_decimal_places):
    arr = round_result(result, n_decimal_places)

    # create variants
    check1 = numpy.sin(arr)
    check2 = numpy.subtract(numpy.cos(numpy.multiply(arr, 2.0)),
                            numpy.square(arr))
    check3 = numpy.cos(numpy.add(arr, 2.0))
    check4 = numpy.sin(numpy.multiply(numpy.square(arr), 2.0))
    check5 = numpy.sin(numpy.multiply(arr, 1.5))
    check6 = numpy.add(numpy.cos(numpy.multiply(arr, 0.5)),
                            numpy.sin(numpy.add(numpy.power(arr, 3.0), 4.0)))
    
    # get hash values for variants
    hash1 = hash_function.js_hash(check1)
    hash2 = hash_function.js_hash(check2)
    hash3 = hash_function.js_hash(check3)
    hash4 = hash_function.js_hash(check4)
    hash5 = hash_function.js_hash(check5)
    hash6 = hash_function.js_hash(check6)
    
    return [hash1, hash2, hash3, hash4, hash5, hash6]
    
def check_and_send(result, compare_with, mail_content):
    assert(isinstance(compare_with, Result))
    assert(isinstance(mail_content, MailContent))
    hash_values = get_hash_values(result, 2)
    is_correct = compare_with.check(hash_values[:2])
    if is_correct:
        values = simple_gui.right()
        if values is None:
            print("Sie haben den Vorgang abgebrochen. Die Ergebnisse"
                  " konnten nicht gesendet werden.")
        else:
            # process user data
            matrikelnummer = int(values[1])
            hash_mnr = hash_function.hash_matrikelnummer(matrikelnummer)
            name = values[0]
            mailaddress = values[2]
            sender = "\"%s\" <%s>" % (name, mailaddress)
            usr = values[3]
            pw = values[4]
            result_round = round_result(result, 2).tolist()
            # prepare mail
            masked_hv = compare_with.mask(hash_values[2:])
            receiver, subject, text, attachements = \
                mail_content.get_mail_zusatzaufgabe([masked_hv, result_round,
                                                     hash_mnr, name])
            # send mail
            try:
                sended = send_mail.send_mail(receiver, subject, text,
                                             attachements, sender, usr, pw)
            except:
                sended = False
                
            if sended:
                print("Ihre Lösung wurde erfolgreich eingesendet.")
                print("\n{}".format(text))
            else:
                print("Die Ergebnisse konnten nicht gesendet werden.")
                print("\nFalls dieses Problem weiterhin auftritt können Sie")
                print("folgende e-Mail manuell mit Betreff \"{}\"".format(
                        subject))
                print("an {} senden:\n{}".format(receiver, text))
    else:
        simple_gui.wrong()

def main():
    result = input("1 + 1 = ")
    desired_values = Result([0x8781d2ed, 0x87bd63ee],
                        [0x8785d217, 0x858aaab7, 0x8789f407, 0xf1d82f4f])
    receiver = "replace.with.your.name@tu-ilmenau.de"
    mail = MailContent(receiver,
                       "ANI 2018 Uebung 0 (Test) Zusatzaufgabe 0",
                       "check_results.py")
    check_and_send(result, desired_values, mail)
    
if __name__ == "__main__":
    main()
