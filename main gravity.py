import numpy as np
import pygame_gui
import pygame
import sys
import random
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets

pygame.init()
screen = pygame.display.set_mode((1200,700))
manager = pygame_gui.UIManager((1200,700))
manager2 = pygame_gui.UIManager((1200,700))

slider_mass = pygame_gui.elements.UIHorizontalSlider(
   relative_rect=pygame.Rect(50,50,200,30),
   start_value=10,
   value_range=(0,100),
   manager=manager
)
mass_label = pygame_gui.elements.UILabel(
   relative_rect=pygame.Rect(80,20,100,20),
   text = "Mass",
   manager=manager
)
mass_value = pygame_gui.elements.UILabel(
   relative_rect=pygame.Rect(250,50,80,20),
   text = "10",
   manager=manager
)

slider_G = pygame_gui.elements.UIHorizontalSlider(
   relative_rect=pygame.Rect(50,200,200,30),
   start_value=100,
   value_range=(0,1000),
   manager=manager
)
G_label = pygame_gui.elements.UILabel(
   relative_rect=pygame.Rect(80,170,100,20),
   text = "G",
   manager=manager
)
G_value = pygame_gui.elements.UILabel(
   relative_rect=pygame.Rect(250,200,100,20),
   text="10",
   manager=manager
)
vel_slider = pygame_gui.elements.UIHorizontalSlider(
   relative_rect=pygame.Rect(50,300,200,30),
   start_value=10,
   value_range=(0,100),
   manager=manager
)
vel_label = pygame_gui.elements.UILabel(
   relative_rect=(50,270,100,20),
   text = "velocity",
   manager=manager
)
vel_value = pygame_gui.elements.UILabel(
   relative_rect=pygame.Rect(350,300,100,30),
   text = "10",
   manager=manager)
t = 0


class masses:
   def __init__ (self,mass, pos, vel, acc, Force, radius, trail, x, y, z, KE, KE_val, GPE, GPE_val, E_calc,t_val):
      self.pos = pos
      self.mass = mass
      self.vel = vel
      self.acc = acc
      self.Force = Force
      self.dt = 0.05
      self.radius = radius
      self.trail = trail
      self.x = x
      self.y = y
      self.z = z
      self.KE = KE
      self.GPE = GPE
      self.E_calc = E_calc
      self.GPE_val = GPE_val
      self.KE_val = KE_val
      self.t_val = t_val

      self.plot = None
      self.curve_KE = None
      self.curve_PE = None

   def acc_calc(self):
      self.acc = self.Force/self.mass
   def vel_calc(self):
      self.vel += self.acc * self.dt
   def KE_calc(self):
      self.KE = 0.5*self.mass*np.dot(self.vel,self.vel)  
   def pos_calc(self):
      self.pos += self.vel * self.dt
      self.trail.append(self.pos.copy())
   def draw_body(self):
      pygame.draw.circle(screen, (self.x,self.y,self.z), (self.pos[0],self.pos[1]), self.radius)
   def draw_trail(self):
      if len(self.trail)>1:
        pygame.draw.lines(screen,(self.x,self.y,self.z), False, self.trail ,2)
      

 
class arrows:
   def __init__(self,origin,vector):
      self.orig = origin
      self.vector = vector
   def draw_arrow(self):
      self.tipp = self.orig+self.vector
      pygame.draw.line(screen,(10,240,10),self.orig,self.tipp,3)
      pygame.draw.circle(screen,(240,10,10),self.tipp,3)
      

class simulate:
  def __init__(self, mass_value):
     self.bodies = []
     self.arrows = []

  def gravity_calc(self, slider_G):
     for body in self.bodies:
        body.Force = np.zeros(2)

     G = slider_G.get_current_value()
     for i in range(len(self.bodies)):
        for j in range(i+1,len(self.bodies)):
           Rel_pos = self.bodies[j].pos-self.bodies[i].pos  
           Relm = np.linalg.norm(Rel_pos) 
           direction = Rel_pos/Relm
           if Relm > 1e-4:
             self.bodies[i].Force += (G*self.bodies[i].mass*self.bodies[j].mass/(Relm)**2)*direction
             self.bodies[j].Force -= (G*self.bodies[i].mass*self.bodies[j].mass/(Relm)**2)*direction
             
             
           if Relm < self.bodies[i].radius + self.bodies[j].radius:
              rel_vel = self.bodies[j].vel - self.bodies[i].vel
              if np.dot(rel_vel,direction)<0:
                 vcosi = np.dot(self.bodies[i].vel, direction)*direction
                 vcosj = np.dot(self.bodies[j].vel,direction)*direction
                 mi = self.bodies[i].mass
                 mj = self.bodies[j].mass
                 self.bodies[i].vel += -2*vcosi + 2*(mi*vcosi+mj*vcosj)/(mi+mj)
                 self.bodies[j].vel += -2*vcosj + 2*(mi*vcosi+mj*vcosj)/(mi+mj)
                 overlap = self.bodies[i].radius + self.bodies[j].radius - Relm
                 self.bodies[i].pos -= direction*overlap*mj/(mi+mj)
                 self.bodies[j].pos += direction*overlap*mi/(mi+mj)
  
  def arrow_calc(self):
     for i in range(len(self.arrows)):
        self.arrows[i].orig = self.bodies[i].pos
        self.arrows[i].vector = self.bodies[i].acc*4

  def GPE_calc(self, body, slider_G):
     body.GPE = 0
     G = slider_G.get_current_value()
     for other in self.bodies:
           if other is not body:
             Rel_pos = other.pos-body.pos  
             Relm = np.linalg.norm(Rel_pos)
             body.GPE += (-G*body.mass*other.mass/(Relm))
           
