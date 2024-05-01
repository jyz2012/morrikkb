import pyglet as pgt
from perlin_noise import PerlinNoise
from random import randint,random,seed
from os.path import exists
from os import listdir,remove
from easygui import enterbox,msgbox
from time import time

class Block():
    def __init__(self,cid):
        self.id=cid
    def use(self):
        global iscrafting,istooling,curchoi
        if not iscrafting and not istooling:
            if self.id==7:
                iscrafting=True
                curchoi=0
            if self.id==10:
                istooling=True
                curchoi=0

class Item():
    def __init__(self,cid):
        self.id=cid
        self.cnt=0
        self.diglvl=0
        self.tid=0
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

class Tool():
    def __init__(self,ctid,cfirst,csecond):
        self.first=cfirst
        self.second=csecond
        self.tid=ctid
        self.id=12
        self.cnt=0
        self.canuse=0
        self.damage=0
        self.name=iname[cfirst]+' '+iname[csecond]+' '+tname[ctid]
        self.diglvl=0
        if self.first==9:
            self.diglvl=1
            self.canuse+=32
            self.damage=3
        elif self.first==10:
            self.diglvl=2
            self.canuse+=64
            self.damage=5
        elif self.first==16:
            self.diglvl=3
            self.canuse+=128
            self.damage=7
        elif self.first==25:
            self.canuse+=192
            self.diglvl=3
            self.damage=7
        elif self.first==28:
            self.canuse+=128
            self.diglvl=3
            self.damage=7
        if self.first==21:
            self.diglvl=1
            self.canuse+=32
        elif self.first==22:
            self.diglvl=2
            self.canuse+=64
            self.damage=3
        elif self.first==23:
            self.diglvl=3
            self.canuse+=128
            self.damage=4
        elif self.first==26:
            self.canuse+=192
            self.diglvl=3
            self.damage=6
        elif self.first==29:
            self.canuse+=128
            self.diglvl=3
            self.damage=6
        if self.second==15:
            self.canuse+=8
        elif self.second==30:
            self.canuse+=16
    def use(self,num):
        entities[0].backpack[entities[0].chosi][entities[0].chosj].canuse-=num
        if entities[0].backpack[entities[0].chosi][entities[0].chosj].canuse<=0:
            entities[0].backpack[entities[0].chosi][entities[0].chosj]=Item(0)

