import pyglet as pgt
from perlin_noise import PerlinNoise
from random import randint,random,seed
from os.path import exists
from os import listdir,remove
from easygui import enterbox,msgbox
from time import time

class Block():
    def __init__(self,cid,x,y):
        global dheights
        self.id=cid
        if not self.id in (0,4,5,9,11,12,22,24,25,26,28,29,30,\
                           31,33,34,35,36,39,40,41,42,43,44,45):
            self.clight=light[self.id]
        else:
            if y<=dheights[x] and not isdark:
                self.clight=8
            else:
                self.clight=0
        self.light=self.clight
    def use(self,x,y):
        global iscrafting,istooling,curchoi,entities,lentities,dentities,\
               world,lworld,dworld,isdark
        if not iscrafting and not istooling:
            if self.id==7:
                iscrafting=True
                curchoi=0
            if self.id==10:
                istooling=True
                curchoi=0
        if entities[0].backpack[entities[0].chosi][entities[0].chosj].id==48:
            if self.id==38:
                entities[0].bdel(48,1)
                if not entities[0].badd(49,1):
                    entities.append(Dropped(entities[0].x,entities[0].y,49))
                self.id=0
                if y<=dheights[x]:
                    self.clight=8
                else:
                    self.clight=0
            elif self.id in (39,40,41,42,43,44,45):
                self.id=0
                if y<=dheights[x]:
                    self.clight=8
                else:
                    self.clight=0
        if self.id==47:
            if isdark==False:
                isdark=True
                lworld=list(world)
                world=list(dworld)
                lentities=list(entities)
                entities=list(dentities)
                if(len(entities)==0):
                    entities.append(lentities[0])
                else:
                    entities[0]=lentities[0]
            else:
                isdark=False
                dworld=list(world)
                world=list(lworld)
                dentities=list(entities)
                entities=list(lentities)
                if(len(entities)==0):
                    entities.append(dentities[0])
                else:
                    entities[0]=dentities[0]
            world[x][y]=Block(47,x,y)
    def update(self,x,y):
        self.light=self.clight
        if canlit[world[x+1][y].id] or world[x+1][y].clight>0:
            self.light=max(self.light,world[x+1][y].light-1)
        if canlit[world[x-1][y].id] or world[x+1][y].clight>0:
            self.light=max(self.light,world[x-1][y].light-1)
        if canlit[world[x][y+1].id] or world[x+1][y].clight>0:
            self.light=max(self.light,world[x][y+1].light-1)
        if canlit[world[x][y-1].id] or world[x+1][y].clight>0:
            self.light=max(self.light,world[x][y-1].light-1)
        if self.id==28:
            if random()<0.002:
                self.id=12
        elif self.id==29:
            if random()<0.001:
                trheight=randint(4,6)
                world[x][y]=Block(3,x,y)
                if world[x][y-1].id==0:
                    world[x][y-1]=Block(3,x,y-1)
                for j in range(y-2,y-trheight-1,-1):
                    if world[x][j].id==0:
                        world[x][j]=Block(3,x,j)
                    if random()>0.2 and world[x+1][j].id==0:
                        world[x+1][j]=Block(4,x+1,j)
                    if random()>0.2 and world[x-1][j].id==0:
                        world[x-1][j]=Block(4,x-1,j)
                if world[x-1][y-trheight-1].id==0:
                    world[x-1][y-trheight-1]=Block(4,x-1,y-trheight-1)
        elif self.id==30:
            if random()<0.001:
                trheight=randint(4,6)
                world[x][y]=Block(23,x,y)
                if world[x][y-1].id==0:
                    world[x][y-1]=Block(23,x,y-1)
                for j in range(y-2,y-trheight-1,-1):
                    if world[x][j].id==0:
                        world[x][j]=Block(23,x,j)
                    if random()>0.2 and world[x+1][j].id==0:
                        world[x+1][j]=Block(24,x+1,j)
                    if random()>0.2 and world[x-1][j].id==0:
                        world[x-1][j]=Block(24,x-1,j)
                if world[x-1][y-trheight-1].id==0:
                    world[x-1][y-trheight-1]=Block(24,x-1,y-trheight-1)
        elif self.id==33:
            if random()<0.001:
                trheight=randint(5,9)
                if world[x][y-1].id==0:
                    world[x][y-1]=Block(3,x,y-1)
                world[x][y]=Block(3,x,y-1)
                for j in range(y-2,y-trheight-1,-1):
                    if world[x][j].id==0:
                        world[x][j]=Block(32,x,j)
                    if random()>0.2 and world[x+1][j].id==0:
                        world[x+1][j]=Block(31,x+1,j)
                    if random()>0.2 and world[x-1][j].id==0:
                        world[x-1][j]=Block(31,x-1,j)
                if world[x][y-trheight-1].id==0:
                    world[x][y-trheight-1]=Block(31,x,y-trheight-1)
        elif self.id in (38,39,40,41,42,43,44,45):
            if world[x][y+1].id==0:
                world[x][y+1]=Block(self.id,x,y+1)
                self.id=0
                if y<=dheights[x] and not isdark:
                    self.clight=8
                else:
                    self.clight=0
            elif world[x][y+1].id in (39,40,41,42,43,44,45):
                curheight=(46-self.id)+(46-world[x][y+1].id)
                if curheight<=8:
                    world[x][y+1].id=46-curheight
                    self.id=0
                    if y<=dheights[x] and not isdark:
                        self.clight=8
                    else:
                        self.clight=0
                else:
                    world[x][y+1].id=38
                    self.id=46-(curheight-8)
            else:
                if world[x+1][y].id==0 and self.id<45:
                    curheight=46-self.id
                    world[x+1][y].id=46-(curheight//2)
                    self.id=46-(curheight//2+curheight%2)
                elif world[x+1][y].id in (38,39,40,41,42,43,44,45):
                    curheight=(46-self.id)+(46-world[x+1][y].id)
                    if curheight>1:
                        world[x+1][y].id=46-(curheight//2)
                        self.id=46-(curheight//2+curheight%2)
                if world[x-1][y].id==0 and self.id<45:
                    curheight=46-self.id
                    world[x-1][y].id=46-(curheight//2)
                    self.id=46-(curheight//2+curheight%2)
                elif world[x-1][y].id in (38,39,40,41,42,43,44,45):
                    curheight=(46-self.id)+(46-world[x-1][y].id)
                    if curheight>1:
                        world[x-1][y].id=46-(curheight//2)
                        self.id=46-(curheight//2+curheight%2)

class Item():
    def __init__(self,cid):
        self.id=cid
        self.cnt=0
        self.diglvl=0
        self.tid=0
        self.lastdmg=0
    def use(self):
        global respawnx,respawny,manao
        if self.id==3:
            if not entities[0].badd(6,1):
                entities.append(Dropped(entities[0].x,entities[0].y,6))
            self.cnt-=1
            if self.cnt==0:
                self.id=0
        elif self.id==4:
            entities[0].hungrier(-4)
            entities[0].hurt(-4)
            self.cnt-=1
            if self.cnt==0:
                self.id=0
        elif self.id==31:
            if entities[0].y>=196:
                entities.append(SonOTRocks(entities[0].x,entities[0].y-2))
                self.cnt-=1
                if self.cnt==0:
                    self.id=0
        elif self.id==42:
            respawnx=entities[0].x
            respawny=entities[0].y
            self.cnt-=1
            if self.cnt==0:
                self.id=0
        elif self.id==49:
            if world[entities[0].x][entities[0].y-1].id==0:
                world[entities[0].x][entities[0].y-1]=Block(38,entities[0].x,entities[0].y)
                self.cnt-=1
                if self.cnt==0:
                    self.id=0
                if not entities[0].badd(48,1):
                    entities.append(Dropped(entities[0].x,entities[0].y,48))
        elif self.id==50:
            chid=59
            summ=0
            for i in manao:
                if i:
                    summ+=1
                else:
                    summ+=8
            mrnd=random()
            curin=0
            for i in range(7):
                if not manao[i]:
                    curin+=8
                else:
                    curin+=1
                if mrnd<curin/summ:
                    chid=i+59
                    print(mrnd,curin)
                    break
            if not entities[0].badd(chid,1):
                entities.append(Dropped(entities[0].x,entities[0].y,chid))
            self.cnt-=1
            if self.cnt==0:
                self.id=0
        elif self.id==55:
            entities[0].hungrier(-7)
            entities[0].hurt(-6)
            self.cnt-=1
            if self.cnt==0:
                self.id=0
        elif self.id==58:
            entities[0].hurt(4)
            self.cnt-=1
            if self.cnt==0:
                self.id=0

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
        self.lastdmg=0
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
    def __init__(self,cx,cy,cxx,cyy,cid,cmxhe,cmxhu,cwidth,cheight):
        self.x=cx
        self.y=cy
        self.xx=cxx
        self.yy=cyy
        self.id=cid
        self.jump=0
        self.ishurten=False
        self.heart=self.mxheart=cmxhe
        self.hunger=self.mxhunger=cmxhu
        self.width=cwidth
        self.height=cheight
        enum[self.id]+=1
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
        if self.x<2:
            self.x+=1
        elif self.x>1022:
            self.x-=1
        if self.y<2:
            self.y+=1
        elif self.y>254:
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
    def dis(self,x,y):
        res=0
        if x<self.x:
            res+=self.x-x
        elif x>self.x+self.width:
            res+=x-self.x-self.width
        if y<self.y-self.height:
            res+=self.y-self.height-y
        elif y>self.y:
            res+=y-self.y
        return res

class Player(Entity):
    def __init__(self):
        super().__init__(512,110,0,0,0,20,20,1,2)
        self.isleft=False
        self.isright=False
        self.isclimbing=False
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
    def draw(self,batch):
        if self.isleft or self.isright:
            sprite=pgt.sprite.Sprite(x=512,y=288,
                                   img=eimages[0][self.lastleft][int(self.flick)%4],
                                     batch=batch)
        elif self.isclimbing:
            sprite=pgt.sprite.Sprite(x=512,y=288,
                                   img=eimages[0][2][0],
                                     batch=batch)
        else:
            sprite=pgt.sprite.Sprite(x=512,y=288,
                                   img=eimages[0][self.lastleft][0],
                                     batch=batch)

        sprite.draw()
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
                if time()-self.backpack[i][j].lastdmg<2:
                    ilist.append(pgt.sprite.Sprite(
                        x=916-i*34,y=504-j*34,
                        img=cooldownbg,
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
        if self.falling() and self.jump<0.95 and self.y<240 and \
           not (self.isclimbing and self.canclimb()):
            for i in range(int(64*((not self.inwater())*0.5+0.5)*dt)):
                if self.falling() and self.jump<0.95 and self.y<240:
                    self.move(0,1)
                    self.fallen+=1
        if not self.falling() or (self.isclimbing and self.canclimb()):
            if self.fallen>=128 and not (self.isclimbing and self.canclimb()):
                self.hurt(self.fallen//32)
            self.fallen=0
        if self.isclimbing:
            for i in range(int(48*((not self.inwater())*0.5+0.5)*dt)):
                if self.canclimb() and self.y>20:
                    self.move(0,-1)
                    self.moved+=1
        if self.isleft and self.canleft():
            for i in range(int(64*((not self.inwater())*0.5+0.5)*dt)):
                if self.x<1000 and self.canleft():
                    self.move(1,0)
                    self.moved+=1
        if self.isright and self.canright():
            for i in range(int(64*((not self.inwater())*0.5+0.5)*dt)):
                if self.x>20 and self.canright():
                    self.move(-1,0)
                    self.moved+=1
        if self.jump>0.95:
            for i in range(int(64*dt)):
                if self.canjump() and self.y>20:
                    self.move(0,-1)
                    self.moved+=0.5
            self.jump+=96*dt
            if self.jump>64:
                self.jump=0
        if world[self.x][self.y+1].id==17:
            world[self.x][self.y+1]=Block(0,self.x,self.y+1)
            entities.append(QueenOTClouds(self.x,self.y-2))
        if world[self.x+1-(self.xx==0)][self.y+1].id==17:
            world[self.x+1-(self.xx==0)][self.y+1]=Block(0,self.x+1-(self.xx==0),self.y+1)
            entities.append(QueenOTClouds(self.x,self.y-2))
        if world[self.x][self.y+1].id==18:
            world[self.x][self.y+1]=Block(0,self.x,self.y+1)
        if world[self.x+1-(self.xx==0)][self.y+1].id==18:
            world[self.x+1-(self.xx==0)][self.y+1]=Block(0,self.x+1-(self.xx==0),self.y+1)
        if self.moved>=960:
            self.hungrier(1)
            self.moved=0
        if self.hunger<=0 and self.moved>=160:
            self.heart-=1
            self.moved=0
        if self.heart<=0:
            isdead=True
        self.flick+=dt*8
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
    def baddt2(self,tid,first,second,canuse,damage):
        for i in range(8):
            for j in range(6):
                if self.backpack[i][j].id==0:
                    self.backpack[i][j]=Tool(tid,first,second)
                    self.backpack[i][j].canuse=canuse
                    self.backpack[i][j].damage=damage
                    return True
        return False
    def bput(self,curx,cury):
        if put[self.backpack[self.chosi][self.chosj].id]!=0:
            world[curx][cury]=Block(put[self.backpack[self.chosi][self.chosj].id],curx,cury)
            self.backpack[self.chosi][self.chosj].cnt-=1
            if(self.backpack[self.chosi][self.chosj].cnt==0):
                self.backpack[self.chosi][self.chosj]=Item(0)
    def buse(self):
        if self.backpack[self.chosi][self.chosj].id!=12:
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
               fall[world[self.x+1][self.y-2+(self.jump>0.95)].id] and \
               fall[world[self.x+1][self.y-(self.yy==0)].id]
    def canright(self):
        return fall[world[self.x-(self.xx==0)][self.y-1].id] and \
               fall[world[self.x-(self.xx==0)][self.y-2+(self.jump>0.95)].id] and \
               fall[world[self.x-(self.xx==0)][self.y-(self.yy==0)].id]
    def canjump(self):
        return fall[world[self.x][self.y-2-(self.yy==0)].id] and \
               fall[world[self.x+1-(self.xx==0)][self.y-2-(self.yy==0)].id]
    def falling(self):
        return fall[world[self.x][self.y].id] and \
               fall[world[self.x+1-(self.xx==0)][self.y].id]
    def canclimb(self):
        return (climb[world[self.x+1][self.y-1].id] or \
               climb[world[self.x+1][self.y-2].id] or \
               climb[world[self.x+1][self.y-(self.yy==0)].id] or \
               climb[world[self.x][self.y-1].id] or \
               climb[world[self.x][self.y-2].id] or \
               climb[world[self.x][self.y-(self.yy==0)].id]) and \
               self.canjump()
    def inwater(self):
        return world[self.x+1][self.y-1].id in (38,39,40,41,42,43,44,45) or \
               world[self.x+1][self.y-2].id in (38,39,40,41,42,43,44,45) or \
               world[self.x+1][self.y-(self.yy==0)].id in (38,39,40,41,42,43,44,45) or \
               world[self.x][self.y-1].id in (38,39,40,41,42,43,44,45) or \
               world[self.x][self.y-2].id in (38,39,40,41,42,43,44,45) or \
               world[self.x][self.y-(self.yy==0)].id in (38,39,40,41,42,43,44,45)
    def getfreeze(self):
        return str(self.id)
    
class Dropped(Entity):
    def __init__(self,cx,cy,ciid):
        super().__init__(cx,cy,0,0,1,0,0,1,1)
        self.iid=ciid
        self.crtime=time()
    def draw(self,batch):
        sp=pgt.sprite.Sprite(
                    img=iimages[self.iid],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                    batch=batch)
        sp.draw()
    def falling(self):
        return fall[world[self.x][self.y+1].id]
    def update(self,dt):
        if self.falling():
            self.move(0,64*dt)
    def isdel(self):
        return ((time()-self.crtime)>=2 and entities[0].dis(self.x,self.y)<=2 and entities[0].badd(self.iid,1)) or\
               time()-self.crtime>=120
    def delled(self):
        return
    def getfreeze(self):
        return str(self.id)+' '+str(self.iid)+' '+str(self.x)+' '+str(self.y)

class DroppedTool(Dropped):
    def __init__(self,cx,cy,ctid,cfirst,csecond,ccanuse,cdamage):
        super().__init__(cx,cy,12)
        self.id=3
        self.first=cfirst
        self.second=csecond
        self.tid=ctid
        self.canuse=ccanuse
        self.damage=cdamage
    def isdel(self):
        return (time()-self.crtime)>=2 and abs(entities[0].x-self.x)<=2 and abs(entities[0].y-self.y)<=2 and entities[0].baddt2(self.tid,self.first,self.second,self.canuse,self.damage)
    def draw(self,batch):
        sp=pgt.sprite.Sprite(
                    img=iimages[self.first],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                    batch=batch
                    )
        sp2=pgt.sprite.Sprite(
                    img=iimages[self.second],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                    batch=batch
                    )
        sp.draw()
        sp2.draw()
    def getfreeze(self):
        return str(self.id)+' '+str(self.tid)+' '+str(self.first)+' '+str(self.second)+' '+str(self.canuse)+' '+str(self.x)+' '+str(self.y)+' '+str(self.damage)

class Bird(Entity):
    def __init__(self,cx,cy):
        super().__init__(cx,cy,0,0,2,10,10,1,1)
        self.flick=0
        self.toward=int(random()*5-0.03)
        self.dtsum=0
    def draw(self,batch):
        sp=pgt.sprite.Sprite(
                    img=eimages[self.id][int(self.flick)%5],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                    batch=batch
                    )
        sp.draw()
        if self.ishurten:
            redr=pgt.shapes.Rectangle(x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                                      y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                                      width=32,height=32,
                                      color=(255,0,0,128))
            redr.draw()
            self.ishurten=False
    def canleft(self):
        return fall[world[self.x-1][self.y+1].id] and \
               fall[world[self.x-1][self.y].id]
    def canright(self):
        return fall[world[self.x][self.y+1].id] and \
               fall[world[self.x][self.y].id]
    def canup(self):
        return fall[world[self.x][self.y].id] and \
               fall[world[self.x-1][self.y].id]
    def candown(self):
        return fall[world[self.x][self.y+1].id] and \
               fall[world[self.x-1][self.y+1].id]
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
        self.flick+=dt*12
    def isdel(self):
        return entities[0].dis(self.x,self.y)>=128 or self.heart<=0
    def delled(self):
        entities.append(Dropped(self.x,self.y,51))
    def getfreeze(self):
        return str(self.id)+' '+str(self.x)+' '+str(self.y)+' '+str(self.heart)

class KingOTBirds(Entity):
    def __init__(self,cx,cy):
        super().__init__(cx,cy,0,0,4,250,20,1,1)
        self.flick=0
    def draw(self,batch):
        sp=pgt.sprite.Sprite(
                    img=eimages[4][int(self.flick)%5],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                    batch=batch
                    )
        sp.draw()
        if self.ishurten:
            redr=pgt.shapes.Rectangle(x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                                      y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                                      width=32,height=32,
                                      color=(255,0,0,128))
            redr.draw()
            self.ishurten=False
    def update(self,dt):
        if random()<0.1:
            tx=0
            ty=0
            if self.x<entities[0].x:
                tx=-1
            else:
                tx=1
            if self.y<entities[0].y:
                ty=1
            else:
                ty=-1
            entities.append(Fireball(self.x,self.y,tx,ty))
        if abs(self.x-entities[0].x)>=10:
            if self.x<entities[0].x:
                for i in range(int(64*dt)):
                    if self.canright():
                        self.move(-1,0)
            else:
                for i in range(int(64*dt)):
                    if self.canleft():
                        self.move(1,0)
        self.flick+=dt*12
    def canleft(self):
        return fall[world[self.x-1][self.y+1].id] and fall[world[self.x-1][self.y].id]
    def canright(self):
        return fall[world[self.x][self.y+1].id] and fall[world[self.x][self.y].id]
    def canup(self):
        return fall[world[self.x][self.y].id] and fall[world[self.x-1][self.y].id]
    def candown(self):
        return fall[world[self.x][self.y+1].id] and fall[world[self.x-1][self.y+1].id]
    def isdel(self):
        return self.heart<=0
    def delled(self):
        entities.append(Dropped(self.x,self.y,52))
    def getfreeze(self):
        return str(self.id)+' '+str(self.x)+' '+str(self.y)+' '+str(self.heart)

class AngryBird(Bird):
    def __init__(self,cx,cy):
        super().__init__(cx,cy)
        self.id=5
        enum[self.id]+=1
        enum[2]-=1
        self.lastdmg=0
    def update(self,dt):
        if self.x>entities[0].x+1:
            for i in range(int(64*dt)):
                self.move(1,0)
        elif self.x<=entities[0].x:
            for i in range(int(64*dt)):
                self.move(-1,0)
        if self.y>=entities[0].y:
            for i in range(int(64*dt)):
                self.move(0,-1)
        elif self.y<entities[0].y-1:
            for i in range(int(64*dt)):
                self.move(0,1)
        if entities[0].dis(self.x,self.y)<=1 and \
           time()-self.lastdmg>=(8+random()):
            entities[0].hurt(1)
            self.lastdmg=time()
        self.move(int(random()*2),int(random()*2))

class Shooted(Entity):
    def __init__(self,cx,cy,cid):
        super().__init__(cx,cy,0,0,cid,1,1,1,1)
    def canleft(self):
        return fall[world[self.x-1][self.y+1].id] and fall[world[self.x-1][self.y].id]
    def canright(self):
        return fall[world[self.x][self.y+1].id] and fall[world[self.x][self.y].id]
    def canup(self):
        return fall[world[self.x][self.y].id] and fall[world[self.x-1][self.y].id]
    def candown(self):
        return fall[world[self.x][self.y+1].id] and fall[world[self.x-1][self.y+1].id]

class Fireball(Shooted):
    def __init__(self,cx,cy,ctowardx,ctowardy):
        super().__init__(cx,cy,6)
        self.towardx=ctowardx
        self.towardy=ctowardy
        self.flick=0
        self.crtd=time()
        self.boomed=False
        self.boomed2=False
    def draw(self,batch):
        sp=pgt.sprite.Sprite(
                    img=eimages[6][int(self.flick)],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                    batch=batch
                    )
        if self.boomed:
            sp2=pgt.sprite.Sprite(
                    img=eimages[6][5],
                    x=(entities[0].x-self.x-2)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-3)*32+288+int(entities[0].yy)-self.yy,
                    batch=batch
                    )
            sp2.draw()
            self.boomed2=True
        else:
            sp.draw()
    def update(self,dt):
        if self.towardx<0:
            for i in range(int(64*abs(self.towardx)*dt)):
                    if self.canright():
                        self.move(-1,0)
        else:
            for i in range(int(64*self.towardx*dt)):
                    if self.canleft():
                        self.move(1,0)
        if self.towardy<0:
            for i in range(int(64*abs(self.towardy)*dt)):
                    if self.canup():
                        self.move(0,-1)
        else:
            for i in range(int(64*self.towardy*dt)):
                    if self.canright():
                        self.move(0,1)
        for i in entities:
            if i.dis(self.x,self.y)<=3 and i.id!=6 and i.id!=4 \
               and i.id!=3 and i.id!=1 and i.id!=7:
                self.boomed=True
        self.boomed=self.boomed or (self.towardx>0 and not self.canleft()) or \
               (self.towardx<0 and not self.canright()) or \
               (self.towardy>0 and not self.candown()) or \
               (self.towardy<0 and not self.canup())
        self.flick+=dt*12
    def isdel(self):
        return self.boomed2
    def delled(self):
        for i in entities:
            if i.dis(self.x,self.y)<=3 and i.id!=4 and i.id!=7:
                i.hurt(4)
        for i in range(-3,3):
            for j in range(-3,3):
                if drop[world[self.x+i][self.y+j].id]!=0 and \
                   diglvl[world[self.x+i][self.y+j].id]<=1 and random()<0.75:
                    entities.append(Dropped(self.x+i,self.y+j,
                                            drop[world[self.x+i][self.y+j].id]))
                    world[self.x+i][self.y+j]=Block(0,self.x+i,self.y+j)
    def getfreeze(self):
        return str(self.id)+' '+str(self.x)+' '+str(self.y)+' '+str(self.towardx)+' '+str(self.towardy)

class SonOTRocks(Entity):
    def __init__(self,cx,cy):
        super().__init__(cx,cy,0,0,7,180,1,2,2)
        self.toward=0
        self.lastupd=0
        self.attked=False
    def draw(self,batch):
        sp=pgt.sprite.Sprite(
                    img=eimages[7][0],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                    batch=batch
                    )
        sp.draw()
        if self.ishurten:
            redr=pgt.shapes.Rectangle(x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                                      y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                                      width=32,height=32,
                                      color=(255,0,0,128))
            redr.draw()
            self.ishurten=False
    def update(self,dt):
        if time()-self.lastupd>=1:
            if time()-self.lastupd>=1.5:
                self.lastupd=time()
                self.toward=0
                if self.x>entities[0].x:
                    self.toward+=1
                if self.y<entities[0].y:
                    self.toward+=2
                self.attked=False
            else:
                if random()<0.125:
                    tx=0
                    ty=0
                    if self.x<entities[0].x:
                        tx=-1
                    else:
                        tx=1
                    if self.y<entities[0].y:
                        ty=1
                    else:
                        ty=-1
                    entities.append(Fireball(self.x,self.y,tx,ty))
        if self.toward%2==0:
            for i in range(int(64*dt)):
                self.move(-1,0)
        else:
            for i in range(int(64*dt)):
                self.move(1,0)
        if self.toward/2>0.75:
            for i in range(int(64*dt)):
                self.move(0,1)
        else:
            for i in range(int(64*dt)):
                self.move(0,-1)
        if entities[0].dis(self.x,self.y)<=1 and not self.attked:
            entities[0].hurt(3)
            self.attked=True
    def canleft(self):
        return (fall[world[self.x-1][self.y+1].id] or world[self.x-1][self.y+1].id==2) and \
               (fall[world[self.x-1][self.y].id] or world[self.x-1][self.y].id==2)
    def canright(self):
        return (fall[world[self.x][self.y+1].id] or world[self.x][self.y+1].id==2) and \
               (fall[world[self.x][self.y].id] or world[self.x][self.y].id==2)
    def canup(self):
        return (fall[world[self.x][self.y].id] or world[self.x][self.y].id==2) and \
               (fall[world[self.x-1][self.y].id] or world[self.x-1][self.y].id==2)
    def candown(self):
        return (fall[world[self.x][self.y+1].id] or world[self.x][self.y+1].id==2) and \
               (fall[world[self.x-1][self.y+1].id] or world[self.x-1][self.y+1].id==2)
    def isdel(self):
        return self.heart<=0
    def delled(self):
        entities.append(Dropped(self.x,self.y,53))
    def getfreeze(self):
        return str(self.id)+' '+str(self.x)+' '+str(self.y)+' '+str(self.heart)

class QueenOTClouds(Entity):
    def __init__(self,cx,cy):
        super().__init__(cx,cy,0,0,8,200,10,2,1)
        self.hurttime=0
    def draw(self,batch):
        sp=pgt.sprite.Sprite(
                    img=eimages[8][0],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                    batch=batch
                    )
        sp.draw()
        if self.ishurten:
            redr=pgt.shapes.Rectangle(x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                                      y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                                      width=64,height=32,
                                      color=(255,0,0,128))
            redr.draw()
            self.ishurten=False
        if entities[0].dis(self.x,self.y)<=0:
            sp2=pgt.sprite.Sprite(
                img=eimages[8][1],
                x=0,
                y=0,
                batch=batch)
            sp2.draw()
    def update(self,dt):
        if not entities[0].dis(self.x,self.y)<=0:
            if self.x>entities[0].x:
                self.move(int(dt*48),0)
            elif self.x<entities[0].x:
                self.move(0-int(dt*48),0)
            if self.y<entities[0].y-1:
                self.move(0,int(dt*48))
            elif self.y>=entities[0].y:
                self.move(0,0-int(dt*48))
        else:
            if time()-self.hurttime>=0.5:
                entities[0].hurt(1)
                self.hurttime=time()
    def isdel(self):
        return self.heart<=0
    def delled(self):
        entities.append(Dropped(self.x,self.y,54))
    def getfreeze(self):
        return str(self.id)+' '+str(self.x)+' '+str(self.y)+' '+str(self.heart)

class Pig(Entity):
    def __init__(self,cx,cy):
        super().__init__(cx,cy,0,0,9,20,20,2,1)
        self.flick=0
        self.isleft=False
        self.fallen=0
    def draw(self,batch):
        sp=pgt.sprite.Sprite(
                    img=eimages[9][self.isleft][int(self.flick)%4],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                    batch=batch
                    )
        sp.draw()
        if self.ishurten:
            redr=pgt.shapes.Rectangle(x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                                      y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                                      width=64,height=32,
                                      color=(255,0,0,128))
            redr.draw()
            self.ishurten=False
    def update(self,dt):
        self.flick+=dt*8
        if self.isfall():
            for i in range(int(64*dt)):
                if self.isfall():
                    self.move(0,1)
                    self.fallen+=1
            return
        if self.fallen>=128:
            self.hurt(self.fallen//24)
            self.fallen=0
        if self.isleft:
            for i in range(int(56*dt)):
                if self.canright():
                    self.move(1,0)
        else:
            for i in range(int(56*dt)):
                if self.canleft():
                    self.move(-1,0)
        if random()<0.01:
            self.isleft=not self.isleft
    def isfall(self):
        return fall[world[self.x][self.y+1].id] and \
               fall[world[self.x-1][self.y+1].id] and \
               fall[world[self.x-2+(self.xx==0)][self.y+1].id]
    def canleft(self):
        return fall[world[self.x][self.y-1+(self.yy==0)].id] and \
               fall[world[self.x][self.y].id]
    def canright(self):
        return fall[world[self.x-1-(self.xx==0)][self.y-1+(self.yy==0)].id] and \
               fall[world[self.x-1-(self.xx==0)][self.y].id]
    def canup(self):
        return fall[world[self.x][self.y].id] and \
               fall[world[self.x-1][self.y].id] and \
               fall[world[self.x-2+(self.xx==0)][self.y].id]
    def isdel(self):
        return self.heart<=0 or entities[0].dis(self.x,self.y)>=128
    def delled(self):
        entities.append(Dropped(self.x,self.y,55))
    def getfreeze(self):
        return str(self.id)+' '+str(self.x)+' '+str(self.y)+' '+str(self.heart)

class Zombie(Entity):
    def __init__(self,cx,cy):
        super().__init__(cx,cy,0,0,10,15,-1,1,2)
        self.flick=0
        self.lastleft=True
        self.lastdmg=0
    def draw(self,batch):
        sp=pgt.sprite.Sprite(
                    img=eimages[0][self.lastleft][int(self.flick)%5],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                    batch=batch
                    )
        sp.draw()
        sp2=pgt.sprite.Sprite(
                    img=eimages[10][self.lastleft],
                    x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                    y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                    batch=batch
                    )
        sp2.draw()
        if self.ishurten:
            redr=pgt.shapes.Rectangle(x=(entities[0].x-self.x)*32+512+int(entities[0].xx)+self.xx,
                                      y=(entities[0].y-self.y-1)*32+288+int(entities[0].yy)-self.yy,
                                      width=32,height=64,
                                      color=(255,0,0,128))
            redr.draw()
            self.ishurten=False
    def update(self,dt):
        self.flick+=dt*6
        if entities[0].dis(self.x,self.y)>0:
            if self.x<entities[0].x:
                for i in range(int(dt*56)):
                    if self.canleft():
                        self.move(-1,0)
                    else:
                        if drop[world[self.x+1][self.y-1].id]!=56:
                            if drop[world[self.x+1][self.y-1].id] not in (0,56):
                                entities.append(Dropped(self.x+1,self.y-1,drop[world[self.x+1][self.y-1].id]))
                            world[self.x+1][self.y-1]=Block(0,self.x+1,self.y-1)
                        if drop[self.x+1][self.y-2+(self.yy==0)]!=56:
                            if drop[world[self.x+1][self.y-2+(self.yy==0)].id] not in (0,56):
                                entities.append(Dropped(self.x+1,self.y-2+(self.yy==0),drop[world[self.x+1][self.y-2+(self.yy==0)].id]))
                            world[self.x+1][self.y-2+(self.yy==0)]=Block(0,self.x+1,self.y-2+(self.yy==0))
                        if drop[world[self.x+1][self.y].id]!=56:
                            if drop[world[self.x+1][self.y].id] not in (0,56):
                                entities.append(Dropped(self.x+1,self.y,drop[world[self.x+1][self.y].id]))
                            world[self.x+1][self.y]=Block(0,self.x+1,self.y)
                self.lastleft=True
            else:
                for i in range(int(dt*56)):
                    if self.canright():
                        self.move(1,0)
                    else:
                        if drop[world[self.x-(self.xx==0)][self.y-1].id]!=56:
                            if drop[world[self.x-(self.xx==0)][self.y-1].id] not in (0,56):
                                entities.append(Dropped(self.x-(self.xx==0),self.y-1,drop[world[self.x-(self.xx==0)][self.y-1].id]))
                            world[self.x-(self.xx==0)][self.y-1]=Block(0,self.x-(self.xx==0),self.y-1)
                        if drop[world[self.x-(self.xx==0)][self.y-2+(self.yy==0)].id]!=56:
                            if drop[world[self.x-(self.xx==0)][self.y-2+(self.yy==0)].id] not in (0,56):
                                entities.append(Dropped(self.x-(self.xx==0),self.y-2+(self.yy==0),drop[world[self.x-(self.xx==0)][self.y-2+(self.yy==0)].id]))
                            world[self.x-(self.xx==0)][self.y-2+(self.yy==0)]=Block(0,self.x-(self.xx==0),self.y-2+(self.yy==0))
                        if drop[world[self.x-(self.xx==0)][self.y].id]!=56:
                            if drop[world[self.x-(self.xx==0)][self.y].id] not in (0,56):
                                entities.append(Dropped(self.x-(self.xx==0),self.y,drop[world[self.x-(self.xx==0)][self.y].id]))
                            world[self.x-(self.xx==0)][self.y]=Block(0,self.x-(self.xx==0),self.y)
                self.lastleft=False
        if self.y<entities[0].y-1:
            if drop[world[self.x][self.y+1].id] not in (0,56):
                entities.append(Dropped(self.x,self.y+1,drop[world[self.x][self.y+1].id]))
            world[self.x][self.y+1]=Block(0,self.x,self.y+1)
            if drop[world[self.x+1-(self.xx==0)][self.y+1].id] not in (0,56):
                entities.append(Dropped(self.x+1-(self.xx==0),self.y+1,drop[world[self.x+1-(self.xx==0)][self.y+1].id]))
            world[self.x+1-(self.xx==0)][self.y+1]=Block(0,self.x+1-(self.xx==0),self.y+1)
        if self.falling():
            for i in range(int(dt*64)):
                if self.falling():
                    self.move(0,1)
        if entities[0].dis(self.x,self.y)<1 and time()-self.lastdmg>2:
            entities[0].hurt(4)
            self.lastdmg=time()
    def canleft(self):
        return fall[world[self.x+1][self.y-1].id] and \
               fall[world[self.x+1][self.y-2+(self.yy==0)].id] and \
               fall[world[self.x+1][self.y].id]
    def canright(self):
        return fall[world[self.x-(self.xx==0)][self.y-1].id] and \
               fall[world[self.x-(self.xx==0)][self.y-2+(self.yy==0)].id] and \
               fall[world[self.x-(self.xx==0)][self.y].id]
    def canjump(self):
        return fall[world[self.x][self.y-2-(self.yy==0)].id] and \
               fall[world[self.x+1-(self.xx==0)][self.y-2-(self.yy==0)].id]
    def falling(self):
        return fall[world[self.x][self.y+1].id] and \
               fall[world[self.x+1-(self.xx==0)][self.y+1].id]
    def canclimb(self):
        return (climb[world[self.x+1][self.y-1].id] or \
               climb[world[self.x+1][self.y-2].id] or \
               climb[world[self.x+1][self.y-(self.yy==0)].id] or \
               climb[world[self.x][self.y-1].id] or \
               climb[world[self.x][self.y-2].id] or \
               climb[world[self.x][self.y-(self.yy==0)].id]) and \
               self.canjump()
    def isdel(self):
        return self.heart<=0
    def delled(self):
        entities.append(Dropped(self.x,self.y,58))
    def getfreeze(self):
        return str(self.id)+' '+str(self.x)+' '+str(self.y)+' '+str(self.heart)

noise=PerlinNoise()
worldname='test.world'

def init():
    global ismainmenu,ischoosing,iscrafting,istooling,toolstep,isdead,curchoi,curchoi2,\
           cholist,chol,entities,enum,world,width,height,worlds,chopped,needkotb,\
           dheights,biomes,respawnx,respawny,lworld,dworld,lentities,dentities,\
           isdark,freezing,manao
    ismainmenu=True
    ischoosing=False
    iscrafting=False
    istooling=False
    toolstep=-1
    freezing=False
    isdead=False
    curchoi=0
    curchoi2=0
    cholist=[]
    chol=[]
    chopped=0
    manao=[False,False,False,False,False,False,False]
    respawnx=512
    respawny=110
    needkotb=False
    enum=[]
    for i in range(11):
        enum.append(0)
    entities=[Player()]
    lentities=list(entities)
    dentities=list(entities)
    world=[]
    lworld=[]
    dworld=[]
    isdark=False
    dheights=[]
    biomes=[]
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
window.set_icon(pgt.image.load('imgs/blocks/9.png'))

mainmenuimg=pgt.image.load('imgs/mainmenu.png')
itembg=pgt.image.load('imgs/items/itembg.png')
chositembg=pgt.image.load('imgs/items/chositembg.png')
chositembg_g=pgt.image.load('imgs/items/chositembg_g.png')
cooldownbg=pgt.image.load('imgs/items/cooldownbg.png')
heartimg=pgt.image.load('imgs/heart.png')
halfheartimg=pgt.image.load('imgs/halfheart.png')
hungerimg=pgt.image.load('imgs/hunger.png')
halfhungerimg=pgt.image.load('imgs/halfhunger.png')
images=[]
iimages=[]
timages=[]
eimages=[]
limages=[]
for i in range(49):
    images.append(pgt.image.load('imgs/blocks/'+str(i)+'.png'))
for i in range(68):
    iimages.append(pgt.image.load('imgs/items/'+str(i)+'.png'))
for i in range(3):
    timages.append(pgt.image.load('imgs/tooltypes/'+str(i)+'.png'))
eimages.append([[],[],[]])
for i in range(5):
    eimages[0][0].append(pgt.image.load('imgs/entities/0/right/'+str(i)+'.png'))
    eimages[0][1].append(pgt.image.load('imgs/entities/0/left/'+str(i)+'.png'))
eimages[0][2].append(pgt.image.load('imgs/entities/0/climb/0.png'))
eimages.append([])
eimages.append([])
for i in range(5):
    eimages[2].append(pgt.image.load('imgs/entities/2/'+str(i)+'.png'))
eimages.append([])
eimages.append([])
for i in range(5):
    eimages[4].append(pgt.image.load('imgs/entities/4/'+str(i)+'.png'))
eimages.append([])
for i in range(5):
    eimages[5].append(pgt.image.load('imgs/entities/5/'+str(i)+'.png'))
eimages.append([])
for i in range(6):
    eimages[6].append(pgt.image.load('imgs/entities/6/'+str(i)+'.png'))
eimages.append([])
for i in range(1):
    eimages[7].append(pgt.image.load('imgs/entities/7/'+str(i)+'.png'))
eimages.append([])
for i in range(2):
    eimages[8].append(pgt.image.load('imgs/entities/8/'+str(i)+'.png'))
eimages.append([[],[]])
for i in range(4):
    eimages[9][0].append(pgt.image.load('imgs/entities/9/l/'+str(i)+'.png'))
    eimages[9][1].append(pgt.image.load('imgs/entities/9/r/'+str(i)+'.png'))
eimages.append([])
eimages[10].append(pgt.image.load('imgs/entities/10/l.png'))
eimages[10].append(pgt.image.load('imgs/entities/10/r.png'))
for i in range(9):
    limages.append(pgt.image.load('imgs/light/'+str(i)+'.png'))

hconst=16
wconst=10
edgconst=1
fall=[True,False,False,True,True,True,False,True,False,
      True,True,True,True,False,False,True,False,False,False,
      True,False,True,True,True,True,True,True,False,True,
      True,True,True,True,True,True,True,True,False,True,
      True,True,True,True,True,True,True,False,True,True]
climb=[False,False,False,True,False,False,False,False,False,
       False,False,False,False,False,False,False,False,
       False,False,False,False,False,False,True,False,
       False,False,False,False,True,True,False,True,
       True,False,False,False,False,True,False,False,False,
       False,False,False,False,False,False,True]
drop=[0,1,2,3,4,0,5,6,7,11,13,17,18,24,27,32,33,0,0,34,
      36,37,0,3,38,39,40,41,0,0,0,44,3,0,45,46,47,0,0,
      0,0,0,0,0,0,0,50,56,57]
light=[8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,8,0,0,0,
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
       0]
canlit=[True,False,False,False,True,True,False,False,False,
        True,False,True,True,False,False,True,True,False,False,
        True,False,False,True,False,True,True,True,True,True,
        True,True,True,True,True,True,True,True,True,True,
        True,True,True,True,True,True,True,True,False,False,
        True]
put=[0,1,2,3,29,0,7,8,0,0,0,9,0,10,0,0,0,11,
     0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,16,19,0,20,21,
     30,25,26,27,0,28,33,34,35,36,0,0,0,0,0,0,0,0,47,
     48,0,0,0,0,0,0,0,0,0,0]
diglvl=[0,0,1,0,0,0,2,0,0,0,1,0,1,3,3,0,0,10000,10000,0,0,2,#雪块(line.2,col.6)：铲子
        0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,1,10000,10000,10000,10000
        ,10000,10000,10000,10000,3,10000,0]
digtype=[0,0,1,0,0,0,1,0,0,0,1,0,2,1,1,0,0,1,1,0,0,2,
         0,0,0,0,0,0,2,2,2,0,0,2,0,0,0,1,1,1,1,1,1,1,1,1,
         1,0,0]
iname=[' ','泥土','石头','木头','苹果','铁锭','合成桩',
       '木板','镐头模板','木镐头','石镐头','小黄花',' ',
       '工具制作桩','握柄模板','木握柄','铁镐头','小石子',
       '棉花','线','锄头模板','木锄头头','石锄头头','铁锄头头',
       '银锭','银镐头','银锄头头','金锭','金镐头','金锄头头',
       '石握柄','岩石之心','松散的云','云','火把','布',
       '沙子','仙人掌','松果','雪球','蕨','雪块','铁苹果',
       '棉花种子','可可','粉色郁金香','橘黄郁金香','玫瑰',
       '空木桶','水桶','未打磨的玛瑙','羽毛','彩虹羽毛',
       '岩石雕塑','云巅皇冠','生猪肉','暗夜祭坛','攀爬绳',
       '腐烂的脑子','红色玛瑙','橙色玛瑙','黄色玛瑙','绿色玛瑙',
       '蓝色玛瑙','紫色玛瑙','黑色玛瑙','七彩玛瑙','死亡玛瑙']
tname=[' ','镐子','锄头']
craftdict={2:((17,8),),6:((3,1),),7:((3,1),),8:((7,1),),9:((8,1),(3,1)),
           10:((8,1),(2,1)),13:((3,1),(2,1)),14:((7,1),),15:((14,1),(3,1)),
           16:((8,1),(5,1)),19:((18,1),),20:((7,1),),21:((20,1),(3,1)),
           22:((20,1),(2,1)),23:((20,1),(5,1)),25:((8,1),(24,1)),
           26:((20,1),(24,1)),28:((8,1),(27,1)),29:((20,1),(27,1)),
           30:((14,1),(2,1)),31:((2,512),),33:((32,8),),32:((33,1),),
           34:((15,1),(35,1)),35:((19,2),),41:((39,8),),42:((4,1),(5,1)),
           43:((18,1),),48:((3,1),),56:((52,1),(53,1),(54,1)),
           57:((19,2),),66:((59,1),(60,1),(61,1),(62,1),(63,1),(64,1),(65,1)),
           67:((66,1),(58,1))}
cancraft=[0,0,2,7,19,57,35,43,34,41,42,6,13,56,66,67,48,8,9,10,16,25,28,20,
          21,22,23,26,29,14,15,30,31,33,32,0,0]
cancraftnum=[0,0,1,2,2,4,1,2,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
             1,1,1,1,1,1,1,1,1,1,8,0,0]
tooltype=[0,0,1,2,0,0]
toolneed={1:(0,1),2:(2,1)}
toolitems={0:(9,10,16,25,28),1:(15,30),2:(21,22,23,26,29)}

def worldgnr():
    global world,dheights,biomes,lworld,dworld
    world=[]
    dheights=[]
    biomes=[1,3,5,0,0,6,4,2]
    if random()<0.5:
        biomes[0]=2
        biomes[7]=1
    if random()<0.5:
        biomes[1]=4
        biomes[6]=3
    if random()<0.5:
        biomes[2]=6
        biomes[5]=5
    for i in range(width):
        dworld.append([])
        for j in range(height):
            if noise([i/8+1025,j/8+1025])>0.275:
                dworld[i].append(Block(6,i,j))
            elif noise([i/4+1025,j/4+1025])>0.425:
                dworld[i].append(Block(13,i,j))
            elif noise([i/4+1025,j/4+1025])<-0.425:
                dworld[i].append(Block(14,i,j))
            elif noise([i/4+2050,j/4+2050])>0.45:
                dworld[i].append(Block(46,i,j))
            else:
                dworld[i].append(Block(2,i,j))
    for i in range(width):
        world.append([])
        dheight=int(noise(i/32)*28)+114
        dheights.append(dheight)
        dwidth=randint(3,6)
        for j in range(dheight):
            if j>50 and j<60:
                iscloud=noise([i/18,j/5])
                if iscloud>0.05 and iscloud<0.15:
                    world[i].append(Block(15,i,j))
                elif iscloud>0.2:
                    world[i].append(Block(16,i,j))
                else:
                    world[i].append(Block(0,i,j))
            else:
                world[i].append(Block(0,i,j))
        curbio=biomes[i//128]
        if curbio==0 or curbio==1:
            for j in range(dheight,dheight+dwidth):
                world[i].append(Block(1,i,j))
        elif curbio==5:
            for j in range(dheight,dheight+dwidth):
                world[i].append(Block(20,i,j))
        elif curbio==3:
            for j in range(dheight,dheight+dwidth):
                world[i].append(Block(2,i,j))
        elif curbio==2:
            for j in range(dheight,dheight+dwidth):
                world[i].append(Block(38,i,j))
        else:
            for j in range(dheight,dheight+dwidth):
                world[i].append(Block(1,i,j))
        for j in range(dheight+dwidth,height):
            if noise([i/8,j/8])>0.3:
                world[i].append(Block(6,i,j))
            elif noise([i/4,j/4])>0.45:
                world[i].append(Block(13,i,j))
            elif noise([i/4,j/4])<-0.45:
                world[i].append(Block(14,i,j))
            else:
                world[i].append(Block(2,i,j))
        if curbio==0:
            grandom=random()
            if grandom<0.2:
                world[i][dheight]=Block(9,i,j)
            elif grandom<0.4:
                world[i][dheight]=Block(11,i,j)
            elif grandom<0.5:
                world[i][dheight]=Block(12,i,j)
            else:
                world[i][dheight]=Block(5,i,j)
            if i>3 and random()<0.125:
                trheight=randint(4,6)
                exdheight=dheights[i-1]
                world[i-1][exdheight-1]=world[i-1][exdheight]=Block(3,i,j)
                for j in range(exdheight-2,exdheight-trheight-1,-1):
                    world[i-1][j]=Block(3,i,j)
                    if random()>0.2:
                        world[i][j]=Block(4,i,j)
                    if random()>0.2:
                        world[i-2][j]=Block(4,i,j)
                world[i-1][exdheight-trheight-1]=Block(4,i,j)
        elif curbio==5:
            grandom=random()
            if grandom<0.125:
                cheight=randint(2,4)
                for j in range(cheight):
                    world[i][dheight-j-1]=Block(21,i,dheight-1-j)
            elif grandom<0.325:
                world[i][dheight-1]=Block(11,i,dheight-1)
        elif curbio==3:
            grandom=random()
            if grandom<0.375:
                world[i][dheight-1]=Block(11,i,dheight-1)
            else:
                world[i][dheight-1]=Block(22,i,dheight-1)
        elif curbio==1:
            grandom=random()
            if grandom<0.2:
                world[i][dheight]=Block(26,i,j)
            elif grandom<0.4:
                world[i][dheight]=Block(25,i,j)
            else:
                world[i][dheight]=Block(22,i,j)
            if i>3 and random()<0.125:
                trheight=randint(4,6)
                exdheight=int(noise((i-1)/32)*28)+114
                world[i-1][exdheight-1]=world[i-1][exdheight]=Block(23,i,j)
                for j in range(exdheight-2,exdheight-trheight-1,-1):
                    world[i-1][j]=Block(23,i,j)
                    if random()>0.2:
                        world[i][j]=Block(24,i,j)
                    if random()>0.2:
                        world[i-2][j]=Block(24,i,j)
                world[i-1][exdheight-trheight-1]=Block(24,i,j)
        elif curbio==6:
            grandom=random()
            if grandom<0.125:
                world[i][dheight]=Block(11,i,j)
            else:
                world[i][dheight]=Block(5,i,j)
            trandom=random()
            if i>3 and trandom<0.4:
                trheight=randint(5,9)
                exdheight=dheights[i-1]
                world[i-1][exdheight-1]=world[i-1][exdheight]=Block(3,i,j)
                for j in range(exdheight-2,exdheight-trheight-1,-1):
                    world[i-1][j]=Block(32,i,j)
                    if random()>0.2:
                        world[i][j]=Block(31,i,j)
                    if random()>0.2:
                        world[i-2][j]=Block(31,i,j)
                world[i-1][exdheight-trheight-1]=Block(31,i,j)
            elif i>3 and trandom<0.65:
                trheight=randint(1,3)
                exdheight=dheights[i-1]
                for j in range(exdheight,exdheight-trheight-1,-1):
                    world[i-1][j]=Block(32,i,j)
                    if random()>0.125:
                        world[i][j]=Block(4,i,j)
                    if random()>0.125:
                        world[i-2][j]=Block(4,i,j)
                world[i-1][exdheight-trheight-1]=Block(4,i,j)
        elif curbio==4:
            grandom=random()
            if grandom<0.2:
                world[i][dheight]=Block(9,i,j)
            elif grandom<0.3:
                world[i][dheight]=Block(11,i,j)
            elif grandom<0.5:
                world[i][dheight]=Block(34,i,j)
            elif grandom<0.6:
                world[i][dheight]=Block(35,i,j)
            elif grandom<0.7:
                world[i][dheight]=Block(36,i,j)
            else:
                world[i][dheight]=Block(5,i,j)
            if i>3 and random()<0.1:
                trheight=randint(4,6)
                exdheight=dheights[i-1]
                world[i-1][exdheight-1]=world[i-1][exdheight]=Block(3,i,j)
                for j in range(exdheight-2,exdheight-trheight-1,-1):
                    world[i-1][j]=Block(3,i,j)
                    if random()>0.2:
                        world[i][j]=Block(4,i,j)
                    if random()>0.2:
                        world[i-2][j]=Block(4,i,j)
                world[i-1][exdheight-trheight-1]=Block(4,i,j)
        elif curbio==2:
            world[i][dheight]=Block(37,i,dheight)
            if random()<0.2:
                world[i][dheight-1]=Block(11,i,dheight-1)
    if random()>0.5:
        world[256][50]=Block(17,256,50)
        world[768][50]=Block(18,768,50)
    else:
        world[256][50]=Block(18,256,50)
        world[768][50]=Block(17,768,50)
    for i in range(-1,2):
        world[256+i][51]=Block(16,256+i,51)
        world[768+i][51]=Block(16,768+i,51)
    lworld=list(world)
    print(biomes)

def freeze(dt):
    global lentities,lworld,dentities,dworld,world,entities,freezing
    freezing=True
    if ismainmenu or ischoosing:
        return
    try:
        with open('world/'+worldname,'w') as f:
            f.write(str(chopped)+'\n')
            for i in manao:
                f.write(str(i)+' ')
            f.write('\n')
            f.write(str(respawnx)+' '+str(respawny)+'\n')
            for i in biomes:
                f.write(str(i)+' ')
            f.write('\n')
            f.write(str(entities[0].x)+'\n')
            f.write(str(entities[0].y)+'\n')
            f.write(str(entities[0].heart)+'\n')
            f.write(str(entities[0].hunger)+'\n')
            f.write(str(isdark)+'\n')
            f.write(str(len(lentities))+'\n')
            if isdark:
                dentities=list(entities)
                world=list(world)
            else:
                lentities=list(entities)
                lworld=list(world)
            for i in range(len(lentities)):
                f.write(lentities[i].getfreeze())
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
                    f.write(str(lworld[i][j].id)+' ')
                f.write(str(dheights[i]))
                f.write('\n')
            f.write(str(len(dentities))+'\n')
            for i in range(len(dentities)):
                f.write(dentities[i].getfreeze())
                f.write('\n')
            for i in range(width):
                for j in range(height):
                    f.write(str(dworld[i][j].id)+' ')
                f.write('\n')
    except:
        freeze(dt)
    freezing=False

def readworld():
    global chopped,respawnx,respawny,biomes,lworld,dworld,world,\
           entities,lentities,dentities,isdark,manao
    if exists('world/'+worldname):
        with open('world/'+worldname,'r') as f:
            chopped=int(f.readline().strip())
            manaol=f.readline().strip().split(' ')
            for i in range(7):
                manao[i]=bool(manaol[i]=='True')
            respawnx,respawny=f.readline().strip().split(' ')
            respawnx=int(respawnx)
            respawny=int(respawny)
            biomes=f.readline().strip().split(' ')
            for i in range(len(biomes)):
                biomes[i]=int(biomes[i])
            entities[0].x=int(f.readline().strip())
            entities[0].y=int(f.readline().strip())
            entities[0].heart=int(f.readline().strip())
            entities[0].hunger=int(f.readline().strip())
            tsisdark=bool(f.readline().strip()=='True')
            isdark=False
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
                    enum[2]+=1
                elif curs[0]==3:
                    entities.append(DroppedTool(curs[3],curs[4],curs[1],curs[2],curs[5],curs[6],curs[7]))
                elif curs[0]==4:
                    entities.append(KingOTBirds(curs[1],curs[2]))
                    entities[len(entities)-1].heart=curs[3]
                elif curs[0]==5:
                    entities.append(AngryBird(curs[1],curs[2]))
                    entities[len(entities)-1].heart=curs[3]
                elif curs[0]==6:
                    entities.append(Fireball(curs[1],curs[2],curs[3],curs[4]))
                elif curs[0]==7:
                    entities.append(SonOTRocks(curs[1],curs[2]))
                    entities[len(entities)-1].heart=curs[3]
                elif curs[0]==8:
                    entities.append(QueenOTClouds(curs[1],curs[2]))
                    entities[len(entities)-1].heart=curs[3]
                elif curs[0]==9:
                    entities.append(Pig(curs[1],curs[2]))
                    entities[len(entities)-1].heart=curs[3]
                elif curs[0]==10:
                    entities.append(Zombie(curs[1],curs[2]))
                    entities[len(entities)-1].heart=curs[3]
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
                dheights.append(int(linee[height]))
                for j in range(height):
                    world[i].append(Block(int(linee[j]),i,j))
            lworld=list(world)
            isdark=True
            enlen=int(f.readline().strip())
            for i in range(enlen):
                curs=f.readline()
                curs=curs.strip().split(' ')
                for i in range(len(curs)):
                    curs[i]=int(curs[i])
                if curs[0]==1:
                    dentities.append(Dropped(curs[2],curs[3],curs[1]))
                elif curs[0]==2:
                    dentities.append(Bird(curs[1],curs[2]))
                    dentities[len(dentities)-1].heart=curs[3]
                    enum[2]+=1
                elif curs[0]==3:
                    dentities.append(DroppedTool(curs[3],curs[4],curs[1],curs[2],curs[5],curs[6],curs[7]))
                elif curs[0]==4:
                    dentities.append(KingOTBirds(curs[1],curs[2]))
                    dentities[len(dentities)-1].heart=curs[3]
                elif curs[0]==5:
                    dentities.append(AngryBird(curs[1],curs[2]))
                    dentities[len(dentities)-1].heart=curs[3]
                elif curs[0]==6:
                    dentities.append(Fireball(curs[1],curs[2],curs[3],curs[4]))
                elif curs[0]==7:
                    dentities.append(SonOTRocks(curs[1],curs[2]))
                    dentities[len(dentities)-1].heart=curs[3]
                elif curs[0]==8:
                    dentities.append(QueenOTClouds(curs[1],curs[2]))
                    dentities[len(dentities)-1].heart=curs[3]
                elif curs[0]==9:
                    dentities.append(Pig(curs[1],curs[2]))
                    dentities[len(dentities)-1].heart=curs[3]
                elif curs[0]==10:
                    dentities.append(Zombie(curs[1],curs[2]))
                    dentities[len(dentities)-1].heart=curs[3]
            for i in range(width):
                linee=f.readline().strip().split(' ')
                dworld.append([])
                for j in range(height):
                    dworld[i].append(Block(int(linee[j]),i,j))
            isdark=False
    if tsisdark:
        jtblock=Block(47,2,2)
        jtblock.use(2,2)
        isdark=True

@window.event
def on_key_press(symbol,modifiers):
    global iscrafting,curchoi,ismainmenu,ischoosing,worldname,worlds,isdead
    global istooling,toolstep,cholist,curchoi2,chol
    if ischoosing and not ismainmenu:
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
                init()
                readworld()
                ismainmenu=False
                ischoosing=False
        if symbol==pgt.window.key.BACKSPACE:
            ismainmenu=True
            ischoosing=False
    elif isdead==True:
        if symbol==pgt.window.key.ENTER:
            entities[0].heart=entities[0].mxheart
            entities[0].hunger=entities[0].mxhunger
            entities[0].x=respawnx
            entities[0].y=respawny
            isdead=False
    if symbol==pgt.window.key.A:
        entities[0].isleft=True
        entities[0].lastleft=True
    if symbol==pgt.window.key.D:
        entities[0].isright=True
        entities[0].lastleft=False
    if symbol==pgt.window.key.W:
        entities[0].isclimbing=True
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
                    for j in range(cnt):
                        entities[0].badd(craftdict[cancraft[curchoi+2]][j][0],craftdict[cancraft[curchoi+2]][j][1])
                    entities[0].bdel(cancraft[curchoi+2],cancraftnum[curchoi+2])
                    break
                cnt+=1
        elif istooling==True:
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
            if time()-entities[0].backpack[entities[0].chosi][entities[0].chosj].lastdmg>=1:
                entities[0].backpack[entities[0].chosi][entities[0].chosj].lastdmg=time()
                for i in range(1,len(entities)):
                    if entities[i].dis(entities[0].x,entities[0].y)<=3 and \
                       ((entities[i].x>=entities[0].x and entities[0].lastleft) or \
                        (entities[i].x<=entities[0].x and not entities[0].lastleft)):
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
    if symbol==pgt.window.key.W:
        entities[0].isclimbing=False

@window.event
def on_mouse_press(x,y,button,modifiers):
    global ismainmenu,ischoosing,curchoi,isdead,chopped
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
       entities[0].dis(curx,cury)<=3 and \
       entities[0].backpack[entities[0].chosi][entities[0].chosj].diglvl>=diglvl[world[curx][cury].id] and \
       (digtype[world[curx][cury].id]==0 or entities[0].backpack[entities[0].chosi][entities[0].chosj].tid==digtype[world[curx][cury].id]):
        if drop[world[curx][cury].id]!=0:
            entities.append(Dropped(curx,cury,drop[world[curx][cury].id]))
            entities[0].moved+=1
            if entities[0].backpack[entities[0].chosi][entities[0].chosj].id==12:
                entities[0].backpack[entities[0].chosi][entities[0].chosj].use(1)
        if world[curx][cury].id==3 or world[curx][cury].id==23 or \
           world[curx][cury].id==32:
            chopped+=1
        world[curx][cury]=Block(0,curx,cury)
    if button==pgt.window.mouse.RIGHT and entities[0].dis(curx,cury)<=3:
        if world[curx][cury].id==0:
            entities[0].bput(curx,cury)
            entities[0].moved+=1
        else:
            world[curx][cury].use(curx,cury)
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

    blocksp=[]
    blbatch=pgt.graphics.Batch()
    blbatch2=pgt.graphics.Batch()
    for i in range(34):
        for j in range(20):
            if world[i+entities[0].x-hconst][j+entities[0].y-wconst].light>0 and \
               not world[i+entities[0].x-hconst][j+entities[0].y-wconst].id==0:
                blocksp.append(pgt.sprite.Sprite(
                    img=images[world[i+entities[0].x-hconst][j+entities[0].y-wconst].id],
                    x=1024-(i*32)+int(entities[0].xx),
                    y=576-(j*32)+int(entities[0].yy),
                    batch=blbatch))
            if world[i+entities[0].x-hconst][j+entities[0].y-wconst].light<8:
                blocksp.append(pgt.sprite.Sprite(
                    img=limages[world[i+entities[0].x-hconst][j+entities[0].y-wconst].light],
                    x=1024-(i*32)+int(entities[0].xx),
                    y=576-(j*32)+int(entities[0].yy),
                    batch=blbatch2))
    blbatch.draw()

    ebatch=pgt.graphics.Batch()
    for i in entities:
        if isdead==True and i.id==0:
            continue
        if abs(i.x-entities[0].x)>=30 or abs(i.y-entities[0].y)>=30:
            continue
        i.draw(ebatch)
    ebatch.draw()
    blbatch2.draw()
    
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
    fps_display.draw()

def update(dt):
    global chopped,needkotb
    if ismainmenu or ischoosing or isdead:
        return
    dct=0
    if not freezing:
        if not isdark:
            if random()<0.02:
                if random()>0.5:
                    newx=int(random()*32+32)+entities[0].x
                else:
                    newx=int(random()*32+32)*-1+entities[0].x
                if random()>0.5:
                    newy=int(random()*32+32)+entities[0].y-10
                else:
                    newy=int(random()*32+32)*-1+entities[0].y-10
                if newx>0 and newx<1024 and newy>0 and newy<256:
                    if fall[world[newx][newy].id] and \
                       newy<dheights[newx] and enum[2]<100:
                        entities.append(Bird(newx,newy))
            if random()<0.005:
                if random()>0.5:
                    newx=int(random()*32+32)+entities[0].x
                else:
                    newx=int(random()*32+32)*-1+entities[0].x
                if newx>0 and newx<1024 and enum[9]<100 and \
                   biomes[newx//128] in (4,0):
                    newy=dheights[newx]-1
                    if fall[world[newx][newy].id] and fall[world[newx][newy-1].id]:
                        entities.append(Pig(newx,newy))
        else:
            if random()<0.01 and enum[10]<15:
                if random()>0.5:
                    newx=int(random()*32+32)+entities[0].x
                else:
                    newx=int(random()*32+32)*-1+entities[0].x
                newy=int(random()*32+32)*-1+entities[0].y
                if newx>0 and newx<1024 and newy>0 and newy<256:
                    entities.append(Zombie(newx,newy))
        if chopped>=100:
            for i in range(100):
                if random()>0.5:
                    newx=int(random()*24+32)+entities[0].x
                else:
                    newx=int(random()*24+32)*-1+entities[0].x
                if random()>0.5:
                    newy=int(random()*20+32)+entities[0].y-10
                else:
                    newy=int(random()*20+32)*-1+entities[0].y-10
                if fall[world[newx][newy].id] and \
                   newy<int(noise(newx/32)*28)+114:
                    entities.append(AngryBird(newx,newy))
            chopped=0
        if enum[5]>0:
            needkotb=True
        if enum[5]==0 and needkotb:
            entities.append(KingOTBirds(entities[0].x,entities[0].y-2))
            needkotb=False
        for i in range(len(entities)):
            if abs(entities[0].x-entities[i-dct].x)<=64 and \
               abs(entities[0].y-entities[i-dct].y)<=64 and \
               (entities[i-dct].id!=1 or abs(entities[0].y-entities[i-dct].y)<=10):
                entities[i-dct].update(dt)
                if entities[i-dct].isdel():
                    entities[i-dct].delled()
                    entities.pop(i-dct)
                    dct+=1
                    enum[entities[i-dct].id]-=1
        for i in range(34):
            for j in range(22):
                world[i+entities[0].x-hconst][j+entities[0].y-wconst].update(
                    i+entities[0].x-hconst,j+entities[0].y-wconst)

init()

pgt.clock.schedule_interval(update,1/40.)
pgt.clock.schedule_interval(freeze,10)
pgt.app.run()