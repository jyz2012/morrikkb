import pyglet as pgt
from perlin_noise import PerlinNoise
from random import randint,random,seed
from os.path import exists
from os import listdir,remove
from easygui import enterbox

class Block():
    def __init__(self,cid):
        self.id=cid
    def use(self):
        global iscrafting
        if self.id==7:
            iscrafting=True

class Item():
    def __init__(self,cid):
        self.id=cid
        self.cnt=0
    def use(self):
        if self.id==3:
            if entities[0].badd(6,1):
                self.cnt-=1
                if self.cnt==0:
                    self.id=0
        if self.id==4:
            entities[0].hungrier(-4)
            entities[0].hurt(-4)
            self.cnt-=1

class Entity():
    def __init__(self,cx,cy,cxx,cyy,cid,cmxhe,cmxhu):
        self.x=cx
        self.y=cy
        self.xx=cxx
        self.yy=cyy
        self.id=cid
        self.jump=0
        self.heart=self.mxheart=cmxhe
        self.hunger=self.mxhunger=cmxhu
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
    def hungrier(self,dx):
        self.hunger-=dx
        if self.hunger>self.mxhunger:
            self.hunger=self.mxhunger
    def hurt(self,dx):
        self.heart-=dx
        if self.heart>self.mxheart:
            self.heart=self.mxheart

