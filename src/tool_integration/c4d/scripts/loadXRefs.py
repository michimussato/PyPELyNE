import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    #xrefName = r'/test/something'
    myXref = c4d.BaseObject(c4d.Oxref)
    #op = c4d.BaseObject(c4d.Osceneinstance)
    myXref[c4d.ID_CA_XREF_GENERATOR] = 1
    myXref[c4d.ID_CA_XREF_LOADED] = 1
    
    #doc.InsertObject( op )
    myXref[c4d.ID_CA_XREF_FILE] = 'samplerInfo_0001.c4d'
    myXref[c4d.ID_CA_XREF_REF_STATEFILE] = "nouveaufichier.c4d" 
    doc.InsertObject( myXref )
    c4d.EventAdd()

if __name__ == '__main__':
    main()
