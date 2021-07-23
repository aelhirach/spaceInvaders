# -*- coding: utf-8 -*-
"""
@author: EL HIRACH Abderrazzak
"""
from tkinter import *
from tkinter.messagebox import *
from random import randint, choice


# functions : ---
def Xmax():
    x = 0
    for en in invaders:
        if gameScene.coords(en)[0] > x:
            x = gameScene.coords(en)[0]
    return x

def Xmin():
    x = W
    for en in invaders:
        if gameScene.coords(en)[0] < x:
            x = gameScene.coords(en)[0]
    return x


def init():
    "..."
    me.append(gameScene.create_rectangle(x, y, x + shipSize, y + shipSize, fill=myColor))
    for i in range(nw):
        for j in range(nh):
            x1 = x_init + i * shipSize + i * sp
            y1 = y_init + j * shipSize + j * sp
            invaders.append(gameScene.create_rectangle(x1, y1, x1 + shipSize, y1 + shipSize, width=2, fill=invadersColor))

    numberOfLivesValue.config(text=str(lives))
    numberOfInvadersValue.config(text=str(len(invaders)))


def startStop():
    #start & stop the game
    global coul, flag
    if flag == 0:
        flag = 1
        moveInvaders()
    else:
        flag = 0


def changeCanvasColor():
    global bg_color
    bg_color = choice(bg_color_palette)
    while bg_color in [myColor, invaders_bullets_color, myBulletsColor, invadersColor]:
        bg_color = choice(bg_color_palette)
    gameScene.configure(bg=bg_color)


def changeMyShipColor():
    global myColor, me
    myColor = choice(bg_color_palette)
    gameScene.itemconfig(me, fill=myColor)


def changeInvadersBulletsColor():
    global invaders_bullets_color, bullets
    invaders_bullets_color = choice(bg_color_palette)
    for b in bullets:
        if b[1] == "enbulet":
            gameScene.itemconfig(b, fill=invaders_bullets_color)


def changeMyBulletsColor():
    global myBulletsColor, bullets
    myBulletsColor = choice(bg_color_palette)
    for b in bullets:
        if b[1] == "mybullets":
            gameScene.itemconfig(b, fill=myBulletsColor)


def changeInvadersColor():
    global invadersColor, invaders
    invadersColor = choice(bg_color_palette)
    gameScene.itemconfig(invaders, fill=invadersColor)


def isOnColision(bullet, bloc):
    coord_bullet = gameScene.coords(bullet)  # x_tf_1, y_tf_1, x_br_1, y_br_1
    coord_bloc = gameScene.coords(bloc)  # x_tf_2, y_tf_2, x_br_2, y_br_2

    x_tf_1, y_tf_1, x_br_1, y_br_1 = coord_bullet[0], coord_bullet[1], coord_bullet[2], coord_bullet[3]
    x_tf_2, y_tf_2, x_br_2, y_br_2  = coord_bloc[0], coord_bloc[1], coord_bloc[2], coord_bloc[3]

    return (x_tf_1 < x_br_2) and (x_br_1 > x_tf_2) and (y_br_1 > y_tf_2)


def moveInvaders():
    """..."""
    global dx, dy, lives
    # calculate (dx et dy) according to the xmin xmax and the current postion of the invaders
    xmax = Xmax()
    xmin = Xmin()
    if dy > 0:
        dy = 0
        if xmin - deltaX < 0:
            dx = deltaX
        else:
            dx = -deltaX
    else:
        if xmin - deltaX < 0:
            dy = deltaY
            dx = 0
        elif xmax + deltaX > W:
            dy = deltaY
            dx = 0
    # move invaders with dx et dy
    for li in invaders:
        gameScene.move(li, dx, dy)
        # generate a random integer between 1-100 and check if equal to 1, if that is the case, invader will shoot a bullet
        if randint(1, 1 / probabilityBullet) == 1:
            x1 = gameScene.coords(li)[0] + shipSize / 2 - cb / 2
            y1 = gameScene.coords(li)[3]
            enBullet = gameScene.create_rectangle(x1, y1, x1 + cb, y1 + cb, fill=invaders_bullets_color)
            bullets.append(
                [enBullet, 'enbullet', deltaYBullet])

    bullet_to_delete = []
    for b in bullets:
        coord_b = gameScene.coords(b[0])
        if coord_b[3] < 0 or coord_b[1] > H:
            bullet_to_delete.append(b)
        else:
            gameScene.move(b[0], 0, b[2])  # Move the bullet of the invader to the bottom

            if b[1] == 'enbullet' and isOnColision(b[0], me[0]):
                bullet_to_delete.append(b)
                lives -= 1
                numberOfLivesValue.config(text=str(lives))

                if (lives == 0):
                    startStop()
                    showinfo("Game over", "You lost all your lives")

            elif b[1] == 'mybullets':
                myBulletIsDestroyed = False
                # check collision between bullets & invaders
                for ennemisBullet in bullets:
                    if ennemisBullet[1] == 'enbullet' and isOnColision(ennemisBullet[0], b[0]):
                        bullet_to_delete.append(ennemisBullet)
                        bullet_to_delete.append(b)
                        myBulletIsDestroyed = True
                        break
                if not myBulletIsDestroyed:
                    for e in invaders:
                        if isOnColision(e, b[0]):
                            bullet_to_delete.append(b)
                            gameScene.delete(e)
                            invaders.remove(e)
                            numberOfInvadersValue.config(text=str(len(invaders)))
                            if (len(invaders) == 0):
                                startStop()
                                showinfo("You win", "You killed all the invaders")

                            break

    for b in bullet_to_delete:
        if (b in bullets):
            bullets.remove(b)
        gameScene.delete(b[0])

    if flag == 1:
        mainScreen.after(deltaT, moveInvaders)


