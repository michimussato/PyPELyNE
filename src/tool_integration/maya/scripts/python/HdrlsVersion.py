###################################################################################
# (c) Lightmap Ltd 2012
#
# Script simply to hold version information.
###################################################################################
gHdrlsScriptsVersion = 0.45

def GetHdrlsScriptVersion():
    global gHdrlsScriptsVersion
    strVersion = "v" + str(round(gHdrlsScriptsVersion, 3)) + " "# + " (c)2012-2013 Lightmap LTD"
    return strVersion
