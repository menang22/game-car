#coding: utf-8
from __future__ import division
import curses,time,random,threading,sys,os
"""
o-o
|+|
o-o
"""


"""




Hayo mau apa lu?

mau recode?
yahahaha ga mampu yahahaha


kalo ga mampu coding chat w sini biar w ajarin ya wkwkwk
wa : 0896 8200 9902

sfx:* yahahah bocah recode



"""




score = 0.0
menu = ["Play","Help","Info","Exit"]
mobillawan = []
tstop = False
pause = False
health = 3
def removelawan(max):
    global mobillawan,tstop
    yy,xx = max
    while not tstop:
      for n,i in enumerate(mobillawan):
          if i[0] == yy-1 and not pause:
              mobillawan.remove(mobillawan[n])
    return

def createlawan(slp,max):
    global mobillawan,tstop
    yy,xx = max
    while not tstop:
      if not pause:
         mobillawan.append([2,random.randint(0,xx-1)])
         time.sleep(slp)
    return

def lawan(sls,max):
    global mobillawan,tstop,score,slo
    yy,xx = max
    while not tstop:
      for n,i in enumerate(mobillawan):
          if i[0] < yy and not pause:
             try:
                mobillawan[n][0] += 1
             except IndexError:
                pass
      if not pause:
         score += 0.01
         time.sleep(sls)
    return

