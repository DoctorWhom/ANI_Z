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
Basic GUIs for feedback and user input

Implementation is based on example code from
[1] http://easygui.sourceforge.net/tutorial.html

@author: Markus Eisenbach
@date:   2015/03/19
"""

from six.moves import input

from . import easygui

def wrong():
    easygui.msgbox('Die Lösung ist leider falsch.', 'Hinweis')

def right():
    msg = "Die Lösungs ist korrekt.\n\nZum Einsenden Ihrer Lösung geben Sie" \
            + " bitte Ihre Daten ein:"
    title = "Login"
    fieldNames = ["Name", "Matrikelnummer", "e-Mail Adresse",
                  "Benutzername", "Passwort"]
    fieldValues = ["", "", "@tu-ilmenau.de"]
    
    # repeat untile none of the fields was left blank
    while True:
        fieldValues = easygui.multpasswordbox(msg, title, fieldNames, fieldValues)
        
        if fieldValues is None: # cancel
            break
        
        # check if every field is filled
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + \
                    ('"%s" is a required field.\n' % fieldNames[i])
            elif i == 2 and fieldValues[i].strip() == "@tu-ilmenau.de":
                errmsg = errmsg + \
                    ('"%s" is a required field.\n' % fieldNames[i])
                
        if errmsg == "": # no problems found
            break
        
        # report errors and try again
        msg = errmsg
    
    return fieldValues

def mail_login(message = None, userdata = None):
    msg = "Bitte geben Sie Ihre Zugangsdaten ein:"
    title = "Login"
    fieldNames = ["Name", "e-Mail Adresse",
                  "Benutzername", "Passwort"]
    fieldValues = ["", "@tu-ilmenau.de"]
    
    # prefill fields
    if not (message is None):
        msg = message
    
    # prefill fields
    if not (userdata is None):
        fieldValues = userdata
    
    # repeat untile none of the fields was left blank
    while True:
        fieldValues = easygui.multpasswordbox(msg, title, fieldNames, fieldValues)
        
        if fieldValues is None: # cancel
            break
        
        # check if every field is filled
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + \
                    ('"%s" is a required field.\n' % fieldNames[i])
            elif i == 1 and fieldValues[i].strip() == "@tu-ilmenau.de":
                errmsg = errmsg + \
                    ('"%s" is a required field.\n' % fieldNames[i])
                
        if errmsg == "": # no problems found
            break
        
        # report errors and try again
        msg = errmsg
        
    if fieldValues is None:
        fieldValues = ["unknown", "unknown", "unknown", "unknown"]
    name = fieldValues[0]
    mailadress = fieldValues[1]
    emailfrom = "\"%s\" <%s>" % (name, mailadress)
    user = fieldValues[2]
    pw = fieldValues[3]
    
    return emailfrom, user, pw

def replace_umlaute(text):
    translations = (
        (u'\N{LATIN SMALL LETTER U WITH DIAERESIS}', u'ue'),
        (u'\N{LATIN SMALL LETTER O WITH DIAERESIS}', u'oe'),
        (u'\N{LATIN SMALL LETTER A WITH DIAERESIS}', u'ae'),
        (u'\N{LATIN SMALL LETTER SHARP S}', u'ss'),
        (u'\N{LATIN CAPITAL LETTER U WITH DIAERESIS}', u'Ue'),
        (u'\N{LATIN CAPITAL LETTER O WITH DIAERESIS}', u'Oe'),
        (u'\N{LATIN CAPITAL LETTER A WITH DIAERESIS}', u'Ae'),
        )
        
    out = text
    for from_str, to_str in translations:
        out = out.replace(from_str, to_str)
        
    return out
    
def main():
    answer = int(input("1 + 1 = "))
    if answer == 2:
        data = right()
        if data is None:
            print("Abbruch durch Nutzer")
        else:
            pw_len = len(data[4])
            data[4] = "*" * pw_len
            print("Reply was:", data)
    else:
        wrong()

if __name__ == "__main__":
    main()
