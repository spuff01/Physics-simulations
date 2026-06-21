import numpy as np
import pyqtgraph as pg
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import pygame


params = {
    "m1": 3,
    "m2": 3,
   "m_s": 0.2,
   "pos1": np.array([250.0,570.0]),
   "pos2" : np.array([750.0,570.0]),
   "vel1" : np.array([50.0,-0.0]),
   "vel2" : np.array([0.0,0.0]),
   "vel3" : np.array([0.0,0.0]),
   "acc1" : np.array([0.0,0.0]),
   "acc2" : np.array([0.0,0.0]),
   "acc3" : np.array([0.0,0.0]),
    "k" : 5
}

trail1 = []
trail2 = []

spring = {
    "Lo" : 150,
"amplitude" : 6,
"n" : 500,
"frequency" : 25*np.pi,
"points" : [],
"min_length" : 30,
"mu" : 0.5
}

slider_x = 50
slider_y = 50
slider_width = 200
slider_min = 0
slider_max = 100
slider_value = 50
dragging = False

dt = 0.005


##app = QApplication(sys.argv)
##win = pg.GraphicsLayoutWidget(show=True)
## = win.addPlot()
##plot.setYRange(-100,20)
##plot.disableAutoRange()

pygame.init()
screen = pygame.display.set_mode((1200, 700))
floor = pygame.Rect(0,570,1200,320)
clock = pygame.time.Clock()
num = 1

def slider():
  global screen, slider_x, slider_y,slider_width,slider_min,slider_max,slider_value,knob_x,dragging, current_screen
  while current_screen == "slider":
      
    screen.fill((0,0,0))  
    pygame.draw.line(screen,(200,200,200),(slider_min,slider_y),
       (slider_min + slider_width,slider_y),5 )
    done_button = pygame.Rect(
      600,500,150,50
    )
    pygame.draw.rect(screen,(50,200,20),done_button)
    knob_x = slider_min + (
    (slider_value-slider_min)/(slider_max-slider_min)
        )*slider_width
    pygame.draw.circle(
        screen, (255,0,0),(int(knob_x),slider_y),10
      )
    pygame.display.flip()
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
              mx, my = pygame.mouse.get_pos()
              if (
               abs(mx-knob_x)<10 and
                abs(my-slider_y)<10
              ):
                  dragging = True
               
              if done_button.collidepoint(event.pos):
                print("clicked")
                current_screen = "update"  
                  
      if event.type == pygame.MOUSEBUTTONUP:
        dragging = False
      if dragging == True:
         mx,my = pygame.mouse.get_pos()
         mx = max(slider_min,min(slider_min + slider_width, mx))
         slider_value = slider_min + (
          (mx-slider_min)/slider_width
        )*(slider_max-slider_min)
         params["k"]=slider_value
     





##plot.addItem(ball1)
##ball2  =pg.ScatterPlotItem(size=10, brush = 'r')
##plot.addItem(ball2)


def update(params,spring):

        global trail1, trail2,num
        m1 = params["m1"]
        m2 = params["m2"]
        m_s = params["m_s"]
        pos1 = params["pos1"]
        pos2 = params["pos2"]
        vel1 = params["vel1"]
        vel2 = params["vel2"]
        vel3 = params["vel3"]
        acc1 = params["acc1"]
        acc2 = params["acc2"]
        acc3 = params["acc3"]
        k = params["k"]
        Lo = spring["Lo"]
        amplitude = spring["amplitude"]
        n = spring["n"]
        frequency = spring["frequency"]
        points = spring["points"]
        min_length = spring["min_length"]
        mu = spring["mu"]
        


        Rel_pos = pos2 - pos1
        distance = np.linalg.norm(Rel_pos)
        a=0
        g = np.array([0,3])
        velm1 = np.linalg.norm(vel1)
        velm2 = np.linalg.norm(vel2)
        if velm1 > 1e-8:
           dirv1 = vel1/velm1
        else:
           dirv1 = np.zeros(2)
        if velm2 > 1e-8:
           dirv2 = vel2 / velm2
        else:
           dirv2 = np.zeros(2)

        if distance > 1e-7:
           direction = Rel_pos/distance
        else:
            direction = np.zeros(2)  
        perp_dir = np.array([-direction[1],direction[0]])
        dx = distance - Lo
        SForce1 = k*dx*direction
        SForce2 = SForce1*-1
        F1 = a*(velm1)*dirv1*-1
        F2 = a*(velm2)*dirv2*-1

        Force1 = SForce1 + m1*g +F1
        Force2 = SForce2 + m2*g +F2
        F1N = np.zeros(2)
        F2N = np.zeros(2)
        if pos1[1] > 570:
            F1N= np.array([0,-Force1[1]])
        if pos2[1] > 570:
            F2N = np.array([0,-Force2[1]])
        fr_1 = -np.linalg.norm(F1N)*mu*np.dot(dirv1,[1,0])  
        fr_2 = -np.linalg.norm(F1N)*mu*np.dot(dirv2,[1,0])
        acc1 = (Force1 + F1N + fr_1)/m1
        acc2 = (Force2 + F2N+fr_2)/m2
        acc3 = g
 
        vel1 += acc1*dt
        vel2+= acc2*dt
        vel3 += acc3*dt
        pos1 += vel1*dt
        pos2 += vel2*dt
        
        if pos1[1]>570:
            pos1[1]=570
            vel1[1]=0
        if pos2[1]>570:
            pos2[1]=570
            vel2[1]=0    
        if distance <= min_length:
            overlap = min_length - distance
            pos1 -= overlap*direction*0.6
            pos2 += overlap*direction*0.6
            vrel = vel2 - vel1
            vdot = np.dot(vel2 - vel1,direction)
            
            if num < 5:
              impulse = vdot*direction*0.6
              
              vel1 += impulse
              vel2 -= impulse
              num = num+1
    
            
        
        
    
        trail1.append(pos1.copy())
        trail2.append(pos2.copy())

       ##ball1.setData([pos1[0]],[pos1[1]])
    ##ball2.setData([pos2[0]],[pos2[1]])
    ##trail1.setData(trail1_x,trail1_y)
    ##.setData(trail2_x,trail2_y)
        
        screen.fill((135,206,235))
        pygame.draw.rect(screen, (50,180,50),floor)
        if len(trail1) > 1:
            pygame.draw.lines(screen,(25,222,4),False,[(int(p[0]),int(p[1])) for p in trail1],2) 
            pygame.draw.lines(screen,(222,22,40),False,[(int(p[0]),int(p[1])) for p in trail2],2) 
        points = []    
        for i in range(n+1):
            t=i/n
            base = pos1 + Rel_pos*t
            offset = np.sin(frequency*t)*amplitude*perp_dir
            points.append(base + offset)
        
        pygame.draw.lines(screen,(210,10,120),False,points,int(5/(distance)**0.1))

        
        pygame.draw.circle(
            screen,
            (20,200,20),
            (int(pos1[0]),int(pos1[1])),
            17)
        
        pygame.draw.circle(screen,(250,10,40),(int(pos2[0]),int(pos2[1])),17)
        pygame.display.flip()
    


current_screen = "slider"
Running = True
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           Running = False

    if current_screen == "slider":
        slider()      
    elif current_screen == "update":
        update(params,spring)
    clock.tick(200)       
pygame.quit()      

  
##pygame.draw.line(screen, color, start, end, width)
##pygame.draw.circle(screen, color, position, radius)

##trail1 = plot.plot([],pen='y')
##timer = QTimer()
##timer.start(int(dt*1000)) 
##sys.exit(app.exec_()) 

    


