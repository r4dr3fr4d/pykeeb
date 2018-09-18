from openpyscad import *
#from math import *

DSA_KEY_WIDTH = 18.415

def project(piece, size=500): #Is this function really necessary?
    """
    Mirrors (xy), hulls, and subtracts beneath the xy-plane, in that order.
    Allows for creation of sides/walls.
    Size defaults to 'arbitrarily large'.
    """
    return ((piece + piece.mirror([0,0,1])).hull() 
        - Cube([size, size, size], center=True).translate([0,0,-size/2]))
