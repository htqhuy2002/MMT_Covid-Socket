import socket 
import threading
import json
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import customtkinter
from PIL import ImageTk, Image
import time
from time import strftime
from datetime import date

def Register(tk,mk):
    with open("data/accounts.json") as f:
        array = json.load(f)

    if (tk in array.keys()) == True:
        return "Tài khoản đã tồn tại! Mời bạn đăng kí lại!"
    else:
        array[tk] = mk
        with open("data/accounts.json", "r+") as f:
            f.seek(0)
            json.dump(array, f, indent=4)
        return "Đăng kí thành công!"

def Login(tk, mk):
    with open("data/accounts.json", "r") as f:
        array = json.load(f)
    if (tk in array.keys()) == True:
        if array[tk] == mk:
            return "Đăng nhập thành công!"
        else:
            return "Bạn nhập sai mật khẩu!"
    else:
        return "Tài khoản không tồn tại! Vui lòng đăng kí tài khoản!"

def handleClient(conn: socket, addr,history,account):
    history.append(time.strftime('%I:%M:%S:%p')+": " + str(addr) +" đã kết nối")
    msg = None
    while (True):
        msg = conn.recv(1024).decode(FORMAT)
        if(msg=="Thoat"):       
            break

        if(msg=="Client xin đăng nhập"):
            history.append(time.strftime('%I:%M:%S:%p')+": " + str(addr) + " xin đăng nhập")
            msg="Cho phép đăng nhập"
            conn.sendall(msg.encode(FORMAT))
            msg = conn.recv(1024).decode(FORMAT)
            tk = msg
            msg=="support"
            conn.sendall(msg.encode(FORMAT))
            msg = conn.recv(1024).decode(FORMAT)
            mk = msg
            msg = Login(tk,mk)
            conn.sendall(msg.encode(FORMAT))
            msg = conn.recv(1024).decode(FORMAT)
            if(msg=="Đăng nhập thành công!"):
                history.append(time.strftime('%I:%M:%S:%p')+": " + str(addr) + " đăng nhập thành công")
                account.append(tk)

                while(True):
                    msg = conn.recv(1024).decode(FORMAT)
                    if(msg=="Client đăng xuất"):
                        history.append(time.strftime('%I:%M:%S:%p')+": " + str(addr) + " đăng xuất")
                        msg="support"
                        conn.sendall(msg.encode(FORMAT))
                        msg = conn.recv(1024).decode(FORMAT)
                        account.remove(msg)
                        msg="support"
                        conn.sendall(msg.encode(FORMAT))
                        break
                    
                    with open("data/data_covid.json", "r+") as f:
                        array = json.load(f)

                    if(msg in array.keys()):
                        date = msg
                        msg = "Sẵn sàng gửi dữ liệu"
                        conn.sendall(msg.encode(FORMAT))
                        for i in range(0,63):
                            msg = array[date][i]["Tinh_thanh"]
                            conn.sendall(msg.encode(FORMAT))
                            msg = conn.recv(1024).decode(FORMAT)
                            
                            msg = array[date][i]["Ca_nhiem"]
                            conn.sendall(msg.encode(FORMAT))
                            msg = conn.recv(1024).decode(FORMAT)

                            msg = array[date][i]["Tu_vong"]
                            conn.sendall(msg.encode(FORMAT))
                            msg = conn.recv(1024).decode(FORMAT)

                            msg = array[date][i]["Ca_mac_moi"]
                            conn.sendall(msg.encode(FORMAT))
                            msg = conn.recv(1024).decode(FORMAT)
                    
                    else:
                        msg = "Không tồn tại"
                        conn.sendall(msg.encode(FORMAT))

        elif(msg=="Client xin đăng kí"):
            history.append(time.strftime('%I:%M:%S:%p')+": " + str(addr) + " xin đăng kí")
            msg="Cho phép đăng kí"
            conn.sendall(msg.encode(FORMAT))
            msg = conn.recv(1024).decode(FORMAT)
            tk = msg
            msg=="support"
            conn.sendall(msg.encode(FORMAT))
            msg = conn.recv(1024).decode(FORMAT)
            mk = msg
            msg = Register(tk,mk)
            conn.sendall(msg.encode(FORMAT))
            msg = conn.recv(1024).decode(FORMAT)

        else:
            msg="support"
            conn.sendall(msg.encode(FORMAT))
            msg = conn.recv(1024).decode(FORMAT)
    
    history.append(time.strftime('%I:%M:%S:%p')+": " + str(addr) +" đã rời khỏi")
    conn.close()

