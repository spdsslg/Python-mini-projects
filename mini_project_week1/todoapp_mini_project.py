import sys
import sqlite3
from sqlite3 import Error

class Task:
    def __init__(self, name: str, id: int = None, done: bool = False)->None:
        #this is a validation below
        assert len(name)>0, f"The task name must not be empty!"

        self.id = id
        self.name = name
        self.done = done

    def __str__(self):
        stat = "✓" if self.done else "✗"
        return f"[{stat}] {self.id}:{self.name}"

    @classmethod
    def all(cls, connection):
        query = """
        SELECT *
        FROM tasks
        ORDER BY id
        """
        rows = execute_read_query(connection, query)
        return [cls(name=row[1],id=row[0], done=row[2]) for row in rows]
    
    @classmethod
    def find_due_tasks(cls, connection):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT *
        FROM tasks
        WHERE done = 0
        """)
        temp_tuples = cursor.fetchall()
        return [cls(name=row[1],id=row[0],done=row[2]) for row in temp_tuples]
    
    @classmethod
    def find_done_tasks(cls, connection):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT *
        FROM tasks
        WHERE done = 1
        """)
        temp_tuples = cursor.fetchall()
        return [cls(name=row[1],id=row[0],done=row[2]) for row in temp_tuples]
    
    
    def save(self, connection):

        cursor = connection.cursor()

        if(self.id is None):   #this is executed if the object is not yet in the database
            if(self.name_duplicate_check(connection)):
                print(f"Oops... a task like '{self.name}' already exists!")
                return
            
            cursor.execute("""
                        INSERT INTO tasks(name,done) VALUES(?,?); 
                        """, (self.name, int(self.done))) #creating a new row
            self.id = cursor.lastrowid
        else:                  #if the object exists in db we update its values
            cursor.execute("""
            UPDATE tasks 
            SET name = ?, done = ?
            WHERE id = ?;
            """, (self.name, self.done, self.id))
        
        connection.commit()

    def name_duplicate_check(self, connection):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT *
        FROM tasks
        WHERE name LIKE ?
        """, (self.name,))
        temp_name = cursor.fetchone()
        if(temp_name):
            return True
        return False

    def mark_as_done(self, connection):
        if(not self.done):
            self.done = True
            print(f"Task {self.id} with name '{self.name}' is successfully marked as DONE")
            self.save(connection)
        else:
            print(f"Task {self.id} with name '{self.name}' is ALREADY marked as DONE!")
    
    def mark_as_undone(self, connection):
        if(self.done):
            self.done = False
            print(f"Task {self.id} with name '{self.name}' is successfully marked as UNDONE")
            self.save(connection)
        else:
            print(f"Task {self.id} with name '{self.name}' is ALREADY marked as UNDONE!")

    def delete_task(self, connection):
        cursor = connection.cursor()
        try:
            cursor.execute("""
            DELETE FROM tasks
            WHERE id = ?
            """, (self.id,))
            connection.commit()
        except Error as err:
            print(f"An error occurred while trying to delete task {self.id}: {self.name}")
        


def establish_connection(filename):
    connection = None
    try:
        connection = sqlite3.connect(filename)
        print(f"connected to db with path {filename} successfully!")
    except Error as err:
        print(f"An error '{err}' occurred while connecting")
    
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("query executed successfully!")
    except Error as err:
        print(f"An error '{err}' occurred while executing query")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"An error '{err}' occurred while trying to read a query")

def create_table(connect):  #function that creates a table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        done INTEGER NOT NULL DEFAULT 0
    );
    """
    execute_query(connect, create_table_query)

def clear_table(connection):
    cursor = connection.cursor()
    clear_query = """
    DELETE FROM tasks;
    """
    try:
        cursor.execute(clear_query)
        cursor.execute("""
        DELETE FROM sqlite_sequence
        WHERE name = 'tasks';
        """)
        connection.commit()
        print("All tasks have been successfully deleted!")
    except Error as err:
        print("Error '{err} occurred while trying to delete all tasks!'")


def find_task_by_name(connection, key_name):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT *
    FROM tasks
    WHERE name = ?
    """, (key_name,))
    temp_tuple = cursor.fetchone()
    if(temp_tuple):
        return Task(temp_tuple[1], temp_tuple[0], temp_tuple[2])
    else:
        return None
    

def print_all_table(connection):
    table = Task.all(connection)
    if(not table):
        print("Currently there are no tasks to list!")
    for task in table:
        print(task)


def main():
    connect = establish_connection("./mini_projects/mini_project_week1/todo.sqlite") 
    create_table(connect)

    choice = ''
    valid_choices = [str(i) for i in range(0,9)]
    while(choice != '0'):
        print("""
        0. Exit
        1. Print all tasks
        2. Print all due tasks
        3. Print all done tasks
        4. Add new task
        5. Mark a task as done 
        6. Mark a task as undone
        7. Delete a task
        8. Delete all tasks
        """)

        choice = str(input())
        if(choice not in valid_choices):
            print(f"Invalid command, enter a number from 0 to {len(valid_choices) - 1}")
            continue
        
        if(choice == '0'):
            sys.exit(0)
        
        elif(choice == '1'):
            print_all_table(connect)

        elif(choice == '2'):
            due_tasks = Task.find_due_tasks(connect)
            for t in due_tasks:
                print(t)

        elif(choice == '3'):
            done_tasks = Task.find_done_tasks(connect)
            for t in done_tasks:
                print(t)

        elif(choice == '4'):
            print("Enter a name for the task: ", end='')
            new_name = str(input())
            new_task = Task(new_name)
            new_task.save(connect)

        elif(choice == '5'):
            print("Enter a name of the task you want to mark as done: ",end='')
            done_name = str(input())
            done_task = find_task_by_name(connect, done_name)
            if(not done_task):
                print(f"There is no such task as '{done_task}' in a list!")
                continue
            else:
                done_task.mark_as_done(connect)

        elif(choice == '6'):
            print("Enter a name of the task you want to mark as undone: ",end='')
            undone_name = str(input())
            undone_task = find_task_by_name(connect, undone_name)
            if(not undone_task):
                print(f"There is no such task as '{undone_task}' in a list!")
                continue
            else:
                undone_task.mark_as_undone(connect)
            

        elif(choice == '7'):
            print("Enter a name of the task you want to delete: ",end='')
            to_delete_name = str(input())
            to_delete_task = find_task_by_name(connect, to_delete_name)
            if(not to_delete_task):
                print(f"There is no such task as '{to_delete_name}' in a list!")
                continue
            else:
                to_delete_task.delete_task(connect)

        elif(choice == '8'):
            clear_table(connect)


    # task1 = Task("practice SQL")
    # task1.save(connect)

    # print_all_table()

    # task1.delete_task(connect)

    # table = Task.all(connect)
    # for task in table:
    #     print(task)

    #clear_table(connect)



if __name__ == '__main__':
    main()

