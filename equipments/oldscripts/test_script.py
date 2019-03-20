from tkinter import *



master=Tk()
canvas=Canvas(master,width=100,height=100,bg='red')
canvas.pack()

#poly1=canvas.create_polygon(50,20,50,50,70,50,70,20,fill="gold")
#poly2=canvas.create_polygon(50,20,60,10,80,10,70,20,fill="grey")
#poly3=canvas.create_polygon(80,10,80,40,70,50,70,20,fill="gold")
height=20
width=30
slack=10
x,y=50,20
a1,a2=x,y
b1,b2=a1,a2+height
c1,c2=b1+width,b2
d1,d2=c1+slack,c2-slack
e1,e2=d1,d2-height
f1,f2=e1-width,e2
poly4=canvas.create_polygon(a1,a2,b1,b2,c1,c2,d1,d2,e1,e2,f1,f2,fill="grey")







master.mainloop()