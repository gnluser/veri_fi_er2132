from tkinter import *
import networkx as nx

master=Tk()
'''
frame=Frame(master,height=200,width=300,bd=30)
frame.pack()
canvas=Canvas(frame,bg='pink')#height=200,width=100)
canvas.pack(side=RIGHT,fill=BOTH,expand=True)
#frame.grid(row=1,column=0)
#frame2=Frame(master,height=200,width=100,bg="red")
#f@rame2.pack()
new_frame=Frame(master,height=200,width=100,bd=30)
canvas2=Canvas(new_frame,bg='yellow')
new_frame.pack(side=LEFT)
canvas2.pack(side=RIGHT,fill=BOTH,expand=True)
#Label1=Label(canvas,text="Testing label")
#Label1.pack()
frame=Frame(master)
frame.pack(side=LEFT)
master.mainloop()
'''


g=nx.Graph()
edge_list=[[1,2],[1,4],[1,3],[2,3],[3,5]]
g.add_edges_from(edge_list)
print(g.node)
#print(sorted(g.graph.node,key= lambda node : g.degree(node)))
print(list(g.degree(g.node)))
for term in g.degree(g.node):
    print(term[1])
print(sorted(list([g.degree(g.node)]),key= lambda x:x[1]))

#f1 = Frame(master, bd=1, relief=SUNKEN,height=100,width=100)
#f2 = Frame(master, bd=1, relief=SUNKEN)
#split = 0.5
#f1.place(rely=0, relheight=split, relwidth=1)
#f2.place(rely=split, relheight=1.0-split, relwidth=1)
#f1.pack()
#f2.pack()
frame=Frame(master,bg='black')
frame.pack()
canvas=Canvas(master,bg='yellow')
canvas.pack(side=LEFT)#canvas.grid(row=0,column=1)
#canvas2=Canvas(master,bg="pink")
#canvas2.pack(side=RIGHT)#canvas2.grid(row=0,column=0)
master.mainloop()

