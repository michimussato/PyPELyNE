#ifndef __C4D_SYMBOLS__
#define __C4D_SYMBOLS__

enum
{
	// string table definitions
	RF_PARTICLE_IMPORTER	= 1026261,
	RF_PARTICLE_EXPORTER,
	RF_SD_IMPORTER,
	RF_SD_EXPORTER,
	RF_SD_ANIM,
	RF_MESH_IMPORTER,
	RF_PARTICLE_NODE,
	RF_PARTICLE_EXPORTER_DLG,
	RF_SD_EXPORTER_DLG,
	RF_MESH_EXPORTER		= 1026928,
	RF_MESH_EXPORTER_DLG,
	RF_SD_READER			= 1028472,
	RF_MELTMATERIAL			= 1031575,
    RF_PARTICLESHADER       = 1031723,

	// RF Particle Exporter
	//
	// combos
	//
	P_EXP_GAS				= 1,
	P_EXP_LIQUID			= 8,
	P_EXP_DUMB				= 5,
	P_EXP_ELASTIC			= 7,

	P_EXP_FPS30				= 30,
	P_EXP_FPS25				= 25,
	P_EXP_FPS24				= 24,

	// groups
	P_EXP_TAB				= 10100,
	P_EXP_SETUP,
	P_EXP_PARTICLE,

	// setup
	P_EXP_PSYS,
	P_EXP_DIR,
	P_EXP_NAME,
	P_EXP_PADDING,
	P_EXP_START,
	P_EXP_END,
	P_EXP_INC,
	P_EXP_INFO,
	P_EXP_BUTTON,
	P_EXP_CANCEL,

	// particle file
	P_EXP_FLUIDNAME,
	P_EXP_FLUIDTYPE,
	P_EXP_FPS,
	P_EXP_SCENE_SCALE,
	P_EXP_RADIUS,
	P_EXP_EMITTER_POSX,
	P_EXP_EMITTER_POSY,
	P_EXP_EMITTER_POSZ,
	P_EXP_EMITTER_ROTX,
	P_EXP_EMITTER_ROTY,
	P_EXP_EMITTER_ROTZ,
	P_EXP_EMITTER_SCALEX,
	P_EXP_EMITTER_SCALEY,
	P_EXP_EMITTER_SCALEZ,

	// RF SD Importer
	//
	// setup
  	SD_IMP_SETUP,

	SD_IMP_CAM,
	SD_IMP_OBJ,
	SD_IMP_OBJNUM,
	SD_IMP_OBJDESC,
	SD_IMP_SCALE,
	SD_IMP_CREATE,
	SD_IMP_TEX,
	SD_IMP_NORM,
	SD_IMP_KEYS,
	SD_IMP_BUTTON,
	SD_IMP_CANCEL,

	// RF SD Exporter
	//
	// setup
  	SD_EXP_SETUP,

	SD_EXP_FILE,
	SD_EXP_START,
	SD_EXP_END,
	SD_EXP_INC,
	SD_EXP_SCALE,
	SD_EXP_ADDCAM,
	SD_EXP_CAM,
	SD_EXP_OBJ_TITLE,
	SD_EXP_SDOBJ_TITLE,
	SD_EXP_ADDALLOBJ,
	SD_EXP_ADDOBJ,
	SD_EXP_REMOVEOBJ,
	SD_EXP_REMOVEALLOBJ,
	SD_EXP_ADDMODE,
	SD_EXP_SETMODE,
	SD_EXP_MODE_MATRIX,
	SD_EXP_MODE_VERTEX,
	SD_EXP_OBJECTS,
	SD_EXP_SDOBJECTS,
	SD_EXP_INFO,
	SD_EXP_BUTTON,
	SD_EXP_CANCEL,

	// RF Mesh Exporter
	//
	// setup
	M_EXP_SETUP,

	M_EXP_OBJ,
	M_EXP_DIR,
	M_EXP_NAME,
	M_EXP_PADDING,
	M_EXP_START,
	M_EXP_END,
	M_EXP_INC,
	M_EXP_INFO,
	M_EXP_BUTTON,
	M_EXP_CANCEL,

	M_EXP_TEX,
	M_EXP_NUMF,
	M_EXP_VEL,
	M_EXP_RECALC_VEL,

	// v2.1.7
	P_EXP_CALC_VELOCITY = 11000,
    // v2.2.7
	P_EXP_FORMAT,
	P_EXP_FORMAT_RF2012,
	P_EXP_FORMAT_RF2012_STR,
	P_EXP_FORMAT_RF2013,
	P_EXP_FORMAT_RF2013_STR,
		
// End of symbol definition
  _DUMMY_ELEMENT_
};

#endif