def curo(c,speed_spawn = 0.5,speed_movement = 0.3):
    global mobillawan,health,pause,slo
    curses.curs_set(0)
    yy,xx = c.getmaxyx()
    car = [yy-2,xx//2-1]
    c.erase()
    c.addstr(car[0]-2,car[1],"o-o")
    c.addstr(car[0]-1,car[1],"|+|")
    c.addstr(car[0],car[1],"o-o")
    c.addstr(yy-1,0,"-"*(xx-1))
    c.attron(curses.color_pair(1))
    c.addstr(yy//2,xx//2 - len("Press right or left to move the car")//2,"Press right or left to move the car")
    c.attroff(curses.color_pair(1))
    c.addstr(0,xx-len("Made by JustA Hacker")-1,"Made by JustA Hacker")
    c.addstr(1,0,"-"*(xx-1))
    c.addstr(0,xx//2-health//2,"❤"*health+"   ")
    c.refresh()
    sthread = True
    lose = False
    while True:
      inp = c.getch()
      if inp == curses.KEY_UP and not pause:
         slo = 0.2
      else :
         slo = 1
      if sthread:
         t1 = threading.Thread(target=createlawan,args=(speed_spawn,[yy,xx]))
         t2 = threading.Thread(target=lawan,args=(speed_movement,[yy,xx]))
         t3 = threading.Thread(target=removelawan,args=([yy,xx],))
         t1.daemon = True
         t2.daemon = True
         t3.daemon = True
         t1.start()
         t2.start()
         t3.start()
         c.nodelay(1)
         sthread = False
      if inp == curses.KEY_RIGHT and not pause:
         car[1] += 3
         inp = ""
      elif inp == curses.KEY_LEFT and not pause:
         car[1] -= 3
         inp = ""
      elif inp == ord(" "):
         if pause:
            pause = False
            c.nodelay(1)
            inp = ""
         else:
            pause = True
            lon = "Press 'space' button to continue game"
            c.attron(curses.color_pair(1))
            c.addstr(yy//2-1,xx//2 - len("Game is paused")//2,"Game is paused")
            c.addstr(yy//2,xx//2 - len(lon)//2,lon)
            c.attroff(curses.color_pair(1))
            c.refresh()
            c.nodelay(1)
            continue
      if car[1] < 0:
         car[1] += 3
      elif car[1] > xx-3:
         car[1] -= 3
      if not pause:
         c.erase()
         for i in mobillawan:
             if i[0] < yy-1:
                c.addstr(i[0],i[1],"🚘")
      for i in sorted(mobillawan,reverse=True,key = lambda x:x[0]):
          if i[1] in range(car[1]-1,car[1]+2) and i[0] == car[0] or i[1] in range(car[1]-1,car[1]+2) and i[0] == car[0]-1 or i[1] in range(car[1]-1,car[1]+2) and i[0] == car[0]-2:
             mobillawan.remove(i)
             health +=-1
             c.erase()
             break
      if not pause:
         c.addstr(yy-1,0,"-"*(xx-1))
         c.addstr(car[0]-2,car[1],"o-o")
         c.addstr(car[0]-1,car[1],"|+|")
         c.addstr(car[0],car[1],"o-o")
         c.addstr(1,0,"-"*(xx-1))
         c.addstr(0,xx//2-health//2,"❤"*health)
         c.addstr(0,0,"Score : {} KM". format(score))
         c.addstr(0,xx-len("Made by menang22")-1,"Made by JustA Hacker")
         c.refresh()
         c.refresh()
      if health == 0:
         lose = True
      else:
         lose = False
      if lose:
         tstop = True
         c.nodelay(0)
         while True:
           c.addstr(yy//2-1,xx//2-len("You Lose!")//2,"You Lose!")
           c.addstr(yy//2,xx//2-len("Press Q or q to exit")//2,"Press Q or q to exit")
           c.addstr(0,xx-1,str(health))
           c.refresh()
           cok = c.getch()
           if cok == 113 or cok == 81:
              return

def print_menu(c,current,yy,xx,menu,title = "Select menu"):
    c.clear()
    tx = xx // 2 - len(title) // 2
    ty = yy // 2 - len(menu)//2 - len(menu) // 2
    c.attron(curses.color_pair(2))
    c.addstr(ty,tx,title)
    c.attroff(curses.color_pair(2))
    for n,i in enumerate(menu):
        x = xx // 2 - len(i)//2
        y = yy // 2 - len(menu)//2 + n
        if current == n:
           c.attron(curses.color_pair(1))
           c.addstr(y,x,i)
           c.attroff(curses.color_pair(1))
        else:
           c.addstr(y,x,i)
        c.refresh()

def print_multiline(c,text_list,yy,xx):
    c.clear()
    c.attron(curses.color_pair(2))
    for n,i in enumerate(text_list):
        x = xx // 2 - len(i) // 2
        y = yy // 2 - len(menu) // 2 + n
        c.addstr(y,x,i)
    c.attroff(curses.color_pair(2))
    c.refresh()

def cur(c,menu,title = "Select menu"):
    yy,xx = c.getmaxyx()
    current = 0
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
    curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_CYAN)
    curses.curs_set(0)
    print_menu(c,current,yy,xx,menu,title = title)

    while True:
      tex = c.getch()
      if tex == curses.KEY_UP:
         current -= 1
      elif tex == curses.KEY_DOWN:
         current += 1
      elif tex == curses.KEY_MOUSE:
         break
      if current < 0:
         current = len(menu)-1
      elif current > len(menu)-1:
         current = 0
      if tex == 10:
         break
      print_menu(c,current,yy,xx,menu,title)
    if menu[current] == "Play":
       cur(c,["Easy","Medium","Hard","Insane"],title = "Select Level")
    elif menu[current] == "Help":
       print_multiline(c,["Press B or b to back to menu","","(in game keys)","Press right or left key to move the car","Press 'space' button to pause / play game"],yy,xx)
       while True:
         cok = c.getch()
         if cok == ord("b") or cok == ord("B"):
            c.clear()
            cur(c,["Play","Help","Info","Exit"])
            break
    elif menu[current] == "Info":
       print_multiline(c,["Author : JustAHacker","Youtube : JustA Hacker","github : https://github.com/justahackers","instagram : agung.rafasyah","","","Team :","Black Coder Crush","Spongebob cyber team","","","","Press B or b to back to menu"],yy,xx)
       while True:
          cok = c.getch()
          if cok == ord("b") or cok == ord("B"):
             cur(c,["Play","Help","Info","Exit"])
             break
    elif menu[current] == "Exit":
         return

    elif menu[current] == "Easy":
         curo(c,xx / 100,0.7)

    elif menu[current] == "Medium":
         curo(c,xx / 150,0.7)

    elif menu[current] == "Hard":
         curo(c,xx / 200,0.4)

    elif menu[current] == "Insane":
         curo(c,xx / 600,0.3)
curses.wrapper(cur,menu)
