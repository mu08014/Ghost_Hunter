from collections import defaultdict

from pyglet.image import load, ImageGrid, Animation
from pyglet.window import key
import pyglet.resource

import cocos.actions
import cocos.layer
import cocos.sprite
import cocos.collision_model as cm
import cocos.euclid as eu

import random

class Actor(cocos.sprite.Sprite):
	def __init__(self, image, x, y):
		super(Actor, self).__init__(image)
		self.x = x
		self.y = y
		self.position = eu.Vector2(x, y)
		self.cshape = cm.AARectShape(self.position,
									 self.width * 0.5,
									 self.height * 0.5)

	def move(self, offsetx, offsety):
		self.position += eu.Vector2(offsetx, offsety)
		self.cshape.center += eu.Vector2(offsetx, offsety)

	def update(self, elapsed):
		pass

	def collide(self, other):
		pass

class Player(Actor):
	KEY_PRESSED = defaultdict(int)
	CANSHOOT = True
	NUMBER = 0
	
	Px = 0
	Py = 0
	Pvx = 0
	Pvy = 0

	PlayerPosition = []
	lives = 1

	def __init__(self, x, y):
		self.img = 'image/Individual/MainCharacter_LW_F9.png'
		super(Player, self).__init__(self.img, x, y)
		self.v = 200
		self.vector = eu.Vector2(0, 0)
		self.time = 0
		self.delta = 0
		self.Debug = None
		self.playerhit = pyglet.resource.media('sound/playerhit.mp3')

	def update(self, elapsed):
		pressed = Player.KEY_PRESSED
		movementx = pressed[key.D] - pressed[key.A]
		movementy = pressed[key.W] - pressed[key.S]

		shootx = pressed[key.RIGHT] - pressed[key.LEFT]
		shooty = pressed[key.UP] - pressed[key.DOWN]

		w = self.width * 0.5
		h = self.height * 0.5
		vx = 0
		vy = 0

		if movementx != 0:
			if w <= self.x <= self.parent.width - w:
				vx = movementx
			elif self.x < w:
				self.x = w
			elif self.x > self.parent.width - w:
				self.x = self.parent.width - w

		if movementy != 0:
			if h <= self.y <= self.parent.height - h:
				vy = movementy
			elif self.y < h:
				self.y = h
			elif self.y > self.parent.height - h:
				self.y = self.parent.height - h

		v0 = pow(vx**2 + vy**2, 0.5)
		if v0 != 0:
			vx = vx/v0 * elapsed * self.v * 1.0
			vy = vy/v0 * elapsed * self.v * 1.0
		self.move(vx, vy)

		if shootx == 0 and shooty == 0:
			if movementy < 0:
				if movementx > 0:
					self.img = 'image/Individual/MainCharacter_LW_F7.png'
				elif movementx < 0:
					self.img = 'image/Individual/MainCharacter_LW_F13.png'
				else:
					self.img = 'image/Individual/MainCharacter_LW_F9.png'
			elif movementy > 0:
				if movementx > 0:
					self.img = 'image/Individual/MainCharacter_LW_F7.png'
				elif movementx < 0:
					self.img = 'image/Individual/MainCharacter_LW_F13.png'
				else:
					self.img = 'image/Individual/MainCharacter_LW_F3.png'
			else:
				if movementx > 0:
					self.img = 'image/Individual/MainCharacter_LW_F7.png'
				elif movementx < 0:
					self.img = 'image/Individual/MainCharacter_LW_F13.png'
		else:
			if shooty < 0:
				if shootx > 0:
					self.img = 'image/Individual/MainCharacter_LW_F7.png'
					if Player.CANSHOOT == True:
						self.parent.add(Shoot(self.x+50, self.y-50, 1, -1))
						Player.CANSHOOT = False
				elif shootx < 0:
					self.img = 'image/Individual/MainCharacter_LW_F13.png'
					if Player.CANSHOOT == True:	
						self.parent.add(Shoot(self.x-50, self.y-50, -1, -1))
						Player.CANSHOOT = False
				else:
					self.img = 'image/Individual/MainCharacter_LW_F9.png'
					if Player.CANSHOOT == True:
						self.parent.add(Shoot(self.x, self.y-50, 0, -1))
						Player.CANSHOOT = False
			elif shooty > 0:
				if shootx > 0:
					self.img = 'image/Individual/MainCharacter_LW_F7.png'
					if Player.CANSHOOT == True:
						self.parent.add(Shoot(self.x+50, self.y+50, 1, 1))
						Player.CANSHOOT = False
				elif shootx < 0:
					self.img = 'image/Individual/MainCharacter_LW_F13.png'
					if Player.CANSHOOT == True:
						self.parent.add(Shoot(self.x-50, self.y+50, -1, 1))
						Player.CANSHOOT = False
				else:
					self.img = 'image/Individual/MainCharacter_LW_F3.png'
					if Player.CANSHOOT == True:
						self.parent.add(Shoot(self.x, self.y+50, 0, 1))
						Player.CANSHOOT = False
			else:
				if shootx > 0:
					self.img = 'image/Individual/MainCharacter_LW_F7.png'
					if Player.CANSHOOT == True:
						self.parent.add(Shoot(self.x+50, self.y, 1, 0))
						Player.CANSHOOT = False
				elif shootx < 0:
					self.img = 'image/Individual/MainCharacter_LW_F13.png'
					if Player.CANSHOOT == True:
						self.parent.add(Shoot(self.x-50, self.y, -1, 0))
						Player.CANSHOOT = False

		self.image = load(self.img)

		Player.Px = self.x
		Player.Py = self.y
		if v0 != 0:
			Player.Pvx = vx/v0 * self.v * 0.5
			Player.Pvy = vy/v0 * self.v * 0.5
		else:
			Player.Pvx = 0
			Player.Pvy = 0
		
		if not Player.CANSHOOT:
			self.time += elapsed
			if self.time >= 1:
				Player.CANSHOOT = True
				self.time = 0
		
		Player.PlayerPosition.append((self.x, self.y))
		if self.delta >= 2.0:
			del Player.PlayerPosition[0]
		else:
			self.delta += elapsed

	def collide(self, other):
		if isinstance(other, GhostBoss):
			other.kill()
			other.hpbar.kill()
			self.playerhit.play()
			Player.lives -= 1
		elif isinstance(other, Ghost) and self.Debug != other:
			Player.NUMBER += 1
			self.playerhit.play()
			if Player.NUMBER < 4:
				self.Debug = other
				other.gcollide()
			else:
				other.gcollide()
				Player.lives -= 1
		elif isinstance(other, PlayerClone):
			other.kill()
			self.playerhit.play()
			Player.lives -= 1
		

