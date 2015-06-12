import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    
    c4d.CallCommand(100004768) # Select Children
    c4d.CallCommand(100004794) # Invert Selection
    
    
    c4d.CallCommand(1027569) # MagicSolo

if __name__=='__main__':
    main()
