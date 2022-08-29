import os, sys, cv2
import numpy as np

# ========================================================= #
# ===  resize__images.py                                === #
# ========================================================= #

def resize__images( images=None, resize=None ):

    # ------------------------------------------------- #
    # --- [1] check arguments                       --- #
    # ------------------------------------------------- #
    if ( images is None ): sys.exit( "[save__imageAsMovie.py] images == ???" )
    if ( resize is None ): resize = 600
    
    # ------------------------------------------------- #
    # --- [2] if the type is list                   --- #
    # ------------------------------------------------- #
    if ( type( images ) is list ):
        try:
            images   = np.array( images )
        except:
            if ( resize is  )
            hgt, wdt = ( images[0] ).shape[0:2]
            resize   = (  )
