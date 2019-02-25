

from all_dependencies import *

portal_width=200
portal_height=200


onboarding_dependency_file=""


class Onboarding_Portal():


    def __init__(self):
        #self.onboarding_portal_flag=0
        #self.onboarding = Tk()
        #self.onboarding_frame = Frame(self.onboarding)
        pass

    def checking_equipments_compatibility(self):
        #self.first_component
        #self.second_component
        pass# )


    def add_widgets_to_onboarding(self):
        self.first_equipment_label=Label(self.onboarding_frame,text="First Equipment")
        self.second_equipment_label=Label(self.onboarding_frame,text="Second Equipment")
        self.first_equipment_entry = Entry(self.onboarding_frame)
        self.second_equipment_entry=Entry(self.onboarding_frame)
        self.comment_section=Entry(self.onboarding_frame)
        self.first_equipment_label.grid(row=0,column=0)
        self.first_equipment_entry.grid(row=0,column=1)
        self.second_equipment_label.grid(row=1,column=0)
        self.second_equipment_entry.grid(row=1,column=1)
        self.comment_section.grid(row=2,column=0,rowspan=4,columnspan=2)


    def checking_services_possible_on_path(self):
        pass


    def checking_ports_compatibility(self):
        pass


    def checking_service_compatibility_on_port(self):
        pass


    def load_onboarding_rules(self):
        pass

    def create_onboarding_portal_window(self,master,node_frame):
        self.node_frame=node_frame
        #self.node_frame.onboarding_portal_button.destroy()
        #if self.onboarding_portal_flag == 0:
        self.onboarding_frame=Frame(self.node_frame.network_frame.canvas)
        self.onboarding_window=self.node_frame.network_frame.canvas.create_window(canvas_width,100,window=self.onboarding_frame,width=100,height=canvas_height)
        self.onboarding_portal_flag =1
        self.onboarding_frame.config(width=300,height=1000,bg='steelblue')
        self.onboarding_frame.pack(side="right")
        self.add_widgets_to_onboarding()

    def exit_onboarding_portal(self):
        self.onboarding_frame.destroy()
        self.node_frame.moving_back_to_verifier()

    def create_cell_on_portal(self,x,y,width,height):
        pass


'''
onboarding=Tk()
onboarding_portal=Onboarding_Portal()
onboarding_portal.create_onboarding_portal_window(onboarding)
onboarding.mainloop()
'''