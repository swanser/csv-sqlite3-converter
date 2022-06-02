#CSV to SQLite3 Database Converter v0.1
#By Stephen Wanser
#Circa 2022
#A Robots.software Joint

import tkinter
from tkinter import filedialog, messagebox
import sqlite3
import csv

class dataBaser(tkinter.Frame):
    '''
       Class for a GUI window which allows user to select a CSV, optionally specify a table name,
       and create an SQLite3 Database file with name of the user's specification.
    '''

    def __init__(self, parent):

        #Init Window and Frame
        self.parent = parent
        tkinter.Frame.__init__(self, parent)
        self.parent.wm_title("CSV to SQLite3 Database Converter v1 by Stephen Wanser")
        self.generateWidgets()

    def generateWidgets(self):

        #Generate GUI Widgets
        self.mainFrame = tkinter.Frame(self)
        self.mainFrame.grid(row = 0, column = 0)
        self.mainFrame.targetCSVFrame = tkinter.LabelFrame(self.mainFrame, text = "CSV Databaser")  
        self.mainFrame.targetCSVFrame.grid(row = 0, column = 0)
        self.mainFrame.targetCSVFrame.targetText = tkinter.Text(self.mainFrame.targetCSVFrame, height = 1, width = 100)
        self.mainFrame.targetCSVFrame.targetText.grid(row = 0, column = 1, sticky = 'w')
        self.mainFrame.targetCSVButton = tkinter.Button(self.mainFrame.targetCSVFrame, text = "Select CSV", command = self.selectCSV)
        self.mainFrame.targetCSVButton.grid(row = 0, column = 0, sticky = 'w')
        self.mainFrame.tableFrame = tkinter.Frame(self.mainFrame.targetCSVFrame)
        self.mainFrame.tableFrame.grid(row = 1, column = 0, columnspan = 2)
        self.mainFrame.tableNameLabel = tkinter.Label(self.mainFrame.tableFrame, text = "Table Name:")
        self.mainFrame.tableNameLabel.grid(row = 1, column = 0)
        self.mainFrame.tableNameText = tkinter.Text(self.mainFrame.tableFrame, height = 1, width = 25)
        self.mainFrame.tableNameText.grid(row = 1, column = 1)
        self.mainFrame.manifestButton = tkinter.Button(self.mainFrame, text = "Create Database", command = self.manifestDB)
        self.mainFrame.manifestButton.grid(row = 2, column = 0)
        self.grid(row = 0, column = 0)

    def selectCSV(self):

        #Select CSV File
        try:
            self.csvFileName = filedialog.askopenfilename(filetypes = (('CSV Files', '*.csv'),('All Files', '*.*') ) )
            self.mainFrame.targetCSVFrame.targetText.insert('1.0', self.csvFileName)
        except Exception as e:
            print(e)
            pass

    def manifestDB(self):

        #Ensure user has specified CSV file for input prior to trying to click create database button
        if hasattr(self, 'csvFileName'):    

            #Get Table Name, set to MAIN if none specified
            tableName = self.mainFrame.tableNameText.get('1.0', tkinter.END)
            if tableName == "":tableName = "MAIN"

            #Set database filename for output, add .sq3 file extension if user did not
            self.fileName = filedialog.asksaveasfilename(filetypes = (('SQL3LITE Database files', '*.sq3'),('All Files', '*.*') ) )
            if self.fileName[-4:].lower() != ".sq3": self.fileName = self.fileName + ".sq3"

            #Read CSV and store in list
            data_rows = []
            print("Reading CSV")
            with open(self.csvFileName, newline='', encoding='utf-8-sig') as csvFile:
                reader = csv.reader(csvFile, delimiter=',')
                for each_line in reader:
                    data_rows.append(each_line)

            #Initialize database connection and cursor, create table
            self.conn = sqlite3.connect(self.fileName)
            self.cursor = self.conn.cursor()
            createString = f"CREATE TABLE {tableName} (id INTEGER PRIMARY KEY)"
            self.cursor.execute(createString)
            self.conn.commit()

            #Add Columns based on CSV header row
            for eachColumn in data_rows[0]:
                addColumnString = f"ALTER TABLE {tableName} ADD COLUMN {eachColumn} STRING"
                self.cursor.execute(addColumnString)
            self.conn.commit()  
            print("Connected to database")

            #Build out column part of insert string
            counter = 0
            columnString = "("
            for each_column in data_rows[0]:
                columnString = columnString + data_rows[0][counter] + ","
                counter = counter + 1
            columns = columnString[:-1]
            columns = columns + ")"

            #Build out values part of insert string, create insert string, and insert
            for eachRow in data_rows[1:20]:
                counter = 0
                valueString = "("
                for each_value in eachRow:
                    valueString = valueString + '"' + each_value + '"' + ","
                    counter = counter + 1
                values = valueString[:-1]
                values = values + ")"
                insertString = f"INSERT INTO {tableName} {columns} VALUES {values}"
                print(insertString)
                self.cursor.execute(insertString)                

            #Commit changes to database file
            self.conn.commit()
            print("Database manifestation complete.")
            message = "Database " + self.fileName + " creation completed successfully."
            messagebox.showinfo(title="Notice!", message=message)
        else:
            return
       
if __name__ == "__main__":
    newWindow = tkinter.Tk()
    dataBaser(newWindow)

