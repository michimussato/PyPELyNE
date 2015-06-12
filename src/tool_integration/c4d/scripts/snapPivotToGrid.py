import c4d
from c4d.modules import snap

# https://developers.maxon.net/docs/Cinema4DPythonSDK/help/modules/c4d.modules/snap/index.html?highlight=snap#module-c4d.modules.snap

def main():
    
    # Check snap state
    res = snap.IsSnapEnabled(doc)
    if not res:
        # Enable snap if not activated
        snap.EnableSnap(True, doc)
        print "Snap Enabled:", snap.IsSnapEnabled(doc)
    
    # Get snap settings
    bc = snap.GetSnapSettings(doc)

    # Change snap settings
    
    # Set 3D snapping mode
    bc[c4d.SNAP_SETTINGS_MODE] = c4d.SNAP_SETTINGS_MODE_3D
    snap.SetSnapSettings(doc, bc)
    
    # Check quantizing state
    if bc[c4d.QUANTIZE_ENABLED]:
        # Disable quantizing if not activated
        c4d.CallCommand(c4d.QUANTIZE_ENABLED)
        c4d.EventAdd()
        print "Quantize Enabled:", snap.IsQuantizeEnabled(doc)
    
    # Set quantize scale step
    snap.SetQuantizeStep(doc, None, c4d.QUANTIZE_SCALE, 0.5)
    print "Quantize Scale Step:",  snap.GetQuantizeStep(doc, None, c4d.QUANTIZE_SCALE)

    # Print workplane object and matrix
    print "Workplane Object:", snap.GetWorkplaneObject(doc)
    print "Workplane Matrix:", snap.GetWorkplaneMatrix(doc, None)
    
    # Check if workplane is locked
    if not snap.IsWorkplaneLock(doc):
        # Lock workplane
        snap.SetWorkplaneLock(doc.GetActiveBaseDraw(), True)
        print "Workplane Locked:", snap.IsWorkplaneLock(doc)


if __name__=='__main__':
    main()