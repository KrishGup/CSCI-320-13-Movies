import datetime
import math
import sys
import os
import psycopg2

logged_in = False
is_admin = False # not sure if we need this but just in case
curs = None
conn = None
userId = "" # probably a better way then to store this globally

def main(cursor, connection):
    global curs, conn, logged_in, userId
    curs = cursor
    conn = connection
    print("Welcome to the Movies Application")
    while True:
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
                userId = ""
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
    global logged_in, is_admin, userId
    print("Login")
    email = input('Email: ')
    password = input('password: ')

    if email == 'admin' and password == 'password':
        print('admin')
        is_admin = True
        # do the admin things here

    curs.execute("SELECT * FROM movie_lover WHERE uemail = %s AND password = %s", (email, password))

    user = curs.fetchone()
    
    if user:
        logged_in = True
        userId = str(user[0])
        print("User ID: " + userId)
        print("Welcome " + user[2]) # username
        curs.execute("SELECT count(*) from follows where followeduid = %s", (userId, )) # get the number of followers and following
        info = curs.fetchone()
        followers =  str(info[0]) if info else "0"
        curs.execute("SELECT count(*) from follows where followeruid = %s", (userId, )) # get the number of followers and following
        info = curs.fetchone()
        following = str(info[0]) if info else "0"
        print("You have " + followers + " followers")
        print("You are following " + following + " people")
    else:
        print("Invalid email or password")




if __name__ == "__main__":
    print("run from db_connection.py")
    
        
#except:
    #print("Connection failed")





