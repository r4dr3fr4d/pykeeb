from openpyscad import * 
from .pykeeb import *
from .keyswitch_mount import *
from math import asin,sin,cos,acos,degrees,radians

class Keyboard_matrix:
	def __init__(self, r, c, row_spacing=1.5, column_spacing=1.5, plate_thickness=3, origin=[0,0,0], x_tent=0, y_tent=0, z_tent=0, mount_length=DSA_KEY_WIDTH, mount_width=DSA_KEY_WIDTH, switch_type='alps', mx_notches=True):
		self.rows = r
		self.columns = c
		self.modifiers = modifiers
		self.mount_length = mount_length 
		self.mount_width = mount_width 
		self.plate_thickness = plate_thickness 
		self.row_spacing = row_spacing 
		self.column_spacing = column_spacing 
		self.x_tent = x_tent 
		self.y_tent = y_tent 
		self.z_tent = z_tent 
		self.origin = origin
		self.col_hull_thickness = .01
		self.col_hull_extrude = .01
		self.row_hull_thickness = .01
		self.row_hull_extrude = .01
		self.ch_thickness = .01
		self.wall = Cube(0)
		self.wall_thickness = 3 #front/back walls
		self.wall_extrude = 3 
		self.side_wall_thickness = 3
		self.side_extrude = 3
		self.wall_x = .01 #for extra wall_hull thickness
		self.wall_y = .01 #for extra wall_hull thickness
		self.switch_type = switch_type
		self.mx_notches = mx_notches

		self.rm = self.row_modifiers = [[0, 0, 0, 0, 0, 0]  for b in range(r)] 
		self.cm = self.column_modifiers = [[0, 0, 0, 0, 0, 0]  for a in range(c)] 
		self.im = self.indiv_modifiers = [[[0, 0, 0, 0, 0, 0] for a in range(c)] for b in range(r)] 
		self.ik = self.ignore_keys = [[False for a in range(c)] for b in range(r)] 
		self.generate()


	def arc_rows(self, R):
		"""This function 2-dimensionally projects the keyboard rows onto a circle with radius R on the x-z axes."""

		#TODO: Make the focus of the circle adjustable

		unit_width=(self.row_spacing+self.mount_width)
		unitangle=degrees(2*asin(unit_width/(2*R)))


		focus_x= self.origin[0]+((self.rows/2)*unit_width)
		focus_z=self.origin[2]+R

		
		for row in range(self.rows):
		    x=row*unit_width

		    theta=-(((self.rows-1)/2)-row)*unitangle

		    zt=focus_z-((cos(radians(theta))*R))
		    xt=(focus_x+(sin(radians(theta))*(R+7)))-x
		    self.rm[row]= [0, xt, zt, theta, 0, 0]

	def arc_cols(self, R):
		"""This function 2-dimensionally projects the keyboard columns onto a circle with radius R on the y-z axes."""

		#TODO: Make the focus of the circle adjustable

		unit_width=(self.column_spacing+self.mount_width)
		unitangle=degrees(2*asin(unit_width/(2*R)))


		focus_y= self.origin[0]+((self.columns/2)*unit_width)
		focus_z=self.origin[2]+R

		
		for col in range(self.columns):
		    y=col*unit_width

		    theta=-(((self.columns-1)/2)-col)*unitangle

		    zt=focus_z-((cos(radians(theta))*R))
		    yt=(focus_y+(sin(radians(theta))*(R+7)))-y
		    self.cm[col]= [yt, 0, zt, 0, -theta, 0]




	def generate(self):	
		"""Generates the matrix w.r.t current modifier data.  Needs to be called for any modifier changes to be reflected before calling get_matrix()."""

		modifiers = [[list(map(sum, zip(self.rm[row], self.cm[column], self.im[row][column]))) for column in range(self.columns)] for row in range(self.rows)]
		modifiers = [[modifiers[row][column] + [self.ik[row][column]] for column in range(self.columns)] for row in range(self.rows)]

		#def __init__(self, transformations, ik=False, switch_type='alps', mount_length=DSA_KEY_WIDTH, mount_width=DSA_KEY_WIDTH, mx_notches=True):
		self.sm = self.switch_matrix = [[Keyswitch_mount([list(map(sum, zip(modifiers[row][column][:3], [column * (self.mount_width + self.column_spacing), row * (self.mount_length + self.row_spacing), 0]))) + modifiers[row][column][3:6], [self.origin[0], self.origin[1], self.origin[2], self.x_tent, self.y_tent, self.z_tent]], modifiers[row][column][6], self.switch_type, self.mount_length, self.mount_width, self.mx_notches) for column in range(self.columns)] for row in range(self.rows)]

		self.row_hulls = [[(self.sm[row][column].get_front(self.row_hull_thickness, self.row_hull_extrude) + self.sm[row+1][column].get_back(self.row_hull_thickness, self.row_hull_extrude)).hull() for column in range(self.columns)] for row in range(self.rows-1)] 

		self.column_hulls = [[(self.sm[row][column].get_right(self.col_hull_thickness, self.col_hull_extrude) + self.sm[row][column+1].get_left(self.col_hull_thickness, self.col_hull_extrude)).hull() for column in range(self.columns - 1)] for row in range(self.rows)] 
		
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

	def get_matrix(self): #needs more elegant solution, maybe using __add__?
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
						x += self.left_wall_hulls[row]
				if column == self.columns - 1:
					x += self.right_wall[row]
					if row < self.rows - 1:
						x += self.right_wall_hulls[row]
				if row < self.rows - 1:
					x += self.row_hulls[row][column]
					if column < self.columns - 1:
						x += self.corner_hulls[row][column]
				if column < self.columns - 1:
					x += self.column_hulls[row][column]
		return x

	def get_plate(self): #needs more elegant solution, maybe using __add__?
		"""Returns the union of the keyswitch mounts and their connecting hulls to form a plate"""
		x = Cube(0)
		for column in range(self.columns):
			for row in range(self.rows):
				x += self.sm[row][column].get_switch_at_location() 
				if column < self.columns - 1:
					x += self.column_hulls[row][column]
				if row < self.rows - 1:
					x += self.row_hulls[row][column]
					if column < self.columns - 1:
						x += self.corner_hulls[row][column]
		return x


	def get_walls(self): #needs more elegant solution, maybe using __add__?
		"""Returns the union of all the keyboard side walls and their connecting hulls to form a case"""
		x = Cube(0)
		for column in range(self.columns):
			for row in range(self.rows):
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
						x += self.left_wall_hulls[row]
				if column == self.columns - 1:
					x += self.right_wall[row]
					if row < self.rows - 1:
						x += self.right_wall_hulls[row]
		return x
