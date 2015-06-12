// C4D-DialogResource
DIALOG DLG_IMPFILE
{
  NAME CAPTION_TEXT; CENTER_V; CENTER_H; 
  
  GROUP 
  {
    ALIGN_TOP; CENTER_H; 
    BORDERSIZE 10, 0, 10, 0; 
    COLUMNS 1;
    SPACE 4, 4;
    
    GROUP 
    {
      CENTER_V; CENTER_H; 
      BORDERSIZE 10, 10, 10, 10; 
      COLUMNS 3;
      SPACE 4, 4;
      
      USERAREA IDC_LOGO { CENTER_V; CENTER_H; SIZE 128, 64; }
      GROUP 
      {
        CENTER_V; CENTER_H; 
        BORDERSIZE 10, 0, 10, 0; 
        COLUMNS 1;
        SPACE 4, 4;
        
        STATICTEXT  { NAME IDS_HTX1; CENTER_V; CENTER_H; }
        STATICTEXT  { NAME IDS_HTX2; CENTER_V; CENTER_H; }
        STATICTEXT  { NAME IDS_HTX3; CENTER_V; CENTER_H; }
        STATICTEXT  { NAME IDS_HTX4; CENTER_V; CENTER_H; }
        STATICTEXT  { NAME IDS_HTX5; CENTER_V; CENTER_H; }
      }
      USERAREA IDC_RTLOGO { CENTER_V; CENTER_H; SIZE 128, 64; }
    }
    GROUP 
    {
      NAME IDS_DTITLE; FIT_V; SCALE_V; CENTER_H; 
      BORDERSTYLE BORDER_GROUP_IN; BORDERSIZE 10, 10, 10, 10; 
      COLUMNS 1;
      SPACE 10, 10;
      
      GROUP 
      {
        ALIGN_TOP; ALIGN_LEFT; 
        BORDERSIZE 0, 0, 0, 0; 
        COLUMNS 2;
        SPACE 10, 10;
        
        GROUP 
        {
          ALIGN_TOP; ALIGN_LEFT; 
          BORDERSIZE 0, 0, 0, 0; 
          COLUMNS 2;
          SPACE 4, 4;
          
          STATICTEXT  { NAME IDS_SCALEF; CENTER_V; ALIGN_RIGHT; }
          EDITNUMBER IDC_FSCALE
          { CENTER_V; ALIGN_LEFT; SIZE 54, 0; }
        }
      }
      GROUP 
      {
        ALIGN_TOP; CENTER_H; 
        BORDERSIZE 0, 0, 0, 0; 
        COLUMNS 2;
        SPACE 10, 10;
        
        GROUP IDC_GENERALG
        {
          NAME IDS_GENERALG; FIT_V; SCALE_V; ALIGN_LEFT; 
          BORDERSTYLE BORDER_GROUP_IN; BORDERSIZE 4, 4, 4, 4; 
          COLUMNS 1;
          SPACE 4, 4;
          
          CHECKBOX IDC_MPNGONS { NAME IDS_MPNGONS; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_MPNORMS { NAME IDS_MPNRMS; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_MPGROUPS { NAME IDS_MPGRPS; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_MPREGIONS { NAME IDS_MPRGNS; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_MPMATS { NAME IDS_MPMATS; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_MPUVS { NAME IDS_MPUVS; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_FLIPU2 { NAME IDS_FLIPU2; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_FLIPV2 { NAME IDS_FLIPV2; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_FACEREV { NAME IDS_FACEREV; ALIGN_TOP; ALIGN_LEFT;  }
        }
        GROUP 
        {
          ALIGN_TOP; ALIGN_LEFT; 
          BORDERSIZE 0, 0, 0, 0; 
          ROWS 2;
          SPACE 4, 4;
          
          GROUP IDC_MESHSPLITG
          {
            NAME IDS_MESHG; FIT_V; SCALE_V; FIT_H; SCALE_H; 
            BORDERSTYLE BORDER_GROUP_IN; BORDERSIZE 4, 4, 4, 4; 
            COLUMNS 1;
            SPACE 4, 4;
            
            RADIOGADGET IDC_SPLITNONE { NAME IDS_SPLITN; ALIGN_TOP; ALIGN_LEFT;  }
            RADIOGADGET IDC_SPLITGROUP { NAME IDS_SPLITG; ALIGN_TOP; ALIGN_LEFT;  }
            RADIOGADGET IDC_SPLITREGION { NAME IDS_SPLITR; ALIGN_TOP; ALIGN_LEFT;  }
            RADIOGADGET IDC_SPLITMATERIAL { NAME IDS_SPLITM; ALIGN_TOP; ALIGN_LEFT;  }
          }
          GROUP IDC_DOCOPTG
          {
            NAME IDS_DOCOPTS; FIT_V; SCALE_V; FIT_H; SCALE_H; 
            BORDERSTYLE BORDER_GROUP_IN; BORDERSIZE 4, 4, 4, 4; 
            COLUMNS 1;
            SPACE 4, 4;
            
            RADIOGADGET IDC_DOCNEW { NAME IDS_DOCNEW; ALIGN_TOP; ALIGN_LEFT;  }
            RADIOGADGET IDC_DOCMERGE { NAME IDS_DOCMERGE; ALIGN_TOP; ALIGN_LEFT;  }
          }
        }
      }
    }
    GROUP 
    {
      CENTER_V; CENTER_H; 
      BORDERSIZE 0, 4, 0, 4; 
      SPACE 4, 4;
      
      DLGGROUP { OK; CANCEL; }
    }
  }
}