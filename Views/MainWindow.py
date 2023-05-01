# ***********************************************************************************************************************
# *                                                                                                                     *
# *   MainWindow.py                                                                                                     *
# *   Authors: Robert B. Wilson, Alex Baker, Jordan Phillips, Gabriel Snider, Steven Dorsey, Yoshinori Agari            *
# *   The purpose of this file is to load the MainWindow UI file upon initialization and also provide logic for         *
# *   all of the widgets used throughout the MainWindow UI                                                              *
# *                                                                                                                     *
# ***********************************************************************************************************************

import time

from PyQt5.QtCore import QMetaObject, pyqtSlot, Q_ARG
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import PyQt5
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
import sys
from classes.Database import Database
from classes.User import User
from classes.Security import Security
import threading
import pysftp
import os

class MainWindow(QtWidgets.QMainWindow):
    # Function: Constructor
    # Parameters: None
    # Return: MainWindow UI object
    # Loads the MainWindow.UI file and initializes all of the widget logic
    def __init__(self):
        # Call QMainWindow Constructor
        super(MainWindow, self).__init__()
        # Load MainWindow.UI
        uic.loadUi(r"./views/MainWindow.ui", self)
        # Initialize User
        self.User = User()
        # Initialize Security Object
        self.Security = Security()
        # Load Widgets
        self.Admin_Button = self.findChild(QtWidgets.QLabel, "Admin_Button")
        self.Stacked_Widget = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
        self.Login_Button = self.findChild(QtWidgets.QPushButton, "Login_Button")
        self.Username_LineEdit = self.findChild(QtWidgets.QLineEdit, "Username_LineEdit")
        self.Password_LineEdit = self.findChild(QtWidgets.QLineEdit, "Password_LineEdit")
        self.Users_List = self.findChild(QtWidgets.QListWidget, "Users_List")
        self.AddUser_Button = self.findChild(QtWidgets.QPushButton, "AddUser_Button")
        self.NewUserUsername_LineEdit = self.findChild(QtWidgets.QLineEdit, "NewUserUsername_LineEdit")
        self.NewUserPassword_LineEdit = self.findChild(QtWidgets.QLineEdit, "NewUserPassword_LineEdit")
        self.DeleteUsers_Button = self.findChild(QtWidgets.QPushButton, "DeleteUsers_Button")
        self.LoginError_Label = self.findChild(QtWidgets.QLabel, "LoginError_Label")
        self.NewConnectionServer_LineEdit = self.findChild(QtWidgets.QLineEdit, "NewConnectionServer_LineEdit")
        self.NewConnectionUsername_LineEdit = self.findChild(QtWidgets.QLineEdit, "NewConnectionUsername_LineEdit")
        self.NewConnectionPassword_LineEdit = self.findChild(QtWidgets.QLineEdit, "NewConnectionPassword_LineEdit")
        self.NewConnectionRemoteDirectory_LineEdit = self.findChild(QtWidgets.QLineEdit, "NewConnectionRemoteDirectory_LineEdit")
        self.AddConnection_Button = self.findChild(QtWidgets.QPushButton, "AddConnection_Button")
        self.AdminConnections_Table = self.findChild(QtWidgets.QTableWidget, "AdminConnections_Table")
        self.DeleteConnectionsButton = self.findChild(QtWidgets.QPushButton, "DeleteConnections_Button")
        self.PresetsConnections_Table = self.findChild(QtWidgets.QTableWidget, "PresetsConnections_Table")
        self.PresetsFileSelector_Button = self.findChild(QtWidgets.QPushButton, "PresetsFileSelector_Button")
        self.PresetsFiles_List = self.findChild(QtWidgets.QListWidget, "PresetsFiles_List")
        self.PresetsConnections_Table = self.findChild(QtWidgets.QTableWidget, "PresetsConnections_Table")
        self.PresetsFilesClear_Button = self.findChild(QtWidgets.QPushButton, "PresetsFilesClear_Button")
        self.PresetsDisplayAll_Button = self.findChild(QtWidgets.QPushButton, "PresetsDisplayAll_Button")
        self.PresetsName_LineEdit = self.findChild(QtWidgets.QLineEdit, "PresetsName_LineEdit")
        self.PresetsAddPreset_Button = self.findChild(QtWidgets.QPushButton, "PresetsAddPreset_Button")
        self.PresetsPresets_List = self.findChild(QtWidgets.QListWidget, "PresetsPresets_List")
        self.PresetsDeletePresets_Button = self.findChild(QtWidgets.QPushButton, "PresetsDeletePresets_Button")
        self.HomeConnections_Table = self.findChild(QtWidgets.QTableWidget, "HomeConnections_Table")
        self.HomePresets_List = self.findChild(QtWidgets.QListWidget, "HomePresets_List")
        self.HomeUpload_Table = self.findChild(QtWidgets.QTableWidget, "HomeUpload_Table")
        self.HomeUploadTable_Clear_Button = self.findChild(QtWidgets.QPushButton, "HomeUploadTable_Clear_Button")
        self.HomeUploadTable_Remove_Button = self.findChild(QtWidgets.QPushButton, "HomeUploadTable_Remove_Button")
        self.HomeUploadTable_Add_Button = self.findChild(QtWidgets.QPushButton, "HomeUploadTable_Add_Button")
        self.HomeUploadTable_Upload_Button = self.findChild(QtWidgets.QPushButton, "HomeUploadTable_Upload_Button")
        self.JobsStartDate_LineEdit = self.findChild(QtWidgets.QLineEdit, "JobsStartDate_LineEdit")
        self.JobsEndDate_LineEdit = self.findChild(QtWidgets.QLineEdit, "JobsEndDate_LineEdit")
        self.JobsPresets_ComboBox = self.findChild(QtWidgets.QComboBox, "JobsPresets_ComboBox")
        self.JobsSchedule_ComboBox = self.findChild(QtWidgets.QComboBox, "JobsSchedule_ComboBox")
        self.JobsAddJob_Button = self.findChild(QtWidgets.QPushButton, "JobsAddJob_Button")
        self.JobsName_LineEdit = self.findChild(QtWidgets.QLineEdit, "JobsName_LineEdit")
        self.JobsStartTime_TimeEdit = self.findChild(QtWidgets.QTimeEdit, "JobsStartTime_TimeEdit")
        self.JobsTable_Table = self.findChild(QtWidgets.QTableWidget, "JobsTable_Table")
        self.JobsDeleteJobs_Button = self.findChild(QtWidgets.QPushButton, "JobsDeleteJobs_Button")
        
        # Connect Event Logic
        self.Admin_Button.mousePressEvent = self.Admin_Button_Logic
        self.Login_Button.clicked.connect(self.Login_Button_Logic)
        self.AddUser_Button.clicked.connect(self.AddUser_Button_Logic)
        self.DeleteUsers_Button.clicked.connect(self.DeleteUsers_Button_Logic)
        self.AddConnection_Button.clicked.connect(self.AddConnection_Button_Logic)
        self.DeleteConnections_Button.clicked.connect(self.DeleteConnections_Button_Logic)
        self.PresetsFileSelector_Button.clicked.connect(self.PresetsFileSelector_Button_Logic)
        self.PresetsFilesClear_Button.clicked.connect(self.PresetsFilesClear_Button_Logic)
        self.PresetsDisplayAll_Button.clicked.connect(self.PresetsDisplayAll_Button_Logic)
        self.PresetsAddPreset_Button.clicked.connect(self.PresetsAddPreset_Button_Logic)
        self.PresetsDeletePresets_Button.clicked.connect(self.PresetsDeletePresets_Button_logic)
        self.HomeUploadTable_Clear_Button.clicked.connect(self.HomeUploadTable_Clear_Button_Logic)
        self.HomeUploadTable_Remove_Button.clicked.connect(self.HomeUploadTable_Remove_Button_Logic)
        self.HomeUploadTable_Add_Button.clicked.connect(self.HomeUploadTable_Add_Button_Logic)
        self.HomeUploadTable_Upload_Button.clicked.connect(self.HomeUploadTable_Upload_Button_Logic)
        self.JobsAddJob_Button.clicked.connect(self.JobsAddJob_Button_logic)
        self.JobsDeleteJobs_Button.clicked.connect(self.JobsDeleteJobs_Button_Logic)

        # Initialize LineEdit validations
        validator = QRegExpValidator(QRegExp("^(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])/[0-9]{4}$"), self.JobsStartDate_LineEdit)
        self.JobsStartDate_LineEdit.setValidator(validator)
        self.JobsEndDate_LineEdit.setValidator(validator)
        # Initialize Jobs ComboBoxes
        self.Initialize_JobsComboBoxes()
        # Initialize data-structure to keep up with files added from local filesystem
        self.LocalRelations = []
        # Initialize Jobs Table
        self.Display_Jobs()
        # Initialize default Stacked Widget Page
        self.Stacked_Widget.setCurrentIndex(0)
        # Initialize Users List
        self.Display_Users()
        # Initialize Connection Tables
        self.Display_Connections()
        # Initialize Error Messages to Hidden
        self.LoginError_Label.hide()
        # Initialize Preset Lists
        self.Display_Presets()
        # Initialize Preset List Item Selection Event Handler
        self.PresetsPresets_List.itemSelectionChanged.connect(self.Handle_PresetItemSelection)
        # Initialize Home Preset List Item Selection Event Handler
        self.HomePresets_List.itemSelectionChanged.connect(self.Handle_HomePresetItemSelection)
        # Initialize Home Connections Item Selection Event Handler
        self.HomeConnections_Table.itemSelectionChanged.connect(self.Handle_HomeConnectionsItemSelection)
        # Initialize Table Column Widths for each table in the application
        self.Prettify_Tables()
        # Display Window
        self.show()
    


    # Function: Admin_Button_Logic
    # Parameters: mousePressedEvent
    # Return: None
    # Checks if a user has been logged in, if yes --> it changes the current stacked widget index to the admin page. If no --> it changes the current stacked widget index to the login page.
    def Admin_Button_Logic(self, event):
        # case user is at the home page and not logged in
        if self.Stacked_Widget.currentIndex() == 0 and not self.User.isAuthenticated:
            self.Stacked_Widget.setCurrentIndex(1)
            self.Admin_Button.setText("Home")
        # case user is at the home page and are logged in
        elif self.Stacked_Widget.currentIndex() == 0 and self.User.isAuthenticated:
            self.Stacked_Widget.setCurrentIndex(2)
            self.Admin_Button.setText("Home")
        # case user is at the login page
        elif self.Stacked_Widget.currentIndex() == 1:
            self.Stacked_Widget.setCurrentIndex(0)
            self.Admin_Button.setText("Admin")
        # case user is at the admin page
        else:
            self.Stacked_Widget.setCurrentIndex(0)
            self.Admin_Button.setText("Admin")
    


    # Function: Login_Button_Logic
    # Parameters: None
    # Return: None
    # Fetches text from Username and Password QLineEdit Widgets and attempts to authenticate the user based on this data. If the user is authenticated, the user will be redirected to the admin page. Otherwise a invalid login notification will be displayed.
    def Login_Button_Logic(self):
        # get username and password claims
        username = self.Username_LineEdit.text()
        password = self.Password_LineEdit.text()
        # Show loading cursor
        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        # convert password to hashed version
        hashedPassword = self.Security.getMD5(password)
        # attempt to authenticate
        if self.User.authenticate(username, hashedPassword):
            # update widgets and redirect to admin page
            self.Stacked_Widget.setCurrentIndex(2)
            self.Admin_Button.setText("Home")
            self.setWindowTitle("SFTPPipeline - Welcome " + self.User.Username)
        else:
            # Display login error notification
            self.LoginError_Label.show()
            # Reset username and password LineEdits
            self.Username_LineEdit.setText("")
            self.Password_LineEdit.setText("")
        # Restore default cursor
        QApplication.restoreOverrideCursor()
    


    # Function: Display_Users
    # Parameters: None
    # Return: None
    # Clears out the Users_List Widget in the administrative view, and populates the list widget with usernames from the database
    def Display_Users(self):
        # Establish database connection
        db = Database()
        # Clear Users_List Widget
        self.Users_List.clear()
        # Fetch users from database
        users = db.getUsers()
        # Populate Users_List widget
        for user in users:
            self.Users_List.addItem(user[1])
        # Clean up database connection
        del db



    # Function: AddUser_Button_Logic
    # Parameters: None
    # Return: None
    # Attempts to add a new user, if user input information is an empty string, the function will return
    def AddUser_Button_Logic(self):
        # Establish a database connection
        db = Database()
        # Fetch user input
        username = self.NewUserUsername_LineEdit.text()
        password = self.NewUserPassword_LineEdit.text()
        # verify user input
        if username.strip() == "" or password.strip() == "":
            del db
            return
        # Show loading cursor
        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        # Secure password
        hashPassword = self.Security.getMD5(password)
        db.addUser(username, hashPassword)
        # Clean up database connection
        del db
        # Restore default cursor
        QApplication.restoreOverrideCursor()
        # Set LineEdits to empty string
        self.NewUserUsername_LineEdit.setText("")
        self.NewUserPassword_LineEdit.setText("")
        # Refresh List
        self.Display_Users()
    


    # Function DeleteUsers_Button_Logic
    # Parameters: None
    # Return: None
    # Deletes all selected Users in the Users_List widget from the database
    def DeleteUsers_Button_Logic(self):
        # Establish a database connection
        db = Database()
        # Get selected users in the Users_List widget
        selectedUsers = self.Users_List.selectedItems()
        # Iterate through each selected user
        for user in selectedUsers:
            # Delete the user from the datbase
            db.deleteUser(user.text())
        # Clean up database connection
        del db
        # Update the Users_List widget
        self.Display_Users()
        


    # Function: AddConnection_Button_Logic
    # Parameters: None
    # Return: None
    # Attempts to add a new connection to the database. If a LineEdit is empty, it will return.
    def AddConnection_Button_Logic(self):
        # Fetch user input data
        server = self.NewConnectionServer_LineEdit.text()
        username = self.NewConnectionUsername_LineEdit.text()
        password = self.NewConnectionPassword_LineEdit.text()
        remoteDirectory = self.NewConnectionRemoteDirectory_LineEdit.text()
        # validate user input
        if server.strip() == "" or username.strip() == "" or password.strip() == "" or remoteDirectory.strip() == "":
            return
        # Establish database connection
        db = Database()
        # Add new connection
        db.addConnection(server, username, password, remoteDirectory)
        # Clean up database connection
        del db
        # Reset LineEdit text
        self.NewConnectionServer_LineEdit.setText("")
        self.NewConnectionUsername_LineEdit.setText("")
        self.NewConnectionPassword_LineEdit.setText("")
        self.NewConnectionRemoteDirectory_LineEdit.setText("")
        # Refresh Connection Tables
        self.Display_Connections()



    # Function: Display_Connections
    # Parameters: None
    # Return: None
    # Resets all of the connection tables in the application, then fetches connections from the database and displays them on all connection tables in the application.
    def Display_Connections(self):
        # Clear tables
        self.AdminConnections_Table.clearContents()
        self.AdminConnections_Table.setRowCount(0)
        self.PresetsConnections_Table.clearContents()
        self.PresetsConnections_Table.setRowCount(0)
        self.HomeConnections_Table.clearContents()
        self.HomeConnections_Table.setRowCount(0)
        # Establish database connection
        db = Database()
        # Fetch Connection Data
        connections = db.getConnections()
        # clean up database connection
        del db
        # set new rows for the tables
        self.AdminConnections_Table.setRowCount(len(connections))
        self.PresetsConnections_Table.setRowCount(len(connections))
        self.HomeConnections_Table.setRowCount(len(connections))
        # enumerate connections list and insert data into the tables
        for row, connection in enumerate(connections):
            self.AdminConnections_Table.setItem(row, 0, QTableWidgetItem(connection[1]))
            self.AdminConnections_Table.setItem(row, 1, QTableWidgetItem(connection[4]))
            self.PresetsConnections_Table.setItem(row, 0, QTableWidgetItem(connection[1]))
            self.PresetsConnections_Table.setItem(row, 1, QTableWidgetItem(connection[4]))
            self.HomeConnections_Table.setItem(row, 0, QTableWidgetItem(connection[1]))
            self.HomeConnections_Table.setItem(row, 1, QTableWidgetItem(connection[4]))
    


    #
    def DeleteConnections_Button_Logic(self):
        print("hi")
        selectedItems = self.AdminConnections_Table.selectedItems()
        selectedRows = set()
        for item in selectedItems:
            selectedRows.add(item.row())
        if selectedRows:
            db = Database()
            connections = []
            for row in selectedRows:
                server = self.AdminConnections_Table.item(row, 0)
                remote = self.AdminConnections_Table.item(row, 1)
                con = db.getConnection(server.text(), remote.text())
                connections.append(con[0][0])
                print(server.text() + remote.text())
                #print(item.text())
            for c in connections:
                db.deleteConnection(c)
            del db
            self.Display_Connections()




    def SelectFiles(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            return filenames
    


    def PresetsFileSelector_Button_Logic(self):
        files = self.SelectFiles()
        if files is not None:
            self.PresetsFiles_List.addItems(files)
    


    def PresetsFilesClear_Button_Logic(self):
        self.PresetsFiles_List.clear()
    


    def PresetsDisplayAll_Button_Logic(self):
        self.Display_Connections()
    


    def PresetsAddPreset_Button_Logic(self):
        print("Clicked")
        # get files
        files = [self.PresetsFiles_List.item(index).text() for index in range(self.PresetsFiles_List.count())]
        # get name
        name = self.PresetsName_LineEdit.text()
        # get selected rows
        selectedItems = self.PresetsConnections_Table.selectedItems()
        selectedRows = set()
        for item in selectedItems:
            selectedRows.add(item.row())
        # if there are selected rows
        if selectedRows:
            db = Database()
            connections = []
            # for each row, get connection id
            for row in selectedRows:
                server = self.PresetsConnections_Table.item(row, 0)
                remotedirectory = self.PresetsConnections_Table.item(row, 1)
                con = db.getConnection(server.text(), remotedirectory.text())
                # append connection id
                connections.append(con[0][0])
            # insert preset into db (name, files[], connections[])
            db.addPreset(name, files, connections)
            del db
            self.PresetsFiles_List.clear()
            self.Display_Presets()
    


    def Display_Presets(self):
        db = Database()
        names = db.getPresetNames()
        del db
        self.PresetsPresets_List.clear()
        self.PresetsPresets_List.addItems(names)
        self.HomePresets_List.clear()
        self.HomePresets_List.addItems(names)
    
    
    def PresetsDeletePresets_Button_logic(self):
        # Establish a database connection
        db = Database()
        # Get selected users in the Users_List widget
        selectedPresets = self.PresetsPresets_List.selectedItems()
        # Iterate through each selected user
        for preset in selectedPresets:
            # Delete the user from the datbase
            db.deletePresets(preset.text())
        # Clean up database connection
        del db
        # clear files table
        self.PresetsFiles_List.clear()
        # clear selected connections
        self.PresetsConnections_Table.clearSelection()
        # Update the Users_List widget
        self.Display_Presets()



    def Handle_PresetItemSelection(self):
        try:
            selectedPreset = self.PresetsPresets_List.currentItem()
            if selectedPreset is not None:
                db = Database()
                relations = db.getRelations(selectedPreset.text())
                del db
                self.PresetsFiles_List.clear()
                self.PresetsFiles_List.addItems(relations[0])
                self.PresetsConnections_Table.clearSelection()
                for connection in relations[1]:
                    for row in range(self.PresetsConnections_Table.rowCount()):
                        for column in range(self.PresetsConnections_Table.columnCount()):
                            server = self.PresetsConnections_Table.item(row, column)
                            if server is not None and server.text() == connection[0]:
                                remoteDir = self.PresetsConnections_Table.item(row, column+1)
                                if remoteDir is not None and remoteDir.text() == connection[1]:
                                    self.PresetsConnections_Table.selectRow(row)
        except:
            pass

    


    def Prettify_Tables(self):
        # list of all tables
        Tables = [self.HomeUpload_Table, self.HomeConnections_Table, self.AdminConnections_Table, self.PresetsConnections_Table]
        # Iterate through each table and fix column width
        for table in Tables:
            header = table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

    

    def Handle_HomePresetItemSelection(self):
        try:
            # Clear all but custom
            self.Refine_HomeUpload_Table()
            # get selected presets
            selectedPresets = self.HomePresets_List.selectedItems()
            # if selected, get each entry for each preset
            if selectedPresets is not None:
                db = Database()
                for preset in selectedPresets:
                    relation = db.getRelations(preset.text())
                    #print(relation)
                    #print("Rel Bel")
                    #print(relation[1][0])
                    # iterate files
                    
                    for c in range(len(relation[1])):
                        for f in relation[0]:
                            print(relation[1][c][0])
                            # append relation to table
                            newRow = self.HomeUpload_Table.rowCount()
                            self.HomeUpload_Table.insertRow(newRow)
                            self.HomeUpload_Table.setItem(self.HomeUpload_Table.rowCount()-1, 0, QTableWidgetItem(f))
                            self.HomeUpload_Table.setItem(self.HomeUpload_Table.rowCount()-1, 1,QTableWidgetItem(relation[1][c][0]))
                            self.HomeUpload_Table.setItem(self.HomeUpload_Table.rowCount()-1, 2, QTableWidgetItem(relation[1][c][1]))
                            self.HomeUpload_Table.setItem(self.HomeUpload_Table.rowCount()-1, 3, QTableWidgetItem(preset.text()))
                            progressBar = QProgressBar()
                            progressBar.setAlignment(Qt.AlignCenter)
                            progressBar.setValue(0)
                            self.HomeUpload_Table.setCellWidget(newRow, 4, progressBar)
                    print("\n")
                del db

        except:
            pass



    def Refine_HomeUpload_Table(self):
        #self.HomeUpload_Table.clear()
        # for each row
        # if cell not selected, or cell not local
        # rem
        self.HomeUpload_Table.setRowCount(0)
        # add back local relations
        for relation in self.LocalRelations:
            newRow = self.HomeUpload_Table.rowCount()
            self.HomeUpload_Table.insertRow(newRow)
            self.HomeUpload_Table.setItem(self.HomeUpload_Table.rowCount()-1, 0, QTableWidgetItem(relation[0]))
            self.HomeUpload_Table.setItem(self.HomeUpload_Table.rowCount()-1, 1,QTableWidgetItem(relation[1]))
            self.HomeUpload_Table.setItem(self.HomeUpload_Table.rowCount()-1, 2, QTableWidgetItem(relation[2]))
            self.HomeUpload_Table.setItem(self.HomeUpload_Table.rowCount()-1, 3, QTableWidgetItem(relation[3]))
            progressBar = QProgressBar()
            progressBar.setAlignment(Qt.AlignCenter)
            progressBar.setValue(0)
            self.HomeUpload_Table.setCellWidget(newRow, 4, progressBar)
    

    @pyqtSlot()
    def HomeUploadTable_Clear_Button_Logic(self):
        self.HomeUpload_Table.setRowCount(0)
        self.HomePresets_List.clearSelection()
        self.LocalRelations.clear()
    


    def HomeUploadTable_Remove_Button_Logic(self):
        selectedItems = self.HomeUpload_Table.selectedItems()
        selectedRows = set()
        for item in selectedItems:
            selectedRows.add(item.row())
        for row in sorted(selectedRows, reverse=True):
            if self.HomeUpload_Table.item(row, 3).text() == "Local File System":
                for relation in self.LocalRelations:
                    print(relation)
                    if relation[0] == self.HomeUpload_Table.item(row, 0).text() and relation[1].text() == self.HomeUpload_Table.item(row, 1).text() and relation[2].text() == self.HomeUpload_Table.item(row, 2).text() and relation[3] == self.HomeUpload_Table.item(row, 3).text():
                       self.HomeUpload_Table.removeRow(row)
                       self.LocalRelations.remove(relation)
                       break;
            else:
                self.HomeUpload_Table.removeRow(row)
    


    def Handle_HomeConnectionsItemSelection(self):
        selectedItems = self.HomeConnections_Table.selectedItems()
        if len(selectedItems) > 0:
            self.HomeUploadTable_Add_Button.setEnabled(True)
            self.HomeUploadTable_Add_Button.setStyleSheet("background-color: lightblue; border: 1px solid black; color: black;")
        else:
            self.HomeUploadTable_Add_Button.setEnabled(False)
            self.HomeUploadTable_Add_Button.setStyleSheet("background-color: white; border: 1px solid gray; color: gray;")



    def HomeUploadTable_Add_Button_Logic(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Open file", "", "All files (*.*)")
        if file_paths:
            for fpath in file_paths:
                selectedItem = self.HomeConnections_Table.selectedItems()
                row = selectedItem[0].row()
                server = self.HomeConnections_Table.item(row, 0)
                remoteDirectory = self.HomeConnections_Table.item(row, 1)
                fs = "Local File System"
                newRow = self.HomeUpload_Table.rowCount()
                self.HomeUpload_Table.insertRow(newRow)
                self.HomeUpload_Table.setItem(self.HomeUpload_Table.rowCount()-1, 0, QTableWidgetItem(fpath))
                self.HomeUpload_Table.setItem(self.HomeUpload_Table.rowCount()-1, 1,QTableWidgetItem(server))
                self.HomeUpload_Table.setItem(self.HomeUpload_Table.rowCount()-1, 2, QTableWidgetItem(remoteDirectory))
                self.HomeUpload_Table.setItem(self.HomeUpload_Table.rowCount()-1, 3, QTableWidgetItem(fs))
                progressBar = QProgressBar()
                progressBar.setAlignment(Qt.AlignCenter)
                progressBar.setValue(0)
                self.HomeUpload_Table.setCellWidget(newRow, 4, progressBar)
                relation = [fpath, server, remoteDirectory, fs]
                self.LocalRelations.append(relation)

    

    def HomeUploadTable_Upload_Button_Logic(self):
        # prompt confirm
        message_box = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to upload ' + str(self.HomeUpload_Table.rowCount()) + ' files?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # check
        if message_box == QMessageBox.Yes:
            self.Initialize_ProgressBars()
            thread = threading.Thread(target=self.Upload)
            thread.start()
            # thread.join()
            # notification


    def callback(self, transferred, total):
        self.transferred = transferred
        self.total = total
        percent = transferred / total * 100
        print(f"{transferred}/{total} bytes transferred ({percent:.2f}%)")
           
    def Upload(self):
         # Freeze widgets
        self.HomePresets_List.setEnabled(False)
        self.HomeConnections_Table.setEnabled(False)
        self.HomeUploadTable_Add_Button.setEnabled(False)
        self.HomeUploadTable_Remove_Button.setEnabled(False)
        self.HomeUploadTable_Clear_Button.setEnabled(False)
        self.HomeUploadTable_Upload_Button.setEnabled(False)

        # Establish DB connection
        db = Database()
        #QApplication.processEvents()
        for row in range(self.HomeUpload_Table.rowCount()):
            local_filePath = self.HomeUpload_Table.item(row, 0).text()
            server = self.HomeUpload_Table.item(row, 1).text()
            remoteDirectory = self.HomeUpload_Table.item(row, 2).text()
            credentials = db.getConnectionCredentials(server)
            cnopts1 = pysftp.CnOpts()
            cnopts1.hostkeys=None

            progrssbar = self.HomeUpload_Table.cellWidget(row, 4)
            print(server)
            print(credentials[0][0])
            print(credentials[0][1])
            #print(credentials)
            try:
                with pysftp.Connection(host=server, username=credentials[0][0], password=credentials[0][1], port=22, cnopts=cnopts1) as sftp:
                    print("Connected!")
                    with sftp.cd(remoteDirectory):
                        sftp.put(local_filePath, callback=self.callback)
                        progrssbar.setValue(100)
                        
            except:
                progrssbar.setFormat("Error: 0%")
                progrssbar.setStyleSheet("background-color: red;font-size: 15px;")
                print("Could not send")
            #credentials = QMetaObject.invokeMethod(db, "getConnectionCredentials", Qt.AutoConnection, Q_ARG(str, server))
            #print(credentials)
            #progressBar = self.HomeUpload_Table.cellWidget(row, 4)
            #progressBar.setValue(100)
            #time.sleep(5)
        del db
        # Restore Widgets
        self.HomePresets_List.setEnabled(True)
        self.HomeConnections_Table.setEnabled(True)
        if len(self.HomeConnections_Table.selectedItems()) > 0:
            self.HomeUploadTable_Add_Button.setEnabled(True)
        self.HomeUploadTable_Remove_Button.setEnabled(True)
        self.HomeUploadTable_Clear_Button.setEnabled(True)
        self.HomeUploadTable_Upload_Button.setEnabled(True)

        # QMetaObject.invokeMethod(self, "HomeUploadTable_Clear_Button_Logic", Qt.QueuedConnection)
        # get freeze widgets
        # for each row
        # file , server, remote dir, GET Username, Get Password
        # try to make a connection
        # upload - report back to progress bar for each segment
        # check complete
        # after iteration, unlock widgets


    def Initialize_ProgressBars(self):
        for row in range(self.HomeUpload_Table.rowCount()):
            progressBar = QProgressBar()
            progressBar.setValue(0)
            progressBar.setAlignment(Qt.AlignCenter)
            self.HomeUpload_Table.setCellWidget(row, 4, progressBar)
    


    def Initialize_JobsComboBoxes(self):
        scheduleItems = ["MINUTE", "HOURLY", "DAILY", "WEEKLY", "MONTHLY", "ONCE", "ONLOGON", "ONIDLE"]
        self.JobsSchedule_ComboBox.addItems(scheduleItems)

        db = Database()
        self.JobsPresets_ComboBox.addItems(db.getPresetNames())
        del(db)
    

    def JobsAddJob_Button_logic(self):
        if len(self.JobsName_LineEdit.text().strip()) == 0:
            return
        name = self.JobsName_LineEdit.text()
        preset = self.JobsPresets_ComboBox.currentText()
        schedule = self.JobsSchedule_ComboBox.currentText()
        startTime = self.JobsStartTime_TimeEdit.time().toString("hh:mm")
        startDate = self.JobsStartDate_LineEdit.text()
        endDate = self.JobsEndDate_LineEdit.text()

        cmd = self.addScheduledTask(name, preset, schedule, startTime, startDate, endDate)
        db = Database()
        db.addJob(name, cmd, preset, schedule, startTime, startDate, endDate)
        del db
        self.Display_Jobs()




    def Display_Jobs(self):
        db = Database()
        Jobs = db.getJobs()

        self.JobsTable_Table.setRowCount(0)
        for row, job in enumerate(Jobs):
            #cls
            # print(job[7])
            preset = db.getPreset(job[7])
            print(preset)
            self.JobsTable_Table.insertRow(row)
            self.JobsTable_Table.setItem(row, 0, QTableWidgetItem(job[1]))
            self.JobsTable_Table.setItem(row, 1, QTableWidgetItem(preset[0][0]))
            self.JobsTable_Table.setItem(row, 2, QTableWidgetItem(job[3]))
            self.JobsTable_Table.setItem(row, 3, QTableWidgetItem(job[4]))
            self.JobsTable_Table.setItem(row, 4, QTableWidgetItem(job[5]))
            self.JobsTable_Table.setItem(row, 5, QTableWidgetItem(job[6]))
            self.JobsTable_Table.setItem(row, 6, QTableWidgetItem(job[7]))
        del db


    def addScheduledTask(self, name, preset, schedule, startTime, startDate, endDate):
        db = Database()
        presetID = db.getPresetID(preset)
        print(presetID)
        
        del db
        filepath = os.path.abspath(sys.argv[0])
        
        # get preset ID
        debug_cmd = cmd = f"python {filepath} {presetID[0][0]}"
        #production_cmd = cmd = f"start {filepath} {presetID[0][0]}"
        
        #os.system('schtasks /create /tn "Task Name" /tr "{}" /sc {} /st 00:00'.format(command, schedule))
        if len(startDate) == 0:
            print("Start is none")
            schedule = f'schtasks /create /tn "{name}" /tr "{debug_cmd}" /sc {schedule} /st {startTime}'
        elif len(startDate) > 0 and len(endDate) == 0:
            schedule = f'schtasks /create /tn "{name}" /tr "{debug_cmd}" /sc {schedule} /st {startTime} /sd {startDate}'
        else:
            schedule = f'schtasks /create /tn "{name}" /tr "{debug_cmd}" /sc {schedule} /st {startTime} /sd {startDate} /ed {endDate}'
        
        os.system(schedule)
        return schedule
        print(schedule)
        #print(filepath)

    
    def JobsDeleteJobs_Button_Logic(self):
        db = Database()
        for row in self.JobsTable_Table.selectionModel().selectedRows():
            name = self.JobsTable_Table.item(row.row(), 0).text()
            os.system(f'schtasks /delete /tn "{name}" /f')
            db.deleteJob(name)
            print(name)
        del db
        self.Display_Jobs()

    

#app = QApplication(sys.argv)
#window = MainWindow()
#app.exec_()