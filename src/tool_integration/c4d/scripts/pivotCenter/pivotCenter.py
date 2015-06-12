import c4d
from c4d import gui


'''
center pivot:
get global position
get
'''


# credits: http://forums.cgsociety.org/archive/index.php/t-1052433.html

zero = c4d.Vector( 0,0,0 )
normScale = c4d.Vector( 1,1,1 )
def main():
    objList=doc.GetActiveObjects( True )# get the selected objects
    for obj in objList:
        #print obj.GetTypeName()
        #if not obj.GetTypeName() == 'Null':

        pivotPos = obj.GetAbsPos()
        bBoxCenter = obj.GetMp()
        print pivotPos
        print bBoxCenter
        absPos = pivotPos + bBoxCenter
        print pivotPos + bBoxCenter
        
        obj.SetAbsPos( zero )
        
        
        points = obj.GetAllPoints()
        pcount = obj.GetPointCount()
        

            

        
if __name__=='__main__':
    main()