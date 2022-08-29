import numpy as np
import cv2
import os, sys
import nkOpenCV.detect__ARmarker as arm
    

# ========================================================= #
# ===  perspectiveTransform__byARmarker.py              === #
# ========================================================= #

def perspectiveTransform__byARmarker( image=None, imgFile=None, markerType="aruco.DICT_4X4_50", \
                                      ARm_designs=None, ARmFile=None, figSize=None, \
                                      outFile=None ):

    # ------------------------------------------------- #
    # --- [1] load image                            --- #
    # ------------------------------------------------- #
    if ( image is None ):
        if ( imgFile is None ):
            sys.exit( "[perspectiveTransform__byARmarker.py] image == ???" )
        else:
            image = cv2.imread( imgFile )
    if ( figSize is None ):
        print( "[perspectiveTransform__byARmarker.py] figSize = ??? " )
        print( "[perspectiveTransform__byARmarker.py] figSize = (1200,900) is used here." )
        figSize = (600,600)

    # ------------------------------------------------- #
    # --- [2] detect AR marker                      --- #
    # ------------------------------------------------- #
    markers, ids = arm.detect__ARmarker( image=image, markerType=markerType )
    if ( len( ids ) < 4 ):
        print( "[perspectiveTransform__byARmarker.py] ARm_detects is less than 4... " )
        print( "[perspectiveTransform__byARmarker.py] failed to detect AR marker correctly." )
        return( None )
    else:
        ARm_detects  = np.array( ( np.average( markers, axis=1 ) )[ list(ids) ], \
                                 dtype=np.float32 )
        
    # ------------------------------------------------- #
    # --- [3] load settings for armarker            --- #
    # ------------------------------------------------- #
    if ( ARm_designs is None ):
        if ( ARmFile is None ):
            print( "[perspectiveTransform__byARmarker.py] ARm_designs and ARmFile is None. [ERROR]" )
            sys.exit()
        else:
            with open( ARmFile, "r" ) as f:
                ARm_designs = np.array( np.loadtxt( f ), dtype=np.float32 )
    else:
        if ( ARm_detects.shape != ARm_designs.shape ):
            print( "[perspectiveTransform__byARmarker.py] different size of ARm_detects / ARm_designs... " )
            print( "[perspectiveTransform__byARmarker.py] ARm_detects's shape :: {}".format( ARm_detects.shape ) )
            print( "[perspectiveTransform__byARmarker.py] ARm_designs's shape :: {}".format( ARm_designs.shape ) )
            print( "[perspectiveTransform__byARmarker.py] failed to detect AR marker correctly.... [CAUTION] " )
            return( None )
            
    # ------------------------------------------------- #
    # --- [4] get Matrix / conversion               --- #
    # ------------------------------------------------- #
    matrix  = cv2.getPerspectiveTransform( ARm_detects, ARm_designs )
    image_  = cv2.warpPerspective( image, matrix, figSize )
    success = True
    
    # ------------------------------------------------- #
    # --- [5] return                                --- #
    # ------------------------------------------------- #
    if ( outFile is not None ):
        cv2.imwrite( outFile, image_ )
        print( "[perspectiveTransform__byARmarker.py] outFile = {}".format( outFile ) )
    return( image_ )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    imgFile  = "test/trapezoidal01.jpg"
    ARmFile  = "test/ARmarker_pos.dat"
    outFile  = "test/out.jpg"
    figSize  = (1200,900)
    image    = perspectiveTransform__byARmarker( imgFile=imgFile, ARmFile=ARmFile, \
                                                 figSize=figSize )
    if ( image is None ):
        print()
        print( "[perspectiveTransform__byARmarker.py] failed to detect 4 AR markers... " )
        sys.exit()
        
    # -- write image -- # 
    original = cv2.imread( imgFile )
    original = cv2.resize( original, dsize=figSize )
    image    = cv2.hconcat( [original,image] )
    cv2.imwrite( outFile, image )
    print( "[perspectiveTransform__byARmarker.py] outFile :: {}".format( outFile ) )
    
