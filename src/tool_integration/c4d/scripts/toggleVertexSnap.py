# toggleVertexSnap.py
'''
from: dmodeling.h
#ifndef DMODELING_H__
#define DMODELING_H__

enum
{
	QUANTIZE_SETTINGS							= 1000,						/// Groups
	GUIDES_SETTINGS								= 1001,
	SNAP_LIST											= 1002,
	SNAPMODE_COMBO								= 1003,						/// Snap Mode switch Auto/2d/3d
		SNAP_SETTINGS_MODE_AUTO								= 0,
		SNAP_SETTINGS_MODE_2D									= 1,
		SNAP_SETTINGS_MODE_3D									= 2,


	SNAP_SETTINGS									= 440000119,			/// Group - The ID for the settings in the document MODELING_SETTINGS container	(stored as BaseContainer)

	SNAP_SETTINGS_RADIUS					= 440000120,	 		/// Real - The radius for the snap
	SNAP_SETTINGS_ENABLED					= 440000121,			/// Bool - ID for the command to enable the snap
	SNAP_SETTINGS_TOOL						= 440000138,			/// Bool - Store these settings with this tool rather than globally for all tools in the document
	QUANTIZE_ENABLED							= 431000005,			/// Bool - ID for the command to enable quantizing
	QUANTIZE_MOVE									= 440000131,			/// Real - Quantize step for movement
	QUANTIZE_SCALE								= 440000132,			/// Real - Quantize step for scaling
	QUANTIZE_ROTATE								= 440000133,			/// Real - Quantize step for rotation
	QUANTIZE_TEXTURE							= 440000134,			/// Real - Quantize step for movement with textures (UV space)
	QUANTIZE_GRID									= 440000139,			/// Bool - Set quantize move step to use the grid size

	SNAP_SETTINGS_MODE						= 431000020,			/// LONG - hold one of snap mode can be SNAP_SETTINGS_MODE_AUTO/SNAP_SETTINGS_MODE_2D/SNAP_SETTINGS_MODE_3D

	SNAP_SETTINGS_AUTO						= 431000018,			/// Command ID - Auto 2d/3d Snap mode
	SNAP_SETTINGS_3D							= 431000016,			/// Command ID - 3d snap mode
	SNAP_SETTINGS_2D							= 431000019,			/// Command ID - 2d snam mode

	SNAP_SETTINGS_GUIDEANGLE			= 431000002,			/// Real - Angle step for guides

	/////////////////////////////////////////////////////////////////////
	/// Snap Modes

	SNAPMODE_GUIDE								= 440000113,			/// Snap to guide obejcts
	SNAPMODE_INTERSECTION					= 440000114,			/// Snap to the intersections of objects and guides
	SNAPMODE_POINT								= 440000115,			/// Snap to a vertex on a mesh
	SNAPMODE_SPLINE								= 440000116,			/// Snap to any point along a spline
	SNAPMODE_DYNAMICGUIDE					= 440000117,			/// Snap using dynamic or "inferred" guides
	SNAPMODE_SPLINEMID						= 440000122,			/// Snap to the middle of a spline segment
	SNAPMODE_EDGE									= 440000123,			/// Snap to any point along an edge
	SNAPMODE_EDGEMID							= 440000124,			/// Snap to middle of an edge
	SNAPMODE_POLYGON							= 440000125,			/// Snap to the surface of a polygon
	SNAPMODE_POLYGONCENTER				= 440000126,			/// Snap to the center of individual polygons
	SNAPMODE_WORKPLANE						= 440000127,			/// Snap to the surface of the workplane
	SNAPMODE_AXIS									= 440000128,			/// Snap to the axis of an object
	SNAPMODE_ORTHO								= 440000129,			/// Snap perpendicular to guides edges and splines
	SNAPMODE_GRIDPOINT						= 431000000,			/// Snap to the intersection points of the grid on the workplane
	SNAPMODE_GRIDLINE							= 431000001,			/// Snap to the grid lines on the workplane
	SNAPMODE_MIDPOINT							= 431000013,			/// Snap for mid points .. it allow subsnap for each parent mode that have it
	SNAPMODE_GUIDEMID							= 431000014				/// Snap The mid point in between of static guides interesections
};

#endif	// DMODELING_H__
'''

import c4d
from c4d import gui

