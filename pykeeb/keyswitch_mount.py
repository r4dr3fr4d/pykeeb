from openpyscad import *
from .pykeeb import *

class Keyswitch_mount:
	#width is X, length is Y
	thickness = 3
	alps_keyswitch = Import('/usr/models/matias.stl').color('Gray')
	mx_keyswitch = Import('/usr/models/cherry.stl').color('Gray')
	dsa_key = Import('/usr/models/dsa_1u.stl').color('White') #18x18x8mm 
	def __init__(self, transformations, ik=False, switch_type='alps', mount_length=DSA_KEY_WIDTH, mount_width=DSA_KEY_WIDTH):
		"""Sets up single switch-mount geometry, with transformations, W.R.T. switch type."""
		mx_length = 14.4
		mx_width = 14.4
		alps_length = 12.8
		alps_width = 15.5
		self.mount_length = mount_length 
		self.mount_width = mount_width
		self.switch_type = switch_type
		mx_hole = Cube([mx_width, mx_length, self.thickness], center=True)
		alps_hole = Cube([alps_width, alps_length, self.thickness], center=True)
		if switch_type == 'mx':
			self.switch_mount = Cube([self.mount_width, self.mount_length, self.thickness], center=True) - mx_hole
		if switch_type == 'alps':
			self.switch_mount = Cube([self.mount_width, self.mount_length, self.thickness], center=True) - alps_hole 
		self.ignore_key = ik
		self.transformations = transformations

	def transform(self, x):
		"""Applies a list (tiers) of lists (each following the format [x-translate, y-translate, z-translate, x-rotate, y-rotate, z-rotate]) to the mount, one tier at a time."""
		if any(isinstance(l, list) for l in self.transformations):
			for tier in self.transformations:
				x = x.rotate(tier[3:]).translate(tier[0:3])
		else:
			x = x.rotate(self.transformations[3:]).translate(self.transformations[0:3])
		return x

	#def __add__(self, other):
		#return self.switch_mount.rotate(self.rotation).translate(self.origin) + other.switch_mount.rotate(other.rotation).translate(other.origin)

	def get_switch_at_location(self, hull=False):
		"""Returns the mount with transformations applied."""
		if self.ignore_key == True: return Cube(0).disable()
		if hull == True: #helpful for cutting away hulls/stuff in the way of switch hole. Need to think about how to improve.
			cutaway = self.switch_mount.hull() - self.switch_mount.hull().translate([-7,0,0]) #hack
			cutaway = cutaway.translate([0,0,-self.thickness]) #hack
			return self.transform(cutaway)
		else:
			return self.transform(self.switch_mount)

	def get_keyswitch(self):
		"""Returns model of switch in its place in the mount."""
		if self.switch_type == 'alps':
			return self.transform(self.alps_keyswitch.rotate([180, 0,90]).translate([0, 0, 9]))
		if self.switch_type == 'mx':
			return self.transform(self.mx_keyswitch.rotate([180, 0,90]).translate([0, 0, 9]))

	def get_keycap(self, down=False): 
		"""Returns model of keycap in it's rest position, or depressed position if 'down' == True."""
		if down: return self.transform(self.dsa_key.translate([0, 0, 4]))
		return self.transform(self.dsa_key.translate([0, 0, 7]))

	def get_side(self, side, thickness=.01, extrude=0, extend=True):
		"""Returns Cube (rect. prism) of width 'thickness' that sticks out of the mount by length of 'extrude', specified by a given 'side' (front, back, left, or right).  'extend' will hull the returned Cube with the actual side of the mount."""
		if extrude > thickness and extend == True:
			thickness = extrude
		if side == 'left': cube = Cube([thickness, self.mount_length, self.thickness]).translate([-self.mount_width/2 - extrude, -self.mount_length/2, -self.thickness/2])
		elif side == 'right': cube = Cube([thickness, self.mount_length, self.thickness]).translate([self.mount_width/2 - thickness + extrude, -self.mount_length/2, -self.thickness/2])
		elif side == 'front': cube = Cube([self.mount_width, thickness, self.thickness]).translate([-self.mount_width/2, self.mount_length/2 - thickness + extrude, -self.thickness/2])
		elif side == 'back': cube = Cube([self.mount_width, thickness, self.thickness]).translate([-self.mount_width/2, -self.mount_length/2 - extrude, -self.thickness/2])
		if self.ignore_key == True: cube = cube.disable()
		return self.transform(cube)

	def get_front(self, thickness=.01, extrude=0, extend=True): 
		"""Wrapper.  See get_side()."""
		return self.get_side('front', thickness, extrude, extend)

	def get_back(self, thickness=.01, extrude=0, extend=True): 
		"""Wrapper.  See get_side()."""
		return self.get_side('back', thickness, extrude, extend)

	def get_left(self, thickness=.01, extrude=0, extend=True): 
		"""Wrapper.  See get_side()."""
		return self.get_side('left', thickness, extrude, extend)

	def get_right(self, thickness=.01, extrude=0, extend=True): 
		"""Wrapper.  See get_side()."""
		return self.get_side('right', thickness, extrude, extend)

	def get_corner(self, position, x, y, x_extrude=0, y_extrude=0, extend=True):
		"""Returns Cube (rect. prism) of length/width x/y that extrudes of the mount's corner (specified by fl, fr, bl, or br, for 'front left', 'front right', etc) by lengths x_extrude and y_extrude.  'extend will hull the returned Cube with the actual corner of the mount."""
		if extend == True:
			if x_extrude > x:
				x = x_extrude
			if y_extrude > y:
				y = y_extrude
		corner = Cube([x, y, self.thickness])
		if position == 'fl': corner = corner.translate([-self.mount_width/2 - x_extrude, self.mount_length/2 - y + y_extrude, -self.thickness/2])
		elif position == 'fr': corner = corner.translate([self.mount_width/2 - x + x_extrude, self.mount_length/2 - y + y_extrude, -self.thickness/2])
		elif position == 'bl': corner = corner.translate([-self.mount_width/2 - x_extrude, -self.mount_length/2 - y_extrude, -self.thickness/2])
		elif position == 'br': corner = corner.translate([self.mount_width/2 - x + x_extrude, -self.mount_length/2 - y_extrude, -self.thickness/2])
		if self.ignore_key == True: corner = corner.disable()
		return self.transform(corner)
