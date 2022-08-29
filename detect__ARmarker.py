import cv2, os, sys
import numpy as np

# return :: ( markers, ids )
#
#     - markers :: [ nDetected, 4-corner (4), x&y (2) ]
#     - ids     :: [ nDetected ]  <=  ID of AR marker.
#

# ========================================================= #
# ===  detect__ARmarker.py                              === #
# ========================================================= #

def detect__ARmarker( image=None, markerType="aruco.DICT_4X4_50", reorder=None ):

    # ------------------------------------------------- #
    # --- [1] argument image check                  --- #
    # ------------------------------------------------- #
    if ( image is None ): sys.exit( "[detect__ARmarker.py] image == ??? " )
    image_ = np.copy( image )
    if ( image_.ndim == 3 ): image_ = cv2.cvtColor( image_, cv2.COLOR_BGR2GRAY )

    # ------------------------------------------------- #
    # --- [2] call aruco ARmaker dictionary         --- #
    # ------------------------------------------------- #
    aruco    = cv2.aruco
    if   ( markerType == "aruco.DICT_4X4_50"  ):
        markers_dict  = aruco.getPredefinedDictionary( aruco.DICT_4X4_50  )
    elif ( markerType == "aruco.DICT_5X5_100" ):
        markers_dict  = aruco.getPredefinedDictionary( aruco.DICT_5X5_100 )
    else:
        print( "[detect__ARmarker.py] unknown markerType == {}".format( markerType ) )
        print( "[detect__ARmarker.py] markerType :: [ aruco.DICT_4X4_50, aruco.DICT_5X5_100 ]" )
        sys.exit()

    # ------------------------------------------------- #
    # --- [3] detect AR marker                      --- #
    # ------------------------------------------------- #
    corners, ids, rejectedImgPoints = aruco.detectMarkers( image_, markers_dict )
    if ( ids is None ):
        index    = None
        markers  = np.array( [] )
        ids      = np.array( [] )
    else:
        index    = np.argsort( np.reshape( ids, (-1) ) )
        markers  = np.array( [ corners[iid][0,...] for iid in index ] )
        ids      = np.array( [     ids[iid][0,...] for iid in index ] )

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    if ( ( reorder is not None ) and ( len( ids ) > 0 ) ) :
        markers = markers[ reorder ]
        ids     = ids    [ reorder ]
    return( markers, ids )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    inpFile    = "test/trapezoidal01.jpg"
    image      = cv2.imread( inpFile )
    marker,ids = detect__ARmarker( image=image )
    print( " marker's shape :: {}".format( marker.shape ) )
    print( "     id's shape :: {}".format( ids.shape    ) )
    print( marker )
    print( ids )