def toggleVertexSnap():
    
    doc = c4d.documents.GetActiveDocument()
    
    snap = c4d.modules.snap.GetSnapSettings( doc )
    #snapWorkplane = c4d.modules.snap.GetSnapSettings( doc, 10 )
    
    snapEnabled = c4d.modules.snap.IsSnapEnabled( doc )
    
    print( snapEnabled )
    
    if snapEnabled == True:
        print( 'snap on' )
        #c4d.modules.snap.EnableSnap( False, doc, 440000121 )
        c4d.modules.snap.EnableSnap( False, doc )
        print( 'and disabled' )
        #print( 'and off now' )xx
    elif snapEnabled == False:
        print( 'snap off' )
        print( 'snap-grid state: %i' %snapEnabled )
        
        
        c4d.modules.snap.EnableSnap( True, doc )
        
        snap[c4d.SNAP_SETTINGS_MODE] = c4d.SNAP_SETTINGS_MODE_AUTO
        print( 'SNAP_SETTINGS_MODE = %i' %snap[c4d.SNAP_SETTINGS_MODE] )
        
        snap[c4d.SNAPMODE_GUIDE] = False
        print( 'SNAPMODE_GUIDE = %i' %snap[c4d.SNAPMODE_GUIDE] )
        snap[c4d.SNAPMODE_INTERSECTION] = False
        print( 'SNAPMODE_INTERSECTION = %i' %snap[c4d.SNAPMODE_INTERSECTION] )
        snap[c4d.SNAPMODE_POINT] = False
        print( 'SNAPMODE_POINT = %i' %snap[c4d.SNAPMODE_POINT] )
        snap[c4d.SNAPMODE_SPLINE] = False
        print( 'SNAPMODE_SPLINE = %i' %snap[c4d.SNAPMODE_SPLINE] )
        snap[c4d.SNAPMODE_DYNAMICGUIDE] = False
        print( 'SNAPMODE_DYNAMICGUIDE = %i' %snap[c4d.SNAPMODE_DYNAMICGUIDE] )
        snap[c4d.SNAPMODE_EDGE] = False
        print( 'SNAPMODE_EDGE = %i' %snap[c4d.SNAPMODE_EDGE] )
        snap[c4d.SNAPMODE_EDGEMID] = False
        print( 'SNAPMODE_EDGEMID = %i' %snap[c4d.SNAPMODE_EDGEMID] )
        snap[c4d.SNAPMODE_POLYGON] = False
        print( 'SNAPMODE_POLYGON = %i' %snap[c4d.SNAPMODE_POLYGON] )
        snap[c4d.SNAPMODE_POLYGONCENTER] = False
        print( 'SNAPMODE_POLYGONCENTER = %i' %snap[c4d.SNAPMODE_POLYGONCENTER] )
        snap[c4d.SNAPMODE_WORKPLANE] = True
        print( 'SNAPMODE_WORKPLANE = %i' %snap[c4d.SNAPMODE_WORKPLANE] )
        snap[c4d.SNAPMODE_AXIS] = True
        print( 'SNAPMODE_AXIS = %i' %snap[c4d.SNAPMODE_AXIS] )
        snap[c4d.SNAPMODE_ORTHO] = True
        print( 'SNAPMODE_ORTHO = %i' %snap[c4d.SNAPMODE_ORTHO] )
        snap[c4d.SNAPMODE_GRIDPOINT] = True
        print( 'SNAPMODE_GRIDPOINT = %i' %snap[c4d.SNAPMODE_GRIDPOINT] )
        snap[c4d.SNAPMODE_GRIDLINE] = False
        print( 'SNAPMODE_GRIDLINE = %i' %snap[c4d.SNAPMODE_GRIDLINE] )
        snap[c4d.SNAPMODE_MIDPOINT] = False
        print( 'SNAPMODE_MIDPOINT = %i' %snap[c4d.SNAPMODE_MIDPOINT] )
        snap[c4d.SNAPMODE_GUIDEMID] = False
        print( 'SNAPMODE_GUIDEMID = %i' %snap[c4d.SNAPMODE_GUIDEMID] )
        
        
        print( 'and enabled' )
        #c4d.modules.snap.EnableSnap( True, doc, 440000121 )
        #print( 'and on now' )
        
        docCurrent = c4d.documents.GetActiveDocument()
        
        snapCurrent = c4d.modules.snap.GetSnapSettings( docCurrent )
        
        snapEnabledCurrent = c4d.modules.snap.IsSnapEnabled( docCurrent )
    
        print( 'current snap-grid state: %i' %snapEnabledCurrent )
    

    


if __name__=='__main__':
    toggleVertexSnap()
