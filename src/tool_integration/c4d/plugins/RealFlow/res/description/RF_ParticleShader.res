CONTAINER RF_PARTICLESHADER
{
	NAME RFParticleShader;
	INCLUDE Mpreview;
	INCLUDE Xbase;

	GROUP RF_PARTICLESHADER_SETUP
	{
		DEFAULT 1;

        BOOL RF_PARTICLESHADER_USE_DISPLAY_COLOR {}
		LONG RF_PARTICLESHADER_COLOR_MODE
		{
			CYCLE
			{
				RF_PARTICLESHADER_COLOR_NONE;
				RF_PARTICLESHADER_COLOR_VELOCITY;
				RF_PARTICLESHADER_COLOR_NORMAL;
				RF_PARTICLESHADER_COLOR_FORCE;
				RF_PARTICLESHADER_COLOR_TEXTUREU;
				RF_PARTICLESHADER_COLOR_TEXTUREV;
				RF_PARTICLESHADER_COLOR_NEIGHBOR;
				RF_PARTICLESHADER_COLOR_AGE;
				RF_PARTICLESHADER_COLOR_ISOLATION;
				RF_PARTICLESHADER_COLOR_VISCOSITY;
				RF_PARTICLESHADER_COLOR_DENSITY;
				RF_PARTICLESHADER_COLOR_PRESSURE;
				RF_PARTICLESHADER_COLOR_MASS;
				RF_PARTICLESHADER_COLOR_TEMPERATURE;
				RF_PARTICLESHADER_COLOR_VORTICITY;
			}
		}
		GRADIENT RF_PARTICLESHADER_MAG_COLOR {COLOR;}
	}
}
