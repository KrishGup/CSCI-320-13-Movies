def movie_lover_ui(uid, conn):
    curs = conn.cursor()

    curs.execute("SELECT firstname FROM movie_lover WHERE uid = %s", (uid,))
    name = curs.fetchone()[0]
    print("hello " + name)

    curs.execute("select count(*) from follows where followeduid = %s", (uid,))
    followercount = curs.fetchone()[0]
    print("you have "+ str(followercount) + " followers")

    curs.execute("select count(*) from follows where followeruid = %s", (uid,))
    followedcount = curs.fetchone()[0]
    print("you follow "+ str(followedcount) + " movie lover(s)")
