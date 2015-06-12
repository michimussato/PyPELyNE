#hypoly.com

#Select the layers you want to mute in the layer manager.
#hold Shift while running the script to mute every other layer that is not selected
import c4d
from c4d import gui

def getNextLayer(layer):
    if layer.GetDown():
         return layer.GetDown()
    while layer.GetUp() and not layer.GetNext():
         layer = layer.GetUp()
    return layer.GetNext()

def main():

    doc = c4d.documents.GetActiveDocument()
    bc = c4d.BaseContainer()
    root = doc.GetLayerObjectRoot()
    layer = root.GetDown()
    toggled = 0
    
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if not bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:        
            # Mute Selected Layers
            while layer:
                if layer.GetBit(c4d.BIT_ACTIVE):
                    layer_data = layer.GetLayerData(doc)
                    layer_data['view'] = not layer_data['view']
                    layer_data['render'] = not layer_data['render']
                    layer_data['manager'] = not layer_data['manager']
                    layer_data['locked'] = not layer_data['locked']
                    layer_data['generators'] = not layer_data['generators']
                    layer_data['expressions'] = not layer_data['expressions']
                    layer_data['animation'] = not layer_data['animation']
                    layer_data['deformers'] = not layer_data['deformers']
                    layer.SetLayerData(doc,layer_data)
                    toggled = 1
        
                if not layer.GetBit(c4d.BIT_ACTIVE):
                    toggled = 1
                    
                layer = getNextLayer(layer)
        else:
            # Solo Selected Layers if Shift is pressed
            while layer:
                if not layer.GetBit(c4d.BIT_ACTIVE):
                    layer_data = layer.GetLayerData(doc)
                    layer_data['view'] = not layer_data['view']
                    layer_data['render'] = not layer_data['render']
                    layer_data['manager'] = not layer_data['manager']
                    layer_data['locked'] = not layer_data['locked']
                    layer_data['generators'] = not layer_data['generators']
                    layer_data['expressions'] = not layer_data['expressions']
                    layer_data['animation'] = not layer_data['animation']
                    layer_data['deformers'] = not layer_data['deformers']
                    layer.SetLayerData(doc,layer_data)
                    toggled = 1
        
                if layer.GetBit(c4d.BIT_ACTIVE):
                    layer_data = layer.GetLayerData(doc)
                    layer_data['solo'] = not layer_data['solo']
                    layer.SetLayerData(doc,layer_data)
                    toggled = 1
                    
                layer = getNextLayer(layer)
        
    if toggled == 0:
        gui.MessageDialog("Select a layer")
        return False
    
    c4d.EventAdd()

if __name__=='__main__':
    main()