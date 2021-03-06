# Author: Jason Wheeler
# E-mail: init6@init6.me
# Project: ScoreBoard for thelab.ms CTF
# 
# Lic: GPLv3
#

from datetime import date
import sys, re, sqlite3, hashlib, json

def updateSB():
    try:
        json_db = {}
        json_db['Teams'] = []
        teams = []
        hs = []
        status = None
        conn = sqlite3.connect('scoreboard.db')

        with conn:
            cur = conn.cursor()

            cur.execute("SELECT * FROM teams")
            rows = cur.fetchall()
            for row in rows:
                teams.append(row[0])
            for hName in teams:
                tableName = 'a'+hName
                cur.execute("SELECT * FROM "+tableName)
                teamRow = cur.fetchone()
                team = {}
                team['TeamHash'] = hName
                team['TeamName'] = teamRow[1]
                team['flagCount'] = teamRow[3]
                team['teamPoints'] = teamRow[5]
                team['Rank'] = 0
                json_db['Teams'].append( team )

            for k in json_db['Teams']:
                hs.append(k['teamPoints'])
            #sort hs. then go through list if hs equals teamPoints take index as place. 
            hs = sorted(hs, reverse=True)
            for k in json_db['Teams']:
                k['Rank'] = int(hs.index(k['teamPoints'])) + 1
                
            return json_db
        
    except sqlite3.Error as e:
        print ( "Error %s:" % e.args[0] )
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            
def addTeam(hName, name):
    try:
        teams = []
        tableName = 'a'+hName
        status = None
        conn = sqlite3.connect('scoreboard.db')

        with conn:
            cur = conn.cursor()

            cur.execute("SELECT * FROM teams")
            rows = cur.fetchall()
            #if table is empty no teams have been added go ahead and add team.
            if not rows:
                cur.execute("INSERT INTO teams VALUES (?, ?)", (hName, name))
                conn.commit()
                createTeamDB(hName)
                cur.execute("INSERT INTO "+tableName+" VALUES (?, ?, ?, ?, ?, ?)", (hName, name, 0, 0, 0, 0))
                status = "success"
                return status

            #Creates a list of all teams then it checks to see if hName is already in the database
            #if not adds it. if so prints error msg.
            else:
                for row in rows:
                    teams.append(row[0])
                    
                if hName not in teams:
                    cur.execute("INSERT INTO teams VALUES (?, ?)", (hName, name))
                    conn.commit()
                    createTeamDB(hName)
                    cur.execute("INSERT INTO "+tableName+" VALUES (?, ?, ?, ?, ?, ?)", (hName, name, 0, 0, 0, 0))
                    status = "success"
                    return status

                else:
                    print ( "Team already registered in database" )
                    status = "Fail"
                    return status

    except sqlite3.Error as e:
        print ( "Error %s:" % e.args[0] )
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            
    
def updateTeam(hName, flag):
    teams = []
    flagIDs = []
    tableName = 'a'+hName
    status = None
    #get flagID and points. If flagID not None continue else. error. 
    flagID, points = checkFlag(flag)
    
    if flagID:
        try:
            conn = sqlite3.connect('scoreboard.db')

            with conn:
                cur = conn.cursor()

                cur.execute("SELECT * FROM teams")
                rows = cur.fetchall()
                #if table is empty no teams have been added. so can't update a team register first.
                if not rows:
                    return status

                #Creates a list of all teams then it checks to see if hName is in the database.
                #if so, updates flag, if not, errors.
                else:
                    for row in rows:
                        teams.append(row[0])
                        
                    if hName in teams:
                        #Get current flag Count and Team Points. 
                        cur.execute("SELECT * FROM "+tableName)
                        teamRow = cur.fetchone()
                        
                        teamFlags = teamRow[3]
                        teamPoints = teamRow[5]

                        cur.execute("SELECT * FROM "+tableName)
                        rows = cur.fetchall()
                        for row in rows:
                            flagIDs.append(row[2])
                        #Check to see if flagID has been submitted before and awarded. 
                        if flagID not in flagIDs:
                            teamPoints += points
                            #How many flags does the team have.
                            hFlags = int(teamFlags) + 1

                            cur.execute("UPDATE "+tableName+" SET flags=?,tPoints=? WHERE hName=?", (str(hFlags), teamPoints, hName)  )
                            cur.execute("INSERT INTO "+tableName+" VALUES (?,?,?,?,?,?)", (0, 0, flagID, flag, points, 0) )
                            status = "success"
                            return status
                        else:
                            print ( "Flag has already been submitted" )
                            status = "Fail"
                            return status

                    else:
                        print ( "Team not registered in database. Please check the spelling or register new team and try again. " )
                        return status

        except sqlite3.Error as e:
            print ( "Error %s:" % e.args[0] )
            #sys.exit(1)
            return None

        finally:
            if conn:
                conn.close()
    else:
        print ( "Flag not in database " )
        return status


def checkFlag(flag):
    try:
        flags = {}
        conn = sqlite3.connect('scoreboard.db')

        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM flags")
            rows = cur.fetchall()

            #Creates a list of all teams then it checks to see if hName is in the database. if so, updates flag, if not, errors.
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

def createTeamDB(tableName):
    tableName = 'a'+tableName
    conn = sqlite3.connect('scoreboard.db')
    cur = conn.cursor()


    #create table teams and data names/types 
    cur.execute('CREATE TABLE IF NOT EXISTS '+tableName+' (hName TEXT, name TEXT, flagID INTEGER, flags TEXT, flagPoints INTEGER, tPoints INTEGER)' ) 
    
    conn.commit()
    cur.close()
    conn.close()
    
def createDB():

    conn = sqlite3.connect('scoreboard.db')
    cur = conn.cursor()

    #create table flags and data names/types 
    cur.execute('''CREATE TABLE IF NOT EXISTS flags
                 (id INTEGER PRIMARY KEY, flag TEXT, points INTEGER)''')

    #create table teams and data names/types 
    cur.execute('''CREATE TABLE IF NOT EXISTS teams
                 (hName TEXT, name TEXT)''')

    #create table scoreboard and data names/types 
    cur.execute('''CREATE TABLE IF NOT EXISTS scoreboard
                 (hName TEXT, name TEXT, points INTEGER, place INTEGER)''')
    

  
    conn.commit()
    cur.close()
    conn.close()

    

if __name__ == '__main__':
    main()
