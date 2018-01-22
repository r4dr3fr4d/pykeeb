from openpyscad import *
from .pykeeb import *
from .keyswitch_mount import *

class Keyboard_arc:
	def __init__(self, columns, neg_columns, rows, arc_length, arc_angle, z_arc_length=0, z_arc_angle=0, row_spacing=2, column_spacing=2, plate_thickness=3, origin=[0,0,0], x_tent=0, y_tent=0, z_tent=0, mount_length=DSA_KEY_WIDTH, mount_width=DSA_KEY_WIDTH):
		"""Builds an arc of keyswitch mounts, curvature defined by arc_length, with arc_angle degrees between each mount.  neg_columns allows for mounts to be created on both sides of the origin.  Can also curve in against it's own normal dimension using z_arc_length and z_arc_angle, allowing for some nice sloped key arcs for the thumbs.  Otherwise the same as Keyboard_matrix().  ***NOTE:  Only tested with one row despite accepting multiple rows.***"""
		self.columns = columns + neg_columns
		self.rows = rows
		self.modifiers = modifiers
		self.neg_columns = neg_columns #columns arcing left
		self.row_spacing = row_spacing
		self.column_spacing = column_spacing
		self.mount_length = mount_length #needs to change
		self.mount_width = mount_width #needs to change
		self.arc_length = arc_length
		self.arc_angle = arc_angle 
		self.z_arc_length = z_arc_length 
		self.z_arc_angle = z_arc_angle
		self.origin = origin
		self.x_tent = x_tent
		self.y_tent = y_tent
		self.z_tent = z_tent
		self.rm = row_modifiers = [[0, 0, 0, 0, 0, 0]  for b in range(rows)]
		self.cm = column_modifiers = [[0, 0, 0, 0, 0, 0]  for a in range(columns)]
		self.im = indiv_modifiers = [[[0, 0, 0, 0, 0, 0] for a in range(columns)] for b in range(rows)]
		self.ik = ignore_keys = [[False for a in range(columns)] for b in range(rows)]
		self.hull_thickness = .01
		self.ch_thickness = .01
		self.wall_thickness = 3 #front/back walls
		self.wall_extrude = 3 
		self.side_wall_thickness = 2
		self.side_extrude = 2
		self.wall_x = 0.5 #for extra wall_hull thickness
		self.wall_y = 0.5 #for extra wall_hull thickness

		self.rm = row_modifiers = [[0, 0, 0, 0, 0, 0]  for b in range(rows)] 
		self.cm = column_modifiers = [[0, 0, 0, 0, 0, 0]  for a in range(columns + neg_columns)] 
		self.im = indiv_modifiers = [[[0, 0, 0, 0, 0, 0] for a in range(columns + neg_columns)] for b in range(rows)] 
		self.ik = ignore_keys = [[False for a in range(columns + neg_columns)] for b in range(rows)] 
		self.generate()

	def generate(self):
		modifiers = [[list(map(sum, zip(self.rm[row], self.cm[column], self.im[row][column]))) for column in range(self.columns)] for row in range(self.rows)]
		modifiers = [[modifiers[row][column] + [self.ik[row][column]] for column in range(self.columns)] for row in range(self.rows)]

		self.transformations = [[[modifiers[row][column][:6], [0, self.arc_length, 0,0,0,0], [0, -self.arc_length, 0,0,0, -self.arc_angle * (column - self.neg_columns)], [self.origin[0], self.origin[1], self.origin[2], self.x_tent, self.y_tent, self.z_tent]] for column in range(self.columns)] for row in range(self.rows)] 

		self.sm = self.switch_matrix = [[Keyswitch_mount(self.transformations[row][column], modifiers[row][column][6]) for column in range(self.columns)] for row in range(self.rows)]

		self.row_hulls = [[(self.sm[row][column].get_front(self.hull_thickness) + self.sm[row+1][column].get_back(self.hull_thickness)).hull() for column in range(self.columns)] for row in range(self.rows-1)] 
		self.column_hulls = [[(self.sm[row][column].get_right(self.hull_thickness) + self.sm[row][column+1].get_left(self.hull_thickness)).hull() for column in range(self.columns - 1)] for row in range(self.rows)] 
		
		self.corner_hulls = [[(self.sm[row][column].get_corner('fr', self.ch_thickness, self.ch_thickness) 
					+ self.sm[row][column+1].get_corner('fl', self.ch_thickness, self.ch_thickness) 
					+ self.sm[row+1][column].get_corner('br', self.ch_thickness, self.ch_thickness)
					+ self.sm[row+1][column+1].get_corner('bl', self.ch_thickness, self.ch_thickness)).hull() for column in range(self.columns-1)] for row in range(self.rows-1)] 

		self.front_wall = [project(self.sm[self.rows-1][column].get_front(self.wall_thickness, self.wall_extrude)) for column in range(self.columns)]
		self.front_wall_hulls = [project((self.sm[self.rows-1][column].get_corner('fr', self.wall_x, self.wall_thickness, 0, self.wall_extrude) 
					+ self.sm[self.rows-1][column+1].get_corner('fl', self.wall_x, self.wall_thickness, 0, self.wall_extrude))).hull() for column in range(self.columns - 1)]

		self.back_wall = [project(self.sm[0][column].get_back(self.wall_thickness, self.wall_extrude)) for column in range(self.columns)]
		self.back_wall_hulls = [project((self.sm[0][column].get_corner('br', self.wall_x, self.wall_thickness, 0, self.wall_extrude) 
					+ self.sm[0][column+1].get_corner('bl', self.wall_x, self.wall_thickness, 0, self.wall_extrude))).hull() for column in range(self.columns - 1)]

		self.left_wall = [project(self.sm[row][0].get_left(self.side_wall_thickness, self.side_extrude)) for row in range(self.rows)]
		self.left_wall_hulls = [project((self.sm[row][0].get_corner('fl', self.side_wall_thickness, self.wall_y, self.side_extrude) 
					+ self.sm[row+1][0].get_corner('bl', self.side_wall_thickness, self.wall_y, self.side_extrude)).hull()) for row in range(self.rows - 1)]

		self.right_wall = [project(self.sm[row][self.columns-1].get_right(self.side_wall_thickness, self.side_extrude)) for row in range(self.rows)]
		self.right_wall_hulls = [project((self.sm[row][self.columns-1].get_corner('fr', self.side_wall_thickness, self.wall_y, self.side_extrude) 
					+ self.sm[row+1][self.columns-1].get_corner('br', self.side_wall_thickness, self.wall_y, self.side_extrude)).hull()) for row in range(self.rows - 1)]

		self.front_left_corner = project(self.sm[self.rows-1][0].get_corner('fl', self.side_extrude, self.wall_extrude, self.side_extrude, self.wall_extrude))
		self.front_right_corner = project(self.sm[self.rows-1][self.columns-1].get_corner('fr', self.side_extrude, self.wall_extrude, self.side_extrude, self.wall_extrude))
		self.back_left_corner = project(self.sm[0][0].get_corner('bl', self.side_extrude, self.wall_extrude, self.side_extrude, self.wall_extrude))
		self.back_right_corner = project(self.sm[0][self.columns-1].get_corner('br', self.side_extrude, self.wall_extrude, self.side_extrude, self.wall_extrude))

	def get_arc(self): #needs more elegant solution, maybe using __add__?
		"""Returns the arc matrix."""
		x = Cube(0) 
		for column in range(self.columns):
			for row in range(self.rows):
				x += self.sm[row][column].get_switch_at_location() 
				if row == 0:
					x += self.back_wall[column]
					if column < self.columns - 1:
						x += self.back_wall_hulls[column]
					if column == 0:
						x += self.back_left_corner
					if column == self.columns - 1:
						x += self.back_right_corner
				if row == self.rows - 1:
					x += self.front_wall[column]
					if column < self.columns - 1:
						x += self.front_wall_hulls[column]
					if column == 0:
						x += self.front_left_corner
					if column == self.columns - 1:
						x += self.front_right_corner
				if column == 0:
					x += self.left_wall[row]
					if row < self.rows - 1:
						break
						x += self.left_wall_hulls[row]
				if column == self.columns - 1:
					x += self.right_wall[row]
					if row < self.rows - 1:
						x += self.right_wall_hulls[row]
				if row < self.rows - 1:
					break
					x += self.row_hulls[row][column]
					if column < self.columns - 1:
						x += self.corner_hulls[row][column]
				if column < self.columns - 1:
					x += self.column_hulls[row][column]
		return x
