#!/usr/bin/python2.7

# MIT License

# Copyright (c) [2016] [Nitestryker Software]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import random
import base64
import string
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.PublicKey import RSA
from string import *
from PyQt4.QtGui import *
from PyQt4.QtCore import QTimer

# main program UI
from window import *


# headers 
__author__ = 'Nitestryker software'
__copyright__ = 'Copyright (c) 2016 Nitestryker Software'
__license__ = 'GPL'
__version__ = '0.0.1'
__maintainer__ = 'nitestryker software'
__email__ = 'nitestryker@gmail.com'
__status__ = 'Development'

global key 

# iv ==============================
iv = Random.new().read(AES.block_size)
# =================================

# random-generator =================
random_generator = Random.new().read
#===================================

# update console window ============
def updateconsole(text):
    consolewindow.append(text)
#===================================

# update decryption status window=====
def dupdate(text):
    dstatuswin.append(text)
#=====================================
    
  
# generate key file ===================================================
def genkey(size=32, chars=string.ascii_lowercase + string.ascii_uppercase + string.hexdigits):
    return ''.join(random.choice(chars) for _ in range(size))
def keymaker():
    global secretkey
    secretkey = genkey()
    keytext.setText(secretkey)
#=========================================================================
    
    
#===============================================================================
def keymaster():
    global secretkey
    counter = 0
    while counter <= 0:
        pool = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        length = random.randrange(23, 24)
        trash = join(random.sample(pool, length))
        print "Generated Key: " + trash
        counter = counter + 1
        secretkey = ''.join(trash.split())
        key = secretkey 
        keytext.setText(secretkey)  
#===============================================================================

# save key file =======================================================
def savekeyfile():
    f = open('key.txt', 'w')
    f.write(str(secretkey))
    f.close()
    QtCore.QTimer.singleShot(1, lambda : \

                             updateconsole('Key file saved successfully'))
#=========================================================================

# file selection =========================================================
def selectFile():
    global inputfile
    w = QWidget()
    inputfile = QFileDialog.getOpenFileName(w, 'Open File', '/')
    filetext.setText(str(inputfile))
    QtCore.QTimer.singleShot(1, lambda : \

                             updateconsole('File: ' + inputfile + ' Loaded'))
#=========================================================================

# encryption logic ====================================================
def encrypt_file(in_filename, out_filename, chunk_size, key, iv):
    aes = AES.new(key, AES.MODE_CFB, iv)

    with open(in_filename, 'r') as in_file:
        with open(out_filename, 'w') as out_file:
            while True:
                chunk = in_file.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                out_file.write(aes.encrypt(chunk))
#==========================================================================
              

# encrypt file==============================
def encryptIt():
    global inputfile
    global outputfile
    global delorg
    key = secretkey
    outputfile = outputfile.text()
    encrypt_file(inputfile, outputfile, 8192, key, iv)
    # if delete original is checked 
    if delorg.isChecked() == True:
        inputfile = str(inputfile)
        os.system("shred -vu "+inputfile)
        QtCore.QTimer.singleShot(1, lambda : \

                             updateconsole('Shredded original file'))
    QtCore.QTimer.singleShot(1, lambda : \

                             updateconsole('Encryption successful'))
    QtCore.QTimer.singleShot(1, lambda : \

                             updateconsole('Encrypted File: ' + outputfile))
# ------------- end of encryption -------------------------------------------


#------------ Decryption functions ------------------------------------------

# Import secret Key========================================================
def importsecretkey():
    global mysecretkey
    global zfile 
    w = QWidget()
    mysecretkey = QFileDialog.getOpenFileName(w, 'Open File', '/')
    zfile = str(mysecretkey)
    f = open(zfile, 'r')
    zfileloc = f.read()
    keyfiletxt.setText(zfileloc)
    QtCore.QTimer.singleShot(1, lambda : \

                             dupdate('Encryption Key Loaded'))
#==========================================================================

#Import encrypted file =====================================================

