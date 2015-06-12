import c4d
from c4d import gui
from c4d import documents
#Welcome to the world of Python

activeDoc = documents.GetActiveDocument()

def GetNextObject(op,stop_at_op):
    if op==None: return None
    
    if op.GetDown():
        return op.GetDown()
    
    while not op.GetNext() and op.GetUp() and op.GetUp() != stop_at_op:
        op = op.GetUp()
 
    return op.GetNext()

 
def main():
    myobject = activeDoc.GetActiveObject()
    op = activeDoc.GetActiveObject()
    
    if not myobject.GetDownLast():
        return 
    
    while myobject:
        myobject=GetNextObject(myobject,op)
        activeDoc.SetActiveObject(myobject,c4d.SELECTION_NEW)
        c4d.CallCommand(1011982)

        
 
if __name__=='__main__':
    main()