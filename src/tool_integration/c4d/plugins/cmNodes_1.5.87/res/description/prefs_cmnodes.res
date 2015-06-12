CONTAINER Prefs_cmnodes                         {
    NAME Prefs_cmnodes;

    GROUP PREF_CMN_MAIN_GROUP                   {
        DEFAULT 1;
        COLUMNS 1;

        SEPARATOR PREF_CMN_GROUP_EDITOR         {}
        GROUP                                   {
            LONG PREF_CMN_L_INSERT_NODE         {
                ANIM OFF;
                CYCLE                           {
                    CMN_INSERT_CURSORPOS;
                    CMN_INSERT_ORIGIN;
                    CMN_INSERT_VIEWCENTER;
                }
            }
            LONG PREF_CMN_L_PASTE_NODE          {
                ANIM OFF;
                CYCLE                           {
                    CMN_INSERT_CURSORPOS;
                    CMN_INSERT_ORIGIN;
                    CMN_INSERT_VIEWCENTER;
                    CMN_INSERT_POSITION;
                }
            }
            SEPARATOR                           {LINE;}
            BOOL PREF_CMN_B_SNAPPING            {ANIM OFF; PARENTCOLLAPSE;}
            LONG PREF_CMN_L_SNAP_THRESHOLD      {ANIM OFF; PARENTCOLLAPSE PREF_CMN_B_SNAPPING; MIN 0; MAX 100;}
            SEPARATOR                           {LINE;}
            LONG PREF_CMN_L_PORT_PADDING        {ANIM OFF; MIN 0; MAX 10;}
            LONG PREF_CMN_L_MID_DRAG_THRESHOLD  {ANIM OFF; MIN 10; MAX 100; PARENTCOLLAPSE;}
            BOOL PREF_CMN_B_MID_DRAG_VISIBLE    {ANIM OFF; PARENTCOLLAPSE PREF_CMN_L_MID_DRAG_THRESHOLD;}
            LONG PREF_CMN_L_STAMPSIZE           {
                CYCLE                           {
                    CMN_STAMPSIZE_SMALL;
                    CMN_STAMPSIZE_MEDIUM;
                    CMN_STAMPSIZE_LARGE;
                }
            }
            SEPARATOR                           {}
            BOOL PREF_CMN_B_NEWMATERIAL         {ANIM OFF;}
            BOOL PREF_CMN_B_TOLERANTSELECTION   {ANIM OFF;}
        }
        SEPARATOR PREF_CMN_GROUP_DISPLAY        {}
        GROUP {
            LONG PREF_CMN_L_GRID_WIDTH          {ANIM OFF; MIN 10; MAX 500;}
            LONG PREF_CMN_L_GRID_HEIGHT         {ANIM OFF; MIN 10; MAX 500;}
            SEPARATOR                           {LINE;}
            LONG PREF_CMN_L_NODE_WIDTH          {ANIM OFF; MIN 80; MAX 500;}
            BOOL PREF_CMN_B_AUTOLABELS          {ANIM OFF;}
            SEPARATOR                           {LINE;}
            COLOR PREF_CMN_C_WIRECOLOR          {ANIM OFF;}
            COLOR PREF_CMN_C_WIREACTIVE         {ANIM OFF;}
            COLOR PREF_CMN_C_NOTE_INDICATOR     {ANIM OFF;}
            SEPARATOR                           {LINE;}
            LONG PREF_CMN_L_WIRESTYLE           {
                ANIM OFF;
                CYCLE                           {
                    CMN_WIRESTYLE_STRAIGHT;
                    CMN_WIRESTYLE_BEZIER;
                }
            }
        }
        SEPARATOR PREF_CMN_GROUP_NODECOLORS     {}
        GROUP                                   {
            COLOR PREF_CMN_C_NODES_INPUT        {ANIM OFF;}
            COLOR PREF_CMN_C_NODES_ADJUST       {ANIM OFF;}
            COLOR PREF_CMN_C_NODES_CHANNELS     {ANIM OFF;}
            COLOR PREF_CMN_C_NODES_EFFECTS2D    {ANIM OFF;}
            COLOR PREF_CMN_C_NODES_OUTPUT       {ANIM OFF;}
            COLOR PREF_CMN_C_NODES_UTILITY      {ANIM OFF;}
        }
    }
}
