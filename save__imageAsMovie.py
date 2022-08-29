import os, sys, cv2, copy
import numpy as np


# ========================================================= #
# ===  save__imageAsMovie.py                            === #
# ========================================================= #

def save__imageAsMovie( images=None, outFile=None, resize=None, frame_rate=10 ):

    # ------------------------------------------------- #
    # --- [1] check arguments                       --- #
    # ------------------------------------------------- #
    if ( images  is None ): sys.exit( "[save__imageAsMovie.py] images == ???" )
    if ( outFile is None ): outFile = "out.mov"
    if ( not( type( images ) is np.ndarray ) ):
        sys.exit( "[save__imageAsMovie.py] type( images ) == ??? :: {}".format( type(images) ) )
    extention = os.path.splitext( outFile )
        
    # ------------------------------------------------- #
    # --- [2] resize                                --- #
    # ------------------------------------------------- #
    if ( resize is not None ):
        if ( type(resize) in [ int ]   ):
            hgt, wdt = images.shape[1], images.shape[2]
            if ( hgt >= wdt ):
                hgt, wdt = resize, wdt / hgt * resize
            else:
                hgt, wdt = hgt / wdt * resize, resize
            resize   = ( int(wdt), int(hgt) )
        if ( type(resize) in [ float ] ):
            hgt, wdt = images.shape[1], images.shape[2]
            resize   = ( int( wdt*resize ), int(hgt*resize) )
        resize = tuple( resize )
        mSize  = copy.copy( resize )
        images = np.array( [ cv2.resize( img, dsize=resize ) for img in images ] )
    else:
        hgt, wdt = images.shape[1], images.shape[2]
        mSize    = ( int(wdt), int(hgt) )
        
    # ------------------------------------------------- #
    # --- [3] prepare for saving                    --- #
    # ------------------------------------------------- #
    if ( extention in [ ".mov", ".mp4" ] ):
        fourcc = "mp4v"
    else:
        fourcc = "mp4v"
    write_format = cv2.VideoWriter_fourcc( *fourcc )
    writer       = cv2.VideoWriter( outFile, write_format, frame_rate, mSize )
    print( "[save__movieFrames.py] outFile          :: {} ".format( outFile  ) ) 
    print()

    # ------------------------------------------------- #
    # --- [4] save images as movie                  --- #
    # ------------------------------------------------- #
    for ik,frame in enumerate( images ):
        writer.write( frame )
    
    # ------------------------------------------------- #
    # --- [5] return                                --- #
    # ------------------------------------------------- #
    writer.release()
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #
if ( __name__=="__main__" ):

    images  = np.array( np.random.randint( 0, 128, (20,10,10,3) ), dtype=np.uint8 )
    outFile = "test/out.mov"
    resize  = None
    ret     = save__imageAsMovie( images=images, outFile=outFile, resize=resize )
    