def triggerhandler(event):
    if event.keysym == 'p':
        startStop()
    elif event.keysym == 'Left':
        if gameScene.coords(me[0])[0] - deltaX > 0:
            gameScene.move(me[0], -deltaX, 0)
    elif event.keysym == 'Right':
        if gameScene.coords(me[0])[2] + deltaX < W:
            gameScene.move(me[0], deltaX, 0)
    elif event.keysym == 'space' or event.keysym == 'Up':
        x1 = gameScene.coords(me[0])[0] + shipSize / 2 - cb / 2
        y1 = gameScene.coords(me[0])[1] + cb
        bullets.append(
            [gameScene.create_rectangle(x1, y1, x1 + cb, y1 + cb, fill=myBulletsColor), 'mybullets', -deltaYBullet])

# globale variables :
flag = 0
W, H = 600, 700
shipSize = 20
cb = 6
probabilityBullet = 0.01
sp = 2 * shipSize # space between Invaders
y_init = 80 # initial y position of the top left Invader
x_init = 40  # initial x position of the top left Invader
x = W / 2 - shipSize / 2  # ma positio on x
y = H - 100  # y ma position en y
nw, nh = 6, 4
deltaX, deltaY = 10, 30
dx, dy = deltaX, 0
deltaYBullet = deltaY / 3
deltaT = 80
invaders = []
bullets = []
me = []
lives = 5
invadersColor = 'blue'
invaders_bullets_color = 'red'
myBulletsColor = 'purple'
myColor = 'pink'
bg_color_palette = ['cyan', 'maroon', 'green', 'orange', 'yellow', 'dark grey', 'grey', 'light grey']
bg_color = choice(bg_color_palette)
nb_kill = 0

# The main screen widget :
mainScreen = Tk()



# The game scene widget :
gameScene = Canvas(mainScreen, bg=bg_color, height=H, width=W)
gameScene.grid(row=0, column=0, rowspan=8)

# Buttons & Labels
initBtn = Button(mainScreen, text='Init', command=init)
initBtn.grid(row=0, column=1)
quitBtn = Button(mainScreen, text='Quit', command=mainScreen.destroy)
quitBtn.grid(row=0, column=2)
startStopBtn = Button(mainScreen, text='Start/Stop', command=startStop)
startStopBtn.grid(row=1, column=1)

changeCanvasColorBtn = Button(mainScreen, text='canvas color', command=changeCanvasColor)
changeCanvasColorBtn.grid(row=2, column=1)
changeMyShipColorBtn = Button(mainScreen, text='my ship color', command=changeMyShipColor)
changeMyShipColorBtn.grid(row=2, column=2)
changeInvadersBulletsColorBtn = Button(mainScreen, text='invaders bullets', command=changeInvadersBulletsColor)
changeInvadersBulletsColorBtn.grid(row=3, column=1)
changeMyBulletsColorBtn = Button(mainScreen, text='my bullets color', command=changeMyBulletsColor)
changeMyBulletsColorBtn.grid(row=3, column=2)
changeInvadersColorBtn = Button(mainScreen, text='invaders color', command=changeInvadersColor)
changeInvadersColorBtn.grid(row=4, column=1)

numberOfInvadersLabel = Label(mainScreen, text="Killed invaders : ", bg='white')
numberOfInvadersLabel.grid(sticky="W", row=5, column=1)
numberOfInvadersValue = Label(mainScreen, text=0, bg='white')
numberOfInvadersValue.grid(sticky="W", row=5, column=2)

numberOfLivesLabel = Label(mainScreen, text='Lives :', )
numberOfLivesLabel.grid(sticky="W", row=6, column=1)
numberOfLivesValue = Label(mainScreen, text=0)
numberOfLivesValue.grid(sticky="W", row=6, column=2)


# start the mainloop
mainScreen.bind("<Key>", triggerhandler)
mainScreen.mainloop()