def giaodien_server(history,account):
    def background_server():
        img = Image.open("pic/bg_server.png")
        img = img.resize((700, 400), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(root, image=img)
        panel.image = img
        panel.place(x=0,y=0)

    def reset_history():
        for i in tree1.get_children():
            tree1.delete(i)
        for i in history:
            tree1.insert('', END,values =(i,))
        tree1.after(100,reset_history)

    def reset_account():
        for i in tree2.get_children():
            tree2.delete(i)
        for i in account:
            tree2.insert('', END,values =(i,))
        tree2.after(100,reset_account)

    def clock():
        string=strftime('%I:%M:%S:%p'+"  "+date.today().strftime("%d/%m/%Y"))
        label.config(text=string)
        label.after(1000,clock)

    def click_reset():
        reset_data()
        showinfo("Cập nhật","Cập nhật dữ liệu thành công!")

    def on_closing():
        if askyesno("Bạn muốn thoát?", "Yes or No"):
            root.destroy()

    root = Tk()
    root.title("Server")
    root.geometry("700x400")
    background_server()

    label = Label(root,font=("Digital-7",15),foreground="blue",background="#f0fff0",bd=3)
    label.place(x = 450,y=20)
    clock()

    IP = Label(root,text="IP: "+socket.gethostbyname(socket.gethostname()),
                font=("Bold Arial",8),
                foreground="red",
                background="#f0fff0",bd=3)
    IP.place(x = 450,y=60)

    PORT = Label(root,text="PORT: 65432 ",
                font=("Bold Arial",8),
                foreground="red",
                background="#f0fff0",bd=3)
    PORT.place(x = 610,y=60)

    tree1 = ttk.Treeview(root, selectmode ='browse',height=13)
    tree1.place(x=23,y=100)
    tree1["columns"] = ("1")
    tree1['show'] = 'headings'
        
    tree1.column("1", width = 400, anchor ='w')
    tree1.heading("1", text ="Lịch sử hoạt động")

    vsb1 = Scrollbar(root, orient="vertical", command=tree1.yview)
    vsb1.place(x=428,y=100,height=285)
    tree1.configure(yscrollcommand=vsb1.set)

    tree2 = ttk.Treeview(root, selectmode ='browse',height=13)
    tree2.place(x=460,y=100)
    tree2["columns"] = ("1")
    tree2['show'] = 'headings'
        
    tree2.column("1", width = 200, anchor ='w')
    tree2.heading("1", text ="Tài khoản đang hoạt động")

    vsb2 = Scrollbar(root, orient="vertical", command=tree2.yview)
    vsb2.place(x=665,y=100,height=285)
    tree2.configure(yscrollcommand=vsb2.set)

    signout_button = customtkinter.CTkButton(master=root,text="Cập nhật",
                                                width=100,height=25,bg_color="#D6E0F2",
                                                fg_color="#ffa500",corner_radius=50,
                                                command=click_reset)
    signout_button.place(x=25,y=70)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    reset_history()
    reset_account()
    
    root.resizable(0,0)
    root.mainloop()

def reset_data():
    def RefreshData(times):
        url = "https://vi.wikipedia.org/wiki/B%E1%BA%A3n_m%E1%BA%ABu:D%E1%BB%AF_li%E1%BB%87u_%C4%91%E1%BA%A1i_d%E1%BB%8Bch_COVID-19/S%E1%BB%91_ca_nhi%E1%BB%85m_theo_t%E1%BB%89nh_th%C3%A0nh_t%E1%BA%A1i_Vi%E1%BB%87t_Nam#cite_note-1"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.select_one("#mw-content-text")
        data = titles.text
        Dulieu = []

        for i in range(6,69):
            Dulieu.append([])
            tinhthanh = data.split("\n\n")[i]
            solieu = tinhthanh.split("\n")
            for j in range(1,5):
                Dulieu[i - 6].append(solieu[j])
        
        with open("data/data_covid.json", "r+") as f:
            array = json.load(f)
            if len(array[times]) == 0:
                for i in range(6, 69):
                    toWrite = {"Tinh_thanh": str(Dulieu[i - 6][0]), "Ca_nhiem": str(Dulieu[i - 6][1]), "Tu_vong": str(Dulieu[i - 6][2]), "Ca_mac_moi": str(Dulieu[i - 6][3])}
                    array[times].append(toWrite)
                f.seek(0)
                json.dump(array, f, indent=4)    
            else:
                array[times].clear()
                for i in range(6, 69):
                    toWrite = {"Tinh_thanh": str(Dulieu[i - 6][0]), "Ca_nhiem": str(Dulieu[i - 6][1]), "Tu_vong": str(Dulieu[i - 6][2]), "Ca_mac_moi": str(Dulieu[i - 6][3])}
                    array[times].append(toWrite)
                f.seek(0)
                json.dump(array, f, indent=4)

    def AddData(times):
        url = "https://vi.wikipedia.org/wiki/B%E1%BA%A3n_m%E1%BA%ABu:D%E1%BB%AF_li%E1%BB%87u_%C4%91%E1%BA%A1i_d%E1%BB%8Bch_COVID-19/S%E1%BB%91_ca_nhi%E1%BB%85m_theo_t%E1%BB%89nh_th%C3%A0nh_t%E1%BA%A1i_Vi%E1%BB%87t_Nam#cite_note-1"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.select_one("#mw-content-text")
        data = titles.text
        Dulieu = []
        
        for i in range(6,69):
            Dulieu.append([])
            tinhthanh = data.split("\n\n")[i]
            solieu = tinhthanh.split("\n")
            for j in range(1,5):
                Dulieu[i - 6].append(solieu[j])
        
        with open("data/data_covid.json", "r+") as f:
            array = json.load(f)
            Date = []
            for i in range(6,69):
                toWrite = {"Tinh_thanh": str(Dulieu[i - 6][0]), "Ca_nhiem": str(Dulieu[i - 6][1]), "Tu_vong": str(Dulieu[i - 6][2]), "Ca_mac_moi": str(Dulieu[i - 6][3])}
                Date.append(toWrite)
            array[times] = Date
            f.seek(0)
            json.dump(array, f, indent=4)


    def GetData(times):
        with open("data/data_covid.json", "r+") as f:
            array = json.load(f)
        
        if (times in array.keys()) == True:
            RefreshData(times)
        else:
            AddData(times)

    time = date.today().strftime("%d/%m/%Y")
    GetData(time)

def auto_resetdata():
    while(True):
        reset_data()
        time.sleep(3600)

def socket_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, SERVER_PORT))
    s.listen(20)

    nClient = 0
    while (nClient < 20):
        try:
            conn, addr = s.accept()
            thr = threading.Thread(target=handleClient, args=(conn,addr,history,account))
            thr.daemon = True
            thr.start()
        except:
            showerror("Thông báo","Socket bị lỗi!")
        nClient += 1

    s.close()

if __name__ == "__main__":
    history = ["Waiting for client..."]
    account = []
    HOST = socket.gethostbyname(socket.gethostname()) 
    SERVER_PORT = 65432 
    FORMAT = "utf8"

    try:
        t1 = threading.Thread(target=giaodien_server,args=(history,account,))
        t2 = threading.Thread(target=socket_server)
        t2.daemon = True
        t3 = threading.Thread(target=auto_resetdata)
        t3.daemon = True

        t1.start()
        t2.start()
        t3.start()

        t1.join()

    except:
        showerror("Thông báo","Lỗi chương trình!")