class PlayerClone(Actor):
	ACTIVE = False
	def __init__(self, x, y, image='image/Individual/MainCharacter_LW_F9.png'):
		super(PlayerClone, self).__init__(image, x, y)
		self.color = (255, 0, 0)
		self.num = 0
		self.v = 130
		self.x = x
		self.y = y
		if Player.NUMBER == 1:
			self.num = 1
		elif Player.NUMBER == 2:
			self.num = 2
		elif Player.NUMBER == 3:
			self.num = 3

	def update(self, elapsed):
		if self.num == 1:
			self.x = Player.PlayerPosition[0][0]
			self.y = Player.PlayerPosition[0][1]
			self.cshape = cm.AARectShape(self.position,
									 self.width * 0.5,
									 self.height * 0.5)
		elif self.num == 2:
			self.x = Player.PlayerPosition[int(len(Player.PlayerPosition)/3)-1][0]
			self.y = Player.PlayerPosition[int(len(Player.PlayerPosition)/3)-1][1]
			self.cshape = cm.AARectShape(self.position,
									 self.width * 0.5,
									 self.height * 0.5)
		elif self.num == 3:
			self.x = Player.PlayerPosition[int(len(Player.PlayerPosition)*2/3)-1][0]
			self.y = Player.PlayerPosition[int(len(Player.PlayerPosition)*2/3)-1][1]
			self.cshape = cm.AARectShape(self.position,
									 self.width * 0.5,
									 self.height * 0.5)
		elif self.num == 4:
			self.x = Player.PlayerPosition[-1][0]
			self.y = Player.PlayerPosition[-1][1]
			self.cshape = cm.AARectShape(self.position,
									 self.width * 0.5,
									 self.height * 0.5)
		if PlayerClone.ACTIVE:
			self.color = (0, 0, 0)
		else:
			self.color = (255, 0, 0)

	def collide(self, other):
		if PlayerClone.ACTIVE:
			if isinstance(other, Ghost):
				if not isinstance(other, GhostBoss):
					other.gcollide()

