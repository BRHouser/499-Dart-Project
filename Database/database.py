import sqlite3
from sqlite3 import Error
import os


# Input: The address of the database, a 2D Array of the header rows of the databases
# Output: The connection to the database
# The purpose of this function is to create a connection to an already existing database
# or create a new database
def create_connection(database_file_directory):
    connection = None
   # try:
   #     connection = create_database(database_file_directory, list_of_table_names, header_of_database)
   # except Error as e:
    connection = sqlite3.connect(database_file_directory, check_same_thread=False)
    
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


# Input: the database_connection not the cursor, the name of the table to insert information, a list of information (2d array) wanting to be added
# The purpose of this function is to update the database
def add_information(database_connection, name_of_table, list_of_information):
    information = get_information(database_connection, name_of_table)
    if len(information) == 1:
        counter = 0
        for x in list_of_information:
            x.insert(0, counter)
            counter = counter + 1
    else:
        last_index = information[len(information) - 1][0] + 1
        for x in list_of_information:
            x.insert(0, last_index)
            last_index = last_index + 1
    cursor = database_connection.cursor()
    questionmarks = ''
    insert_information = ''

    # Finds the column information from the original tables
    cursor.execute("SELECT * FROM " + name_of_table)     
    col_name_list = [tuple[0] for tuple in cursor.description]

    for i in col_name_list:
        if i == col_name_list[0]:
            insert_information += str(i)
            questionmarks = '?'
        else:
            insert_information += ', ' + str(i)
            questionmarks += ',?'
    insert_information = 'INSERT INTO ' + name_of_table +'(' + insert_information + ') VALUES (' + questionmarks + ');'
    cursor.executemany(insert_information, list_of_information)
    database_connection.commit()
    cursor.close()


# Input: the database_connection not the cursor, the name of the table to insert information, an array of a row of information wanting to be added
# The purpose of this function is to update a row in a table based on the id of the row
def replace_row(database_connection, name_of_table, row_information):
    insert_row_information = ''
    insert_column_information = ''

    cursor = database_connection.cursor()


    # Finds the column information from the original tables
    cursor.execute("SELECT * FROM " + name_of_table)     
    col_name_list = [tuple[0] for tuple in cursor.description]

    for i in range(len(col_name_list)):
        if i == 0:
            insert_column_information += str(col_name_list[0])
            insert_row_information += str(row_information[0])
        else:
            insert_column_information += ', ' + str(col_name_list[i])
            insert_row_information += ', ' + str(row_information[i])
    execute_string = "UPDATE " + name_of_table + " SET " 
    for i in range(1,len(row_information)):
        if i != len(row_information) - 1:
            execute_string = execute_string + col_name_list[i] + " = '" + row_information[i] +"', "
        else:
            execute_string = execute_string + col_name_list[i] + " = '" + row_information[i] + "' "
    execute_string = execute_string + " WHERE " + col_name_list[0] + " = '" + row_information[0] + "';"
    cursor.execute(execute_string)
    database_connection.commit()
    cursor.close()
 


# Input: the connection to the database, The name of the table
# The purpose of this function is to delete a table in the database. For instance if a competitor is deleted, then the table containing
# his information should also be deleted
def delete_table(database_connection, name_of_table):
    cursor = database_connection.cursor()
    cursor.execute("DROP TABLE " + name_of_table + ";")
    database_connection.commit()
    cursor.close()

# Input: the connection to the database, the name of the table, an array that contains the information of the row
# The purpose of this function is to delete the row given
def delete_row(database_connection, name_of_table, row_array):
    cursor = database_connection.cursor()

    cursor.execute("SELECT * FROM " + name_of_table)      
    col_name_list = [tuple[0] for tuple in cursor.description]

    cursor.execute("DELETE FROM " + str(name_of_table) + " WHERE " + str(col_name_list[0]) + "='" + str(row_array[0]) + "';")
    database_connection.commit()
    cursor.close()

# Input: the connection to the database, the name of the table, an array that contains the column information
# Output: boolean, true if player is added, false if player is not added
# The purpose of this function is to add a table to the database and create a Database if needed
def add_table(database_connection, name_of_table, array_of_columns):
    cursor = database_connection.cursor()
    execute = "CREATE TABLE " + name_of_table + " ( "
    for column_name in array_of_columns:
        if column_name == array_of_columns[len(array_of_columns) - 1]:
            execute =  execute + " " + column_name + " str);"
        else:
            execute = execute + column_name + " str, "
    try:    #'CREATE TABLE some ( id str, SET str, LEG str, Throw_1 str, Throw_2 str, Throw_3 str,  Score str);'
        cursor.execute(execute)
        database_connection.commit()
        cursor.close()
        return True
    except Error as e:
        return False



# JUST TO SHOW HOW EVERYTHING WORKS TOGETHER
def main():
    database_address = os.getcwd() + "/Dart_Scorer_Database.db"
    #header_info_1 = ["id", "banana", 'apple', 'something']
   # header_info_2 = ["id", 'Dart Statistics', 'Competitor', 'somethingElse']
    #list_of_table_names = ["Competitor_Information", "Dart_Information"]
    #header_info = [header_info_1, header_info_2]
    #information_to_add = [["0", "Ben Swalley", "Marshall Rosenhoover", "3 something"], ["1",'100','2','3'], ["2","SOMETHING", "Marshall", "MMMMM"]]

    #database = create_connection(database_address, header_info, list_of_table_names)
    database = create_connection(database_address)
    info = get_information(database, "List_Matches")
    for x in info:
        delete_row(database, "List_Matches", x)
    #delete_table(database, "THE_BIG_CHUNGUS_Tyler_Chan_Record")
    #add_table(database, "some", ["id", "_Set_", "_Leg_", "Throw_1", "Throw_2",  "Throw_3", "Score"])
    #delete_table(database, "THE_BIG_CHUNGUS2_Tyler_Chan_Record")
    #delete_table(database, "THE_BIG_CHUNGUS2_Marshall_Rosenhoover_Record")
    delete_table(database, "Zelda_Test_Test_Record")
    delete_table(database, "Zelda_Mitchell_Dodson_Record")
    #delete_table(database, "ddddd_Tyler_Chan_Record")
    #delete_table(database, "ddddd_Marshall_Rosenhoover_Record")
    #delete_table(database, "Gabe_Henneberger_Statistics")
    
    #database = create_connection(database_address, header_info, list_of_table_names)
    #information_to_add = ["0", "Marshall", "Rosenhoover"]
    #add_information(database, "Marshall_Rosenhoover_Statistics", [information_to_add])
    #delete_row(database, "List_of_Players", information_to_add)
    #replace_row(database, "Competitor_Information", ["1",'LAUREN','MARSHALL','ANN'])
    
    #add_table(database, "Current_Match", ["id", "Player1Name", "Player2Name","Score", "NumberOfLegs", "NumberOfSets", "Location", "Date"])



if __name__ == '__main__':
    main()
