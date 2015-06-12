CONTAINER Ncolorspace                   {
    NAME Ncolorspace;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES       {
        DEFAULT 1;

        LONG NCSP_LONG_COLOR_SRC        {
            CYCLE                       {
                NCSP_RGB;
                NCSP_SRGB;
                NCSP_HSV;
                NCSP_HSL;
            }
        }
        LONG NCSP_LONG_COLOR_DST        {
            CYCLE                       {
                NCSP_RGB;
                NCSP_SRGB;
                NCSP_HSV;
                NCSP_HSL;
            }
        }
    }
}