class Shoot(Actor):
	def __init__(self, x, y, sx, sy, img='image/Shoot.png'):
		super(Shoot, self).__init__(img, x, y)
		self.v = 500
		self.vx = (self.v * sx * 1.0) / pow(sx**2 + sy**2, 0.5)
		self.vy = (self.v * sy * 1.0) / pow(sx**2 + sy**2, 0.5)
		self.speed = eu.Vector2((self.v * sx * 1.0) / pow(sx**2 + sy**2, 0.5), (self.v * sy * 1.0) / pow(sx**2 + sy**2, 0.5))
		self.shootsound = pyglet.resource.media('sound/shoot.mp3')
		self.shootsound.play()
	
	def update(self, elapsed):
		self.move(self.vx * elapsed, self.vy * elapsed)

	def collide(self, other):
		if isinstance(other, Ghost):
			if GameLayer.GN > 0:
				GameLayer.GN -= 1
			other.gcollide()
			self.kill()
			if isinstance(other, GhostBoss):
				other.color = (255, 0, 0)
				other.belta += 0.01

class Ghost(Actor):
	def load_animation(imge = 'image/Ghost.png'):
		seq = ImageGrid(load(imge), 1, 2)
		return Animation.from_image_sequence(seq, 0.5)

	def __init__(self, img, x, y):
		super(Ghost, self).__init__(img, x, y)
		if GameLayer.HARDMODE:
			self.v = 150
		else:
			self.v = 120
		self.health = 1
		self.ghosthit = pyglet.resource.media('sound/ghosthit.mp3')

	def on_exit(self):
		super(Ghost, self).on_exit()
	
	def gcollide(self):
		self.health -= 1
		self.ghosthit.play()
		if self.health == 0:
			self.kill()
		if isinstance(self, GhostBoss):
			self.hpbar.hpbarupdate(self.health*1.0/self.maxhealth)
		else:
			GameLayer.ghost.remove(self)

class Ghost1(Ghost):
	def __init__(self, img, x, y):
		super(Ghost1, self).__init__(img, x, y)
		self.x = x
		self.y = y

	def make_ghost1(x, y):
		anim = Ghost.load_animation()
		return Ghost1(anim, x, y)

	def update(self, elapsed):
		dx = Player.Px - self.x
		dy = Player.Py - self.y
		d = (dx**2 + dy**2)**0.5
		dx = dx/d * self.v * elapsed
		dy = dy/d * self.v * elapsed
		self.move(dx, dy)

class Ghost2(Ghost):
	def __init__(self, img, x, y):
		super(Ghost2, self).__init__(img, x, y)
		self.x = x
		self.y = y
		self.color = (0, 255, 0)

	def make_ghost2(x, y):
		anim = Ghost.load_animation()
		return Ghost2(anim, x, y)

	def update(self, elapsed):
		dx = Player.Px + Player.Pvx*0.4 - self.x
		dy = Player.Py + Player.Pvy*0.4 - self.y
		d = (dx**2 + dy**2)**0.5
		dx = dx/d * self.v * elapsed
		dy = dy/d * self.v * elapsed
		self.move(dx, dy)

