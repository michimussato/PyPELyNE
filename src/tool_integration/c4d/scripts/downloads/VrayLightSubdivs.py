import c4d

def GetNextObject(op):
    if op==None: return None
    
    if op.GetDown(): return op.GetDown()
    
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()
 
def main():
    objects = doc.GetFirstObject()
    if objects==None: return
    
    lightsubdiv = c4d.gui.InputDialog('Vray Light Subdivisions', '8')
    try:
        lightsubdiv = int(lightsubdiv)
    except ValueError:
        c4d.gui.MessageDialog('Please enter in a subdivision value.')
        return
 
    while objects:
        objtags = objects.GetTags()
        for tag in objtags:
            Tagtype = tag.GetTypeName()
            if Tagtype == "VrayLight":
                tag[c4d.VRAYLIGHTTAG_AREA_SUBDIVS]  = lightsubdiv   
        objects = GetNextObject(objects)
 
    c4d.EventAdd()
    
main()