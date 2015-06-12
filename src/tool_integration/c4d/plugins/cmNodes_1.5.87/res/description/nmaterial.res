CONTAINER Nmaterial                     {
    NAME Nmaterial;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES       {
        DEFAULT 1;

        LINK NMTL_LINK_MATERIAL         {ANIM OFF; ACCEPT {Mmaterial;}}

        SEPARATOR                       {}

        BOOL NMTL_BOOL_COLOR            {ANIM OFF;}
        BOOL NMTL_BOOL_DIFFUSION        {ANIM OFF;}
        BOOL NMTL_BOOL_LUMINANCE        {ANIM OFF;}
        BOOL NMTL_BOOL_TRANSPARENCY     {ANIM OFF;}
        BOOL NMTL_BOOL_REFLECTION       {ANIM OFF;}
        BOOL NMTL_BOOL_ENVIRONMENT      {ANIM OFF;}
        BOOL NMTL_BOOL_BUMP             {ANIM OFF;}
        BOOL NMTL_BOOL_NORMAL           {ANIM OFF;}
        BOOL NMTL_BOOL_ALPHA            {ANIM OFF;}
        BOOL NMTL_BOOL_SPECULAR         {ANIM OFF;}
        BOOL NMTL_BOOL_DISPLACEMENT     {ANIM OFF;}
    }
}