class Entity():
    def __init__(self,cx,cy,cxx,cyy,cid,cmxhe,cmxhu):
        self.x=cx
        self.y=cy
        self.xx=cxx
        self.yy=cyy
        self.id=cid
        self.jump=0
        self.ishurten=False
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
        self.ishurten=True
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
        self.lastleft=True
        self.flick=0
        for i in range(8):
            self.backpack.append([])
            for j in range(6):
                self.backpack[i].append(Item(0))
    def draw(self):
        if self.isleft or self.isright:
            sprite=pgt.sprite.Sprite(x=512,y=288,
                                   img=eimages[0][self.lastleft][self.flick%4])
        else:
            sprite=pgt.sprite.Sprite(x=512,y=288,
                                   img=eimages[0][self.lastleft][0])

        sprite.draw()
        self.flick+=1
        if self.ishurten:
            redr=pgt.shapes.Rectangle(x=512,
                                      y=288,
                                      width=32,height=64,
                                      color=(255,0,0,128))
            redr.draw()
            self.ishurten=False
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
                if self.backpack[i][j].id!=12:
                    ilist.append(pgt.sprite.Sprite(
                        x=924-i*34,y=512-j*34,
                        img=iimages[self.backpack[i][j].id],
                        batch=ibatch
                        ))
                else:
                    ilist.append(pgt.sprite.Sprite(
                        x=924-i*34,y=512-j*34,
                        img=iimages[self.backpack[i][j].first],
                        batch=ibatch
                        ))
                    ilist.append(pgt.sprite.Sprite(
                        x=924-i*34,y=512-j*34,
                        img=iimages[self.backpack[i][j].second],
                        batch=ibatch
                        ))
                if self.backpack[i][j].cnt!=0:
                    ilist.append(pgt.text.Label(str(self.backpack[i][j].cnt),
                              font_name='Times New Roman',
                              font_size=9,
                              x=892-(i-1)*34,y=512-j*34,
                              anchor_x='center',anchor_y='center',
                              batch=ibatch))
        if self.backpack[self.chosi][self.chosj].id!=12:
            ilist.append(pgt.text.Label(iname[self.backpack[self.chosi][self.chosj].id],
                              font_name='Times New Roman',
                              font_size=9,
                              x=896-2.5*34,y=500-5*34,
                              anchor_x='center',anchor_y='center',
                              batch=ibatch))
        else:
            ilist.append(pgt.text.Label(self.backpack[self.chosi][self.chosj].name,
                              font_name='Times New Roman',
                              font_size=9,
                              x=896-2.5*34,y=500-5*34,
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
                self.jump=0
        if self.moved>=960:
            self.hungrier(1)
            self.moved=0
        if self.hunger<=0 and self.moved>=160:
            self.heart-=1
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
    def baddt(self,tid,first,second):
        for i in range(8):
            for j in range(6):
                if self.backpack[i][j].id==0:
                    self.backpack[i][j]=Tool(tid,first,second)
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
        return fall[world[self.x+1][self.y-1].id] and \
               fall[world[self.x+1][self.y-2].id] and \
               fall[world[self.x+1][self.y-(self.yy==0)].id]
    def canright(self):
        return fall[world[self.x-(self.xx==0 and not self.jump>=0.95)][self.y-1].id] and \
               fall[world[self.x-(self.xx==0 and not self.jump>=0.95)][self.y-2].id] and \
               fall[world[self.x-(self.xx==0 and not self.jump>=0.95)][self.y-(self.yy==0)].id]
    def canjump(self):
        return fall[world[self.x][self.y-2].id] and \
               fall[world[self.x+1-(self.xx==0)][self.y-2].id]
    def falling(self):
        return fall[world[self.x][self.y].id] and \
               fall[world[self.x+1-(self.xx==0)][self.y].id]
    
class Dropped(Entity):
    def __init__(self,cx,cy,ciid):
        super().__init__(cx,cy,0,0,1,0,0)
        self.iid=ciid
        self.crtime=time()
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
        return (time()-self.crtime)>=2 and abs(entities[0].x-self.x)<=2 and abs(entities[0].y-self.y)<=2 and entities[0].badd(self.iid,1)
    def delled(self):
        return
    def getfreeze(self):
        return str(self.id)+' '+str(self.iid)+' '+str(self.x)+' '+str(self.y)

class DroppedTool(Dropped):
    def __init__(self,cx,cy,ctid,cfirst,csecond,ccanuse,cdamage):
        super().__init__(cx,cy,12)
        self.iid=3
        self.first=cfirst
        self.second=csecond
        self.tid=ctid
        self.canuse=ccanuse
        self.damage=cdamage
    def isdel(self):
        return (time()-self.crtime)>=2 and abs(entities[0].x-self.x)<=2 and abs(entities[0].y-self.y)<=2 and entities[0].baddt(self.tid,self.first,self.second,self.canuse,self.damage)
    def draw(self):
        sp=pgt.sprite.Sprite(
                    img=iimages[self.first],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy
                    )
        sp2=pgt.sprite.Sprite(
                    img=iimages[self.second],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy
                    )
        sp.draw()
        sp2.draw()
    def getfreeze(self):
        return str(self.tid)+' '+str(self.first)+' '+str(self.second)+' '+str(self.canuse)+' '+str(self.x)+' '+str(self.y)+' '+str(self.damage)

class Bird(Entity):
    def __init__(self,cx,cy):
        super().__init__(cx,cy,0,0,2,10,10)
        self.flick=0
        self.toward=int(random()*5-0.03)
        self.dtsum=0
    def draw(self):
        sp=pgt.sprite.Sprite(
                    img=eimages[2][self.flick],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy
                    )
        sp.draw()
        if self.ishurten:
            redr=pgt.shapes.Rectangle(x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                                      y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                                      width=32,height=32,
                                      color=(255,0,0,128))
            redr.draw()
            self.ishurten=False
        self.flick+=1
        self.flick%=5
    def canleft(self):
        return fall[world[self.x-1][self.y+1].id] and fall[world[self.x-1][self.y].id]
    def canright(self):
        return fall[world[self.x][self.y+1].id] and fall[world[self.x][self.y].id]
    def canup(self):
        return fall[world[self.x][self.y].id] and fall[world[self.x-1][self.y].id]
    def candown(self):
        return fall[world[self.x][self.y+1].id] and fall[world[self.x-1][self.y+1].id]
    def move(self,dxx,dyy):
        self.xx+=dxx
        self.yy+=dyy
        if self.xx>=32:
            self.xx-=32
            self.x-=1
        elif self.xx<0:
            self.xx+=32
            self.x+=1
        if self.yy>=32:
            self.yy-=32
            self.y+=1
        elif self.yy<0:
            self.yy+=32
            self.y-=1
    def update(self,dt):
        if self.toward==1:
            for i in range(int(64*dt)):
                if self.canleft():
                    self.move(1,0)
        elif self.toward==2:
            for i in range(int(64*dt)):
                if self.canright():
                    self.move(-1,0)
        elif self.toward==3:
            for i in range(int(64*dt)):
                if self.canup():
                  self.move(0,-1)
        elif self.toward==0:
            for i in range(int(64*dt)):
                if self.candown():
                    self.move(0,1)
        self.dtsum+=dt
        if self.dtsum>=7:
            self.toward=int(random()*5-0.03)
        if self.dtsum>=8:
            self.dtsum=0
    def isdel(self):
        return (abs(self.x-entities[0].x)>=128 or abs(self.y-entities[0].y)>=128) or self.heart<=0
    def delled(self):
        pass
    def getfreeze(self):
        return str(self.id)+' '+str(self.x)+' '+str(self.y)+' '+str(self.heart)

noise=PerlinNoise()
worldname='test.world'

def init():
    global ismainmenu,ischoosing,iscrafting,istooling,toolstep,isdead,curchoi,curchoi2,\
           cholist,chol,entities,world,width,height,worlds
    ismainmenu=True
    ischoosing=False
    iscrafting=False
    istooling=False
    toolstep=-1
    isdead=False
    curchoi=0
    curchoi2=0
    cholist=[]
    chol=[]
    entities=[Player()]
    world=[]
    width=1024
    height=256
    worlds=listdir('world/')
    worlds.insert(0,' ')
    worlds.insert(0,' ')
    worlds.append('创建一个新世界')
    worlds.append('删除一个世界')
    worlds.append(' ')
    worlds.append(' ')

window=pgt.window.Window(1024,576)
window.set_caption('Morrikk')
keys=pgt.window.key.KeyStateHandler()
window.push_handlers(keys)
fps_display=pgt.window.FPSDisplay(window=window)

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
timages=[]
eimages=[]
for i in range(15):
    images.append(pgt.image.load('imgs/blocks/'+str(i)+'.png'))
for i in range(31):
    iimages.append(pgt.image.load('imgs/items/'+str(i)+'.png'))
for i in range(3):
    timages.append(pgt.image.load('imgs/tooltypes/'+str(i)+'.png'))
eimages.append([[],[]])
for i in range(5):
    eimages[0][0].append(pgt.image.load('imgs/entities/0/right/'+str(i)+'.png'))
    eimages[0][1].append(pgt.image.load('imgs/entities/0/left/'+str(i)+'.png'))
eimages.append([])
eimages.append([])
for i in range(5):
    eimages[2].append(pgt.image.load('imgs/entities/2/'+str(i)+'.png'))

hconst=16
wconst=10
edgconst=1
fall=[True,False,False,False,True,True,False,False,False,
      True,False,True,True,False,False]
drop=[0,1,2,3,4,0,5,6,7,11,13,17,18,24,27]
put=[0,1,2,3,0,0,7,8,0,0,0,9,0,10,0,0,0,11,
     0,0,0,0,0,0,0,0,0]
diglvl=[0,0,1,0,0,0,2,0,0,0,1,0,1,3,3]
digtype=[0,0,1,0,0,0,1,0,0,0,1,0,2,1,1]
iname=[' ','泥土','石头','木头','苹果','铁锭','合成桩',
       '木板','镐头模板','木镐头','石镐头','小黄花',' ',
       '工具制作桩','握柄模板','木握柄','铁镐头','小石子',
       '棉花','线','锄头模板','木锄头头','石锄头头','铁锄头头',
       '银锭','银镐头','银锄头头','金锭','金镐头','金锄头头',
       '石握柄']
tname=[' ','镐子','锄头']
craftdict={2:((17,8),),6:((3,1),),7:((3,1),),8:((7,1),),9:((8,1),(3,1)),
           10:((8,1),(2,1)),13:((3,1),(2,1)),14:((7,1),),15:((14,1),(3,1)),
           16:((8,1),(5,1)),19:((18,1),),20:((7,1),),21:((20,1),(3,1)),
           22:((20,1),(2,1)),23:((20,1),(5,1)),25:((8,1),(24,1)),
           26:((20,1),(24,1)),28:((8,1),(27,1)),29:((20,1),(27,1)),
           30:((14,1),(2,1))}
cancraft=[0,0,2,7,19,6,13,8,9,10,16,25,28,20,21,22,23,
          26,29,14,15,30,0,0]
cancraftnum=[0,0,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,
             1,1,1,1,1,0,0]
tooltype=[0,0,1,2,0,0]
toolneed={1:(0,1),2:(2,1)}
toolitems={0:(9,10,16,25,28),1:(15,30),2:(21,22,23,26,29)}

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
            elif noise([i/4,j/4])>0.45:
                world[i].append(Block(13))
            elif noise([i/4,j/4])<-0.45:
                world[i].append(Block(14))
            else:
                world[i].append(Block(2))
        grandom=random()
        if grandom<0.2:
            world[i][dheight]=Block(9)
        elif grandom<0.4:
            world[i][dheight]=Block(11)
        elif grandom<0.5:
            world[i][dheight]=Block(12)
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
                if entities[0].backpack[i][j].id!=12:
                    f.write(str(entities[0].backpack[i][j].cnt)+' ')
                else:
                    f.write(str(entities[0].backpack[i][j].tid)+'^')
                    f.write(str(entities[0].backpack[i][j].first)+'^')
                    f.write(str(entities[0].backpack[i][j].second)+'^')
                    f.write(str(entities[0].backpack[i][j].canuse)+'^')
                    f.write(str(entities[0].backpack[i][j].damage)+' ')
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
                for i in range(len(curs)):
                    curs[i]=int(curs[i])
                if curs[0]==1:
                    entities.append(Dropped(curs[2],curs[3],curs[1]))
                elif curs[0]==2:
                    entities.append(Bird(curs[1],curs[2]))
                    entities[len(entities)-1].heart=curs[3]
                elif curs[0]==3:
                    entities.append(Dropped(curs[3],curs[4],curs[1],curs[2],curs[5]))
            for i in range(8):
                linee=f.readline().strip().split(' ')
                for j in range(6):
                    entities[0].backpack[i][j]=Item(int(linee[j*2]))
                    if int(linee[j*2])!=12:
                        entities[0].backpack[i][j].cnt=int(linee[j*2+1])
                    else:
                        curline=linee[j*2+1].strip().split('^')
                        entities[0].backpack[i][j]=Tool(
                            int(curline[0]),
                            int(curline[1]),
                            int(curline[2]))
                        entities[0].backpack[i][j].canuse=int(curline[3])
                        entities[0].backpack[i][j].damage=int(curline[4])
            for i in range(width):
                linee=f.readline().strip().split(' ')
                world.append([])
                for j in range(height):
                    world[i].append(Block(int(linee[j])))

@window.event
def on_key_press(symbol,modifiers):
    global iscrafting,curchoi,ismainmenu,ischoosing,worldname,worlds,isdead
    global istooling,toolstep,cholist,curchoi2,chol
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
                try:
                    seedd=int(enterbox('请输入这个世界的种子编号'))
                except ValueError:
                    msgbox('种子错误：种子编号必须为数字')
                else:
                    seed(seedd)
                    noise=PerlinNoise(seed=seedd)
                    worldgnr()
                    ischoosing=False
                    freeze(0)
                    ischoosing=True
                    msgbox('世界创建成功')
                    init()
            elif worldname=='删除一个世界':
                worldname=enterbox('请输入被删除的世界的名字')+'.world'
                if exists('world/'+worldname):
                    remove('world/'+worldname)
                    msgbox('世界删除成功')
                else:
                    msgbox('未找到世界：请确保世界名正确并且没有.world后缀')
                init()
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
        entities[0].lastleft=True
    if symbol==pgt.window.key.D:
        entities[0].isright=True
        entities[0].lastleft=False
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
        elif istooling==True:
            istooling=False
        elif toolstep>=0:
            pass
        else:
            freeze(0)
            ischoosing=True
            entities[0]=Player()
            worlds=listdir('world/')
            worlds.insert(0,' ')
            worlds.insert(0,' ')
            worlds.append('创建一个新世界')
            worlds.append('删除一个世界')
            worlds.append(' ')
            worlds.append(' ')
            curchoi=0
    if symbol==pgt.window.key.PAGEUP:
        if iscrafting==True or istooling==True:
            if curchoi>0:
                curchoi-=1
        if toolstep>=0:
            if curchoi2>0:
                curchoi2-=1
    if symbol==pgt.window.key.PAGEDOWN:
        if iscrafting==True:
            if curchoi<len(cancraft)-5:
                curchoi+=1
        elif istooling==True:
            if curchoi<len(tooltype)-5:
                curchoi+=1
        elif toolstep>=0:
            if curchoi2<len(cholist)-5:
                curchoi2+=1
    if symbol==pgt.window.key.ENTER:
        if iscrafting==True:
            cnt=0
            entities[0].badd(cancraft[curchoi+2],cancraftnum[curchoi+2])
            for i in craftdict[cancraft[curchoi+2]]:
                if not entities[0].bdel(i[0],i[1]):
                    for j in range(cnt-1):
                        entities[0].badd(craftdict[cancraft[curchoi+2]][j][0],craftdict[cancraft[curchoi+2]][j][1])
                    entities[0].bdel(cancraft[curchoi+2],cancraftnum[curchoi+2])
                    break
                cnt+=1
        if istooling==True:
            cholist=[0,0]
            chol=[]
            flag=False
            for i in range(8):
                for j in range(6):
                    if entities[0].backpack[i][j].id in toolitems[toolneed[tooltype[curchoi+2]][0]]:
                        cholist.append(entities[0].backpack[i][j].id)
            for k in range(len(toolneed[tooltype[curchoi+2]])):
                flag=False
                for i in range(8):
                    for j in range(6):
                        if entities[0].backpack[i][j].id in toolitems[toolneed[tooltype[curchoi+2]][k]]:
                            flag=True
                if flag==False:
                    break
            cholist.append(0)
            cholist.append(0)
            if flag==True:
                istooling=False
                toolstep=0
                curchoi2=0
        elif toolstep>=0:
            entities[0].bdel(cholist[curchoi2+2],1)
            chol.append(cholist[curchoi2+2])
            toolstep+=1
            if toolstep>=len(toolneed[tooltype[curchoi+2]]):
                toolstep=-1
                entities[0].baddt(tooltype[curchoi+2],chol[0],chol[1])
                istooling=True
            else:
                curchoi2=0
                cholist=[0,0,]
                for i in range(8):
                    for j in range(6):
                        if entities[0].backpack[i][j].id in toolitems[toolneed[tooltype[curchoi+2]][toolstep]]:
                            cholist.append(entities[0].backpack[i][j].id)
                cholist.append(0)
                cholist.append(0)
        else:
            for i in range(1,len(entities)):
                if abs(entities[i].x-entities[0].x)+abs(entities[i].y-entities[0].y)<=4:
                    if entities[0].backpack[entities[0].chosi][entities[0].chosj].id!=12:
                        entities[i].hurt(2)
                    else:
                        entities[i].hurt(entities[0].backpack[entities[0].chosi][entities[0].chosj].damage)
            
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
    if symbol==pgt.window.key.K:
        if not iscrafting and not istooling and not toolstep>=0:
            if entities[0].backpack[entities[0].chosi][entities[0].chosj].cnt>0:
                if entities[0].backpack[entities[0].chosi][entities[0].chosj].id!=12:
                    if modifiers & pgt.window.key.MOD_SHIFT:
                        cntt=entities[0].backpack[entities[0].chosi][entities[0].chosj].cnt
                        for i in range(cntt):
                            entities.append(Dropped(entities[0].x,entities[0].y-1,\
                                            entities[0].backpack[entities[0].chosi][entities[0].chosj].id))
                            entities[0].bdel(entities[0].backpack[entities[0].chosi][entities[0].chosj].id,1)
                    else:
                        entities[0].bdel(entities[0].backpack[entities[0].chosi][entities[0].chosj].id,1)
                        entities.append(Dropped(entities[0].x,entities[0].y-1,\
                                            entities[0].backpack[entities[0].chosi][entities[0].chosj].id))
            else:
                if entities[0].backpack[entities[0].chosi][entities[0].chosj].id==12:
                    entities[0].backpack[entities[0].chosi][entities[0].chosj].id=0
                    entities.append(DroppedTool(entities[0].x,entities[0].y-1,entities[0].backpack[entities[0].chosi][entities[0].chosj].tid,\
                                            entities[0].backpack[entities[0].chosi][entities[0].chosj].first,
                                            entities[0].backpack[entities[0].chosi][entities[0].chosj].second,
                                            entities[0].backpack[entities[0].chosi][entities[0].chosj].canuse,
                                            entities[0].backpack[entities[0].chosi][entities[0].chosj].damage))
            

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
    cury=wconst-int((y-entities[0].yy)/32)+entities[0].y-edgconst-1
    if button==pgt.window.mouse.LEFT and \
       abs(curx-entities[0].x)+abs(cury-entities[0].y)<=4 and \
       entities[0].backpack[entities[0].chosi][entities[0].chosj].diglvl>=diglvl[world[curx][cury].id] and \
       (digtype[world[curx][cury].id]==0 or entities[0].backpack[entities[0].chosi][entities[0].chosj].tid==digtype[world[curx][cury].id]):
        if drop[world[curx][cury].id]!=0:
            entities.append(Dropped(curx,cury,drop[world[curx][cury].id]))
            entities[0].moved+=1
            if entities[0].backpack[entities[0].chosi][entities[0].chosj].id==12:
                entities[0].backpack[entities[0].chosi][entities[0].chosj].use(1)
        world[curx][cury]=Block(0)
    if button==pgt.window.mouse.RIGHT and abs(curx-entities[0].x)+abs(cury-entities[0].y)<=4:
        if world[curx][cury].id==0:
            entities[0].bput(curx,cury)
            entities[0].moved+=1
        else:
            world[curx][cury].use()
            entities[0].moved+=0.5

@window.event
def on_draw():
    global curchoi,worlds,isdead
    
    window.clear()

    if ismainmenu==True:
        spr=pgt.sprite.Sprite(
            x=0,y=0,
            img=mainmenuimg)
        spr.draw()
        starttip=pgt.text.Label('点击任意处以开始',
                        font_name='Times New Roman',
                        font_size=24,
                        color=(0,0,0,255),
                        x=window.width//2,
                        y=window.height//4,
                        anchor_x='center', anchor_y='center')
        starttip.draw()
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
        if abs(i.x-entities[0].x)>=30 or abs(i.y-entities[0].y)>=30:
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
    if istooling==True:
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
                img=timages[tooltype[curchoi+i]],
                x=966,y=512-i*34,
                batch=guibatch))
        for i in range(len(toolneed[tooltype[curchoi+2]])):
            guisp.append(pgt.sprite.Sprite(
                    img=itembg,
                    x=992,y=504-i*34,
                    batch=guibatch))
            guisp.append(pgt.sprite.Sprite(
                img=iimages[toolitems[toolneed[tooltype[curchoi+2]][i]][0]],
                x=1000,y=512-i*34,
                batch=guibatch))
    if toolstep>=0:
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
                img=iimages[cholist[curchoi2+i]],
                x=966,y=512-i*34,
                batch=guibatch))
    guibatch.draw()

def update(dt):
    if ismainmenu or ischoosing or isdead:
        return
    dct=0
    if random()<0.02:
        if random()>0.5:
            newx=int(random()*32+32)+entities[0].x
        else:
            newx=int(random()*32+32)*-1+entities[0].x
        if random()>0.5:
            newy=int(random()*32+32)+entities[0].y-10
        else:
            newy=int(random()*32+32)*-1+entities[0].y-10
        if fall[world[newx][newy].id] and \
           newy<int(noise(newx/32)*28)+114:
            entities.append(Bird(newx,newy))
    for i in range(len(entities)):
        entities[i-dct].update(dt)
        if entities[i-dct].isdel():
            entities[i-dct].delled()
            entities.pop(i-dct)
            dct+=1

init()

pgt.clock.schedule_interval(update,1/40.)
pgt.clock.schedule_interval(freeze,10)
pgt.app.run()
