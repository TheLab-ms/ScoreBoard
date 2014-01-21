# Author: Jason Wheeler
# E-mail: init6@init6.me
# Project: ScoreBoard for thelab.ms CTF
# 
# Lic: GPLv3
#

from datetime import date
import sys, re, sqlite3, hashlib, json

#Set to True during game to prevent non-sense to FlagDB.
ctf = False

def main():
    
    #initialize the database with tables
    if not ctf:
        createDB()
    updateSB()
    '''
    answer = input( "add team? \n" )
    if answer == 'y':
        TeamName = input( "Enter TeamName \n" )
        hTeamName = hashlib.sha1(TeamName.encode()).hexdigest()

        status = addTeam(hTeamName, TeamName)

        if status:
            print ( " Team %s was added. \n" % TeamName )
    else:
        pass

    answer = input( "enter flag y or n" )
    if answer == 'y':
        flag = input( "Flag: \n" )
        points = input( "Points: \n" )
        status = addFlag(flag, points)
        if status:
            print ( "Flag %s was added with %s points. \n" % (flag, points)) 
    else:
        pass

    answer = input( "Update team y or n. \n" )
    if answer == 'y':
        TeamName = input( "Enter TeamName \n" )
        hTeamName = hashlib.sha1(TeamName.encode()).hexdigest()
        flag = input( "Enter Flag: \n" )

        status = updateTeam(hTeamName, flag)
        if status:
            print ( "Team %s was updated. \n" % (TeamName) )
    '''
    
    
def updateSB():
    try:
        json_db = {}
        json_db['Teams'] = []
        teams = []
        highScore = 0
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
                teamRow = cur.fetchone() #hName TEXT, name TEXT, flagID INTEGER, flags TEXT, flagPoints INTEGER, tPoints INTEGER
                team = {}
                team['TeamHash'] = hName
                team['TeamName'] = teamRow[1]
                team['flagCount'] = teamRow[3]
                team['teamPoints'] = teamRow[5]
                team['Rank'] = 0
                json_db['Teams'].append( team )
            print( json.dumps(json_db, indent=4, separators=(',', ': ')) )
            for x in range(0,len(teams)*2):
                for k in json_db['Teams']:
                    currentRank = k['Rank']
                    if k['teamPoints'] > highScore:
                        highScore = k['teamPoints']
                        k['Rank'] = currentRank + 1
                        
            print( json.dumps(json_db, indent=4, separators=(',', ': ')) )
                    


                
                
    
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

            #Creates a list of all teams then it checks to see if hName is already in the database if not adds it. if so prints error msg.
            #hName TEXT, name TEXT, flagID INTEGER, flags TEXT, flagPoints INTEGER, tPoints INTEGER
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

                #Creates a list of all teams then it checks to see if hName is in the database. if so, updates flag, if not, errors.
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
                     
                            #hName TEXT, name TEXT, flagID INTEGER, flags TEXT, flagPoints INTEGER, tPoints INTEGER
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
            sys.exit(1)

        finally:
            if conn:
                conn.close()
    else:
        print ( "Flag not in database " )
        return status

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
