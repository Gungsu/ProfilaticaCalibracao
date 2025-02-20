import customtkinter
import os
from PIL import Image
import serial
import time
import threading

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()        
        
        self.readSerial = False
        self.switchManu = 83
        self.leituraSerial = b"0"
        
        self.title("Profilatica Manutencao")
        self.geometry("820x600")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "profilatica_logo.png")), size=(90, 90))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        
        self.add_alert_image_Y = customtkinter.CTkImage(Image.open(os.path.join(image_path, "alertLed_Y.png")), size=(20, 20))
        self.add_alert_image_G = customtkinter.CTkImage(Image.open(os.path.join(image_path, "alertLed_G.png")), size=(20, 20))
        self.add_alert_image_R = customtkinter.CTkImage(Image.open(os.path.join(image_path, "alertLed_R.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Conexão",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Identificação",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Calibração",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        
        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, columnspan=3, sticky="ew", padx=0, pady=10)

        self.home_label_alert = customtkinter.CTkLabel(self.home_frame, text="",compound="left", font=customtkinter.CTkFont(size=15, weight="normal"))
        self.home_label_alert.grid(row=1, column=1, padx=10, pady=20, sticky="ew")
        
        self.home_frame_label_connectSerial = customtkinter.CTkLabel(self.home_frame, text="SERIAL")
        self.home_frame_label_connectSerial.grid(row=2, column=0, padx=20, pady=20)
        
        self.home_serial_entry = customtkinter.CTkEntry(self.home_frame,placeholder_text="COM")
        self.home_serial_entry.grid(row=2, column=1, padx=20, pady=20)
        
        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="Conectar", image=self.chat_image, command=self.frame_1_button_connect)
        self.home_frame_button_1.grid(row=2, column=2, padx=20, pady=20)
        
        #self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        #self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        #self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        #self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        self.cali_frame2_button_2 = customtkinter.CTkButton(self.second_frame, text="Modo Manut.", image=self.image_icon_image, compound="right", command=lambda: self.enviaComando("FW:","55"))
        self.cali_frame2_button_2.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.frame2_label_alert = customtkinter.CTkLabel(self.second_frame, text="",compound="left", font=customtkinter.CTkFont(size=15, weight="normal"))
        self.frame2_label_alert.grid(row=0, column=1, padx=10, pady=20, sticky="ew")
        
        self.frame2_label_produto = customtkinter.CTkLabel(self.second_frame, text=" Produto:",image=self.add_alert_image_R,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frame2_label_produto.grid(row=1, column=0, padx=10, pady=20, sticky="ew")
        
        self.frame2_produto_entry = customtkinter.CTkEntry(self.second_frame,placeholder_text="Nome do produto",width=200)
        self.frame2_produto_entry.grid(row=1, column=1, padx=20, pady=20, sticky="ew")
        self.frame2_produto_entry.bind("<KeyRelease>",lambda event: self.mudaLed("NP:",self.add_alert_image_Y))
        self.frame2_produto_entry.bind("<Return>",lambda event: self.enviaComando("NP:",self.frame2_produto_entry.get()))
        
        self.frame2_label_ns = customtkinter.CTkLabel(self.second_frame, text=" Num. Serie:",image=self.add_alert_image_R,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frame2_label_ns.grid(row=2, column=0, padx=10, pady=20, sticky="ew")
        
        self.frame2_ns_entry = customtkinter.CTkEntry(self.second_frame,placeholder_text="Numero de serie",width=200)
        self.frame2_ns_entry.grid(row=2, column=1, padx=20, pady=20, sticky="ew")
        self.frame2_ns_entry.bind("<KeyRelease>",lambda event: self.mudaLed("NS:",self.add_alert_image_Y))
        self.frame2_ns_entry.bind("<Return>",lambda event: self.enviaComando("NS:",self.frame2_ns_entry.get()))

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        self.cali_frame3_button_2 = customtkinter.CTkButton(self.third_frame, text="Modo Manut.", compound="right", image=self.image_icon_image,command=lambda: self.enviaComando("FW:","55"))
        self.cali_frame3_button_2.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.frame3_label_alert = customtkinter.CTkLabel(self.third_frame, text="", compound="left", font=customtkinter.CTkFont(size=15, weight="normal"))
        self.frame3_label_alert.grid(row=0, column=1, padx=10, pady=20, sticky="ew")
        
        self.frame3_label_Litro = customtkinter.CTkLabel(self.third_frame, text=" Litro 1 [ml]:",image=self.add_alert_image_R,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frame3_label_Litro.grid(row=1, column=0, padx=10, pady=20, sticky="ew")
        
        self.frame3_litro1_entry = customtkinter.CTkEntry(self.third_frame,placeholder_text="Litro1 [ml]",width=130)
        self.frame3_litro1_entry.grid(row=1, column=1, padx=20, pady=20, sticky="ew")
        self.frame3_litro1_entry.bind("<KeyRelease>",lambda event: self.mudaLed("L1:",self.add_alert_image_Y))
        self.frame3_litro1_entry.bind("<Return>",lambda event: self.enviaComando("L1:",self.frame3_litro1_entry.get()))
        
        self.frame3_label2_Litro = customtkinter.CTkLabel(self.third_frame, text=" Litro 2 [ml]:",image=self.add_alert_image_R,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frame3_label2_Litro.grid(row=2, column=0, padx=10, pady=20, sticky="ew")
        
        self.frame3_litro2_entry = customtkinter.CTkEntry(self.third_frame,placeholder_text="Litro2 [ml]",width=130)
        self.frame3_litro2_entry.grid(row=2, column=1, padx=20, pady=20, sticky="ew")
        self.frame3_litro2_entry.bind("<KeyRelease>",lambda event: self.mudaLed("L2:",self.add_alert_image_Y))
        self.frame3_litro2_entry.bind("<Return>",lambda event: self.enviaComando("L2:",self.frame3_litro2_entry.get()))
        
        self.frame3_label3_Litro = customtkinter.CTkLabel(self.third_frame, text=" Litro 3 [ml]:",image=self.add_alert_image_R,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frame3_label3_Litro.grid(row=3, column=0, padx=10, pady=20, sticky="ew")
        
        self.frame3_litro3_entry = customtkinter.CTkEntry(self.third_frame,placeholder_text="Litro3 [ml]",width=130)
        self.frame3_litro3_entry.grid(row=3, column=1, padx=20, pady=20, sticky="ew")
        self.frame3_litro3_entry.bind("<KeyRelease>",lambda event: self.mudaLed("L3:",self.add_alert_image_Y))
        self.frame3_litro3_entry.bind("<Return>",lambda event: self.enviaComando("L3:",self.frame3_litro3_entry.get()))
        
        self.frame3_label_Dosagem1 = customtkinter.CTkLabel(self.third_frame, text=" Dosagem 1 [ml]:",image=self.add_alert_image_R,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frame3_label_Dosagem1.grid(row=4, column=0, padx=10, pady=20, sticky="ew")
        
        self.frame3_dosa1_entry = customtkinter.CTkEntry(self.third_frame,placeholder_text="Dosagem 1[ml]",width=130)
        self.frame3_dosa1_entry.grid(row=4, column=1, padx=20, pady=20, sticky="ew")
        self.frame3_dosa1_entry.bind("<KeyRelease>",lambda event: self.mudaLed("P1:",self.add_alert_image_Y))
        self.frame3_dosa1_entry.bind("<Return>",lambda event: self.enviaComando("P1:",self.frame3_dosa1_entry.get()))
        
        self.frame3_label_Dosagem2 = customtkinter.CTkLabel(self.third_frame, text=" Dosagem 2 [ml]:",image=self.add_alert_image_R,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frame3_label_Dosagem2.grid(row=5, column=0, padx=10, pady=20, sticky="ew")
        self.frame3_dosa2_entry = customtkinter.CTkEntry(self.third_frame,placeholder_text="Dosagem 2[ml]",width=130)
        self.frame3_dosa2_entry.grid(row=5, column=1, padx=20, pady=20, sticky="ew")
        self.frame3_dosa2_entry.bind("<KeyRelease>",lambda event: self.mudaLed("P2:",self.add_alert_image_Y))
        self.frame3_dosa2_entry.bind("<Return>",lambda event: self.enviaComando("P2:",self.frame3_dosa2_entry.get()))
        
        self.frame3_label_Dosagem3 = customtkinter.CTkLabel(self.third_frame, text=" Dosagem 3 [ml]:",image=self.add_alert_image_R,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frame3_label_Dosagem3.grid(row=6, column=0, padx=10, pady=20, sticky="ew")
        self.frame3_dosa3_entry = customtkinter.CTkEntry(self.third_frame,placeholder_text="Dosagem 3[ml]",width=130)
        self.frame3_dosa3_entry.grid(row=6, column=1, padx=20, pady=20, sticky="ew")
        self.frame3_dosa3_entry.bind("<KeyRelease>",lambda event: self.mudaLed("P3:",self.add_alert_image_Y))
        self.frame3_dosa3_entry.bind("<Return>",lambda event: self.enviaComando("P3:",self.frame3_dosa3_entry.get()))
        
        self.frame3_label_Cali1 = customtkinter.CTkLabel(self.third_frame, text="Calibração 1:",image=self.add_alert_image_R,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frame3_label_Cali1.grid(row=1, column=2, padx=10, pady=20, sticky="ew")
        self.frame3_cali1_entry = customtkinter.CTkEntry(self.third_frame,placeholder_text="Calibração 1",width=130)
        self.frame3_cali1_entry.grid(row=1, column=3, padx=20, pady=20, sticky="ew")
        self.frame3_cali1_entry.bind("<KeyRelease>",lambda event: self.mudaLed("C1:",self.add_alert_image_Y))
        self.frame3_cali1_entry.bind("<Return>",lambda event: self.enviaComando("C1:",self.frame3_cali1_entry.get()))
        
        self.frame3_label_Cali2 = customtkinter.CTkLabel(self.third_frame, text="Calibração 2:",image=self.add_alert_image_R,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frame3_label_Cali2.grid(row=2, column=2, padx=10, pady=20, sticky="ew")
        self.frame3_cali2_entry = customtkinter.CTkEntry(self.third_frame,placeholder_text="Calibração 2",width=130)
        self.frame3_cali2_entry.grid(row=2, column=3, padx=20, pady=20, sticky="ew")
        self.frame3_cali2_entry.bind("<KeyRelease>",lambda event: self.mudaLed("C2:",self.add_alert_image_Y))
        self.frame3_cali2_entry.bind("<Return>",lambda event: self.enviaComando("C2:",self.frame3_cali2_entry.get()))
        
        self.frame3_label_Cali3 = customtkinter.CTkLabel(self.third_frame, text="Calibração 3:",image=self.add_alert_image_R,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frame3_label_Cali3.grid(row=3, column=2, padx=10, pady=20, sticky="ew")
        self.frame3_cali3_entry = customtkinter.CTkEntry(self.third_frame,placeholder_text="Calibração 3",width=130)
        self.frame3_cali3_entry.grid(row=3, column=3, padx=20, pady=20, sticky="ew")
        self.frame3_cali3_entry.bind("<KeyRelease>",lambda event: self.mudaLed("C3:",self.add_alert_image_Y))
        self.frame3_cali3_entry.bind("<Return>",lambda event: self.enviaComando("C3:",self.frame3_cali3_entry.get()))

        # select default frame
        self.select_frame_by_name("home")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        if self.readSerial:
            self.switchManu = 83
            self.enviaComando("FW:","55")
        self.destroy()
    
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def limparAlerta(self,texto):
        self.home_label_alert.configure(text=texto)
        self.frame2_label_alert.configure(text=texto)
        self.frame3_label_alert.configure(text=texto)
        time.sleep(2)
        self.home_label_alert.configure(text="")
        self.frame2_label_alert.configure(text="")
        self.frame3_label_alert.configure(text="")

    def frame_1_button_connect(self):
        porta = self.home_serial_entry.get()
        
        #try:
        if self.readSerial:
            texto = f"A porta serial {porta} está fechada."
            threadingAlerta = threading.Thread(target=self.limparAlerta,args=(texto,))
            threadingAlerta.start()
            self.readSerial = False
            self.ser.close()
            self.home_frame_button_1.configure(text="Conectar")
        else:
            try:
                self.ser = serial.Serial(porta, 9600)
                texto = f"A porta serial {porta} está aberta."
                threadingAlerta = threading.Thread(target=self.limparAlerta,args=(texto,))
                threadingAlerta.start()
                #comando = "FW:R\n"
                #cmdEncode = comando.encode('utf-8')
                
                #self.ser.write(cmdEncode)
                
                #self.lerSerial(self.ser)
                self.readSerial = True
                threadingSerial = threading.Thread(target=self.lerSerial,args=(self,))
                threadingSerial.daemon = True
                threadingSerial.start()
                self.home_frame_button_1.configure(text="Desconectar")
            except:
                self.readSerial = False
                self.home_frame_button_1.configure(text="Conectar")
    
    def mudaLed(self,campo,valor):
        if campo == "C1:":
            self.frame3_label_Cali1.configure(image=valor)
        elif campo == "C2:":
            self.frame3_label_Cali2.configure(image=valor)
        elif campo == "C3:":
            self.frame3_label_Cali3.configure(image=valor)
        elif campo == "L1:":
            self.frame3_label_Litro.configure(image=valor)
        elif campo == "L2:":
            self.frame3_label2_Litro.configure(image=valor)
        elif campo == "L3:":
            self.frame3_label3_Litro.configure(image=valor)
        elif campo == "P1:":
            self.frame3_label_Dosagem1.configure(image=valor)
        elif campo == "P2:":
            self.frame3_label_Dosagem2.configure(image=valor)
        elif campo == "P3:":
            self.frame3_label_Dosagem3.configure(image=valor)
        elif campo == "NP:":
            self.frame2_label_produto.configure(image=valor)
        elif campo == "NS:":
            self.frame2_label_ns.configure(image=valor)
    
    def preencheCampo(self,campo,valor):
        convValor = int.from_bytes(valor, byteorder='big')
        strValor = str(convValor)
        if campo == b"C1:":
            self.frame3_cali1_entry.delete(0,16)
            self.frame3_cali1_entry.insert(0,strValor)
            self.frame3_label_Cali1.configure(image=self.add_alert_image_G)
        elif campo == b"C2:":
            self.frame3_cali2_entry.delete(0,16)
            self.frame3_cali2_entry.insert(0,strValor)
            self.frame3_label_Cali2.configure(image=self.add_alert_image_G)
        elif campo == b"C3:":
            self.frame3_cali3_entry.delete(0,16)
            self.frame3_cali3_entry.insert(0,strValor)
            self.frame3_label_Cali3.configure(image=self.add_alert_image_G)
        elif campo == b"L1:":
            self.frame3_litro1_entry.delete(0,16)
            self.frame3_litro1_entry.insert(0,str(int(strValor)*100))
            self.frame3_label_Litro.configure(image=self.add_alert_image_G)
        elif campo == b"L2:":
            self.frame3_litro2_entry.delete(0,16)
            self.frame3_litro2_entry.insert(0,str(int(strValor)*100))
            self.frame3_label2_Litro.configure(image=self.add_alert_image_G)
        elif campo == b"L3:":
            self.frame3_litro3_entry.delete(0,16)
            self.frame3_litro3_entry.insert(0,str(int(strValor)*100))
            self.frame3_label3_Litro.configure(image=self.add_alert_image_G)
        elif campo == b"L4:":
            pass
        elif campo == b"P1:":
            self.frame3_dosa1_entry.delete(0,16)
            self.frame3_dosa1_entry.insert(0,str(int(strValor)))
            self.frame3_label_Dosagem1.configure(image=self.add_alert_image_G)
        elif campo == b"P2:":
            self.frame3_dosa2_entry.delete(0,16)
            self.frame3_dosa2_entry.insert(0,str(int(strValor)))
            self.frame3_label_Dosagem2.configure(image=self.add_alert_image_G)
        elif campo == b"P3:":
            self.frame3_dosa3_entry.delete(0,16)
            self.frame3_dosa3_entry.insert(0,str(int(strValor)))
            self.frame3_label_Dosagem3.configure(image=self.add_alert_image_G)
        elif campo == b"NP:":
            texto = ""
            for x in valor:
                if x>=48 and x<=122:
                    texto += chr(x)
            self.frame2_produto_entry.delete(0,16)
            self.frame2_produto_entry.insert(0,texto)
            self.frame2_label_produto.configure(image=self.add_alert_image_G)
        elif campo == b"NS:":
            self.frame2_ns_entry.delete(0,16)
            texto = ""
            for x in valor:
                if x>=48 and x<=122:
                    texto += chr(x)
            self.frame2_ns_entry.insert(0,texto)
            self.frame2_label_ns.configure(image=self.add_alert_image_G)
        elif campo == b"OK":
            threadingAlerta = threading.Thread(target=self.limparAlerta,args=("Comando recebido...",))
            threadingAlerta.start()
        elif campo == b"NOK":
            threadingAlerta = threading.Thread(target=self.limparAlerta,args=("Comando negado...",))
            threadingAlerta.start()
        else:
            strAlerta = "ERRO: " + campo
            threadingAlerta = threading.Thread(target=self.limparAlerta,args=(strAlerta,))
            threadingAlerta.start()
    
    def separaCMDdeValor(self,linha):
        listaDeDados = {b"NOK",b"OK",b"C1:",b"C2:",b"C3:",b"L1:",b"L2:",b"L3:",b"L4:",b"P1:",b"P2:",b"P3:",b"NP:",b"NS:"}
        for i in listaDeDados:
            if i in linha:
                valor = linha.split(i)
                self.preencheCampo(i,valor[1])
        

    def lerSerial(self,der):
        while self.readSerial:
            bytSingle = self.ser.read()
            if bytSingle != b'\n':
                self.leituraSerial = self.leituraSerial + bytSingle
            else:
                #print(f"Dados recebidos: {self.leituraSerial}")
                self.separaCMDdeValor(self.leituraSerial)
                self.leituraSerial = b''
        self.ser.close()
    
    def enviaComando(self,comando,valor):
        if self.readSerial:
            if comando=="FW:":
                valor = self.switchManu
                if self.switchManu == 83:
                    self.switchManu = 82
                    self.cali_frame2_button_2.configure(image=self.add_alert_image_R)
                    self.cali_frame3_button_2.configure(image=self.add_alert_image_R)
                else:
                    self.switchManu = 83
                    self.cali_frame2_button_2.configure(image=self.add_alert_image_G)
                    self.cali_frame3_button_2.configure(image=self.add_alert_image_G)
                valor = str(valor)
                vlrInt = int(valor)
                vlrByte = vlrInt.to_bytes(1, 'big')
            elif comando=="L1:" or comando=="L2:" or comando=="L3:":
                valor = int(int(valor)/100)
                valor = str(valor)
                vlrInt = int(valor)
                vlrByte = vlrInt.to_bytes(1, 'big')
            elif comando=="NS:" or comando=="NP:":
                valor = valor.encode('utf-8')
                vlrByte = valor
            else:
                valor = str(valor)
                vlrInt = int(valor)
                vlrByte = vlrInt.to_bytes(1, 'big')
            cmdByte = comando.encode('utf-8')
            stringUnica = cmdByte+vlrByte
            stringUnica += b'\n'
            self.ser.write(stringUnica)
        else:
            threadingAlerta = threading.Thread(target=self.limparAlerta,args=("Necessario conexao!",))
            threadingAlerta.start()

if __name__ == "__main__":
    app = App()
    app.mainloop()