'''
Created on 19.12.2014

@author: michael.mussato
'''

#from xml.dom import minidom
#from xml.etree import *
import xml.etree.ElementTree as ET
from operator import *
import platform
#import platform

class parseApplicationsXML():
    '''
    classdocs
    '''


    def __init__(self, platform):
        #self.currentPlatform = platform.system()
        
        self.xmlPath = ''
        
        self.families = []
        self.applications = []
        
        self.platform = platform
        
        
        
        self.getXmlPath()
        self.getApplications()
        
        #print self.families
        
    def getXmlPath(self):
        
        if self.platform == "Windows":
            self.xmlPath = r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\conf\applications.xml'

        elif self.platform == "Linux" or self.platform == "Darwin":
            self.xmlPath = r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/conf/applications.xml'

        
        #return self.xmlPath
    
    def getApplications(self):
        
        tree = ET.parse(self.xmlPath)
        root = tree.getroot()
        
#         root.tag
#         root.attrib
        
        for name in root:
            self.families.append(name.attrib)
            #print name.attrib
            for details in name.iter():
                #print details.attrib
                self.applications.append(details.attrib)
#             for subEntry in child.iter():
#                 
#                 #self.applications.append(child.attrib)
#                 self.applications.append(subEntry.attrib)
#             #print child



        

# xmlObject = parseApplicationsXML()
# 
# for i in xmlObject.applications:
#     print i

currentPlatform = platform.system()

tree = ET.parse(r'../conf/applications.xml')
root = tree.getroot()

#print root

for family in root:
    for element in family:
        for vendor in element:
            for platform in vendor:
                print platform
                for executable in platform:
                    print executable
                    for flag in executable:
                        print "hallo"
                        if not executable.items()[0][1] == 'None' and platform.items()[0][1] == currentPlatform:
                        
                            print element.items()[0][1] + ' ' + family.items()[0][1] + ' ' + platform.items()[0][1] + ' ' + executable.tag + ' = ' + executable.items()[0][1]
                    
                #print family.attrib, element.attrib, platform.attrib, executable.tag, executable.attrib
    

    #print name.tag
    #print name.attrib



'''
xmlObject = parseApplicationsXML()
xmlPath = xmlObject.getXmlPath()


#minidomXml = minidom.parse(xmlPath)
tree = ET.parse(xmlPath)
root = tree.getroot()

#root = ET.fromstring

root.tag
root.attrib

for child in root:
    
    print child.tag, child.attrib
    for subEntry in child.iter():
        print subEntry.tag, subEntry.attrib

#for executable in root.iter():
#    print executable.attrib
'''

