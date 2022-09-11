import os, sys
import cv2
import numpy as np

# ========================================================= #
# ===  fit__contourEllipse.py                           === #
# ========================================================= #

def fit__contourEllipse( image=None, threshold=None, imgFile=None, grayFile=None, \
                         xMin=None, yMin=None, xMax=None, yMax=None, \
                         abMin=None, abMax=None ):

    x_, y_, a_, b_, d_ = 0, 1, 2, 3, 4
    
    # ------------------------------------------------- #
    # --- [1] load image                            --- #
    # ------------------------------------------------- #
    if ( image is None ):
        if ( imgFile is None ):
            sys.exit( "[perspectiveTransform__byARmarker.py] image == ???" )
        else:
            image = cv2.imread( imgFile )
    if ( threshold is None ):
        img_gray  = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
        threshold = np.average( img_gray )
        
    # ------------------------------------------------- #
    # --- [2] prepare                               --- #
    # ------------------------------------------------- #
    img_HSV             = cv2.cvtColor( image, cv2.COLOR_BGR2HSV )
    img_H, img_S, img_V = cv2.split( img_HSV )
    _thre, img_gray     = cv2.threshold( img_V, threshold, 255, cv2.THRESH_BINARY )
    if ( grayFile is not None ):
        cv2.imwrite( grayFile, img_gray )

    # ------------------------------------------------- #
    # --- [3] find contours                         --- #
    # ------------------------------------------------- #
    contours, hierarchy = cv2.findContours(img_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # ------------------------------------------------- #
    # --- [4] fit to ellipse                        --- #
    # ------------------------------------------------- #
    ellipses = None
    stack    = []
    for ik,cnt in enumerate( contours ):
        if ( len(cnt) > 5 ):
            xy0,ab,deg  = cv2.fitEllipse( cnt )
            stack      += [ [ *xy0, *ab, deg ] ]
    ellipses = np.array( stack )

    # ------------------------------------------------- #
    # --- [5] select ellipse                        --- #
    # ------------------------------------------------- #
    if (  xMin is not None ):
        index    = np.where( ( ellipses[:,x_] >  xMin ) )
        ellipses = ellipses[index]
    if (  xMax is not None ):
        index    = np.where( ( ellipses[:,x_] <  xMax ) )
        ellipses = ellipses[index]
    if (  yMin is not None ):
        index    = np.where( ( ellipses[:,y_] >  yMin ) )
        ellipses = ellipses[index]
    if (  yMax is not None ):
        index    = np.where( ( ellipses[:,y_] <  yMax ) )
        ellipses = ellipses[index]
    if ( abMin is not None ):
        index    = np.where( ( ellipses[:,a_] > abMin ) & ( ellipses[:,b_] > abMin ) )
        ellipses = ellipses[index]
    if ( abMin is not None ):
        index    = np.where( ( ellipses[:,a_] < abMax ) & ( ellipses[:,b_] < abMax ) )
        ellipses = ellipses[index]
    print( ellipses.shape )
    
    # ------------------------------------------------- #
    # --- [5] return                                --- #
    # ------------------------------------------------- #
    return( ellipses )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    x_, y_, a_, b_, d_ = 0, 1, 2, 3, 4

    imgFile  = "jpg/first.jpg"
    image    = cv2.imread( imgFile )

    ellipses = fit__contourEllipse( image=image, threshold=150, \
                                    yMin=200, yMax=800, abMin=10, abMax=60 )
    
    import nkOpenCV.put__ellipses as ell
    image_   = ell.put__ellipses( image=image, xc=ellipses[:,x_], yc=ellipses[:,y_], \
                                  a1=ellipses[:,a_], a2=ellipses[:,b_], angle=ellipses[:,d_], \
                                  colors="green" )
    cv2.imwrite( "jpg/first_out.jpg", image_ )
    print( "[fit__contourEllipse.py] output :: jpg/first_out.jpg " )
