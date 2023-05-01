# ***********************************************************************************************************************
# *                                                                                                                     *
# *   Database.py                                                                                                       *
# *   Authors: Robert B. Wilson, Alex Baker, Jordan Phillips, Gabriel Snider, Steven Dorsey, Yoshinori Agari            *
# *   The purpose of this file is to provide a easy way to interact with the SFTPPipeline database                      *
# *   Each function uses prepared statements to prevent sql-injection                                                   *
# *                                                                                                                     *
# ***********************************************************************************************************************

import mysql.connector
from datetime import datetime

class Database:
    # Connection Information
    __host = 'localhost'
    __user = 'root'
    __password = 'toor'
    __database = 'SFTPPipeline'
    


    # Function: Constructor
    # Parameters: None
    # Return: If a connection can be established this function will return a Database object, otherwise it will return None
    # Attempts to establish a database connection before a database object is initialized
    def __init__(self):
        try:
            # Connection object
            self.__con = mysql.connector.connect(
                host = self.__host,
                user = self.__user,
                password = self.__password,
                database = self.__database
            )
            # Cursor Object
            self.__cur = self.__con.cursor()
        except:
            print("Could not connect to the SFTPPipeline database...")
            return None
    


    # Function: Destructor
    # Parameters: None
    # Return: None
    # If the object is not None (A database connection has been made), this function attempts to close the connection and cursor attributes before deleting the object.
    def __del__(self):
        if self is not None:
            self.__cur.close()
            self.__con.close()



    # Function: addUser
    # Parameters: username and password of the new user
    # Return: None
    # Attempts to insert new user data into the Users table. If this function fails, a changelog entry will be submitted
    def addUser(self, username, password):
        sql = 'INSERT INTO Users (Username, Password) VALUES (%s, %s)'
        # Attempt to insert date into the Users table
        try:
            self.__cur.execute(sql, (username, password))
            self.__con.commit()
        # Add a changelog entry on fail
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = f"Could not insert {username} into the 'Users' table"
            debug = e
            # Add entry
            self.addChangelog(self, now, message, debug)
            


    # Function: deleteUser
    # Parameters: id (primary key) of the user to be deleted
    # Return: None
    # Attempts to delete a user from the Users table. If this function fails, a changelog entry will be submitted
    def deleteUser(self, username):
        sql = 'DELETE FROM Users WHERE Username = %s'
        # Attempts to delete a user from the Users table
        try:
            self.__cur.execute(sql, (username,))
            self.__con.commit()
        # Add a changelog entry on fail
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = f"Could not delete user username={username} from 'Users' table"
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)



    # Function: getUsers
    # Parameters: None
    # Return: A list of User data from the Users table
    # Attempts to retrieve all users from the Users table. If this function fails, a changelog entry is submitted
    def getUsers(self):
        sql = 'SELECT * FROM Users'
        # Attempt to retrieve all enteries from the Users table
        try:
            self.__cur.execute(sql)
            return self.__cur.fetchall()
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Could not retrieve users from the 'Users' table"
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)



    # Function: getUser
    # Parameters: username and password of the user
    # Return: A list of users with this username and password
    # Attempts to retrieve a use based on their username and password -- this method can be used for authentication. If this function fails, a changelog entry will be submitted
    def getUser(self, username, password):
        sql = "SELECT * FROM Users WHERE Username = %s AND Password = %s"
        # Attempt to retrieve the user
        try:
            self.__cur.execute(sql, (username, password))
            return self.__cur.fetchall()
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Could not retrieve users from the 'Users' table"
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)



    # Function: addChangelog
    # Parameters: Current datetime, uniquely-defined error message, and debug error
    # Return: None
    # Attempts to insert a new changelog entry into the Changelogs table. If this function fails, a debug error is printed
    def addChangelog(self, calendar, message, debug):
        sql = 'INSERT INTO Changelogs (Calendar, Message, Debug) VALUES (%s, %s, %s)'
        # Attempt to insert a new entry
        try:
            self.__cur.execute(sql, (calendar, message, debug))
            self.__con.commit()
        # Print on fail
        except mysql.connector.Error as e:
            print(e)
    


    # Function: deleteChangelog
    # Parameters: id (primary key) of the entry to be deleted
    # Return: None
    # Attempts to delete an entry from the Changelogs table. If this function fails, a changelog entry will be submitted
    def deleteChangelog(self, id):
        sql = 'DELETE FROM Changelogs WHERE id = %s'
        # Attempt to delete changelog entry
        try:
            self.__cur.execute(sql, (id,))
            self.__con.commit()
        # Add a changelog entry on fail
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = f"Could not delete entry id={id}from 'Changelogs' table"
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)



    # Function: getChangelogs
    # Parameters: None
    # Return: A list of Changelog data from the Changelogs table
    # Attempts to retrieve all changelogs from the Changelogs table. If this function fails, a changelog entry is submitted
    def getChangelogs(self):
        sql = 'SELECT * FROM Changelogs'
        # Attempt to retrieve all enteries from the Changelogs table
        try:
            self.__cur.execute(sql)
            return self.__cur.fetchall()
        # Add a changelog entry on fail
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Could not retrieve enteries from the 'Changelog' table"
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)



    # Function: _addFile
    # Parameters: filepath of the file, and the preset-id of its associated preset
    # Return: None
    # Attempts to insert a file into the Files table. If this function fails, a changelog entry will be submitted
    # -- Private Method -- 
    def _addFile(self, filepath, presetID):
        sql = 'INSERT INTO Files (File_Path, Preset_ID) VALUES (%s, %s)'
        # Attemp to insert a new entry
        try:
            self.__cur.execute(sql, (filepath, presetID))
            self.__con.commit()
        # Add a changelog entry on fail
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = f"Could not insert file preset_id={presetID} and path={filepath} into the 'Files' table"
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)



    # Function: _deleteFile
    # Parameters: ID (primary key) of the file to delete
    # Return: None
    # Attempts to delete a file by its ID. If this function fails, a changelog is submitted
    # -- Private Method --
    def _deleteFile(self, id):
        sql = 'DELETE FROM Files WHERE ID = %s'
        # Attempt to delete a entry from the Files table
        try:
            self.__cur.execute(sql, (id,))
            self.__con.commit()
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Could not delete entry Preset_ID={presetID}"
            debug = e
            # Add entry
            self.addChangelog()



    # Function: addPreset
    # Parameters: Name of the preset, the associated connection string, and a list of files to be added to the preset
    # Return: None
    # Attempts to create a new Preset, then retrieve the newly created Preset's ID, then add all associated files to the Files table. If this function fails, a changelog entry is submitted
    # create a preset --> inserts associated data in the file table
    def addPreset(self, name, files, connections):
        sql = "INSERT INTO Presets(Name) VALUES (%s)"
        # Attempt to Create a new Preset, retrieve its ID, and add all associated files to the Files table
        try:
            self.__cur.execute(sql, (name,))
            self.__con.commit()
            # Get the Preset ID
            presetID_sql = 'SELECT * FROM Presets ORDER BY ID DESC LIMIT 1'
            self.__cur.execute(presetID_sql)
            # fetchall() returns a list of each entry from the resulting sql query, so [0][0] returns the first entry's id
            presetID = self.__cur.fetchall()[0][0]
            # Add each file to the files table
            for f in files:
                self._addFile(f, presetID)
            for c in connections:
                self.addPresetConnectionRelation(presetID, c)
        # Add changelog entry on fail
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = f"Could not create Preset with Name={name}"
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)



    def addPresetConnectionRelation(self, presetID, connectionID):
        sql = "INSERT INTO Presets_Connections_Relations(Preset_ID, Connection_ID) VALUES (%s, %s)"
        try:
            self.__cur.execute(sql, (presetID, connectionID))
            self.__con.commit()
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = f"Could not create PresetConnectionRelation with PresetID={presetID} and connectionID={connectionID}"
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)


    # Function: deletePreset
    # Parameters: ID of Preset to delete
    # Returns: None
    # Attempts to delete a Preset, then retrieves all files associated with the preset, then deletes each file. If this function fails, a changelog entry is submitted
    # delete a preset --> deletes associated data in the file table
    def deletePreset(self, id):
        # Attempt to delete all files associated with the preset
        files_sql = 'SELECT * FROM Files WHERE Preset_ID = %s'
        try:
            self.__cur.execute(files_sql, (id,))
            files = self.__cur.fetchall()
            # Attempt to delete each file --> f[0] is the ID of the file
            for f in files:
                self._deleteFile(f[0])
            # Attempt to delete the preset
            sql = 'DELETE FROM Presets WHERE ID = %s'
            self.__cur.execute(sql, (id,))
            self.__con.commit()            
        # Add a changelog entry on fail
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Could not delete preset where ID={id} or Files where Preset_ID={id}"
            debug = e
            # Add entry
            self.addChangelog()
    


    # delete preset - list of names
    # for each preset name
        # get presetID
        # delete Connnection Relations
        # delete Files
        # delete Preset
    def deletePresets(self, preset):
        # preset ID
        sql = 'SELECT ID FROM Presets WHERE NAME = %s'
        # get preset ID
        self.__cur.execute(sql, (preset,))
        Preset_ID = self.__cur.fetchall()
        Preset_ID = list(Preset_ID)
        print(Preset_ID)
        # delete relations
        deleteRelationsSql = 'DELETE FROM Presets_Connections_Relations WHERE Preset_ID = %s'
        deleteFilesSql = 'DELETE FROM Files WHERE Preset_ID = %s'
        deletePresetSql = 'DELETE FROM Presets WHERE ID = %s'
        for id in Preset_ID:
            self.__cur.execute(deleteRelationsSql, (id[0],))
            self.__cur.execute(deleteFilesSql, (id[0],))
            self.__cur.execute(deletePresetSql, (id[0],))
            self.__con.commit()
        





            


    # Function getPresets
    # Parameters: None
    # Return: A list of presets and files representing a single entry in the list. Ex: [ [ (ID, Name, Connection_String), [files...] ] ]
    # Attempts to retrieve all presets entries and their associated files. If this function fails, a changelog entry is submitted
    # view all presets --> select all associated data in the file table. Ex: presets = db.getPresets() ... for preset in presets: preset_file_list = preset[3] ... for files in preset_file_list .. or .. for files in preset[3]
    def getPresets(self):
        presets = []
        # Attemp to retrieve all Presets
        sql = 'SELECT * FROM Presets'
        try:
            self.__cur.execute(sql)
            entries = self.__cur.fetchall()
            # Attempt to retrieve all files associated with the preset
            files_sql = 'SELECT * FROM Files WHERE Preset_ID = %s'
            # build the data-structure [preset, files[]] for each preset entry
            for entry in entries:
                self.__cur.execute(files_sql, (entry[0],))
                files_list = self.__cur.fetchall()
                data = [entry, files_list]
                presets.append(data)
            return presets
        # Add a changelog entry on fail
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = 'Could not retrieve Preset data and associated files'
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)
    


    def getPresetNames(self):
        sql = 'SELECT * FROM Presets'
        try:
            self.__cur.execute(sql)
            presets = [entry[1] for entry in self.__cur.fetchall()]
            return presets
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = 'Could not retrieve Preset names'
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)




    # Function: addConnection
    # Parameters: server (hostname), username, password, remoteDirectory
    # Return: None
    # Attempts to insert a new database entry into the Connections table. If this fails, a changelog entry will be added
    def addConnection(self, server, username, password, remoteDirectory):
        sql = "INSERT INTO Connections (Server, Username, Password, Remote_Directory) VALUES (%s, %s, %s, %s)"
        try:
            self.__cur.execute(sql, (server, username, password, remoteDirectory))
            self.__con.commit()
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Could not create connection with name={server}"
            debug = e
            # Add entry
            self.addChangelog()



    def getConnections(self):
        sql = "SELECT * FROM Connections"
        # Attempt to retrieve all enteries from the Connections table
        try:
            self.__cur.execute(sql)
            return self.__cur.fetchall()
        # Add a changelog entry on fail
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Could not retrieve enteries from the 'Connections' table"
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)
    


    def deleteConnection(self, connectionID):
        sql = "DELETE FROM Presets_Connections_Relations WHERE Connection_ID = %s"
        sql2 = "DELETE FROM Connections WHERE ID = %s"
        try:
            self.__cur.execute(sql, (connectionID,))
            self.__con.commit()

            self.__cur.execute(sql2, (connectionID,))
            self.__con.commit()
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            #message = "Could not delete entry Connection_ID={presetID}"
            debug = e
            # Add entry
            #self.addChangelog()


    def getConnection(self, name, remoteDirectory):
        sql = "SELECT * FROM Connections WHERE Server = %s AND Remote_Directory = %s"
        # Attempt to retrieve all enteries from the Connections table
        try:
            self.__cur.execute(sql, (name, remoteDirectory))
            return self.__cur.fetchall()
        # Add a changelog entry on fail
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Could not retrieve enteries from the 'Connections' table"
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)


    def getConnectionCredentials(self, server):
        sql = "SELECT Username, Password FROM Connections WHERE Server = %s"
        try:
            self.__cur.execute(sql, (server,))
            return self.__cur.fetchall()
        except mysql.connector.Error as e:
            now = datetime.now()
            message = "Could not retrieve enteries from the 'Connections' table"
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)

    def getRelations(self, name):
        # get preset id
        # get files
        # get connections
        #print(name)
        Preset_ID_SQL = 'SELECT ID FROM Presets WHERE Name = %s'
        Files_SQL = 'SELECT File_Path FROM Files WHERE Preset_ID = %s'
        Connection_Relation_SQL = 'SELECT Connection_ID FROM Presets_Connections_Relations WHERE Preset_ID = %s'
        Connection_SQL = 'SELECT Server, Remote_Directory FROM Connections WHERE ID = %s'
        relations = ([],[])
        try:
            self.__cur.execute(Preset_ID_SQL, (name,))
            Preset_ID = self.__cur.fetchall()
            #print("!!")
            #print(Preset_ID[0][0])
            #print(Preset_ID)
            self.__cur.execute(Files_SQL, (Preset_ID[0][0],))
            Files = self.__cur.fetchall()
            for file in Files:
                relations[0].append(file[0])
            
            self.__cur.execute(Connection_Relation_SQL, (Preset_ID[0][0],))
            ConnectionIDs = self.__cur.fetchall()

            for id in ConnectionIDs:
                self.__cur.execute(Connection_SQL, (id[0],))
                temp = self.__cur.fetchall()
                relations[1].append(temp[0])
            #print(relations)
            return relations


        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Error"
            debug = e
            # Add entry
            self.addChangelog(now, message, debug)

    
    # add a job
    def addJob(self, name, command, preset, schedule, startTime, startDate, endDate):
        sql = "INSERT INTO Jobs (Name, Command, Schedule, StartTime, StartDate, EndDate, Preset_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        presetIDSQL = "SELECT ID FROM Presets WHERE Name = %s"
        try:
            self.__cur.execute(presetIDSQL, (preset,))
            Preset_ID = self.__cur.fetchall()

            self.__cur.execute(sql, (name, command, schedule, startTime, startDate, endDate, Preset_ID[0][0]))
            self.__con.commit()            
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Could not create connection with name"
            debug = e
            # Add entry
            self.addChangelog()
    
    def getPreset(self, id):
        sql = "SELECT Name FROM Presets WHERE ID = %s"
        try:
            self.__cur.execute(sql, (id,))
            Preset = self.__cur.fetchall()
            return Preset          
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Could not create connection with name"
            debug = e
            # Add entry
            self.addChangelog()
    

    def getPresetID(self, name):
        sql = "SELECT ID FROM Presets WHERE Name = %s"
        try:
            self.__cur.execute(sql, (name,))
            Preset = self.__cur.fetchall()
            return Preset          
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Could not create connection with name"
            debug = e
            # Add entry
            self.addChangelog()
    # delete a job
    # view all jobs
    def getJobs(self):
        sql = "SELECT * FROM Jobs"
        try:
            self.__cur.execute(sql, ())
            Jobs = self.__cur.fetchall()
            return Jobs
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Could not create connection with name"
            debug = e
            # Add entry
            self.addChangelog()
    

    def deleteJob(self, name):
        sql = "DELETE FROM Jobs WHERE Name = %s"
        try:
            self.__cur.execute(sql, (name,))
            self.__con.commit()
        except mysql.connector.Error as e:
            # Changelog information
            now = datetime.now()
            message = "Could not create connection with name"
            debug = e
            # Add entry
            self.addChangelog()
