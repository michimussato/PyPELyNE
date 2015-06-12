import c4d, os
from c4d import documents
#Welcome to the world of Python


def main():
    
    #Get Active Document
    ActiveDocument = documents.GetActiveDocument()
    
    #Get Rendersettings
    RenderData = ActiveDocument.GetActiveRenderData() 
    
    TimeFrom = RenderData[c4d.RDATA_FRAMEFROM]
    TimeTo = RenderData[c4d.RDATA_FRAMETO]
    
    #Get Document Path & Name
    DocPath = ActiveDocument.GetDocumentPath()
    DocName = ActiveDocument.GetDocumentName()
    DocNameLength = len(DocName)-4
    DocNameShort = DocName[0:DocNameLength]    
                  
    NewFolder = DocPath + '\\' + '_output' + '\\' + DocNameShort
    NewFolderStill = DocPath + '\\' + '_output'
        
    #Create Output Path
    PathSequence = DocPath + '\\' + '_output' + '\\' + DocNameShort + '\\' + DocNameShort + '_'
    PathStill = DocPath + '\\' + '_output' + '\\' + DocNameShort + '_'
        
 
 
    #Functions

    if TimeFrom.GetNumerator() == TimeTo.GetNumerator():
       
        if os.path.exists(NewFolderStill):
        
            print "Output Folder for Still already exists!"
        
        
            #Set Path in Render Settings
            RenderData[c4d.RDATA_PATH] = PathStill
            RenderData[c4d.RDATA_MULTIPASS_FILENAME] = PathStill
        
        else:
            #Create Folders

            os.makedirs(NewFolderStill)
        
            print "Created Output Folder for Still!"
        
            #Set Path in Render Settings
            RenderData[c4d.RDATA_PATH] = PathStill
            RenderData[c4d.RDATA_MULTIPASS_FILENAME] = PathStill
            
    else:
        
        if os.path.exists(NewFolder):
        
            print "Output Folder for sequence already exists!"
        
        
            #Set Path in Render Settings
            RenderData[c4d.RDATA_PATH] = PathSequence
            RenderData[c4d.RDATA_MULTIPASS_FILENAME] = PathSequence
        
        else:
            #Create Folders

            os.makedirs(NewFolder)
        
            print "Created Output Folders for sequence!"
        
            #Set Path in Render Settings
            RenderData[c4d.RDATA_PATH] = PathSequence
            RenderData[c4d.RDATA_MULTIPASS_FILENAME] = PathSequence
           
    c4d.EventAdd()
           

if __name__=='__main__':
    main()
