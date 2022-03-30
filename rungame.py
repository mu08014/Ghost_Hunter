import pyglet.font
import pyglet.resource

import cocos.director 

from menu import new_menu

if __name__=='__main__':
	pyglet.font.add_file('font/Avara.otf')

	cocos.director.director.init(caption = 'Ghost Hunter', width = 1000, height = 750)
	cocos.director.director.run(new_menu())