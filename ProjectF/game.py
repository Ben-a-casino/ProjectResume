import tkinter as tk
import numpy as np
import math
import time

from vec2d import Point
from vec2d import Vec2D
from convexpolygon import ConvexPolygon


class GameObject(ConvexPolygon):

    # Define a game object which inherits Convex Polygon
    
    def __init__(self, points, v_t = Vec2D(), v_r = 0.0, s = 1.0):

        # Attributes are linear velocity
        # rotational velocity
        # and a scale factor
        
        super().__init__(points)
                    
        self.v_t = v_t
        self.v_r = v_r
        self.s_f = s
        
        return
        
    def evolve(self, dt = 1):

        # Update the polygon every time step
        
        self.translate(self.v_t * dt)
        self.rotate(self.v_r * dt)
        self.scale(self.s_f, self.s_f)
        
        return

    def set_id(self, i):

        # Associate an ID to each game object
        
        self.obj_id = i
        return
    


class App(tk.Tk):

    # Use Tkinter with Canvas to create game GUI
    # Refer to : https://docs.python.org/3/library/tkinter.html
    # Refer to : https://tkdocs.com/tutorial/canvas.html
    
    def __init__(self):

        # Create a window
        
        super().__init__()

        self.width  = 900
        self.height = 900
        
        self.C = tk.Canvas(self, width = self.width - 100, height = self.height - 100, bg="#9ebcda")
        self.C.pack()
        self.C.place(x = 50, y = 50)
        self.title('Tkinter Polygon Game')

        # Create random number generator
        self.prng = np.random.default_rng()

        self.set_key_bindings()
        self.reset_vars()
        
        
    def set_key_bindings(self):

        # Set key bindings to move polygon
        self.bind("<Key-Up>", self.handle_up)
        self.bind("<Key-Down>", self.handle_down)
        self.bind("<Key-Left>", self.handle_left)
        self.bind("<Key-Right>", self.handle_right)

        # Set key bindings to rotate and scale
        self.bind("<Key-a>", self.handle_rotate_left)
        self.bind("<Key-d>", self.handle_rotate_right)
        self.bind("<Key-s>", self.handle_shrink)

        # Set key bindings to restart and quit
        self.bind("<Key-r>", self.handle_restart)
        self.bind("<Key-q>", self.handle_quit)

        
    def reset_vars(self):

        # Reset game variables
        self.polygons   = []
        self.shrink     = False
        self.event_list = []
        self.text_id    = None
        self.score_id   = None
        self.score      = 0.0
        self.game_ended = False
        
    def start_game(self):

        # Creating the triangle in the middle
        self.add_polygon(self.width//2, self.height//2, nfaces = 3, size = 100)
        self.polygons[0].v_t = Vec2D(0,0)
        self.polygons[0].v_r = 0

        self.tri_size        = 100

        # Add an event to add polygons
        self.event_list.append(self.after(100, self.add_random_polygon))
        # Add an event to move polygons
        self.event_list.append(self.after(100, self.move_polygons))

        # Create score text object
        self.score_id = self.C.create_text(50, 50, text = 'Score = 0')
        
        return
    
    # All handle methods written below handle keyboard input in gametime
    
    def handle_up(self, event):

        self.polygons[0].v_t = self.polygons[0].v_t + Vec2D(0,-0.1)

    def handle_down(self, event):

        self.polygons[0].v_t = self.polygons[0].v_t + Vec2D(0,0.1)
      
    def handle_left(self, event):

        self.polygons[0].v_t = self.polygons[0].v_t + Vec2D(-0.1,0)

    def handle_right(self, event):

        self.polygons[0].v_t = self.polygons[0].v_t + Vec2D(0.1,0)

    def handle_rotate_left(self, event):

        self.polygons[0].v_r += -0.01

    def handle_rotate_right(self, event):

        self.polygons[0].v_r += 0.01

    def handle_shrink(self, event):

        dr = self.polygons[0].get_centroid() - self.polygons[0].verts[0]
        
        if (dr.x**2 + dr.y**2) >= 20**2 :
            self.polygons[0].scale(0.9, 0.9)

        if not self.shrink:
            self.event_list.append(self.after(100, self.expand_polygon))
               

            
    def handle_quit(self, event):

        # Clear all variables and destroy window
        
        self.clear_frame_vars()
        self.C.delete('all')
        self.C.quit()
        self.destroy()


        
    def handle_restart(self, event):

        # Reset game vars and restart game
        
        time.sleep(1)
        if not self.game_ended:
            self.end_game()
        self.clear_frame_vars()
        self.event_list.append(self.after(100, self.start_game))


        
    def update_score(self):

        # Update the scoreboard
        self.score += 0.1
        self.C.itemconfigure(self.score_id, text = 'Score = '+ str(int(self.score)))
        

        
    def clear_frame_vars(self):

        for p in self.polygons:
            self.C.delete(p.obj_id)
        
        if self.text_id is not None:
            self.C.delete(self.text_id)

        if self.score_id is not None:
            self.C.delete(self.score_id)

        self.reset_vars()

        
            
            
    def cancel_future_events(self):

        # Cancel all future events
        
        for e in self.event_list:
            self.after_cancel(e)

        return

    
    def expand_polygon(self):

        # Expand polygons back to their original size
        
        dr = self.polygons[0].get_centroid() - self.polygons[0].verts[0]
        
        if ((dr.x**2 + dr.y**2) < self.tri_size**2) :
            self.polygons[0].scale(1.01, 1.01)
            self.event_list.append(self.after(100, self.expand_polygon))
            self.shrink = True
        else:
            self.shrink = False

        return


    
    def evolve_all_polygons(self):

        # Update the polygons every time step on Canvas
        
        for p in self.polygons:

            i = p.obj_id
            p.evolve()
            self.C.coords(i, self.get_points(p))                


            
    def point_in_bounds(self, p):

        # Check if a point is within boundary of window
        
        if p.x > self.width or p.x < 0:
            return False

        if p.y > self.height or p.y < 0:
            return False

        return True



    
    def move_polygons(self):

        # Update all polygons 
        
        self.evolve_all_polygons()
        
        to_del = []

        p = self.polygons[0]
        i = p.obj_id            
        c = p.get_centroid()
       
        if not self.point_in_bounds(c):
            
            to_del.append(i)
            self.event_list.append(self.after(1, self.end_game))
            return

        # If polygons move outside frame delete them
        
        for q in self.polygons:
            
            j = q.obj_id
                
            if j == i:
                continue

            c = q.get_centroid()

            if not self.point_in_bounds(c):
                to_del.append(j)

            # Check if any polygon intersects with the triange

            if (p & q):
                to_del.append(i)

                self.C.itemconfig(i, fill='red')
                self.C.itemconfig(j, fill='red')

                
        for o in to_del:
            
            # If triangle overlaps with another polygon end game
            if o == i:
                self.event_list.append(self.after(10, self.end_game))
                return

            self.C.delete(o)
            
        self.event_list.append(self.after(10, self.move_polygons))
        self.event_list.append(self.after(10, self.update_score))

        return


    
    def end_game(self):

        # Cancel all future events and end game

        self.game_ended = True
        self.cancel_future_events()
        self.text_id = self.C.create_text(self.width//2, self.height//2, text="Game Over !!  Enter (i) Enter q to Quit (ii)  r to restart", fill = 'black')
        
        return

    
    def get_rand_color(self):

        # Get a random color
        
        color = '#'

        for i in range(3):
            rgb = self.prng.integers(0,255)
            color += '{0:2X}'.format(rgb) if rgb > 15 else '0'+'{:X}'.format(rgb)

        return color


    
    @staticmethod
    def get_regular_polygon(n, R):

        # Create vertices of a regular polygon
        
        points = []
        for i in range(n):
            points += [Point(R*math.cos((2.0*math.pi*i)/n), (R*math.sin((2.0*math.pi*i)/n))) ]
           
        return points

    
    @staticmethod
    def get_points(g):

        # Get list of points from game object        
        
        points = []
        for p in g.verts:
            points += [p.x, p.y]
        return points


        
    
    def add_polygon(self, x, y, nfaces = None, size = 80, scale_factor = 1.0 ):

        # Add the polygon object to canvas
        
        nfaces   = self.prng.integers(low=4,high=10) if nfaces is None else nfaces
        pgon_pts = self.get_regular_polygon(nfaces, size)

        vx = float(self.prng.uniform(0,1)) if (x < self.width  // 2) else float(-self.prng.uniform(0,1))
        vy = float(self.prng.uniform(0,1)) if (y < self.height // 2) else float(-self.prng.uniform(0,1))
        
        # Create a game object
        obj      = GameObject( pgon_pts, Vec2D(vx, vy), float( 0.01*math.tau*self.prng.random()), scale_factor )
        
        id_part  = self.C.create_polygon(self.get_points(obj), fill=self.get_rand_color(), width=2)

        obj.set_id(id_part)       

        self.polygons.append(obj)

        obj.translate(Vec2D(x, y))
        
        return

    
    def add_random_polygon(self):

        # Method to add a random polygon in the corners
        
        # Bounds 
        bounds = [(1,100), (self.width - 100, self.width)]
        rand_2 = self.prng.integers ( low=0, high=2, size = 2 )
        
        pos_x    = int(self.prng.integers ( low=bounds[rand_2[0]][0], high=bounds[rand_2[0]][1] ))
        pos_y    = int(self.prng.integers ( low=bounds[rand_2[1]][0], high=bounds[rand_2[1]][1] ))
        s_factor = float(self.prng.uniform(low = 0.999, high = 1.001))
        
        self.add_polygon( x = pos_x, y = pos_y,
                          size = int(self.prng.integers(low = 20, high = 50 )), scale_factor = s_factor )
        self.event_list.append(self.after(1000, self.add_random_polygon))
        
        return

    

if __name__ == '__main__':

    app = App()
    app.geometry('900x900+50+50')       
    app.after(100, app.start_game)
    app.mainloop()

    