def EncfileImport():
    global efile 
    w = QWidget()
    encfile = QFileDialog.getOpenFileName(w, 'Open File', '/')
    efile = str(encfile)
    encfileloc.setText(efile)
    QtCore.QTimer.singleShot(1, lambda : \

                             dupdate('Encrypted File Loaded'))
#============================================================================

# decryption logic ==========================================================
def decrypt_file(in_filename, out_filename, chunk_size, key, iv):
    aes = AES.new(key, AES.MODE_CFB, iv)

    with open(in_filename, 'r') as in_file:
        with open(out_filename, 'w') as out_file:
            while True:
                chunk = in_file.read(chunk_size)
                if len(chunk) == 0:
                    break
                out_file.write(aes.decrypt(chunk))
#=============================================================================\
                
# Decrypt File ================================================================
def decryptMe():
    global mysecretkey
    global efile
    global zfile
    f = open(mysecretkey, 'r')
    key = f.read()
    key = str(key)
    outputfile = doutput.text()
    decrypt_file(efile,outputfile,8192,key,iv)
    QtCore.QTimer.singleShot(1, lambda : \

                             dupdate('Decryption successful'))
    QtCore.QTimer.singleShot(1, lambda : \

                             dupdate('File Decrypted: ' + outputfile))
    if delenc.isChecked() == True:
        os.system("shred -vu "+efile)
        QtCore.QTimer.singleShot(1, lambda : \

                             dupdate('Shredded Encrypted file'))        
# ----------- Main Class --------------------------------------------------------                
# Main class ==============================================
class MyForm(QtGui.QMainWindow):
        def __init__(self, parent=None):
                # globals
                global consolewindow
                global genbutton
                global keytext
                global keymaker
                global fileloc
                global filetext
                global delorg
                global encryptit
                global outputfile
                global importkey
                global keyfiletxt
                global dstatuswin
                global encfileloc
                global encfilebtn
                global delenc
                global doutput
                global dbutton
                #build parent user interface
                super(MyForm, self).__init__()
                QtGui.QWidget.__init__(self, parent)
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)

                 # console Window ===================
                consolewindow = self.ui.statuswin_rb
                #===================================

                # ---------- Encryption section -------------------------
                # generate key button  ===========
                genbutton = self.ui.genkey_btn
                genbutton.clicked.connect(keymaker)
                #==================================

                # save key button =================
                savekeybtn =  self.ui.savekey_btn
                savekeybtn.clicked.connect(savekeyfile)
                #==================================
                
                # key text=========================
                keytext = self.ui.key_txt
                #===================================

                # File Selection ===================
                fileloc = self.ui.selectfile_btn
                filetext = self.ui.fileloc_txt
                fileloc.clicked.connect(selectFile)
                outputfile = self.ui.outputname_txt
                delorg = self.ui.delete_cb
                #====================================

                # encrypt button
                encryptit = self.ui.encryptit_btn
                encryptit.clicked.connect(encryptIt)

                # ------- end of encryption section -----------------------

                # --------- Decryption section ----------------------------
                dstatuswin = self.ui.dstatuswin_rb

                # import key for decryption =====================
                importkey = self.ui.importkey_btn
                importkey.clicked.connect(importsecretkey)
                keyfiletxt = self.ui.importkeyfile_txt
                #===============================================

                # import encrypted file ========================
                encfileloc = self.ui.encryptedFile_txt
                encfilebtn = self.ui.importencfile_btn
                encfilebtn.clicked.connect(EncfileImport)
                delenc = self.ui.delenc_cb
                #===============================================

                # Decrypted file Output name
                doutput = self.ui.doutput_txt
                #============================

                # Decryption button
                dbutton = self.ui.decryptit_btn
                dbutton.clicked.connect(decryptMe)
                # -------- end of decryption section -----------------------
               
#===========================================================

# Run Main Class ==================================================               
if __name__ == "__main__":
        app = QtGui.QApplication(sys.argv)
        myapp = MyForm()
        myapp.show()
        sys.exit(app.exec_())
#====================================================================  
