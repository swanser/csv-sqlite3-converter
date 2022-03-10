# csv-sqlite3-converter
GUI to convert CSV file to SQLite3 Database

This GUI program allows a user to specify a comma delimited CSV text file to read in as input.
Optionally, it allows the user to specify the table name that will be the only table in the initial creation of the SQLite3 databsae.
If the user does not specify a table name, the default table name will be set to MAIN.
Once the user clicsk the create database button, it will ask the user to specify the output .SQ3 file.
If the user does not add .SQ3 on the end, it will do so automatically.
The script then reads in the CSV file.
A database with an integer primary key named ID is created.
The table is then created, and the script takes the first row of the CSV file to use as the columns for the databsae.
Each field in the first row of the CSV file becomes a column.
Each subsequent row becomes values inserted into the corresponding column. They are all STRING type values in the database in this initial version.
An info window pops up upon completion of the creation process of the database.