class Ghost3(Ghost):
	def __init__(self, img, x, y):
		super(Ghost3, self).__init__(img, x, y)
		self.x = x
		self.y = y
		self.vx = 1/(2**0.5) * self.v
		self.vy = 1/(2**0.5) * self.v
		self.color = (0, 0, 255)
		self.stop = False
		self.savex = 0
		self.savey = 0
	
	def make_ghost3(x, y):
		anim = Ghost.load_animation()
		return Ghost3(anim, x, y)
		
	def update(self, elapsed):
		if (self.x >= self.parent.width):
			self.vx *= -1
		elif (self.x <= 0):
			self.vx *= -1
		if (self.y >= self.parent.height):
			self.vy *= -1
		elif (self.y <= 0):
			self.vy *= -1
		if self.v == 0:
			self.savex = self.vx
			self.savey = self.vy
			self.vx = 0
			self.vy = 0
			self.stop = True
		elif self.v != 0 and self.stop:
			self.stop = False
			self.vx = self.savex
			self.vy = self.savey
		vvx = self.vx * elapsed
		vvy = self.vy * elapsed
		self.move(vvx, vvy)


class GhostBoss(Ghost):
	BOSSPAGE = False
	def __init__(self, img, x, y):
		super(GhostBoss, self).__init__(img, x, y)
		self.x = x
		self.y = y
		self.v = 50
		if GameLayer.HARDMODE:
			self.maxhealth = 10.0
		else:
			self.maxhealth = 5.0
		self.health = int(self.maxhealth)
		self.belta = 0
		self.bc = self.color

		self.hpbar = hpbar.makehpbar(self.x, self.y + 120)

	def makeboss(x = 0, y = 0, imge='image/boss.png'):
		return GhostBoss(imge, x, y)

	def update(self, elapsed):
		dx = Player.Px - self.x
		dy = Player.Py - self.y
		d = (dx**2 + dy**2)**0.5
		dx = dx/d * self.v * elapsed
		dy = dy/d * self.v * elapsed
		self.move(dx, dy)

		if self.belta > 0:
			self.belta += elapsed
			if self.belta > 0.3:
				self.color = self.bc
				self.belta = 0
		self.hpbar.x = self.x
		self.hpbar.y = self.y + 120

class hpbar(Actor):
	def __init__(self, img, x, y):
		super(hpbar, self).__init__(img, x, y)
		self.img = img
		
	def makehpbar(x, y, img = 'image/health/blood_red_bar.png'):
		return hpbar(img, x, y)

	def hpbarupdate(self, n):
		if n == 1:
			self.img = 'image/health/blood_red_bar.png'
		elif 0.9 <= n < 1:
			self.img = 'image/health/blood_red_bar1.png'
		elif 0.8 <= n < 0.9:
			self.img = 'image/health/blood_red_bar2.png'
		elif 0.7 <= n < 0.8:
			self.img = 'image/health/blood_red_bar3.png'
		elif 0.6 <= n < 0.7:
			self.img = 'image/health/blood_red_bar4.png'
		elif 0.5 <= n < 0.6:
			self.img = 'image/health/blood_red_bar5.png'
		elif 0.4 <= n < 0.5:
			self.img = 'image/health/blood_red_bar6.png'
		elif 0.3 <= n < 0.4:
			self.img = 'image/health/blood_red_bar7.png'
		elif 0.2 <= n < 0.3:
			self.img = 'image/health/blood_red_bar8.png'
		elif 0.1 <= n < 0.2:
			self.img = 'image/health/blood_red_bar9.png'
		elif 0 <= n < 0.1:
			self.img = 'image/health/blood_red_bar10.png'
		self.image = load(self.img)

class Item(Actor):
	def __init__(self, img, x, y):
		super(Item, self).__init__(img, x, y)
		self.getitem = pyglet.resource.media('sound/getitem.mp3')

class healthItem(Item):
	HCHECK = False
	def load_animation(imge = 'image/Item/healthup.png'):
		seq = ImageGrid(load(imge), 1, 4)
		return Animation.from_image_sequence(seq, 0.2)

	def __init__(self, img, x, y):
		super(healthItem, self).__init__(img, x, y)
	
	def makeheal(x, y):
		anim = healthItem.load_animation()
		return healthItem(anim, x, y)

	def collide(self, other):
		if isinstance(other, Player):
			self.kill()
			self.getitem.play()
			healthItem.HCHECK = True

