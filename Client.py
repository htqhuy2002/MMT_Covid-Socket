import socket
from tkinter import *
from tkinter.messagebox import *
import customtkinter
from PIL import ImageTk, Image
from tkinter import ttk
import sys

def giaodien_dangnhap():
    def background_dangnhap():
        img = Image.open("pic/bg_dangnhap.png")
        img = img.resize((600, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(root, image=img)
        panel.image = img
        panel.place(x=0,y=0)

    def background_tracuu():
        img = Image.open("pic/bg_tracuu.png")
        img = img.resize((600, 500), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(root, image=img)
        panel.image = img
        panel.place(x=0,y=0) 

    def recieve_data():
        data = []
        for i in range(0,63):
            data.append([])
            msg = client.recv(1024).decode(FORMAT)
            data[i].append(msg)
            msg = "Đã nhận"
            client.sendall(msg.encode(FORMAT))

            msg = client.recv(1024).decode(FORMAT)
            data[i].append(msg)
            msg = "Đã nhận"
            client.sendall(msg.encode(FORMAT))

            msg = client.recv(1024).decode(FORMAT)
            data[i].append(msg)
            msg = "Đã nhận"
            client.sendall(msg.encode(FORMAT))

            msg = client.recv(1024).decode(FORMAT)
            data[i].append(msg)
            msg = "Đã nhận"
            client.sendall(msg.encode(FORMAT))
        
        return data

    def tracuu():
        def click_dangxuat():
            try:
                if(askyesno("Bạn muốn đăng xuất?", "Yes or No")):
                    msg = "Client đăng xuất"
                    client.sendall(msg.encode(FORMAT))
                    msg = client.recv(1024).decode(FORMAT)
                    msg = entry_user_name.get()
                    client.sendall(msg.encode(FORMAT))
                    msg = client.recv(1024).decode(FORMAT)
                    giaodien_dangnhap()
                    return True
                else:
                    False
            except:
                showerror("Thông báo","Máy chủ đang bảo trì! Vui lòng quay lại sau!")
                giaodien_dangnhap()

        def timkiem_tinhthanh(tinhthanh,data):
            for i in range(0,63):
                if(tinhthanh == data[i][0]):
                    return i
            return -1

        def click_timkiem():
            try:           
                if(entry_time.get()!=""):
                    date = entry_time.get()
                    client.sendall(date.encode(FORMAT))
                    msg = client.recv(1024).decode(FORMAT)
                    if(msg=="Sẵn sàng gửi dữ liệu"):
                        data = recieve_data()
                        tinhthanh = entry_tt.get()
                        index = timkiem_tinhthanh(tinhthanh,data)

                        if(tinhthanh == ""):
                            for i in tree.get_children():
                                tree.delete(i)
                            for i in range(0,63):
                                tree.insert('', END,values =(data[i][0], data[i][1], data[i][2],data[i][3]))
                        else:
                            tinhthanh = entry_tt.get()
                            index = timkiem_tinhthanh(tinhthanh,data)
                            if(index==-1):
                                for i in tree.get_children():
                                    tree.delete(i)
                                tree.insert('', END,values =("Không tồn tại!",'','',''))
                            else:
                                for i in tree.get_children():
                                    tree.delete(i)
                                tree.insert('', END,values =(data[index][0], data[index][1], data[index][2],data[index][3]))
                    else:
                        for i in tree.get_children():
                            tree.delete(i)
                        tree.insert('', END,values =("Không tồn tại!",'','',''))
            except:
                showerror("Thông báo","Máy chủ đang bảo trì! Vui lòng quay lại sau!")
                giaodien_dangnhap()

        def on_closing():
            if askyesno("Bạn muốn thoát?", "Yes or No"):
                if(click_dangxuat()):
                    root.destroy()
                    try:
                        msg = "Thoat"
                        client.sendall(msg.encode(FORMAT))
                        client.close()
                    except:
                        pass
    
        root.title("Tra cứu thông tin Covid - 19")
        root.geometry("600x500")
        background_tracuu()

        tree = ttk.Treeview(root, selectmode ='browse',height=15)
        tree.place(x=10,y=150)
        tree["columns"] = ("1", "2", "3","4")
        tree['show'] = 'headings'
        
        tree.column("1", width = 140, anchor ='w')
        tree.column("2", width = 140, anchor ='e')
        tree.column("3", width = 140, anchor ='e')
        tree.column("4", width = 140, anchor ='e')

        tree.heading("1", text ="Tỉnh - Thành phố")
        tree.heading("2", text ="Số ca nhiễm")
        tree.heading("3", text ="Số ca tử vong")
        tree.heading("4", text ="Số ca mắc mới")

        vsb = Scrollbar(root, orient="vertical", command=tree.yview)
        vsb.place(x=575,y=150,height=325)
        tree.configure(yscrollcommand=vsb.set)

        Hi = Label(root,text = "Xin chào, "+entry_user_name.get()+" !",fg="#00008b",bg="#fbe5d6",font=("Arial Bold",12))
        Hi.place(x=70,y=28)

        signout_button = customtkinter.CTkButton(master=root,text="Đăng xuất",
                                                width=100,height=25,bg_color="#fbe5d6",
                                                fg_color="#ffa500",corner_radius=50,command=click_dangxuat)
        signout_button.place(x=480,y=27)

        tt = Label(root,text = "Tỉnh, thành: ",fg="#00008b",bg="#bf9000",font=("Arial Bold",10))
        tt.place(x=20,y=80)

        entry_tt = customtkinter.CTkEntry(master=root, width=120,bg_color="#bf9000")
        entry_tt.place(x=105,y=78)

        time = Label(root,text = "Thời gian: ",fg="#00008b",bg="#bf9000",font=("Arial Bold",10))
        time.place(x=230,y=80)

        entry_time = customtkinter.CTkEntry(master=root, width=120,bg_color="#bf9000")
        entry_time.place(x=300,y=78)

        find_button = customtkinter.CTkButton(master=root,text="Tìm kiếm",
                                                width=100,height=25,bg_color="#bf9000",
                                                fg_color="#00ffff",corner_radius=50,command=click_timkiem)
        find_button.place(x=480,y=78)

        root.protocol("WM_DELETE_WINDOW", on_closing)
            
    def click_dangnhap():
        try:
            if(entry_user_name.get()=="" or entry_password.get()==""):
                showwarning("Cảnh báo đăng nhập", "Bạn cần phải nhập tài khoản và mật khẩu!")
            else:
                msg = "Client xin đăng nhập"
                client.sendall(msg.encode(FORMAT))
                msg = client.recv(1024).decode(FORMAT)
                msg = entry_user_name.get()
                client.sendall(msg.encode(FORMAT))
                msg = client.recv(1024).decode(FORMAT)
                msg = entry_password.get()
                client.sendall(msg.encode(FORMAT))
                msg = client.recv(1024).decode(FORMAT)
                if(msg=="Đăng nhập thành công!"):
                    showinfo("Thông báo",msg)
                    client.sendall(msg.encode(FORMAT))
                    tracuu()
                else:
                    showwarning("Thông báo", msg)
                    client.sendall(msg.encode(FORMAT))
        except:
            showerror("Thông báo","Máy chủ đang bảo trì! Vui lòng quay lại sau!")

    def click_dangki():
        giaodien_dangki()
        
    def close():
        if askyesno("Bạn muốn thoát?", "Yes or No"):
            root.destroy()
        try:
            msg = "Thoat"
            client.sendall(msg.encode(FORMAT))
            client.close()
        except:
            pass
    
    root.title("Đăng nhập")
    root.geometry("600x300")
    background_dangnhap()
    sign_in_x = 16
    sign_in_y = 84

    sign_in_frame = Frame(root,height=200,width=180,bg="#800000")
    sign_in_frame.place(x=sign_in_x,y=sign_in_y)
    sign_in_frame = Frame(root,height=196,width=176,bg="#add8e6")
    sign_in_frame.place(x=sign_in_x+2,y=sign_in_y+2)

    user_name = Label(root,text = "Tài khoản:",fg="#00008b",font=("Arial Bold",10),bg="#add8e6")
    user_name.place(x=sign_in_x+10,y=sign_in_y+10)
    entry_user_name = customtkinter.CTkEntry(master=root, width=160,bg_color="#add8e6")
    entry_user_name.place(x=sign_in_x+10,y=sign_in_y+30)

    password = Label(root,text = "Mật khẩu:",fg="#00008b",font=("Arial Bold",10),bg="#add8e6")
    password.place(x=sign_in_x+10,y=sign_in_y+60)
    entry_password = customtkinter.CTkEntry(master=root, width=160,bg_color="#add8e6")
    entry_password.place(x=sign_in_x+10,y=sign_in_y+80)

    sign_in_button = customtkinter.CTkButton(master=root,text="Đăng nhập",
                                            width=160,height=25,bg_color="#add8e6",
                                            fg_color="#f0e68c",corner_radius=50,command=click_dangnhap)
    sign_in_button.place(x=sign_in_x+10,y=sign_in_y+120)

    sign_in_button = customtkinter.CTkButton(master=root,text="Đăng kí",
                                            width=160,height=25,bg_color="#add8e6",
                                            fg_color="#f0e68c",corner_radius=50,command=click_dangki)
    sign_in_button.place(x=sign_in_x+10,y=sign_in_y+150)

    root.protocol("WM_DELETE_WINDOW", close)

def giaodien_dangki():
    def background_dangki():
        img = Image.open("pic/bg_dangki.png")
        img = img.resize((250, 350), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(root, image=img)
        panel.image = img
        panel.place(x=0,y=0) 

    def click_hoanthanhdangki():
        try:
            if(entry_user_name.get()=="" or entry_password.get()=="" or entry_repassword.get()==""):
                showwarning("Cảnh báo đăng kí", "Bạn cần phải nhập đầy đủ thông tin!")
            elif entry_password.get()!=entry_repassword.get():
                showwarning("Cảnh báo đăng kí", "Mật khẩu nhập lại không đúng!")
            else:
                msg = "Client xin đăng kí"
                client.sendall(msg.encode(FORMAT))
                msg = client.recv(1024).decode(FORMAT)
                msg = entry_user_name.get()
                client.sendall(msg.encode(FORMAT))
                msg = client.recv(1024).decode(FORMAT)
                msg = entry_password.get()
                client.sendall(msg.encode(FORMAT))
                msg = client.recv(1024).decode(FORMAT)
                if(msg=="Đăng kí thành công!"):
                    showinfo("Thông báo",msg)
                    msg="Hoàn thành đăng kí"
                    client.sendall(msg.encode(FORMAT))
                    giaodien_dangnhap()
                else:
                    showwarning("Thông báo", msg)
                    msg="support"
                    client.sendall(msg.encode(FORMAT))
        except:
            showerror("Thông báo","Máy chủ đang bảo trì! Vui lòng quay lại sau!")
            giaodien_dangnhap()

    def click_quaylai():
        giaodien_dangnhap()

    root.title("Đăng kí")
    root.geometry("250x350")
    background_dangki()

    x = 20
    y = 100

    frame1 = Frame(root,height=240,width=210,bg="#800000")
    frame1.place(x=x,y=y)
    frame2 = Frame(root,height=236,width=206,bg="#add8e6")
    frame2.place(x=x+2,y=y+2)

    user_name = Label(root,text = "Tài khoản:",fg="#00008b",font=("Arial Bold",10),bg="#add8e6")
    user_name.place(x=x+20,y=y+10)
    entry_user_name = customtkinter.CTkEntry(master=root, width=160,bg_color="#add8e6")
    entry_user_name.place(x=x+20,y=y+30)

    password = Label(root,text = "Mật khẩu:",fg="#00008b",font=("Arial Bold",10),bg="#add8e6")
    password.place(x=x+20,y=y+60)
    entry_password = customtkinter.CTkEntry(master=root, width=160,bg_color="#add8e6")
    entry_password.place(x=x+20,y=y+80)

    repassword = Label(root,text = "Nhập lại mật khẩu:",fg="#00008b",font=("Arial Bold",10),bg="#add8e6")
    repassword.place(x=x+20,y=y+110)
    entry_repassword = customtkinter.CTkEntry(master=root, width=160,bg_color="#add8e6")
    entry_repassword.place(x=x+20,y=y+130)

    dangki_button = customtkinter.CTkButton(master=root,text="Đăng kí",
                                            width=160,height=25,bg_color="#add8e6",
                                            fg_color="#f0e68c",corner_radius=50,command=click_hoanthanhdangki)
    dangki_button.place(x=x+20,y=y+170)

    quaylai_button = customtkinter.CTkButton(master=root,text="Quay lại",
                                            width=160,height=25,bg_color="#add8e6",
                                            fg_color="#f0e68c",corner_radius=50,command=click_quaylai)
    quaylai_button.place(x=x+20,y=y+200)

class IP(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("IP")
        master.geometry("200x100")

        ip_frame = Frame(master,height=100,width=200,bg="#add8e6")
        ip_frame.place(x=0,y=0)

        IP = Label(master,text = "Mời bạn nhập IP",fg="#00008b",font=("Arial Bold",10),bg="#add8e6")
        IP.pack()

        self.getHost = StringVar()
        self.entry_ip = customtkinter.CTkEntry(master, width=160,bg_color="#add8e6",textvariable=self.getHost)
        self.entry_ip.bind('<Return>',self.callback)
        self.entry_ip.pack()

        self.IP_button = Button(master,text="Truy cập",width=10,height=1,command=self.master.destroy)
        self.IP_button.place(x=60,y=60)
    
    def callback(*args):
        value = args[0].getHost.get()
        print (value)
        args[0].master.destroy()

def closing():
    sys.exit()

if __name__ == '__main__':
    root_ip = Tk()
    app = IP(master=root_ip)
    root_ip.resizable(0, 0)
    root_ip.protocol("WM_DELETE_WINDOW", closing)
    root_ip.mainloop()

    HOST = app.getHost.get()
    SERVER_PORT = 65432
    FORMAT = "utf8" 

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, SERVER_PORT))
        showinfo("Thông báo","Kết nối thành công")
        root = Tk()
        giaodien_dangnhap()
        root.resizable(0, 0)
        root.mainloop()
    except:
        showinfo("Thông báo","Kết nối đã bị lỗi!")