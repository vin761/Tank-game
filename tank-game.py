from graph import *
import math 
from random import randint


def createPlates(N):# создание мешени
    global plates#глобальный массив
    yPlates=100#у всех одна y-координата
    plates=[]
    for i in range(N):
        brushColor(randColor())
        p=circle(randint(0,500),randint(50,150),randint(10,20))#мишени создаются случайным образом 
                                                    

        plates.append(p)#добавление в массив очередной мишени


def hit(p):#проверка столкновения снаряда и мешени
    global bullet#глобальная переменная

    #координаты снаряда
    x1,y1,x2,y2=coords(bullet)
    #центр снаряда
    xb=x1+r
    yb=y1+r
    #координаты тарелки
    x1p,y1p,x2p,y2p=coords(p)
    xp=(x1p+x2p)/2#координаты центра мишени
    yp=(y1p+y2p)/2
    Rp=(x2p-x1p)/2#радиус мишени
    d2=(xb-xp)**2+(yb-yp)**2#теорема Пифагора
    return d2<=(Rp)**2#возврашает True, если мишень поражена



def movePlates():#движение мишеней
    global plates#глобальный массив
    for p in plates:
        moveObjectBy(p,-2,0)#сдвиг на 2 влево
        x1,y1,x2,y2=coords(p)
        if x1<0:#если мишень вышла за границу окна
            moveObjectBy(p,550,0)#перескочить в право на 550, т.к движение справа налево


def checkCollision():
    global isFlying,bullet,pleats,lbl,score#глобальные переменные
    for p in plates:
        if hit(p):#произошло столкновение снаряда и мишени
            plates.remove(p)#если мишень поражена, изъять ее из списка
            deleteObject(p)#удалить мишень
            score+=1
            lbl["text"]="Счёт:"+str(score)
            moveObjectTo(bullet,x0-r,y0-r)
            isFlying=False
            break


def update():#анимация
    global bullet,xb,yb,isFlying,angleBullet#глобальные переменные
    movePlates()
    if isFlying:#логическая переменная True-снаряд летит, Flse-не летит
        if bullet==None:#если снаряд пока не создан
            brushColor("black")
            bullet=circle(x0,y0,r)#создается обыект снаряд
        else:
            aRad=angleBullet*math.pi/180#угол отклонения снаряда. он должен лететь сответственно повороту пушки
            dx=STEP*math.cos(aRad)
            dy=-STEP*math.sin(aRad)
            moveObjectBy(bullet,dx,dy)#функция движения снаряда
            xb+=dx
            yb+=dy
            checkCollision()#проверяем поподание
            if not circleInView(xb,yb,r):
                deleteObject(bullet)
                bullet=None
                isFlying=False



def drawGun(angleNew):#рисование пушки
    global angle,gun#глобальные переменные
    angle=angleNew#запомнить новый угол
    aRad=angle*math.pi/180#в радианы
    x1=x0+L*math.cos(aRad)
    y1=y0-L*math.sin(aRad)
    if gun==None:#при первом рисовании пушки
        gun=line(x0,y0,x1,y1)
    else:#в остальных случаях, когда пушка уже нарисована
        changeCoords(gun,[(x0,y0),(x1,y1)])


def keyPressed(event):#управление клавишами
    global isFlying,bullet,xb,yb,angleBullet
    
    if event.keycode==VK_LEFT:
        drawGun(angle+5)#влево на 5 градусов при нажатии стрелки "влево"
    elif event.keycode==VK_RIGHT:
        drawGun(angle-5)#вправо на 5 градусов при нажатии стрелки "вправо"
    elif event.keycode==VK_ESCAPE:#выход при нажатии на ESC
        close()
    elif event.keycode==VK_SPACE:
        if not isFlying:
            angleBullet=angle
            aRad=angle*math.pi/180
            xb=x0+L*math.cos(aRad)
            yb=y0-L*math.sin(aRad)
            isFlying=True


#основная программа
H=60; W=30; L=40#размеры танка
x0=200; y0=400; angle=90#пушка. Точка с координатами x0.y0- является центральной
brushColor("pink")#цвет корпуса
rectangle(x0-W/2,y0-H/2,x0+W/2,y0+H/2)#координаты противоположныхвершин корпуса считаются от центра

#башня
penSize(1)
brushColor("red")
circle(x0,y0,W/2)


r=4#радиус снаряда
gun=None#при первом вызове процедуры drawGun значение Gun=0
xb=x0;yb=x0
isFlying=False
bullet=None
STEP=25#коэффицент скорости движения снаряда


penSize(5)
drawGun(angle)#вызваем процедуру рисования пушки
penSize(1)
createPlates(35)#создфем массив (список) с мишенями
score=0#счетчик пораженных мишеней
lbl=label("Счёт:0",10,200,bg="white")


onKey(keyPressed)#вызываем процудуру управления
onTimer(update,10)#вызываем процудуру анимации

run()
