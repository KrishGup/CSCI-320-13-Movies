import datetime
import math
import sys
import os
import psycopg2

userId = "102"   # for testing purposes
logged_in = True  # for testing purposes


is_admin = False # not sure if we need this but just in case
curs = None
conn = None


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
                return
            elif command == "view_collections":
                view_collections()
            elif command == "create_collection":
                create_collection()
            elif command == "name_collection":
                name_collection()
            elif command == "add":
                add_to_collection()
            elif command == "delete":
                remove()
            elif command == "search":
                search()
            elif command == "delete_collection":
                delete_collection()
            elif command == "follow":
                follow()
            elif command == "unfollow":
                unfollow()
            elif command == "watch_movie":
                unfollow()
            elif command == "watch_collection":
                unfollow()
            elif command == "rate":
                rate()
            else:
                print("Invalid command")
                help()

  
def help():
    if logged_in == False:
        print("login - login to your account") # implemented
        print("create - create an account") # implemented
    else: 
        print("logout - logout of your account") # implemented
        print("exit - exit the application") # implemented - confirmed working
        print("view_collections - view your collections") # implemented
        print("create_collection - create a collection") # implemented
        print("add - Add movie to collection") # implemented
        print("delete - deletes movie from collection") # implemented
        print("delete_collection - deletes collection and its contents") # implemented
        print("name_collection - (collection) (name)") 
        print("follow - follow a user") # implemented
        print("unfollow - unfollow a user") # implemented
        print("rate - Add a rating to a movie") # implemented

        print("watch_movie - watch a movie")
        print("watch_collection - watch all movies in a collection")

        print("search - open the search menu")
        
        # Add more commands here

def name_collection():
    print("Name collection")
    collection_name = input("Enter the name of the collection you would like to change: ")
    curs.execute("SELECT * FROM collection WHERE cname = %s", (collection_name,))
    collection = curs.fetchone()
    if collection:
        try:
            new_name = input("Enter the new name of the collection: ")
            curs.execute("UPDATE collection SET cname = %s WHERE cname = %s", (new_name, collection_name,))
            conn.commit()
            print("Collection name was changed")
            curs.execute("SELECT * FROM contains WHERE cname = %s", (collection_name,))
            contains_collections = curs.fetchall()
            
        except Exception as e:
            print("An error occurred:", e)
            conn.rollback()
    else:
        print("Collection not found")

def follow():
    print("Follow user")
    useremail = input("Enter the email of the user you want to follow: ")
    curs.execute("SELECT * FROM movie_lover WHERE uemail = %s", (useremail,))
    user = curs.fetchone()
    if user:
        try:
            curs.execute("INSERT INTO follows (followeruid, followeduid) VALUES (%s, %s)", (userId, user[0]))
            conn.commit()
            print("You are now following " + user[2])
        except Exception as e:
            print("An error occurred:", e)
            conn.rollback()
    else:
        print("User not found")
        
        
def rate():
    print("Rate movie")
    movieid = int(input("Enter the movie ID: "))
    rating = round(float(input("Enter the rating: ")))
    curs.execute("SELECT * FROM movie WHERE mid = %s", (movieid,))
    movie = curs.fetchone()
    if movie:
        try:
            curs.execute("INSERT INTO review (uid, mid, score) VALUES (%s, %s, %s)", (userId, movieid, rating))
            conn.commit()
            print("Movie rated")
        except Exception as e:
            print("An error occurred:", e)
            conn.rollback()
    else:
        print("Movie not found")

def unfollow():
    print("Unfollow user")
    useremail = input("Enter the email of the user you want to unfollow: ")
    curs.execute("SELECT * FROM movie_lover WHERE uemail = %s", (useremail,))
    user = curs.fetchone()
    if user:
        try:
            curs.execute("DELETE FROM follows WHERE followeruid = %s and followeduid = %s", (userId, user[0]))
            conn.commit()
            print("You are no longer following " + user[2])
        except Exception as e:
            print("An error occurred:", e)
            conn.rollback()
    else:
        print("User not found")

def view_collections():
    print("View collections")
    curs.execute("SELECT * FROM collection WHERE uid = %s", (userId,))
    collections = curs.fetchall()
    if collections:
        for collection in collections:
            print(str(collection[0]) + "\n")
    else: 
        print("You have no collections")

def create_collection():
    name = input("Enter the name of the collection: ")
    curs.execute("SELECT * FROM collection WHERE uid = %s", (userId,))
    collections = curs.fetchall()
    if name in collections:
        print("You already have a collection with that name")
    else:
        try:
            curs.execute("INSERT INTO collection (cname, uid) VALUES (%s, %s)", (name, userId))
            conn.commit()
            print("Collection created")
        except Exception as e:
            print("An error occurred:", e)
            conn.rollback()
        
def delete_collection():
    collectionName = input("Enter the name of the collection: ")
    curs.execute("SELECT * FROM collection WHERE uid = %s and cname = %s", (userId, collectionName))
    collections = curs.fetchall()
    if not collections:
        print("Collection not found")
    else:
        try:
            curs.execute("DELETE FROM collection WHERE uid = %s and cname = %s", (userId, collectionName))
            curs.execute("DELETE FROM contains WHERE cname = %s", (collectionName,))
            conn.commit()
            print("Collection deleted")
        except Exception as e:
            print("An error occurred:", e)
            conn.rollback()
    
