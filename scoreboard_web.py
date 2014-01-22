import cherrypy
import datetime
import scoreboard as SB
import json, hashlib

class Root(object):
    @cherrypy.expose
    def index(self):
        """Display Scoreboad"""
        ranks = [] #[1,2,2,4,4]
        done = []
        html = {}
        outhtml = ''
        json_db = SB.updateSB()
        for k in json_db['Teams']:
            ranks.append(k['Rank'])
        ranks = sorted(ranks)

        for rank in ranks:
            for k in json_db['Teams']:
                if k['Rank'] == rank and k['TeamName'] not in done:
                    key = '<p><tr><td>%s</td><td>%s</td><td>%s</td></tr><p>' % (k['Rank'], k['TeamName'], k['teamPoints'])
                    html[key] = rank
                    done.append(k['TeamName'])
        sortedHTML = sorted(html.items(), key=lambda x: x[1])

        for line in sortedHTML:
            outhtml = outhtml + line[0]
            
        
        return '''
<html>
<head>
<title>TheLab.MS CTF</title>
<style type="text/css">
html, body {height:100%; margin:0; padding:0;}
#page-background {position:fixed; top:0; left:0; width:100%; height:100%;}
#content {position:relative; z-index:1; padding:100px;}
</style>
</head>
<body>
    <div id="page-background"><img src="images/bg.jpg" width="100%" height="100%"></div>
    <div id="content">
        <font size="4" color="Green">
        <p><h1> Scoreboard: </h1></p>
            <table border="1" style="color:green; font-size:20pt; text-align:center">
            <th>Rank</th>
            <th>TeamName</th>
            <th>Score</th>
        '''+outhtml+'''
            </table>
        </font>
        <a href="/register"> Click Here to Register Your Awesome Team!</a>
        <br>
        <a href="/submitFlag"> Click Here to Submit that Awesome Flag You Just Found!</a>
    </div>
</body>

</html>
'''

    
    @cherrypy.expose
    def checkFlag(self, TeamName=None, Flag=None):
        """Check the TeamName & Flag"""
        hTeamName = hashlib.sha1(TeamName.encode()).hexdigest()
        status = SB.updateTeam(hTeamName, Flag)
        if status:
            if status == "success":
                return '''
                          <html>
                          <body>
                          <p> Team Name: %s, Flag: %s, Status: %s </p>
                          <a href="/index"> Back to Scoreboard</a>
                          </body>
                          </html>
                       ''' % (TeamName, Flag, status)
            elif status == "Fail":
                return '''
                          <html>
                          <body>
                          <h1>Error: Flag has already been redeemed or bad TeamName</h1>
                          <p> Team Name: %s, Flag: %s, Status: %s </p>
                          <a href="/index"> Back to Scoreboard</a>
                          </body>
                          </html>
                       ''' % (TeamName, Flag, status)

        else:
            return '''
                    <html>
                    <body>
                    <h1> Error:</h1>
                    <a href="/index"> Back to Scoreboard</a>
                    </body>
                    </html>
                   '''
        

    @cherrypy.expose
    def submitFlag(self):
        return '''
        
<html>
<body>
<form action="checkFlag" method="post">
    <p>TeamName</p>
    <input type="text" name="TeamName" value="" size="20" maxlength="40"/>
    <p>Flag</p>
    <input type="text" name="Flag" value="" size="60" maxlength="240"/>
    <p><input type="submit" value="Submit"/></p>
    <p><input type="reset" value="Clear"/></p>
</form>
<a href="/index"> Back to Scoreboard</a>
</body>
</html>
'''

    @cherrypy.expose
    def addTeam(self, TeamName=None):
        """Check the TeamName & Flag"""
        hTeamName = hashlib.sha1(TeamName.encode()).hexdigest()
        status = SB.addTeam(hTeamName, TeamName)
        if status:
            if status == "success":
                return '''
                          <html>
                          <body>
                          <p> Team Name: %s, Status: %s </p>
                          <a href="/index"> Back to Scoreboard</a>
                          </body>
                          </html>
                       ''' % (TeamName, status)
            elif status == "Fail":
                return '''
                          <html>
                          <body>
                          <h1>Error: </h1>
                          <p> Team Name: %s already registered, Status: %s </p>
                          <a href="/index"> Back to Scoreboard</a>
                          </body>
                          </html>
                       ''' % (TeamName, status)

        else:
            return '''
                    <html>
                    <body>
                    <h1> Error:</h1>
                    <a href="/index"> Back to Scoreboard</a>
                    </body>
                    </html>
                   '''
        

    @cherrypy.expose
    def register(self):
        return '''  
                 <html>
                 <body>
                 <form action="addTeam" method="post">
                      <p>TeamName</p>
                      <input type="text" name="TeamName" value="" size="20" maxlength="40"/>
                      <p><input type="submit" value="Submit"/></p>
                    <p><input type="reset" value="Clear"/></p>
                 </form>
                 <a href="/index"> Back to Scoreboard</a>
                 </body>
                 </html>
               '''
    
if __name__ == '__main__':
    SB.createDB() 

    cherrypy.config.update({'server.socket_host': '127.0.0.1',
                            'server.socket_port': 80, })
    #update path to images dir
    #conf = {'/images': {'tools.staticdir.on': True,
    #        'tools.staticdir.dir': 'C:\\Users\\jwheeler\\Documents\\GitHub\\ScoreBoard\\images'}}
    conf = {'/images': {'tools.staticdir.on': True,
            'tools.staticdir.dir': 'C:\\Users\\John\\Documents\\GitHub\\ScoreBoard\\images'}}
    
    print ( conf )
    cherrypy.quickstart(Root(), '/', config=conf)

    #cherrypy.quickstart(Root())                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
