import mysql.connector
from mysql.connector import Error
import os

class DatabaseConnection:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'student_management_system'
        self.user = 'root'
        self.password = ''  # Change this to your MySQL root password
        
    def get_connection(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def execute_query(self, query, params=None):
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if query.strip().upper().startswith('SELECT'):
                    result = cursor.fetchall()
                    return result
                else:
                    connection.commit()
                    return cursor.lastrowid
            except Error as e:
                print(f"Error executing query: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        return None
    
    def call_procedure(self, proc_name, params=None):
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                if params:
                    cursor.callproc(proc_name, params)
                else:
                    cursor.callproc(proc_name)
                
                connection.commit()
                
                # Fetch results if any
                results = []
                for result in cursor.stored_results():
                    results.extend(result.fetchall())
                
                return results if results else True
            except Error as e:
                print(f"Error calling procedure: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        return None