def add_to_collection():
    print("Add to collection")
    movieid = input("Enter the movie ID: ")
    collectionName = input("Enter the collection name: ")
    curs.execute("SELECT * FROM movie WHERE mid = %s", (movieid,))
    movie = curs.fetchone()
    if movie:
        print("Movie found")
        curs.execute("SELECT * FROM collection WHERE uid = %s and cname = %s", (userId, collectionName))
        collections = curs.fetchone()
        if collections:
            try:
                curs.execute("INSERT INTO contains (movieid, cname, uid) VALUES (%s, %s, %s)", (movieid, collectionName, userId))
                conn.commit()
                print("Movie added to collection")
            except Exception as e:
                print("An error occurred:", e)
                conn.rollback()
        else: 
            print("Collection not found")
    else:
        print("Movie not found")
        
def remove():
    print("Remove from collection")
    collectionName = input("Enter the collection name: ")
    curs.execute("SELECT * FROM collection WHERE uid = %s and cname = %s", (userId, collectionName))
    collections = curs.fetchone()
    if not collections:
        print("Collection not found")
        exit()
    else: 
        print("Collection found")
    movieid = input("Enter the movie ID: ")
    curs.execute("SELECT * FROM movie WHERE mid = %s", (movieid,))
    movie = curs.fetchone()
    if movie:
        print("Movie found")
    else:
        print("Movie not found")
        exit()
    if movie and collections:
        try:
            curs.execute("DELETE FROM contains WHERE movieid = %s and cname = %s and uid = %s", (movieid, collectionName, userId))
            conn.commit()
            print("Movie removed from collection")
        except Exception as e:
            print("An error occurred:", e)
            conn.rollback()

def search():
    print("d - search by director")
    print("c - search by cast")
    print("s - search by studio")
    print("t - search by title")
    print("r - search by release date")
    searchtype = input("> ")
    if searchtype == "d":
        director = input("Enter the director: ")

        curs.execute("SELECT * FROM movie WHERE mid IN (SELECT mid FROM directs WHERE conid IN (SELECT conid FROM contributor WHERE contributor.contributorname LIKE %s))", (director,))
        movies = curs.fetchall()
        if movies:
            for movie in movies:
                print(movie)
        else:
            print("No movies found")
    elif searchtype == "c":
        cast = input("Enter the cast member: ")
        curs.execute("SELECT * FROM movie WHERE mid IN (SELECT mid FROM produce WHERE conid IN (SELECT conid FROM contributor WHERE contributor.contributorname LIKE %s))", (cast,))
        movies = curs.fetchall()
        if movies:
            for movie in movies:
                print(movie)
        else:
            print("No movies found")
    elif searchtype == "s":
        studio = input("Enter the studio: ")
        curs.execute("SELECT * FROM movie WHERE mid IN (SELECT mid from publish where sid IN (select sid from studio where studioname like %s))", (studio,))
        movies = curs.fetchall()
        if movies:
            for movie in movies:
                print(movie)
        else:
            print("No movies found")
    elif searchtype == "t":
        title = input("Enter the title: ")
        curs.execute("SELECT * FROM movie WHERE title = %s", (title,))
        movies = curs.fetchall()
        if movies:
            for movie in movies:
                print(str(movie[0]) + " " + movie[1])
        else:
            print("No movies found")
    elif searchtype == "r":
        date_entry = input('Enter a release date in YYYY-MM-DD format:')
        year, month, day = map(int, date_entry.split('-'))
        date1 = datetime.date(year, month, day)
        curs.execute("SELECT * FROM movie WHERE mid in SELECT * FROM host where pid = 42 and releasedate = %s", (date1,))
        movies = curs.fetchall()
        if movies:
            for movie in movies:
                print(str(movie[0]) + " " + movie[1])
        else:
            print("No movies found")
    else:
        print("Invalid search type")
        search()

def create():
    print("\nCreate account")
    curs.execute("select max(uid) from movie_lover")
    uid = curs.fetchone()[0] + 1
    email = input("Email: ").lower()
    username = input("Username: ")
    password = input("Password: ")
    firstname = input("First Name: ")
    lastname = input("Last Name: ")
    creationdate = datetime.datetime.now()
    try:
        curs.execute("INSERT INTO movie_lover (uid, uemail, username, password, firstname, lastname, creationdate) VALUES (%s, %s, %s, %s, %s, %s, %s)", (uid, email, username, password, firstname, lastname, creationdate))
        conn.commit()
        print("Account created \n\n")
        login()
    except Exception as e:
        print("An error occurred:", e)
        conn.rollback()

def login():
    global logged_in, is_admin, userId
    print("Login")
    email = input('email: ').lower()
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
        
        # update access date
        curs.execute("UPDATE movie_lover SET lastaccess = %s WHERE uid = %s", (datetime.datetime.now(), userId))
        
        curs.execute("SELECT count(*) from follows where followeduid = %s", (userId, )) # I don't quite understand why, but that comma is necessary
        info = curs.fetchone()
        followers =  str(info[0]) if info else "0"
        
        curs.execute("SELECT count(*) from follows where followeruid = %s", (userId, )) # the comma makes it a tuple?
        info = curs.fetchone()
        following = str(info[0]) if info else "0"
        
        print("You have " + followers + " followers")
        print("You are following " + following + " people")
        
        
    else:
        print("Invalid email or password\n\n")




if __name__ == "__main__":
    print("run from db_connection.py")
    
        
#except:
    #print("Connection failed")





