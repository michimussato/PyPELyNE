// C4D-DialogResource
DIALOG DLG_EXPFILE
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
      ALIGN_TOP; CENTER_H; 
      BORDERSIZE 10, 6, 10, 0; 
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
      USERAREA IDC_RTLOGO { ALIGN_TOP; ALIGN_LEFT; SIZE 128, 64; }
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
        COLUMNS 3;
        SPACE 4, 4;
        
        STATICTEXT  { NAME IDS_SCALEF; CENTER_V; CENTER_H; }
        EDITNUMBER IDC_FSCALE
        { CENTER_V; FIT_H; SIZE 54, 0; }
      }
      GROUP 
      {
        ALIGN_TOP; CENTER_H; 
        BORDERSIZE 4, 4, 4, 4; 
        COLUMNS 3;
        EQUAL_ROWS; 
        SPACE 10, 10;
        
        GROUP 
        {
          NAME IDS_TGNRL; FIT_V; SCALE_V; FIT_H; SCALE_H; 
          BORDERSTYLE BORDER_GROUP_IN; BORDERSIZE 6, 6, 6, 6; 
          COLUMNS 1;
          SPACE 4, 4;
          
          CHECKBOX IDC_XPNGONS { NAME IDS_XPNGONS; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_XPNORMS { NAME IDS_XPNORMS; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_XPFACES { NAME IDS_XPFACES; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_REVERSE { NAME IDS_REVERSEF; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_XPUV { NAME IDS_XPUV; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_FLIPU { NAME IDS_FLIPU; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_FLIPV { NAME IDS_FLIPV; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_XPMATS { NAME IDS_XPMATS; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_XPGROUPS { NAME IDS_XPGROUPS; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_XPRGNS { NAME IDS_XPRGNS; ALIGN_TOP; ALIGN_LEFT;  }
        }
        GROUP IDC_TFACE
        {
          NAME IDS_TFACE; ALIGN_TOP; FIT_H; SCALE_H; 
          BORDERSTYLE BORDER_GROUP_IN; BORDERSIZE 6, 6, 6, 6; 
          COLUMNS 1;
          SPACE 4, 4;
          
          RADIOGADGET IDC_SORTC { NAME IDS_SORTC; ALIGN_TOP; ALIGN_LEFT;  }
          RADIOGADGET IDC_SORTM { NAME IDS_SORTM; ALIGN_TOP; ALIGN_LEFT;  }
          RADIOGADGET IDC_SORTG { NAME IDS_SORTG; ALIGN_TOP; ALIGN_LEFT;  }
          RADIOGADGET IDC_SORTR { NAME IDS_SORTR; ALIGN_TOP; ALIGN_LEFT;  }
        }
        GROUP IDC_TGROUP
        {
          NAME IDS_TGROUP; ALIGN_TOP; FIT_H; SCALE_H; 
          BORDERSTYLE BORDER_GROUP_IN; BORDERSIZE 6, 6, 6, 6; 
          COLUMNS 1;
          SPACE 4, 4;
          
          CHECKBOX IDC_MESHN { NAME IDS_MESHN; ALIGN_TOP; ALIGN_LEFT;  }
          GROUP 
          {
            ALIGN_TOP; ALIGN_RIGHT; 
            BORDERSIZE 16, 0, 0, 0; 
            COLUMNS 1;
            SPACE 4, 4;
            
            RADIOGADGET IDC_MASG { NAME IDS_XASG; ALIGN_TOP; ALIGN_LEFT;  }
            RADIOGADGET IDC_MASR { NAME IDS_XASR; ALIGN_TOP; ALIGN_LEFT;  }
          }
          GROUP 
          {
            ALIGN_TOP; ALIGN_LEFT; 
            BORDERSIZE 0, 0, 0, 0; 
            COLUMNS 1;
            SPACE 4, 4;
            
            
          }
          CHECKBOX IDC_GTAGN { NAME IDS_GTAGN; ALIGN_TOP; ALIGN_LEFT;  }
          CHECKBOX IDC_HEIRG { NAME IDS_HEIR; ALIGN_TOP; ALIGN_LEFT;  }
        }
      }
    }
  }
  GROUP 
  {
    ALIGN_TOP; ALIGN_LEFT; 
    BORDERSIZE 0, 0, 0, 0; 
    COLUMNS 1;
    SPACE 4, 4;
    
    
  }
  DLGGROUP { OK; CANCEL; }
  GROUP 
  {
    ALIGN_TOP; ALIGN_LEFT; 
    BORDERSIZE 0, 0, 0, 0; 
    SPACE 4, 4;
    
    
  }
}