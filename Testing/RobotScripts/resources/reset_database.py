import sys
sys.path.append('Database')
import os
import database


project_directory = os.getcwd()
project_directory = project_directory[0:project_directory.find("Project") + 7]    
database_address = os.getcwd() + "/Database/Dart_Scorer_Database.db"
database_connection = database.create_connection(database_address)

database.delete_table(database_connection, "Billy_Bob_Statistics")