class Player(Entity):
    def __init__(self):
        super().__init__(512,110,0,0,0,20,20)
        self.isleft=False
        self.isright=False
        self.backpack=[]
        self.chosi=0
        self.chosj=0
        self.lchosi=-1
        self.lchosj=-1
        self.fallen=0
        self.moved=0
        for i in range(8):
            self.backpack.append([])
            for j in range(6):
                self.backpack[i].append(Item(0))
    def draw(self):
        sprite=pgt.sprite.Sprite(x=512,y=288,
                                   img=player1)
        sprite.draw()
    def drawbp(self):
        ibatch=pgt.graphics.Batch()
        ilist=[]
        for i in range(8):
            for j in range(6):
                if i==self.chosi and j==self.chosj:
                    ilist.append(pgt.sprite.Sprite(
                        x=916-i*34,y=504-j*34,
                        img=chositembg,
                        batch=ibatch
                        ))
                elif i==self.lchosi and j==self.lchosj:
                    ilist.append(pgt.sprite.Sprite(
                        x=916-i*34,y=504-j*34,
                        img=chositembg_g,
                        batch=ibatch
                        ))
                else:
                    ilist.append(pgt.sprite.Sprite(
                        x=916-i*34,y=504-j*34,
                        img=itembg,
                        batch=ibatch
                        ))
                ilist.append(pgt.sprite.Sprite(
                    x=924-i*34,y=512-j*34,
                    img=iimages[self.backpack[i][j].id],
                    batch=ibatch
                    ))
                if self.backpack[i][j].cnt!=0:
                    ilist.append(pgt.text.Label(str(self.backpack[i][j].cnt),
                              font_name='Times New Roman',
                              font_size=9,
                              x=892-(i-1)*34,y=512-j*34,
                              anchor_x='center',anchor_y='center',
                              batch=ibatch))
        for i in range(self.heart//2):
            ilist.append(pgt.sprite.Sprite(
                        x=i*34,y=10,
                        img=heartimg,
                        batch=ibatch
                        ))
        if self.heart%2==1:
            ilist.append(pgt.sprite.Sprite(
                        x=(self.heart//2)*34,y=10,
                        img=halfheartimg,
                        batch=ibatch
                        ))
        for i in range(self.hunger//2):
            ilist.append(pgt.sprite.Sprite(
                        x=i*34,y=44,
                        img=hungerimg,
                        batch=ibatch
                        ))
        if self.hunger%2==1:
            ilist.append(pgt.sprite.Sprite(
                        x=(self.hunger//2)*34,y=44,
                        img=halfhungerimg,
                        batch=ibatch
                        ))
        ibatch.draw()
    def update(self,dt):
        global isdead
        if self.falling() and self.jump<0.95:
            for i in range(int(64*dt)):
                if self.falling() and self.jump<0.95:
                    self.move(0,1)
                    self.fallen+=1
        if not self.falling():
            if self.fallen>=128:
                self.hurt(self.fallen//32)
            if self.jump<-33330:
                self.fallen=0
        if self.isleft and self.canleft():
            for i in range(int(64*dt)):
                if self.isleft and self.canleft():
                    self.move(1,0)
                    self.moved+=1
        if self.isright and self.canright():
            for i in range(int(64*dt)):
                if self.isright and self.canright():
                    self.move(-1,0)
                    self.moved+=1
        if self.jump>0.95:
            for i in range(int(64*dt)):
                if self.canjump():
                    self.move(0,-1)
                    self.moved+=0.5
            self.jump+=96*dt
            if self.jump>64:
                self.jump=-33332
        if self.moved>=320:
            self.hungrier(1)
            self.moved=0
        if self.hunger<=0 and self.moved>=160:
            self.heart-=1
            self.moved=0
            self.moved=0
        if self.heart<=0:
            isdead=True
    def badd(self,iid,num):
        for i in range(8):
            for j in range(6):
                if self.backpack[i][j].id==iid:
                    self.backpack[i][j].cnt+=num
                    return True
        for i in range(8):
            for j in range(6):
                if self.backpack[i][j].id==0:
                    self.backpack[i][j]=Item(iid)
                    self.backpack[i][j].cnt+=num
                    return True
        return False
    def bput(self,curx,cury):
        if put[self.backpack[self.chosi][self.chosj].id]!=0:
            world[curx][cury]=Block(put[self.backpack[self.chosi][self.chosj].id])
            self.backpack[self.chosi][self.chosj].cnt-=1
            if(self.backpack[self.chosi][self.chosj].cnt==0):
                self.backpack[self.chosi][self.chosj]=Item(0)
    def buse(self):
        self.backpack[self.chosi][self.chosj].use()
    def bdel(self,iid,num):
        for i in range(8):
            for j in range(6):
                if self.backpack[i][j].id==iid and self.backpack[i][j].cnt>=num:
                    self.backpack[i][j].cnt-=num
                    if self.backpack[i][j].cnt==0:
                        self.backpack[i][j].id=0
                    return True
        return False
    def isdel(self):
        return False
    def delled(self):
        pass
    def canleft(self):
        return fall[world[self.x+1][self.y-1].id] and fall[world[self.x+1][self.y-2+bool(self.yy)*2].id]
    def canright(self):
        return fall[world[self.x][self.y-1].id] and fall[world[self.x][self.y-2+bool(self.yy)*2].id]
    def canjump(self):
        return fall[world[self.x][self.y-2].id]
    def falling(self):
        return fall[world[self.x][self.y].id] and fall[world[self.x+1-(not bool(self.xx))][self.y].id]
    
class Dropped(Entity):
    def __init__(self,cx,cy,ciid):
        super().__init__(cx,cy,0,0,1,0,0)
        self.iid=ciid
    def draw(self):
        sp=pgt.sprite.Sprite(
                    img=iimages[self.iid],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy
                    )
        sp.draw()
    def falling(self):
        return fall[world[self.x][self.y+1].id]
    def update(self,dt):
        if self.falling():
            self.move(0,64*dt)
    def isdel(self):
        return abs(entities[0].x-self.x)<2 and abs(entities[0].y-self.y)<2 and entities[0].badd(self.iid,1)
    def delled(self):
        return
    def getfreeze(self):
        return str(self.id)+' '+str(self.iid)+' '+str(self.x)+' '+str(self.y)

noise=PerlinNoise()
worldname='test.world'

ismainmenu=True
ischoosing=False
iscrafting=False
isdead=False
curchoi=0

window=pgt.window.Window(1024,576)
window.set_caption('Morrikk')
keys=pgt.window.key.KeyStateHandler()
window.push_handlers(keys)
fps_display=pgt.window.FPSDisplay(window=window)
worlds=listdir('world/')
worlds.insert(0,' ')
worlds.insert(0,' ')
worlds.append('创建一个新世界')
worlds.append('删除一个世界')
worlds.append(' ')
worlds.append(' ')
print(worlds)

player1=pgt.image.load('imgs/player1.png')
mainmenuimg=pgt.image.load('imgs/mainmenu.png')
itembg=pgt.image.load('imgs/items/itembg.png')
chositembg=pgt.image.load('imgs/items/chositembg.png')
chositembg_g=pgt.image.load('imgs/items/chositembg_g.png')
heartimg=pgt.image.load('imgs/heart.png')
halfheartimg=pgt.image.load('imgs/halfheart.png')
hungerimg=pgt.image.load('imgs/hunger.png')
halfhungerimg=pgt.image.load('imgs/halfhunger.png')
images=[]
iimages=[]
for i in range(10):
    images.append(pgt.image.load('imgs/blocks/'+str(i)+'.png'))
for i in range(12):
    iimages.append(pgt.image.load('imgs/items/'+str(i)+'.png'))

hconst=16
wconst=10
edgconst=1
fall=[True,False,False,False,True,True,False,False,False,True]
drop=[0,1,2,3,4,0,5,6,7,11]
put=[0,1,2,3,0,0,7,8,0,0,0,9]
iname=[]
craftdict={6:((3,1),),7:((3,1),),8:((7,1),),9:((8,1),(3,1)),
           10:((8,1),(2,1))}
cancraft=[0,0,6,7,8,9,10,0,0]
cancraftnum=[0,0,1,2,1,1,1,0,0]

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
            if noise([i/8,j/8])>0.3:
                world[i].append(Block(6))
            else:
                world[i].append(Block(2))
        if random()<0.2:
            world[i][dheight]=Block(9)
        else:
            world[i][dheight]=Block(5)
        if i>3 and random()<0.125:
            trheight=randint(4,6)
            exdheight=int(noise((i-1)/32)*28)+114
            world[i-1][exdheight-1]=world[i-1][exdheight]=Block(3)
            for j in range(exdheight-2,exdheight-trheight-1,-1):
                world[i-1][j]=Block(3)
                if random()>0.2:
                    world[i][j]=Block(4)
                if random()>0.2:
                    world[i-2][j]=Block(4)
            world[i-1][exdheight-trheight-1]=Block(4)

def freeze(dt):
    if ismainmenu or ischoosing:
        return
    with open('world/'+worldname,'w') as f:
        f.write(str(entities[0].x)+'\n')
        f.write(str(entities[0].y)+'\n')
        f.write(str(entities[0].heart)+'\n')
        f.write(str(entities[0].hunger)+'\n')
        f.write(str(len(entities)-1)+'\n')
        for i in range(1,len(entities)):
            f.write(entities[i].getfreeze())
            f.write('\n')
        for i in range(8):
            for j in range(6):
                f.write(str(entities[0].backpack[i][j].id)+' ')
                f.write(str(entities[0].backpack[i][j].cnt)+' ')
            f.write('\n')
        for i in range(width):
            for j in range(height):
                f.write(str(world[i][j].id)+' ')
            f.write('\n')

def readworld():
    if exists('world/'+worldname):
        with open('world/'+worldname,'r') as f:
            entities[0].x=int(f.readline().strip())
            entities[0].y=int(f.readline().strip())
            entities[0].heart=int(f.readline().strip())
            entities[0].hunger=int(f.readline().strip())
            enlen=int(f.readline().strip())
            for i in range(enlen):
                curs=f.readline()
                curs=curs.strip().split(' ')
                if curs[0]==1:
                    entities.append(Drop(curs[2],curs[3],curs[1]))
            for i in range(8):
                linee=f.readline().strip().split(' ')
                for j in range(6):
                    entities[0].backpack[i][j]=Item(int(linee[j*2]))
                    entities[0].backpack[i][j].cnt=int(linee[j*2+1])
            for i in range(width):
                linee=f.readline().strip().split(' ')
                world.append([])
                for j in range(height):
                    world[i].append(Block(int(linee[j])))

@window.event
def on_key_press(symbol,modifiers):
    global iscrafting,curchoi,ismainmenu,ischoosing,worldname,worlds,isdead
    if ischoosing:
        if symbol==pgt.window.key.PAGEDOWN:
            if curchoi>0:
                curchoi-=1
        if symbol==pgt.window.key.PAGEUP:
            if curchoi<len(worlds)-5:
                curchoi+=1
        if symbol==pgt.window.key.ENTER:
            worldname=worlds[curchoi+2]
            if worldname=='创建一个新世界':
                worldname=enterbox('请输入这个世界的名字')+'.world'
                seedd=int(enterbox('请输入这个世界的种子编号'))
                seed(seedd)
                noise=PerlinNoise(seed=seedd)
                worldgnr()
                ischoosing=False
            elif worldname=='删除一个世界':
                worldname=enterbox('请输入被删除的世界的名字')+'.world'
                if exists('world/'+worldname):
                    remove('world/'+worldname)
                worlds=listdir('world/')
                worlds.insert(0,' ')
                worlds.insert(0,' ')
                worlds.append('创建一个新世界')
                worlds.append('删除一个世界')
                worlds.append(' ')
                worlds.append(' ')
                curchoi=0
            else:
                readworld()
                ischoosing=False
        if symbol==pgt.window.key.BACKSPACE:
            ismainmenu=True
            ischoosing=False
    elif isdead==True:
        if symbol==pgt.window.key.ENTER:
            entities[0].heart=entities[0].mxheart
            entities[0].hunger=entities[0].mxhunger
            isdead=False
    if symbol==pgt.window.key.A:
        entities[0].isleft=True
    if symbol==pgt.window.key.D:
        entities[0].isright=True
    if symbol==pgt.window.key.SPACE and entities[0].jump<0.95 and not entities[0].falling():
        entities[0].jump=1
    if symbol==pgt.window.key.UP:
        entities[0].chosj-=1
        if entities[0].chosj<0:
            entities[0].chosj+=6
    if symbol==pgt.window.key.DOWN:
        entities[0].chosj+=1
        if entities[0].chosj>=6:
            entities[0].chosj-=6
    if symbol==pgt.window.key.LEFT:
        entities[0].chosi+=1
        if entities[0].chosi>=8:
            entities[0].chosi-=8
    if symbol==pgt.window.key.RIGHT:
        entities[0].chosi-=1
        if entities[0].chosi<0:
            entities[0].chosi+=8
    if symbol==pgt.window.key.G:
        entities[0].buse()
    if symbol==pgt.window.key.BACKSPACE:
        if iscrafting==True:
            iscrafting=False
        else:
            freeze(0)
            ischoosing=True
            entities[0]=Player()
    if symbol==pgt.window.key.PAGEUP:
        if iscrafting==True:
            if curchoi>0:
                curchoi-=1
    if symbol==pgt.window.key.PAGEDOWN:
        if iscrafting==True:
            if curchoi<len(cancraft)-5:
                curchoi+=1
    if symbol==pgt.window.key.ENTER:
        if iscrafting==True:
            cnt=0
            entities[0].badd(cancraft[curchoi+2],cancraftnum[curchoi+2])
            for i in craftdict[cancraft[curchoi+2]]:
                if not entities[0].bdel(i[0],i[1]):
                    for j in range(cnt-1):
                        entities[0].badd(i[0],i[1])
                    entities[0].bdel(cancraft[curchoi+2],cancraftnum[curchoi+2])
                    break
                cnt+=1
    if symbol==pgt.window.key.EQUAL:
        if entities[0].lchosi==-1:
            entities[0].lchosi=entities[0].chosi
            entities[0].lchosj=entities[0].chosj
        else:
            chosi=entities[0].chosi
            chosj=entities[0].chosj
            lchosi=entities[0].lchosi
            lchosj=entities[0].lchosj
            t=entities[0].backpack[chosi][chosj]
            entities[0].backpack[chosi][chosj]=entities[0].backpack[lchosi][lchosj]
            entities[0].backpack[lchosi][lchosj]=t
            entities[0].lchosi=-1
                        

@window.event
def on_key_release(symbol,modifiers):
    if ismainmenu or ischoosing:
        return
    if symbol==pgt.window.key.A:
        entities[0].isleft=False
    if symbol==pgt.window.key.D:
        entities[0].isright=False

@window.event
def on_mouse_press(x,y,button,modifiers):
    global ismainmenu,ischoosing,curchoi,isdead
    if ismainmenu==True:
        if button==pgt.window.mouse.LEFT:
            ismainmenu=False
            ischoosing=True
            curchoi=0
    if ischoosing==True or isdead==True:
        return
    curx=hconst-int((x-entities[0].xx)/32)+entities[0].x
    cury=wconst-y//32+entities[0].y-edgconst-1
    if button==pgt.window.mouse.LEFT and abs(curx-entities[0].x)+abs(cury-entities[0].y)<=4:
        if drop[world[curx][cury].id]!=0:
            entities.append(Dropped(curx,cury,drop[world[curx][cury].id]))
        world[curx][cury]=Block(0)
    if button==pgt.window.mouse.RIGHT and abs(curx-entities[0].x)+abs(cury-entities[0].y)<=4:
        if world[curx][cury].id==0:
            entities[0].bput(curx,cury)
        else:
            world[curx][cury].use()

@window.event
def on_draw():
    global curchoi,worlds,isdead
    
    window.clear()

    if ismainmenu==True:
        spr=pgt.sprite.Sprite(
            x=0,y=0,
            img=mainmenuimg)
        spr.draw()
        return

    if ischoosing:
        bg=pgt.shapes.Rectangle(
            x=0,y=0,width=1024,height=576,color=(128,255,255))
        bg.draw()
        for i in range(5):
            if i!=2:
                worldname=pgt.text.Label(worlds[curchoi+i],
                                          font_name='Times New Roman',
                                          font_size=24,
                                          color=(0,0,0,255),
                                          x=window.width//2,
                                          y=i*128,
                                          anchor_x='center', anchor_y='center')
            else:
                worldname=pgt.text.Label(worlds[curchoi+i],
                                          font_name='Times New Roman',
                                          font_size=24,
                                          color=(200,190,0,255),
                                          x=window.width//2,
                                          y=i*128,
                                          anchor_x='center', anchor_y='center')

            worldname.draw()
        return
    
    bg=pgt.shapes.Rectangle(
        x=0,y=0,width=1024,height=576,color=(128,255,255))
    bg.draw()
    fps_display.draw()

    blocksp=[]
    blbatch=pgt.graphics.Batch()
    for i in range(34):
        for j in range(22):
            blocksp.append(pgt.sprite.Sprite(
                img=images[world[i+entities[0].x-hconst][j+entities[0].y-wconst].id],
                x=1024-(i*32)+int(entities[0].xx),
                y=576-(j*32)+int(entities[0].yy),
                batch=blbatch))
    blbatch.draw()
    
    for i in entities:
        if isdead==True and i.id==0:
            continue
        i.draw()
    
    entities[0].drawbp()
    
    if isdead==True:
        redd=pgt.shapes.Rectangle(
            x=0,y=0,width=1024,height=576,color=(255,0,0,128))
        redd.draw()
        deadtxt=pgt.text.Label('你死了',
                                font_name='Times New Roman',
                                font_size=84,
                                color=(255,255,255,255),
                                x=window.width//2,
                                y=window.height//2+100,
                                anchor_x='center', anchor_y='center')
        deadtxt2=pgt.text.Label('点击Enter以复活',
                                font_name='Times New Roman',
                                font_size=24,
                                color=(255,255,255,255),
                                x=window.width//2,
                                y=window.height//4,
                                anchor_x='center', anchor_y='center')
        deadtxt.draw()
        deadtxt2.draw()
        return
    
    guibatch=pgt.graphics.Batch()
    guisp=[]
    if iscrafting:
        for i in range(5):
            if i!=2:
                guisp.append(pgt.sprite.Sprite(
                    img=itembg,
                    x=958,y=504-i*34,
                    batch=guibatch))
            else:
                guisp.append(pgt.sprite.Sprite(
                    img=chositembg,
                    x=958,y=504-i*34,
                    batch=guibatch))
            guisp.append(pgt.sprite.Sprite(
                img=iimages[cancraft[curchoi+i]],
                x=966,y=512-i*34,
                batch=guibatch))
        for i in range(len(craftdict[cancraft[curchoi+2]])):
            guisp.append(pgt.sprite.Sprite(
                    img=itembg,
                    x=992,y=504-i*34,
                    batch=guibatch))
            guisp.append(pgt.sprite.Sprite(
                img=iimages[craftdict[cancraft[curchoi+2]][i][0]],
                x=1000,y=512-i*34,
                batch=guibatch))
            guisp.append(pgt.text.Label(str(craftdict[cancraft[curchoi+2]][i][1]),
                              font_name='Times New Roman',
                              font_size=9,
                              x=1000,y=512-i*34,
                              anchor_x='center',anchor_y='center',
                              batch=guibatch))
            
    guibatch.draw()

def update(dt):
    if ismainmenu or ischoosing or isdead:
        return
    dct=0
    for i in range(len(entities)):
        entities[i-dct].update(dt)
        if entities[i-dct].isdel():
            entities[i-dct].delled()
            entities.pop(i-dct)
            dct+=1

pgt.clock.schedule_interval(update,1/40.)
pgt.clock.schedule_interval(freeze,10)
pgt.app.run()
