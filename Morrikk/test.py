import pyglet as pgt
from perlin_noise import PerlinNoise
from random import randint

class Block():
    def __init__(self,cid):
        self.id=cid

class Entity():
    def __init__(self,cx,cy,cxx,cyy,cid):
        self.x=cx
        self.y=cy
        self.xx=cxx
        self.yy=cyy
        self.id=cid
        self.jump=0
    def update(self,dt):
        if self.jump>0.95:
            self.move(0,-96*dt)
            self.jump+=96*dt
            if self.jump>49:
                self.jump=0
    def move(self,dxx,dyy):
        self.xx+=dxx
        self.yy+=dyy
        if self.xx>=32:
            self.xx-=32
            self.x+=1
        elif self.xx<0:
            self.xx+=32
            self.x-=1
        if self.yy>=32:
            self.yy-=32
            self.y+=1
        elif self.yy<0:
            self.yy+=32
            self.y-=1

class Player(Entity):
    def __init__(self):
        super().__init__(512,110,0,0,0)
        self.isleft=False
        self.isright=False
    def draw(self):
        sprite=pgt.sprite.Sprite(x=512,y=288,
                                   img=player1)
        sprite.draw()
    def update(self,dt):
        if fall[world[self.x][self.y].id] and fall[world[self.x+1][self.y].id] and not self.jump:
            self.move(0,64*dt)
            self.jump=0
        if self.isleft:
            self.move(64*dt,0)
        if self.isright:
            self.move(-64*dt,0)
        super().update(dt)

noise=PerlinNoise(seed=114514)

window=pgt.window.Window(1024,576)
window.set_caption('Morrikk')
keys=pgt.window.key.KeyStateHandler()
window.push_handlers(keys)

player1=pgt.image.load('Morrikk/imgs/player1.png')
images=[]
for i in range(3):
    images.append(pgt.image.load('Morrikk/imgs/'+str(i)+'.png'))

fall=[True,False,False]

entities=[Player()]

world=[]
width=1024
height=256

def worldgnr():
    global world
    world=[]
    for i in range(width):
        world.append([])
        dheight=int(noise(i/32)*28)+114
        dwidth=randint(3,6)
        for j in range(dheight):
            world[i].append(Block(0))
        for j in range(dheight,dheight+dwidth):
            world[i].append(Block(1))
        for j in range(dheight+dwidth,height):
            world[i].append(Block(2))

@window.event
def on_key_press(symbol,modifiers):
    if symbol==pgt.window.key.A:
        entities[0].isleft=True
    if symbol==pgt.window.key.D:
        entities[0].isright=True
    if symbol==pgt.window.key.SPACE and entities[0].jump<0.95:
        entities[0].jump=1
    print('dd')

@window.event
def on_key_release(symbol,modifiers):
    if symbol==pgt.window.key.A:
        entities[0].isleft=False
    if symbol==pgt.window.key.D:
        entities[0].isright=False

@window.event
def on_draw():
    window.clear()
    bg=pgt.shapes.Rectangle(
        x=0,y=0,width=1024,height=576,color=(128,255,255))
    bg.draw()

    blocksp=[]
    blbatch=pgt.graphics.Batch()
    for i in range(34):
        for j in range(22):
            blocksp.append(pgt.sprite.Sprite(
                img=images[world[i+entities[0].x-16][j+entities[0].y-10].id],
                x=1024-(i*32)+int(entities[0].xx),
                y=576-(j*32)+int(entities[0].yy),
                batch=blbatch))
    blbatch.draw()
    
    for i in entities:
        i.draw()

def update(dt):
    for i in entities:
        i.update(dt)

worldgnr()

pgt.clock.schedule_interval(update,1/40.)
pgt.app.run()
