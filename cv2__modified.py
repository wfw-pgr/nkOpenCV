import os, sys
import cv2


# ========================================================= #
# ===  imshow_ :: modified imshow for instant show      === #
# ========================================================= #

def imshow_( image=None, buffername="buffer1" ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( image is None ): sys.exit( "[imshow_] image == ???" )

    
    cv2.imshow( buffername, image )
    print( "[cv2__modified.py] Forcus & Press Any Keys to Close the Window. >>> ", end="" )
    cv2.waitKey(0)
    cv2.destroyWindow( buffername )
    cv2.waitKey(1)
    return()



# ========================================================= #
# ===  imread_ :: modified imread for instant read      === #
# ========================================================= #

def imread_( inpFile=None, returnType="bgr" ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit( "[imread_] inpFile == ???" )
    if ( not( returnType.lower() in [ "rgb", "bgr", "gray" ] ) ):
        sys.exit( "[imread_]  == ???" )

    # ------------------------------------------------- #
    # --- [2] read                                  --- #
    # ------------------------------------------------- #
    img_bgr = cv2.imread( inpFile )

    # ------------------------------------------------- #
    # --- [3] convert color                         --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() == "bgr"  ):
        return( img_bgr )
    elif ( returnType.lower() == "rgb"  ):
        return( cv2.cvtColor( img_bgr, cv2.COLOR_BGR2RGB  ) )
    elif ( returnType.lower() == "gray" ):
        return( cv2.cvtColor( img_bgr, cv2.COLOR_BGR2GRAY ) )

    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    img = cv2.imread( "test/lena_ja.png" )
    imshow_( img )