app = QtWidgets.QApplication([])                
start_button = pygame_gui.elements.UIButton(
           relative_rect=pygame.Rect(1000,500,120,40),
           text = "start",
           manager=manager
        )      
       
pause_button = pygame_gui.elements.UIButton(
           relative_rect=pygame.Rect(1000,600,120,40),
           text = "pause",
           manager=manager2
        )           
sim = simulate(mass_value)
clock = pygame.time.Clock()
Running = True
state = "Menu"
first = True
origin = np.array([300,300])
tip = np.array([300,250])
dragging = False
phy_running = True
graph_visible = False      


while Running:
   can_create = True
   time_delta = clock.tick(60)/1000
   pause_button.set_text("Pause" if phy_running else "Resume")
   for event in pygame.event.get():
      manager.process_events(event)
      manager2.process_events(event)
      if event.type == pygame.QUIT:
         Running = False
          
      if state == "sim":
         if event.type == pygame_gui.UI_BUTTON_PRESSED:
              if event.ui_element == pause_button:
                 phy_running = not phy_running
         if not phy_running:        
            if event.type == pygame.MOUSEBUTTONDOWN:      
               mouse_pos = np.array(pygame.mouse.get_pos(), dtype=float) 
               for i in range(len(sim.bodies)):   #checking if a body selected
                  if np.linalg.norm(mouse_pos-sim.bodies[i].pos)<sim.bodies[i].radius:
                     sim.bodies[i].E_calc = True
                     


                    
      if state == "Menu":
        veldir = (tip-origin)/np.linalg.norm(tip-origin)
        mouse_pos = np.array(pygame.mouse.get_pos(), dtype=float) #check if velpos change
        if event.type == pygame.MOUSEBUTTONUP:
          dragging = False
        if event.type == pygame.MOUSEBUTTONDOWN:    ##(this loop is event driven)
          if np.linalg.norm(mouse_pos - tip)<5:     ##thus seperated from the other
             dragging = True
             
          if not slider_mass.hover_point(*mouse_pos) and not slider_G.hover_point(*mouse_pos) and not start_button.hover_point(*mouse_pos) and not vel_slider.hover_point(*mouse_pos) and np.linalg.norm(mouse_pos-tip)>5:
             if first == True:
               sim.bodies.append(masses(float(mass_value.text),mouse_pos, (vel_slider.get_current_value()) *veldir, np.zeros(2), np.zeros(2), 10*float(mass_value.text)**(1/3), [], random.randrange(0,255,5), random.randrange(0,255,5), random.randrange(0,255,5), 0,[], 0,[], False,[]))
               sim.arrows.append(arrows(mouse_pos,np.zeros(2)))
               first = False
             else:
               for body in sim.bodies:
                 if np.linalg.norm(mouse_pos-body.pos)<body.radius+10*float(mass_value.text)**(1/3):
                   can_create = False
                 
               if can_create:
                  sim.bodies.append(masses(float(mass_value.text),mouse_pos, (vel_slider.get_current_value()) *veldir, np.zeros(2), np.zeros(2), 10*float(mass_value.text)**(1/3), [], random.randrange(0,255,5), random.randrange(0,255,5), random.randrange(0,255,5), 0,[], 0,[], False,[]))
                  sim.arrows.append(arrows(mouse_pos,np.zeros(2)))
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
           if event.ui_element == start_button:
              state = "sim"
        if dragging:
           tip = mouse_pos
           
                  
   if state == "Menu":
      screen.fill((0,0,0))     
      mass_value.set_text(f"{slider_mass.get_current_value():.2f}")
      G_value.set_text(f"{slider_G.get_current_value():.2f}") #to check if sliders changed
      vel_value.set_text(f"{vel_slider.get_current_value():.2f}")
      for body in sim.bodies:
           body.draw_body()   
        
      manager.update(time_delta)
      manager.draw_ui(screen)
      pygame.draw.line(screen,(255,250,0),origin,tip,5)
      pygame.draw.circle(screen,(255,250,0),tip,10)
      pygame.display.flip()

   if state == "sim":
     screen.fill((0,0,0))
     manager2.update(time_delta)
     manager2.draw_ui(screen)

     sim.gravity_calc(slider_G)         
     for i in range(len(sim.bodies)):
        sim.bodies[i].draw_body()
        sim.bodies[i].draw_trail()
        if sim.bodies[i].E_calc==True:
           if phy_running:
             sim.GPE_calc(sim.bodies[i],slider_G)
             sim.bodies[i].GPE_val.append(sim.bodies[i].GPE)
             sim.bodies[i].KE_calc()
             sim.bodies[i].KE_val.append(sim.bodies[i].KE)
             t += sim.bodies[i].dt
             sim.bodies[i].t_val.append(t)
           if sim.bodies[i].plot == None:
              sim.bodies[i].plot= pg.PlotWidget()
              sim.bodies[i].curve_KE = sim.bodies[i].plot.plot(pen='r', name="KE")
              sim.bodies[i].curve_PE = sim.bodies[i].plot.plot(pen= 'y', name = "PE")
              sim.bodies[i].plot.show()
           if sim.bodies[i].plot != None:
               sim.bodies[i].curve_KE.setData(sim.bodies[i].t_val,sim.bodies[i].KE_val)
               sim.bodies[i].curve_PE.setData(sim.bodies[i].t_val,sim.bodies[i].GPE_val)

           
        if phy_running:
          sim.bodies[i].acc_calc()
          sim.bodies[i].vel_calc()
          sim.bodies[i].pos_calc()
             
     for arrow in sim.arrows:
        sim.arrow_calc() 
        arrow.draw_arrow()  
     pygame.display.flip()
     

   

   
   
   


   
    