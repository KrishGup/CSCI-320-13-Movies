def movie_lover_ui(uid, conn):

    print("called")
    curs = conn.cursor()

    curs.execute("SELECT firstname FROM movie_lover WHERE uid = %s", (uid,))
    name = curs.fetchone()[0]
    print("hello " + name)