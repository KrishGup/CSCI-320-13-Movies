import datetime
import math
import sys
import os
import psycopg2

logged_in = False
curs = None
conn = None

def main(cursor, connection):
    global curs, conn
    curs = cursor
    conn = connection
    print("Welcome to the Movies Application")
    while not logged_in:
        command = input("Would you like to login or create an account? \n > ")
        if command == "login":
            login()
        elif command == "create":
            create()
        else:
            print("login - login to your account")
            print("create - create an account")
    while logged_in:
        command = input("Enter a command \n > ")
        if command == "logout":
            logged_in = False
            print("Logged out")
        elif command == "help":
            help()
        elif command == "exit":
            sys.exit()
        else:
            print("Invalid command")
            help()

  
def help():
    if logged_in == False:
        print("login - login to your account")
        print("create - create an account")
    else: 
        print("logout - logout of your account")
        print("exit - exit the application")
        
        # Add more commands here



def create():
    print("\nCreate account")
    curs.execute("select max(uid) from movie_lover")
    uid = curs.fetchone()[0] + 1
    email = input("Email: ")
    username = input("Username: ")
    password = input("Password: ")
    firstname = input("First Name: ")
    lastname = input("Last Name: ")
    creationdate = datetime.datetime.now()
    curs.execute("INSERT INTO movie_lover (uid, uemail, username, password, firstname, lastname, creationdate) VALUES (%s, %s, %s, %s, %s, %s, %s)", (uid, email, username, password, firstname, lastname, creationdate))
    conn.commit()
    print("Account created \n\n")
    login()
    

def login():
    global logged_in
    print("Login")
    email = input('Email: ')
    password = input('password: ')

    if email == 'admin' and password == 'password':
        print('admin')
        # do the admin things here

    curs.execute("SELECT * FROM movie_lover WHERE uemail = %s AND password = %s", (email, password))

    user = curs.fetchone()
    
    if user:
        logged_in = True
        curs.execute() # TODO: SQL state to retrieve followers and following
        info = curs.fetchone()
        followers = str(info[0])
        following = str(info[1])
        print("Welcome " + user[2]) # username
        print("You have " + followers + " followers")
        print("You are following " + following + " people")
    else:
        print("Invalid email or password")


if __name__ == "__main__":
    print("run from db_connection.py")
    
        
#except:
    #print("Connection failed")





