CONTAINER Nblend                                {
    NAME Nblend;

    INCLUDE Nbase;

    GROUP NB_GROUP_NODEPROPERTIES               {
        DEFAULT 1;

        LONG NBLN_LONG_BLENDMODE                {
            CYCLE                               {
                NBLN_MODE_NORMAL;
                NBLN_MODE_SEP;
                NBLN_MODE_DARKEN;
                NBLN_MODE_MULTIPLY;
                NBLN_MODE_COLORBURN;
                NBLN_MODE_LINEARBURN;
                NBLN_MODE_DARKERCOLOR;
                NBLN_MODE_SEP;
                NBLN_MODE_LIGHTEN;
                NBLN_MODE_SCREEN;
                NBLN_MODE_COLORDODGE;
                NBLN_MODE_LINEARDODGE;
                NBLN_MODE_LIGHTERCOLOR;
                NBLN_MODE_SEP;
                NBLN_MODE_OVERLAY;
                NBLN_MODE_SOFTLIGHT;
                NBLN_MODE_HARDLIGHT;
                NBLN_MODE_VIVIDLIGHT;
                NBLN_MODE_LINEARLIGHT;
                NBLN_MODE_PINLIGHT;
                NBLN_MODE_HARDMIX;
                NBLN_MODE_SEP;
                NBLN_MODE_DIFFERENCE;
                NBLN_MODE_EXCLUSION;
                NBLN_MODE_SUBTRACT;
                NBLN_MODE_DIVIDE;
                NBLN_MODE_SEP;
                NBLN_MODE_HUE;
                NBLN_MODE_SATURATION;
                NBLN_MODE_COLOR;
                NBLN_MODE_LUMINOSITY;
                NBLN_MODE_SEP;
                NBLN_MODE_LEVR;
                NBLN_MODE_SEP;
                NBLN_MODE_GRAINEXTRACT;
                NBLN_MODE_GRAINMERGE;
            }
        }
        REAL NBLN_REAL_MIX                      {UNIT PERCENT; MIN 0.0; MAX 100.0; MINSLIDER 0.0; MAXSLIDER 100.0; STEP 0.01; CUSTOMGUI REALSLIDER;}
    }
    SHOW NB_GROUP_MASKPROPERTIES;
}
