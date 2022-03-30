from cocos.layer.util_layers import ColorLayer
import cocos.menu
import cocos.scene
import cocos.layer
import cocos.actions as ac
from cocos.director import director
from cocos.scenes.transitions import FadeTRTransition

import pyglet.app
import pyglet.font

from ghosthunter import new_game

class MainMenu(cocos.menu.Menu):
	HARDMODE = False
	HARDMODEACT = False
	def __init__(self):
		super(MainMenu, self).__init__('Ghost Hunter')

		self.font_title['font_name'] = 'Avara'
		self.font_item['font_name'] = 'Avara'
		self.font_item_selected['font_name'] = 'Avara'
    
		self.menu_anchor_y = 'center'
		self.menu_anchor_x = 'center'

		self.difficulty = ['OFF', 'ON']

		items = []
		items.append(cocos.menu.MenuItem('New Game', self.on_new_game))
		items.append(cocos.menu.MultipleMenuItem('Hard Mode: ', self.set_difficulty, self.difficulty))
		items.append(cocos.menu.ToggleMenuItem('Show FPS: ', self.show_fps, director.show_FPS))
		items.append(cocos.menu.MenuItem('Quit', pyglet.app.exit))

		self.create_menu(items, ac.ScaleTo(1.25, duration=0.25), ac.ScaleTo(1.0, duration=0.25))

	def on_new_game(self):
		director.push(FadeTRTransition(new_game(), duration=2))

	def show_fps(self, val):
		director.show_FPS = val

	def set_difficulty(self, index):
		if index:
			MainMenu.HARDMODE = True
			MainMenu.HARDMODEACT = True

def new_menu():
	scene = cocos.scene.Scene()
	color_layer = cocos.layer.ColorLayer(0, 0, 0, 255)
	scene.add(MainMenu(), z = 1)
	scene.add(color_layer, z = 0)
	return scene

def get_HM():
	return MainMenu.HARDMODE

def get_HMA():
	return MainMenu.HARDMODEACT