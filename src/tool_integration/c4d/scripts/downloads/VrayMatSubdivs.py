import c4d
from c4d import documents
doc = c4d.documents.GetActiveDocument()
Mats = doc.GetMaterials()

def VrayMat_subdiv(matlist):
    i = 0
    MatCount = len(matlist)
    if MatCount==None:return
    matsubdiv = c4d.gui.InputDialog('Vray Material Subdivisions', '8')
    try:
        matsubdiv = int(matsubdiv)
    except ValueError:
        c4d.gui.MessageDialog('Please enter in a subdivision value.')
        return
    speclist = [[c4d.VRAYMATERIAL_SPECULAR1_SUBDIV],
                [c4d.VRAYMATERIAL_SPECULAR2_SUBDIV],
                [c4d.VRAYMATERIAL_SPECULAR3_SUBDIV],
                [c4d.VRAYMATERIAL_SPECULAR4_SUBDIV],
                [c4d.VRAYMATERIAL_TRANSPARENCY_SUBDIV],
                [c4d.VRAYMATERIAL_SPECULAR5_SUBDIV]]
    while i < MatCount:
        Mtype = matlist[i].GetTypeName()
        if Mtype == "VrayAdvancedMaterial":
            for m in speclist:
                matlist[i][m] = matsubdiv 
        elif Mtype == "VRayAdvancedMaterial":
            for m in speclist:
                matlist[i][m] = matsubdiv    
        elif Mtype == "VrayCarPaintMaterial":
            matlist[i][c4d.VRAYCARPAINTMATERIAL_SUBDIVS]  = matsubdiv    
        elif Mtype == "VrayFastSSS2Material":
            matlist[i][c4d.VRAYFASTSSS2MATERIAL_SSS_SPECULARSUBDIVS] = matsubdiv
            matlist[i][c4d.VRAYFASTSSS2MATERIAL_SSS_SUBDIVS] = matsubdiv
        i += 1
    return Mats

def main():  
    VrayMat_subdiv(Mats)
    c4d.EventAdd()
    
if __name__=='__main__':
    main()