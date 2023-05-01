import PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog
import pysftp as sftp

import sys
import os

#SFTP Server Setup
HOST = "sftp.alexpro.net"
PORT = 22
USER_NAME = "team6"
PASSWORD = "sftpPipeline"
cnopts = sftp.CnOpts()
cnopts.hostkeys=None

newPreset = []

#Connect to SFTP Server
try:
    connection = sftp.Connection(host=HOST, username=USER_NAME, password=PASSWORD, cnopts=cnopts)
    print("Connected!")
    connection.cwd("./team6")
    print(connection.pwd)
except:
    print("failed to establish connection")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
    
        super(MainWindow,self).__init__()
        #load UI File
        #uic.loadUi("guitest.ui",self)
        uic.loadUi(r'C:\Users\steve\team-6-sftp-pipeline\Views\guitest.ui',self)
        
        #Define Widgets
        self.Browse_Button = self.findChild(QPushButton, "BrowseButton")
        self.Output_Label = self.findChild(QLabel, "File_Name_Output")
        
        self.Preset_Button = self.findChild(QPushButton, "PresetButton")
        self.Preset_Label = self.findChild(QLabel, "PresetText")
        
        self.Undo_Button = self.findChild(QPushButton, "Undo_Button")
        self.Undo_Button.setEnabled(False)
        
        #Connect Browse_Button to clicker function
        self.Browse_Button.clicked.connect(self.upload_clicker)
        self.Preset_Button.clicked.connect(self.presetClicker)
        self.Undo_Button.clicked.connect(self.undo_clicker)
        
        #Show App
        self.show()
        
    #Upload File Button Clicked
    def upload_clicker(self):
        #Open File Dialog
        global fname_basefile
        
        fname = QFileDialog.getOpenFileName(self, "Open Files", "C:", "All Files (*)")
        fname_basefile = os.path.basename(fname[0])
        
        print("Uploaded File: " + fname_basefile)
        
        #File Upload
        local_path = fname
        remote_path = "/root/team6"
        #Upload Command
        connection.put(fname[0], preserve_mtime=True)
        #Output success message
        print("File " + fname_basefile + " uploaded successfully!")
        
        #output file name to screen
        if fname:
            self.File_Name_Output.setText("File " + fname_basefile + " uploaded successfully!")
            
        #enable undo button after upload
        self.Undo_Button.setEnabled(True)
        
    def undo_clicker(self):
        
        connection.get(fname_basefile, preserve_mtime=True, localpath=r"C:\Users\steve\team-6-sftp-pipeline\GUI-Test\sent-back.txt")
        self.File_Name_Output.setText("File " + fname_basefile + " downloaded successfully!")
    
            
    #Create Preset Button Clicked        
    def presetClicker(self):
        #preset base file name
        global preset_basefile
        #preset open file dialog
        presetName = QFileDialog.getOpenFileNames(self, "Open Files", "C:", "All Files (*)")
        
        #preset_basefile = os.path.basename(presetName)
        #print(preset_basefile)
        newPreset.append(presetName[0])
        #newPreset.append(preset_basefile)
        
        if presetName:
            presetString = ''.join(''.join(y) for y in newPreset)
            self.Preset_Label.setText(presetString)
        
#Initialize App
app = QApplication(sys.argv)
UIWindow = MainWindow()
app.exec_()
    