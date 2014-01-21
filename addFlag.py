# Author: Jason Wheeler
# E-mail: init6@init6.me
# Project: ScoreBoard for thelab.ms CTF
# 
# Lic: GPLv3
#
#This file is to read in flags from file and insert into database. File format: <flag><tab><points>

from datetime import date
import sys, re, sqlite3, hashlib, json

#Set to True during game to prevent non-sense to FlagDB.
ctf = False

def main():
    
    answer = input( "enter flag y or n" )
    if answer == 'y':
        flag = input( "Flag: \n" )
        points = input( "Points: \n" )
        status = addFlag(flag, points)
        if status:
            print ( "Flag %s was added with %s points. \n" % (flag, points)) 
    else:
        pass


#comment out function for game
def addFlag(flag, points):
    if not ctf:
        try:
            flags = []
            status = None
            conn = sqlite3.connect('scoreboard.db')

            with conn:
                cur = conn.cursor()

                cur.execute("SELECT max(id) FROM flags")
                max_id = cur.fetchone()[0]

                cur.execute("SELECT * FROM flags")
                rows = cur.fetchall()
                #if table is empty no flags have been added go ahead and add flag. 
                if not rows:
                    cur.execute("INSERT INTO flags VALUES (?, ?, ?)", (max_id, flag, points))
                    status = "success"
                    return status

                #Creates a list of all flags then it checks to see if flag is already in the database if not adds it. if so prints error msg.
                else:
                    for row in rows:
                        flags.append(row[1])
                        
                    if flag not in flags:
                        max_id += 1
                        cur.execute("INSERT INTO flags VALUES (?, ?, ?)", (max_id, flag, points))
                        status = "success"
                        return status

                    else:
                        print ( "Flag already in database" )
                        status = "Fail"
                        return status

        except sqlite3.Error as e:
            print ( "Error %s:" % e.args[0] )
            sys.exit(1)

        finally:
            if conn:
                conn.close()
        
    
    
def checkFlag(flag):
    try:
        flags = {}
        conn = sqlite3.connect('scoreboard.db')

        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM flags")
            rows = cur.fetchall()

            #Creates a list of all flags then it checks to see if flag is in the database. if so, updates flag, if not, errors.
            for row in rows:
                flags[row[0]] = row[1]
            for flagID, flagName in flags.items():
                if flag == flagName:
                    cur.execute("SELECT * FROM flags WHERE id=?", (str(flagID)))
                    flagRow = cur.fetchone()
                    #returns flagID and Points
                    return flagRow[0], flagRow[2]

            else:
                print ( "Flag not in database" )
                return None, None

    except sqlite3.Error as e:
        print ( "Error %s:" % e.args[0] )
        sys.exit(1)

    finally:
        if conn:
            conn.close()

    

if __name__ == '__main__':
    main()
