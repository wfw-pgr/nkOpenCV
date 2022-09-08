import cv2
import os, sys
import numpy   as np


# ========================================================= #
# ===  put__ellipses.py                                 === #
# ========================================================= #

def put__ellipses( image=None, xc=None, yc=None, rc=None, a1=None, a2=None, angle=None, \
                   colors=None, colorList=[ [255,0,0], [0,255,0] ], colorValues=None, \
                   thickness=2 ):

    # ------------------------------------------------- #
    # --- [1]  arguments                            --- #
    # ------------------------------------------------- #
    if ( image  is None ): sys.exit( "[put__ellipses.py] image == ???" )
    if ( xc     is None ): sys.exit( "[put__ellipses.py] xc    == ???" )
    if ( yc     is None ): sys.exit( "[put__ellipses.py] yc    == ???" )
    if ( ( a1 is None ) or ( a2 is None ) ):
        if ( rc is None ):
            sys.exit( "[put__ellipses.py] a1,a2 or rc == ???" )
        else:
            if ( type(rc) in [ int, float ] ):
                rc = np.ones_like( xc ) * rc
            a1 = np.copy( rc ) * 2.0
            a2 = np.copy( rc ) * 2.0
    if ( angle  is None ):
        angle  = np.zeros( (xc.shape[0]) )
    if ( colors is None ):
        if ( colorValues is not None ):
            colorList = np.array( colorList, dtype=np.uint8 )
            colors    = colorList[ np.array( colorValues, dtype=np.int64 ) ]
        else:
            colors    = np.repeat( np.array( [ [255,0,0] ], dtype=np.uint8 ), \
                                   xc.shape[0], axis=0 )
            
    # ------------------------------------------------- #
    # --- [2] put rectangle on image                --- #
    # ------------------------------------------------- #
    image_             = np.copy( image )
    x_,y_,a1_,a2_,rot_ = 0, 1, 2, 3, 4
    ellipse_vector     = np.concatenate( [ xc[:,None], yc[:,None], \
                                           a1[:,None], a2[:,None], angle[:,None] ], axis=1 )
    for ik,ell in enumerate( ellipse_vector ):
        ellipse = ( ( int(ell[x_]) , int(ell[y_] ) ), \
                    ( int(ell[a1_]), int(ell[a2_]) ), int(ell[rot_]) )
        hcolor  = tuple( [ int(val) for val in colors[ik] ] )
        image_  = cv2.ellipse( image_, ellipse, color=hcolor, thickness=thickness )
    
    # ------------------------------------------------- #
    # --- [3] return                                --- #
    # ------------------------------------------------- #
    return( image_ )



# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #
if ( __name__=="__main__" ):

    x_, y_, z_ = 0, 1, 2
    
    # ------------------------------------------------- #
    # --- [1] preparation                           --- #
    # ------------------------------------------------- #
    figSize     = (1000,1000)
    image       = np.ones( (figSize[y_],figSize[x_],3), dtype=np.uint8 ) * 255

    # ------------------------------------------------- #
    # --- [2] grid-like point to put rectangle      --- #
    # ------------------------------------------------- #
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 200.0, 800.0, 7 ]
    x2MinMaxNum = [ 200.0, 800.0, 7 ]
    x3MinMaxNum = [   0.0,   0.0, 1 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    centers     = coord[:,0:2]

    # ------------------------------------------------- #
    # --- [3] edge-length & colors                  --- #
    # ------------------------------------------------- #
    xc          = np.copy( centers[:,x_] )
    yc          = np.copy( centers[:,y_] )
    rc          = np.random.randint( 10,50, (xc.shape[0],) )
    a1          = np.random.randint( 10,50, (xc.shape[0],) )
    a2          = np.random.randint( 10,50, (xc.shape[0],) )
    angle       = np.random.randint( 0,360, (xc.shape[0],) )
    colorList   = np.array( [ [255,0,0], [0,255,0] ] )
    colorValues = np.array( np.where( np.random.random( centers.shape[0] ) > 0.5, 1, 0 ), \
                            dtype=np.int64 )

    # ------------------------------------------------- #
    # --- [4] put rectangululars                    --- #
    # ------------------------------------------------- #
    image1      = put__ellipses( image=image, xc=xc, yc=yc, rc=rc, \
                                 colorList=colorList, colorValues=colorValues )
    image2      = put__ellipses( image=image, xc=xc, yc=yc, a1=a1, a2=a2, angle=angle, \
                                 colorList=colorList, colorValues=colorValues )

    # ------------------------------------------------- #
    # --- [5] output                                --- #
    # ------------------------------------------------- #
    outFile1     = "test/out1.jpg"
    outFile2     = "test/out2.jpg"
    cv2.imwrite( outFile1, image1 )
    cv2.imwrite( outFile2, image2 )
    print( " outFile1 :: {}".format( outFile1 ) )
    print( " outFile2 :: {}".format( outFile2 ) )
    print()









    # # ------------------------------------------------- #
    # # --- [1]  arguments                            --- #
    # # ------------------------------------------------- #
    # if ( xyuv is not None ):
    #     i
        
    # if ( image   is None ): sys.exit( "[put__ellipses.py] image   == ???" )
    # if ( xyr     is None ):
    #     if ( centers is None ):
    #         if ( ( xc is not None ) and ( yc is not None ) ):
    #             centers = np.concatenate( [np.reshape( xc, (-1,) )[:,None],\
    #                                        np.reshape( yc, (-1,) )[:,None]], axis=1 )
    #         else:
    #             print( "[put__ellipses.py] xyr   == ???" )
    #             print( "[put__ellipses.py] xyr or [xc,yc,rc] or [ centers, rc ] must be given." )
    #             sys.exit()
    #     if ( centers is not None ):
    #         if ( type( rc ) in [ int, float ] ):
    #             rc = np.ones( (centers.shape[0],) ) * rc
    #         if ( type( rc ) in [ list, tuple, np.array ] ):
    #             rc = np.array( edge_length, dtype=np.int64 )
    #         xyr    = np.concatenate( [centers,rc[:,None]], axis=1 )
    #     else:
    #         print( "[put__ellipses.py] xyr   == ???" )
    #         print( "[put__ellipses.py] xyr or [xc,yc,rc] or [ centers, rc ] must be given." )
    #         sys.exit()
    # if ( colors is None ):
    #     if ( colorValues is not None ):
    #         colorList = np.array( colorList, dtype=np.uint8 )
    #         colors    = colorList[ np.array( colorValues, dtype=np.int64 ) ]
    #     else:
    #         colors  = np.repeat( np.array( [ [255,0,0] ], dtype=np.uint8 ), \
    #                              xyr.shape[0], axis=0 )
