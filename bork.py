#!/usr/bin/python3
#A cat eating simulator by Oscar D'amico 
#Last updated: 31 July 2019

from turtle import Screen, Turtle
import random
import time
from time import sleep
from pygame import mixer
from math import sqrt, pow

screen = Screen()
screen.setup(500,500)
screen.title("Bork")
screen.bgcolor("black")

#Game variable
global ball_list, second, timeturtle, round_time, ready, ball_size, youspeed, ball_count, upgrading
global upw, enemy_speed
enemy_speed=10
upw=Turtle()
upw.hideturtle()
upw.penup()
upw.speed(0)
upgrading=False
ball_count=6
ball_size=1.5
timeturtle=Turtle()
timeturtle.penup()
timeturtle.hideturtle()
timeturtle.color("white")
timeturtle.setpos(-20,230)
mixer.init()
mixer.music.load("chomp.wav")
eat_range=200
ball_range=45
ready=False
round_time = 0
ball_list = []
second=time.time()
screen.addshape('dog_left.gif')
screen.addshape('dog_right.gif')
screen.addshape('cat_right.gif')
screen.addshape('cat_left.gif')
screen.addshape('cross.gif')

#Set up play area
pen = Turtle()
pen.width(3)
pen.speed(0)
pen.color("white")
pen.penup()
pen.setpos(-230, -230)
pen.pendown()
pen.hideturtle()
for x in range(4):
    pen.forward(460)
    pen.left(90)

#Set up the player
you = Turtle(shape="dog_right.gif")
cross = Turtle(shape="cross.gif")
cross.hideturtle()
you.speed(0)
cross.speed(0)
you.penup()
cross.penup()
youspeed=5

#Set up the enemy list
enemy = []

def up():
    if ready:
        you.setheading(90)
        you.sety(you.ycor()+youspeed)
        if you.ycor() >= 225:
            you.sety(-225)
        if you.shape()=="dog_right.gif":
            cross.setpos(you.xcor()+100,you.ycor())
        elif you.shape()=="dog_left.gif":
            cross.setpos(you.xcor()-100,you.ycor())

def down():
    if ready:
        you.setheading(270)
        you.sety(you.ycor()-youspeed)
        if you.ycor() <= -225:
            you.sety(225)
        if you.shape()=="dog_right.gif":
            cross.setpos(you.xcor()+100,you.ycor())
        elif you.shape()=="dog_left.gif":
            cross.setpos(you.xcor()-100,you.ycor())

def left():
    if ready:
        if you.shape() == "dog_right.gif":
            you.shape("dog_left.gif")
        you.setx(you.xcor()-youspeed)
        if you.xcor() <= -225:
            you.setx(225)
        cross.setpos(you.xcor()-100,you.ycor())
        

def right():
    if ready:
        if you.shape() == "dog_left.gif":
            you.shape("dog_right.gif")
        you.setx(you.xcor()+youspeed)
        if you.xcor() >= 225:
            you.setx(-225)
        cross.setpos(you.xcor()+100,you.ycor())

def shoot():
    if ready: 
        bullet = Turtle(shape='circle')
        bullet.penup()
        bullet.shapesize(ball_size,ball_size,0)
        bullet.hideturtle()
        bullet.setpos(you.xcor(), you.ycor())
        bullet.color("yellow")
        bullet.showturtle()
        bullet.speed(10)
        if you.shape()=="dog_right.gif":
            bullet.forward(100)
        elif you.shape()=="dog_left.gif":
            bullet.back(100)
        global ball_list
        ball_list.append(bullet)
        if len(ball_list) > ball_count:
            for each in range(0,len(ball_list)):
                ball_list[each].hideturtle()
            ball_list.clear()

def instructions():
    ins = Turtle()
    ins.penup()
    ins.hideturtle()
    ins.setpos(25,-10)
    ins.color("Green")
    ins.write("This is you\n↩",font=(
        "Arial", 20, "normal"))
    sleep(2)
    ins.clear()

    ins.setpos(-180,30)
    ins.write("↕\tMove up and down\n↔\tMove left and right\n(SPACE)\tShoot balls", font=(
        "Arial", 20, "normal"))
    sleep(3)
    ins.clear()

    ins.write("Eat cats", font=(
        "Arial", 20, "normal"))
    sleep(2)
    ins.clear()

def upgrades():
    global upw
    for x in range(0,len(ball_list)):
        ball_list[x].hideturtle()
    ball_list.clear()
    upw.setpos(-110,50)
    upw.color("green")
    upw.write("Select an upgrade\n", font=("Arial", 20, "normal"))
    upw.setpos(-160,50)
    upw.write("+Ball Size   +Run Speed   +Ball Count", font=("Arial", 15, "normal"))
    screen.onclick(choice)


def choice(x,y):
    global ball_range, ball_size, youspeed, ball_count, upgrading, upw
    print(x,y)
    if upgrading:
        if y >= 50 and y <= 70: 
            if x >= -159 and x <= -65:
                upw.clear()
                upw.write("Ball size increased!",font=("Arial", 15, "normal"))
                sleep(1)
                upw.clear() 
                ball_size*=1.2
                ball_range*=1.2
                upgrading=False
            elif x >= -54 and x <= 65:
                upw.clear()
                upw.write("Run speed doubled!",font=("Arial", 15, "normal"))
                sleep(1)
                upw.clear()   
                youspeed*=2
                upgrading=False
            elif x >= 72 and x <= 186:
                upw.clear()
                upw.write("Ball count doubled!",font=("Arial", 15, "normal"))
                sleep(1)
                upw.clear() 
                ball_count*=2
                upgrading=False
    upw.clear()

