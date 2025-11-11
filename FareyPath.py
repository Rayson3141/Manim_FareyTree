from manimlib import config
from manimlib.imports import *
import numpy as np

config.disable_caching = True

class treee(Scene):
    def construct(self):
        #constants
        numerator = 8
        denominator = 3
        n = numerator/np.gcd(numerator,denominator)
        d = denominator/np.gcd(numerator,denominator)
        scale_factor = 2
        spacing = 2.5
        ratio = 0.7

        Farey_Path = self.Eucl(n,d)
        final_scale = (0.45*6)/len(Farey_Path)

        Initial_Vect = [1,1]
        Row_AddL = [[1,1],[0,1]]
        Row_AddR = [[1,0],[1,1]]
        MatTran = [[1,0],[0,1]]
 

        #Start
        circle = VGroup(
            Circle(radius=0.5, color=BLUE, stroke_width=scale_factor*3).set_fill(BLACK, opacity=1),
            TexMobject(r"\frac{1}{1}").scale(scale_factor*0.4)
        ).center()
        circle.move_to(DOWN)

        self.play(ShowCreation(circle))
    
        for i in Farey_Path:
            # ShowCreation the Branches
            Mat = [[Initial_Vect[0] + MatTran[0][0],Initial_Vect[1] + MatTran[0][1]], 
                   [Initial_Vect[0] + MatTran[1][0],Initial_Vect[1] + MatTran[1][1]]]
            self.Gen_Branch(ratio,spacing,scale_factor,Mat)

            # Update after a step down the tree
            if i == 1:
                MatTran = np.matmul(Row_AddL,MatTran)
                Initial_Vect = Mat[1]
            else:
                MatTran = np.matmul(Row_AddR,MatTran)
                Initial_Vect = Mat[0]

            s = Group(*self.mobjects)
            self.play(ApplyMethod(s.shift, -spacing * (ratio * i * RIGHT + DOWN)))
        

        #End
        circle_f = VGroup(
            Circle(radius=1, color=YELLOW, stroke_width=scale_factor*3).set_fill(BLACK, opacity=0)
        ).move_to(DOWN)
        self.play(ShowCreation(circle_f))
        self.wait(1)
        
        #Final Scale
        s = Group(*self.mobjects)
        # s_f = Group(*self.mobjects).center()
        # self.play(Transform(s,s_f))
        # self.play(s.animate.shift(-1*s.get_center()).scale(final_scale))
        self.play(ApplyMethod(s.shift, -1 * s.get_center()))
        self.play(ApplyMethod(s.scale, final_scale))
        self.wait(1)



    def Gen_Branch(self,ratio,spacing,scale_factor,Mat):
        
        Left_Circ = r"\mathbf{\frac{"+str(Mat[0][0])+"}{"+str(Mat[0][1])+"}}"
        Right_Circ = r"\mathbf{\frac{"+str(Mat[1][0])+"}{"+str(Mat[1][1])+"}}"

        circle1 = Group(
            # Circle(radius=scale_factor * 0.375, color=BLUE, stroke_width=scale_factor*3).set_fill(BLACK, opacity=1),
            TexMobject(Left_Circ).scale(scale_factor*0.4)
        ).move_to(spacing*(ratio*LEFT + DOWN))

        circle2 = Group(
            # Circle(radius=scale_factor * 0.375, color=BLUE, stroke_width=scale_factor*3).set_fill(BLACK, opacity=1),
            TexMobject(Right_Circ).scale(scale_factor*0.4)
        ).move_to(spacing*(ratio*RIGHT + DOWN))

        arrow1 = Line(
                [0,0,0], 
                circle1.get_center(),
                buff=0,
                stroke_width=scale_factor*3,
                z_index=-10
            )
        
        arrow2 = Line(
                [0,0,0], 
                circle2.get_center(),
                buff=0,
                stroke_width=scale_factor*3,
                z_index=-10
            )

        circle1.move_to(spacing*(ratio*LEFT +DOWN)+ DOWN)
        circle2.move_to(spacing*(ratio*RIGHT+DOWN)+ DOWN)
        
        self.add(circle1,circle2,arrow1,arrow2)


    def Eucl(self,n,d):
        Farey_path = []
        num = [n,d]
        R=1
        L=-1

        while sum(num)>1:
            if num[0]<num[1]:
                Farey_path.append(R)
                num = [num[0],num[1]-num[0]]
            else:
                Farey_path.append(L)
                num = [num[0]-num[1],num[1]]  

        return Farey_path[:-1]
