from openpyscad import *
#from math import *

DSA_KEY_WIDTH = 18.415

def project(piece): #openpyscad needs the projection feature added to it
	"""Hack that implements 3D to 2D projection feature for positive geometry to the xy plane.  Needs to be implemented in openpyscad."""
	return (piece + piece.translate([0,0,-100])).hull() + Cube(0) - Cube([500, 500, 250], center=True).translate([0,0,-125])