class timeItem(Item):
	TCHECK = False
	def __init__(self, img, x, y):
		super(timeItem, self).__init__(img, x, y)
	
	def maketime(x, y, imge = 'image/Item/timestop.png'):
		return timeItem(imge, x, y)

	def collide(self, other):
		if isinstance(other, Player):
			self.kill()
			self.getitem.play()
			timeItem.TCHECK = True

class cloneItem(Item):
	CCHECK = False
	def __init__(self, img, x, y):
		super(cloneItem, self).__init__(img, x, y)

	def makeclone(x, y, imge = 'image/Item/changeclone.png'):
		return cloneItem(imge, x, y)

	def collide(self, other):
		if isinstance(other, Player):
			self.kill()
			self.getitem.play()
			cloneItem.CCHECK = True

class GameLayer(cocos.layer.Layer):
	is_event_handler = True
	ghost = []
	GN = 30

	HARDMODE = None
	HARDMODEACT = None

	def set_GN(self):
		if GameLayer.HARDMODE:
			GameLayer.GN = 50

	def on_key_press(self, k, _):
		Player.KEY_PRESSED[k] = 1

	def on_key_release(self, k, _):
		Player.KEY_PRESSED[k] = 0

	def __init__(self, hud):
		super(GameLayer, self).__init__()
		w, h = cocos.director.director.get_window_size()
		self.width = w
		self.height = h
		self.time = 0.
		self.delta = 0

		self.hud = hud

		self.spawntime = 0

		self.itemspawnh = True
		self.itemspawn = True

		self.ttime = 0
		self.ctime = 0
		self.stopbug = 0.0

		self.create_player()

		self.bgm = pyglet.resource.media('sound/bgm.mp3')
		self.bgm.play()

		cell = 1.25 * 30
		self.collman = cm.CollisionManagerGrid(0, w, 0, h, cell, cell)
		self.schedule(self.update)

		from menu import get_HM, get_HMA
		GameLayer.HARDMODE = get_HM()
		GameLayer.HARDMODEACT = get_HMA()

		self.set_GN()
		self.initGN = GameLayer.GN
	
	def create_player(self):
		self.player = Player(self.width * 0.5, self.height * 0.5)
		self.add(self.player)

	def create_ghost(self, dt):
		self.time += dt
		rp = {
			0 : [self.width*0.5, self.height*0.05],
			 1 : [self.width*0.5, self.height*0.95],
			  2 : [self.width*0.05, self.height*0.5],
			   3 : [self.width*0.95, self.height*0.5]}
			   
		if GhostBoss.BOSSPAGE:
			self.spawntime = 1.5
		else:
			self.spawntime = 2.0
			
		if self.time >= self.spawntime:
			r = random.randint(0, 3)
			rg = random.choices([1, 2, 3], [0.5, 0.3, 0.2])
			if r == 0:
				if rg[0] == 1:
					GameLayer.ghost.append(Ghost1.make_ghost1(rp[r][0], rp[r][1]))
					self.add(GameLayer.ghost[-1])
				elif rg[0] == 2:
					GameLayer.ghost.append(Ghost2.make_ghost2(rp[r][0], rp[r][1]))
					self.add(GameLayer.ghost[-1])
				elif rg[0] == 3:
					GameLayer.ghost.append(Ghost3.make_ghost3(rp[r][0], rp[r][1]))
					self.add(GameLayer.ghost[-1])
			elif r == 1:
				if rg[0] == 1:
					GameLayer.ghost.append(Ghost1.make_ghost1(rp[r][0], rp[r][1]))
					self.add(GameLayer.ghost[-1])
				elif rg[0] == 2:
					GameLayer.ghost.append(Ghost2.make_ghost2(rp[r][0], rp[r][1]))
					self.add(GameLayer.ghost[-1])
				elif rg[0] == 3:
					GameLayer.ghost.append(Ghost3.make_ghost3(rp[r][0], rp[r][1]))
					self.add(GameLayer.ghost[-1])
			elif r == 2:
				if rg[0] == 1:
					GameLayer.ghost.append(Ghost1.make_ghost1(rp[r][0], rp[r][1]))
					self.add(GameLayer.ghost[-1])
				elif rg[0] == 2:
					GameLayer.ghost.append(Ghost2.make_ghost2(rp[r][0], rp[r][1]))
					self.add(GameLayer.ghost[-1])
				elif rg[0] == 3:
					GameLayer.ghost.append(Ghost3.make_ghost3(rp[r][0], rp[r][1]))
					self.add(GameLayer.ghost[-1])
			elif r == 3:
				if rg[0] == 1:
					GameLayer.ghost.append(Ghost1.make_ghost1(rp[r][0], rp[r][1]))
					self.add(GameLayer.ghost[-1])
				elif rg[0] == 2:
					GameLayer.ghost.append(Ghost2.make_ghost2(rp[r][0], rp[r][1]))
					self.add(GameLayer.ghost[-1])
				elif rg[0] == 3:
					GameLayer.ghost.append(Ghost3.make_ghost3(rp[r][0], rp[r][1]))
					self.add(GameLayer.ghost[-1])
			self.time = 0

	def create_item(self):
		randomx = random.randrange(self.width)
		randomy = random.randrange(self.height)
		while(self.width * 0.45 <= randomx <= self.width * 0.55):
			randomx = random.randrange(self.width)
		while(self.height * 0.45 <= randomy <= self.height * 0.55):
			randomy = random.randrange(self.height)
		randomi = random.randrange(3)
		if (randomi == 0):
			self.item = healthItem.makeheal(randomx, randomy)
			self.add(self.item)
		elif (randomi == 1):
			self.item = timeItem.maketime(randomx, randomy)
			self.add(self.item)
		elif (randomi == 2):
			self.item = cloneItem.makeclone(randomx, randomy)
			self.add(self.item)

	def healthitem(self):
		healthItem.HCHECK = False
		if Player.NUMBER == 1:
			self.clone1.kill()
			self.clone1 = None
		elif Player.NUMBER == 2:
			self.clone2.kill()
			self.clone2 = None
		elif Player.NUMBER == 3:
			self.clone3.kill()
			self.clone3 = None
		Player.NUMBER -= 1

	def timeitem(self, dt):
		if self.ttime == 0:
			for i in GameLayer.ghost:
				i.v = 0
		self.ttime += dt
		if self.ttime >= 3:
			timeItem.TCHECK = False
			self.ttime = 0
			for i in GameLayer.ghost:
				i.v = 120

	def cloneitem(self, dt):
		if Player.NUMBER > 0:
			if self.ctime == 0:
				PlayerClone.ACTIVE = True
			self.ctime += dt
			if self.ctime >= 2:
				cloneItem.CCHECK = False
				self.ctime = 0
				PlayerClone.ACTIVE = False
		else:
			cloneItem.CCHECK = False

	def update(self, dt):
		for _, node in self.children:
			node.update(dt)
		
		#유령 생성
		self.create_ghost(dt)
		
		#아이템 생성
		if GameLayer.GN - self.initGN/2 == 0 and self.itemspawnh:
			self.create_item()
			self.itemspawnh = False
		if GameLayer.GN == 0 and self.itemspawn:
			self.create_item()
			self.itemspawn = False

		#충돌 처리
		self.collman.clear()
		for _, node in self.children:
			self.collman.add(node)
			if not self.collman.knows(node):
				self.remove(node)
			self.collide(node)
		
		if self.collide(self.player) and self.delta == 0:
			self.delta += dt
		
		#하드 모드
		self.stopbug += dt
		if GameLayer.HARDMODEACT and self.delta == 0 and self.stopbug >= 3.0:
			Player.NUMBER += 1
			self.delta += dt
			GameLayer.HARDMODEACT = False

		#클론 생성
		if Player.NUMBER <= 4:
			if Player.NUMBER == 1 and self.delta >= 2.0:
				self.clone1 = PlayerClone(Player.PlayerPosition[0][0], Player.PlayerPosition[0][1])
				self.add(self.clone1)
			elif Player.NUMBER == 2 and self.delta >= 1.3:
				self.clone2 = PlayerClone(Player.PlayerPosition[int(len(Player.PlayerPosition)/3)-1][0], Player.PlayerPosition[int(len(Player.PlayerPosition)/3)-1][1])
				self.add(self.clone2)
			elif Player.NUMBER == 3 and self.delta >= 0.7:
				self.clone3 = PlayerClone(Player.PlayerPosition[int(len(Player.PlayerPosition)*2/3)-1][0], Player.PlayerPosition[int(len(Player.PlayerPosition)*2/3)-1][1])
				self.add(self.clone3)
			elif Player.NUMBER == 4:
				self.clone4 = PlayerClone(Player.Px, Player.Py)
				self.add(self.clone4)

		if 0 < self.delta <= 2:
			self.delta += dt
		elif self.delta > 2:
			self.delta = 0

		#아이템 동작
		if Player.NUMBER > 0 and healthItem.HCHECK:
			self.healthitem()
		if timeItem.TCHECK:
			self.timeitem(dt)
		if Player.NUMBER > 0 and cloneItem.CCHECK:
			self.cloneitem(dt)
		
		#게임 종료 동작
		if Player.lives == 0:
			self.gameover()
		
		#보스 페이즈 진입
		if GameLayer.GN <= 0 and GhostBoss.BOSSPAGE == False:
			GhostBoss.BOSSPAGE = True
			dl = Player.Px
			dr = self.width - Player.Px
			du = self.height - Player.Py
			dd = Player.Py
			m = min(dl, dr, du, dd)
			if m == dl:
				self.boss = GhostBoss.makeboss(0, Player.Py)
				self.add(self.boss)
			elif m == dr:
				self.boss = GhostBoss.makeboss(self.width, Player.Py)
				self.add(self.boss)
			elif m == du:
				self.boss = GhostBoss.makeboss(Player.Px, self.height - 120)
				self.add(self.boss)
			elif m == dd:
				self.boss = GhostBoss.makeboss(Player.Px, 0)
				self.add(self.boss)
			self.add(self.boss.hpbar)

		#게임 승리
		if GhostBoss.BOSSPAGE and self.boss.health == 0:
			self.gamewin()

		self.hud.gn_update()
		self.hud.hardmode_update()

	def collide(self, node):
		if node is not None:
			for other in self.collman.iter_colliding(node):
				node.collide(other)
				return True
		return False

	def gameover(self):
		self.unschedule(self.update)
		game_over = cocos.text.Label('Game Over', font_size=50,
									 anchor_x='center',
									 anchor_y='center')
		game_over.position = self.width * 0.5, self.height * 0.5
		self.add(game_over)
	
	def gamewin(self):
		self.unschedule(self.update)
		game_win = cocos.text.Label('You Win!', font_size=50,
									 anchor_x='center',
									 anchor_y='center')
		game_win.position = self.width * 0.5, self.height * 0.5
		self.add(game_win)