screen.onkey(up, "Up")
screen.onkey(down, "Down")
screen.onkey(left, "Left")
screen.onkey(right, "Right")
screen.onkey(shoot, "space")
screen.listen()

def enemyWave():
    global round_time
    round_time=0
    deathcount=0
    enemy.clear()
    scoreTurt = Turtle()
    scoreTurt.color("white")
    scoreTurt.penup()
    scoreTurt.hideturtle()
    scoreTurt.setpos(-180,230)
    scoreTurt.write("Deathcount: "+str(deathcount), font=("Arial", 12, "normal"))
    for x in range(0,level*5): #populate the enemy list with 5 cats per level
        enemy.append(Turtle(shape="cat_right.gif"))
        enemy[x].hideturtle
        enemy[x].setheading(random.randint(0,359))
        enemy[x].penup()
        enemy[x].speed(0)
        enemy[x].setpos(random.randint(-225,225),random.randint(-215,215))

    while deathcount!=len(enemy): #While deathcount is NOT the length of the enemy list
        if countdown():
            drawsecs()
        for x in range(0,len(enemy)): #For each enemy
            if enemy[x].isvisible(): #If it can be seen, do the following calculations
                if random.randint(0,10) == 7: #if a seven is rolled, change directions
                    enemy[x].right(random.randint(0,360))
                enemy[x].forward(enemy_speed) #Move it forward by enemyspeed
                if enemy[x].xcor() > 215: #Check collision right wall
                    enemy[x].setx(210)
                    enemy[x].left(180)
                    enemy[x].shape("cat_left.gif")
                if enemy[x].xcor() < -215: #Check collision left wall
                    enemy[x].setx(-210)
                    enemy[x].right(180)
                    enemy[x].shape("cat_right.gif")
                if enemy[x].ycor() > 215: #Check ceiling collision
                    enemy[x].sety(210)
                    enemy[x].right(180)
                if enemy[x].ycor() < -215: #Check floor collision
                    enemy[x].sety(-210)
                    enemy[x].left(180)
                if collided(you, enemy[x], eat_range): #Check collision with player
                    enemy[x].hideturtle() #Hide if collided
                    enemy[x].setpos(-600,-600) #Move far away to prevent duplicate collisions
                    deathcount+=1 #Update deathcount
                    chomp(you)
                    scoreTurt.clear()
                    scoreTurt.write("Deathcount: "+str(deathcount), font=("Arial", 12, "normal"))
                for j in range(0,len(ball_list)): #check ball collision
                    if collided(ball_list[j], enemy[x], ball_range):
                        enemy[x].hideturtle() #Hide if collided
                        enemy[x].setpos(-600,-600) #Move far away to prevent duplicate collisions
                        deathcount+=1 #Update deathcount
                        scoreTurt.clear()
                        scoreTurt.write("Deathcount: "+str(deathcount), font=("Arial", 12, "normal"))
    scoreTurt.clear()

def levels(writer, message):
    writer.color("green")
    writer.hideturtle()
    writer.penup()
    writer.setpos(-180,150)
    for x in range(3):
        writer.write(f"{message}", font=("Arial",32,"normal"))
        sleep(0.5)
        writer.clear()
        sleep(0.5)
    ready=True

def collided(player, enemy, range):
    print("Distance:",((player.xcor() - enemy.xcor())** 2) + ((player.ycor() - enemy.ycor())**2))
    print(f"Range:{range}")
    if ((player.xcor() - enemy.xcor())** 2) + ((player.ycor() - enemy.ycor())**2) <= range:
        return True
    else:
         return False

def countdown():
    n=time.time()
    global second
    if n-second >= 1: #if difference in previously recorded second is 1 or more
        second = time.time() #Establish a new global second
        return True #Return true, a.k.a, a second HAS passed
    else:
        return False #A second has not passed

def chomp(player):
    mixer.music.play()
    writer=Turtle()
    writer.penup()
    writer.hideturtle()
    writer.color("red")
    writer.setpos(player.xcor(),player.ycor()+10)
    writer.write("CHOMP!", font=("Butcherman", 20, "normal"))
    sleep(0.1)
    writer.clear()
    

def drawsecs():
    global round_time
    timeturtle.clear()
    timeturtle.write("Round time: "+str(round_time), font=("Arial", 12, "normal"))
    round_time+=1


#instructions()
cross.setpos(you.xcor()+100,you.ycor())
cross.showturtle()
for j in range(0,2):
    for x in range(1,5):
        level=x
        ready=False
        levels(Turtle(), f"Starting level {level}...")
        ready=True
        enemyWave()
        
    upgrading=True
    x=0
    while upgrading:    
        upgrades()
        x+=1
        if x ==10:
            upw.clear()
            x=0
    upw.clear()

    for x in range(5, 1, 10):
        level=x
        ready=False
        levels(Turtle(), f"Starting level {level}...")
        ready=True
        enemyWave()

    enemy_speed*=2
upw.clear()
quit()
screen.mainloop()
