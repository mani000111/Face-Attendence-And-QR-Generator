from tkinter import *
import time,threading,frs_api


def runapp():
    global frs
    frs = Tk()
    frs.focus()

    #window config
    frs.geometry("500x650")
    frs.configure(bg="#4b4a49")
    fg_global = "white"
    bg_global = "#4b4a49"
    frs.title("FACE   RECOGNITION   ATTENDANCE")
    frs.resizable(False,False)#disable maximize button

    #reset_user_conf_level
    def reset_switch_operator(switch):
        if switch=="conf":
            frs_api.reset_present_conf_level=True
        elif switch=="attendance":
            frs_api.reset_attendance_switch=True
        elif switch=="qr":
            frs_api.reset_qr_gena_list_switch=True


    #on close window func
    def exit_func():
        frs.destroy()


    #get current date and time func
    def get_date_time():
        #current date
        current_date = time.ctime().split(" ")
        current_date = f"{current_date[3]} - {current_date[1]} - {current_date[5]}"
        
        #current time
        current_time = time.ctime().split(" ")[4]

        return current_date,current_time

    #clear window func
    def clear_and_recreate_window():
        print("\t\t\t\nClear Attendance list")
        global reg_no_c
        reg_no_c = 1
        main_frame.destroy()
        create_main_window()

    #default label

    #main frame
    def create_main_window():
        global main_frame

        #main frame
        main_frame = Frame(frs,bg=bg_global,highlightbackground=bg_global)
        main_frame.pack(side=TOP)


        #reg no label
        serial_label = Label(main_frame,text="S NO",bg=bg_global,fg="green2",font=(None,12,"bold"),pady=20)
        serial_label.grid(row=0,column=0)


        #name label
        name_label = Label(main_frame,text="NAME",bg=bg_global,fg="green2",font=(None,12,"bold"),padx=50,pady=20)
        name_label.grid(row=0,column=1)


        #status label
        status_label = Label(main_frame,text="STATUS",bg=bg_global,fg="green2",font=(None,12,"bold"),padx=10,pady=20)
        status_label.grid(row=0,column=2)


        #date label
        date_label = Label(main_frame,text="DATE",bg=bg_global,fg="green2",font=(None,12,"bold"),padx=10,pady=20)
        date_label.grid(row=0,column=3)


        #time label
        time_label = Label(main_frame,text="TIME",bg=bg_global,fg="green2",font=(None,12,"bold"),pady=20)
        time_label.grid(row=0,column=4)

    #call main window
    create_main_window()


    #create clear button
    clear_button_frame = Frame(frs)
    clear_button_frame.pack(side=BOTTOM,fill=BOTH)
    clear_button = Button(clear_button_frame,text="Clear data",command=clear_and_recreate_window,bg="green2",fg="black",activebackground=bg_global,activeforeground="green2",font=(None,10,"bold"))
    clear_button.pack(side=RIGHT,padx=20)

    #reset present conf level button
    reset_users_present_level_button = Button(clear_button_frame,text="rst conf_level",command=lambda:reset_switch_operator("conf"))
    reset_users_present_level_button.pack(side=LEFT,padx=20)

    #reset attendance list
    reset_attendance_button = Button(clear_button_frame,text="rst_att",command=lambda:reset_switch_operator("attendance"))
    reset_attendance_button.pack(side=LEFT,padx=20)

    #reset generated qr list
    reset_gena_qr_list_button = Button(clear_button_frame,text="rst_qr_L",command=lambda:reset_switch_operator("qr"))
    reset_gena_qr_list_button.pack(side=LEFT,padx=20)


    global reg_no_c
    reg_no_c = 1
    global make_attendance

    #mark attendance
    def make_attendance(username):
        print(username," Present")
        global reg_no_c

        current_date,current_time = get_date_time()

        #add serial
        new_serial =Label(main_frame,text=str(reg_no_c)+" )",bg=bg_global,fg=fg_global,font=(None,10,"bold"))
        new_serial.grid(row=reg_no_c,column=0)

        #add name
        new_user = Label(main_frame,text=username,bg=bg_global,fg=fg_global,font=(None,10,"bold"))
        new_user.grid(row=reg_no_c,column=1)


        #add status)
        new_status = Label(main_frame,text="PRESENT",bg=bg_global,fg=fg_global,font=(None,10,"bold"))
        new_status.grid(row=reg_no_c,column=2)

        #date
        # new_date = username+str(reg_no_c)
        new_date = Label(main_frame,text=current_date,bg=bg_global,fg=fg_global,font=(None,10,"bold"),padx=10)
        new_date.grid(row=reg_no_c,column=3)

        #time        
        new_time = Label(main_frame,text=current_time,bg=bg_global,fg=fg_global,font=(None,10,"bold"))
        new_time.grid(row=reg_no_c,column=4)

        reg_no_c+=1

    frs.protocol("WM_DELETE_WINDOW",exit_func)
    frs.mainloop()

run_app = threading.Thread(target=runapp)
run_app.start()
