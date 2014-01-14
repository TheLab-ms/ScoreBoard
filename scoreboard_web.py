import cherrypy
import datetime
import ScoreBoard as SB

class Root(object):
    @cherrypy.expose
    def Register(self, TeamName=None, Flag=None):
        """Check the TeamName & Flag"""
        hTeamName = hash(TeamName)
        SB.checkTeam(hTeamName, TeamName)
        isOkay = SB.checkFlag(Flag) 
        if isOkay:
            status = "success"
        else:
            status = "Fail"
        
        return '''
<html>
<body>
<p> Team Name: %s, Flag: %s, Status: %s </p>
</body>
</html>
''' % (TeamName, Flag, status)
    
    @cherrypy.expose
    def index(self):
        return '''
        
<html>
<body>
<form action="Register" method="post">
    <p>TeamName</p>
    <input type="text" name="TeamName" value="" size="20" maxlength="40"/>
    <p>Flag</p>
    <input type="text" name="Flag" value="" size="60" maxlength="240"/>
    <p><input type="submit" value="Submit"/></p>
    <p><input type="reset" value="Clear"/></p>
</form>
</body>
</html>
'''
    
if __name__ == '__main__':

    cherrypy.quickstart(Root())