class HUD(cocos.layer.Layer):
	def __init__(self):
		super(HUD, self).__init__()
		w, h = cocos.director.director.get_window_size()
		self.gn = cocos.text.Label('', font_size = 15)
		self.gn.position = (20, h - 40)
		self.hardHUD = cocos.text.Label('', font_size = 30)
		self.hardHUD.position = (w*0.5-50, h*0.5)
		self.add(self.gn)
		self.add(self.hardHUD)

	def gn_update(self):
		if GameLayer.GN > 0:
			self.gn.element.text = 'Ghost: %s' % GameLayer.GN
		else:
			self.gn.element.text = 'Boss!'
	
	def hardmode_update(self):
		if GameLayer.HARDMODEACT:
			self.hardHUD.element.text = 'MOVE!'
		else:
			self.hardHUD.element.text = ''

def new_game():
	main_scene = cocos.scene.Scene()
	tmx_map = cocos.tiles.load('map/GHMap.tmx')
	bg0 = tmx_map['background']
	bg1 = tmx_map['background2']
	bg0.set_view(0, 0, bg0.px_width, bg0.px_height)
	bg1.set_view(0, 0, bg1.px_width, bg1.px_height)
	main_scene.add(bg0, z = 1)
	main_scene.add(bg1, z = 2)
	hud_layer = HUD()
	main_scene.add(hud_layer, z=4)
	game_layer = GameLayer(hud_layer)
	main_scene.add(game_layer, z=3)
	cocos.director.director.run(main_scene)