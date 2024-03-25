import psycopg2
from sshtunnel import SSHTunnelForwarder
import os
import json
from movie_lover_ui import *

with open('../personal_information.json', 'r') as file:
    data = json.load(file)

username = "sdm9252"
password = data['password']
dbName = "p320_13"


if True:
    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=username,
                            ssh_password=password,
                            remote_bind_address=('127.0.0.1', 5432)) as server:
        server.start()
        print("SSH tunnel established")
        params = {
            'database': dbName,
            'user': username,
            'password': password,
            'host': 'localhost',
            'port': server.local_bind_port
        }


        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print("Database connection established")

        # DB work here....
        email = input('Email: ')
        password = input('password: ')
        email = "user1@example.com"
        password = "pass123"

        if email == 'admin' and password == 'password':
            print('admin')
            # do the admin things here

        curs.execute("SELECT * FROM movie_lover WHERE uemail = %s AND password = %s", (email, password))

        user = curs.fetchone()
        
        if user:
            print(user)
            uid = user[0]
            print(uid)
            movie_lover_ui(uid, conn)

        

        conn.close()
        
        
        
#except:
    #print("Connection failed")





