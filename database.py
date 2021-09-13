import sqlite3
from sqlite3 import Error
import os


# Input: The address of the database, a 2D Array of the header rows of the databases
# Output: The connection to the database
# The purpose of this function is to create a connection to an already existing database
# or create a new database
def create_connection(database_file_directory, header_of_database, list_of_table_names):
    connection = None
    try:
        connection = create_database(database_file_directory, list_of_table_names, header_of_database)
    except Error as e:
        connection = sqlite3.connect(database_file_directory)
    
    return connection

# Input: address_of_database (the address of the new database being created or accessed), name_of_database (the name of the table within the database),
# Input: list_of_wanted_information (list of states that are the same between two tables but the first index has the names of the rows and the last two indexes have the number of seen for each table)
def create_database(address_of_database, name_of_database, header_of_database):
    # creates a connection to the table
    connection = sqlite3.connect(address_of_database)
    cursor = connection.cursor()
    x = 0
    # checks to see if a table needs to be made
    try:
        sqlite_insert_query = ''
        for header in header_of_database:
            for i in header:
                if i == header[0]:
                    sqlite_insert_query = str(header[0]) + ' str'
                else:
                    sqlite_insert_query += ', ' + str(i) + ' str'
            sqlite_insert_query = 'CREATE TABLE ' + str(name_of_database[x]) + '(' + sqlite_insert_query + ')'
            cursor.execute(sqlite_insert_query)
            x += 1
    except Error as e:
        print("DEBUG: ERROR WITH CREATING DATABASE OR DATABASE IS ALREADY CREATED")

    return connection

# Input: Database1 (Connection to a database), Database2 (Connection to a database), 
# Input: name_of_section (the name table to draw information from), limit (the seen lower limit)
# Output: A list 
# The purpose is to get the information of a specified table and return the information in a parseable format
def get_information(database_connection, name_of_table):
    cursor1 = database_connection.cursor()

    # Finds the column information from the original tables
    cursor1.execute("SELECT * FROM " + name_of_table)     
    col_name_list = [tuple[0] for tuple in cursor1.description]
    table_information = []
    table_information.append(col_name_list)


    cursor1.execute("SELECT * FROM " + name_of_table)
    
    for row in cursor1.fetchall():
        table_information.append(row)
    
    cursor1.close()
    return table_information


# Input: the database_connection not the cursor, the name of the table to insert information, a 2D array of information wanting to be added
# The purpose of this array is to update the database
def add_information(database_connection, name_of_table, list_of_information):
    cursor = database_connection.cursor()
    questionmarks = ''
    insert_information = ''

    # Finds the column information from the original tables
    cursor.execute("SELECT * FROM " + name_of_table)     
    col_name_list = [tuple[0] for tuple in cursor.description]
    table_information = []
    table_information.append(col_name_list)

    for i in col_name_list:
        if i == col_name_list[0]:
            insert_information += str(i)
            questionmarks = '?'
        else:
            insert_information += ', ' + i
            questionmarks += ',?'
    insert_information = 'INSERT INTO ' + name_of_table +'(' + insert_information + ') VALUES (' + questionmarks + ');'
    cursor.executemany(insert_information, list_of_information)
    database_connection.commit()
    cursor.close()


# JUST TO SHOW HOW EVERYTHING WORKS TOGETHER
def main():
    database = os.getcwd() + "/Dart_Scorer_Database.db"
    header_info_1 = ["banana", 'apple', 'something']
    header_info_2 = ['Dart Statistics', 'Competitor', 'somethingElse']
    list_of_table_names = ["Competitor_Information", "Dart_Information"]
    header_info = [header_info_1, header_info_2]
    information_to_add = [["2 Banana", "2 Apple", "3 something"], ['1','2','3'], ["SOMETHING", "Marshall", "MMMMM"]]

    database = create_connection(database, header_info, list_of_table_names)
    add_information(database, "Competitor_Information", information_to_add)

if __name__ == '__main__':
    main()
