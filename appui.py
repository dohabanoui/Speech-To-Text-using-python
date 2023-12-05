import tkinter as tk
import tkinter.filedialog as fd
from tkinter import messagebox
import tkinter.ttk as ttk
import os
import transcriptor as trc
import translator as trs
import threading
from pydub import AudioSegment
from pydub.playback import play
import torchaudio


class App(tk.Tk):

    def __init__(self):
        """
        initialise the window with basics informations
        """
        super().__init__()
        self.title("SpeechRecognition")
        self.frame = ttk.Frame(self)
        self.frameB = tk.Frame(self, bg='black', width=80, height=420)

        self.frameB.grid(row=0, column=0)
        self.frame.grid(row=0, column=1)
        self.make_menu()
        self.label = ttk.Label(self.frame, text="Bienvenue", font=('Poppins', '32', 'bold'))
        self.text = ttk.Label(self.frame,
                             text="cette application vous permet de lire,\n de faire la transcription et la traduction \n d'un fichier audio ou d'une requete enregistré ")
        self.inf = ttk.Label(self.frame,
                            text="cette application a été devloppé dans le cadre \nde du module de algorithmique et structure de donnée avec  python",
                            font=("Congenial SemiBold", '8', 'italic'))
        self.inst = ttk.Label(self.frame, text="veuillez ouvrir un fichier pour commencer")
        self.label.pack(pady=10, padx=120)
        self.text.pack()
        self.inf.pack()
        self.inst.pack(pady=50)
        self.btnFrame = tk.Frame(self.frame)
        self.openBtn = ttk.Button(self.btnFrame, text="Open", command=self.start)
        self.recordBtn = ttk.Button(self.btnFrame, text="Record", command=self.start_record)
        self.quitBtn = ttk.Button(self.btnFrame, text="Exit", command=self.destroy)
        self.openBtn.grid(row=0, column=0,padx=10)
        self.recordBtn.grid(row=0, column=1,padx=10)
        self.quitBtn.grid(row=0, column=2,padx=10)
        self.btnFrame.pack(pady=10)
        self.resizable(False, False)

        #simply set the theme
        self.call("source", "azure.tcl")
        self.call("set_theme", "light")
        self.minsize(self.winfo_width(), self.winfo_height())
        self.resizable(False, False)


    def destroy_widget(self):
        """
        Destroy all the widgets in the window
        """
        for widgets in self.winfo_children():
            widgets.destroy()

    def open_file(self):
        self.filepath = fd.askopenfilename()

    def start(self):
        """
        the second frame window
        """
        self.open_file()  

        if self.filepath:
            self.destroy_widget()
            self.make_menu()
            self.make_panels()
            self.show_info()
            

            # Start a thread for transcription
            threading.Thread(target=self.transcript).start()


        else:
            messagebox.showwarning(title="Warning", message="Please select a file to open")

    def start_record(self):
        #the third frame window
        self.destroy_widget()
        self.make_menu()
        self.make_panels_record()


    
    def close(self):
       self.destroy()

    def help(self):
        # Todo : generate a window that describe the utilisation of the interface
        pass

    def make_menu(self):
        """
        generate the menu of the window by given a list of items
        """
        menu_items = ['open', 'help', 'close']
        self.menu = tk.Menu(self, background='black', bg='black', fg='white', foreground='white')
        self.generate_menu(menu_items)
        self.configure(menu=self.menu)

    def generate_menu(self, menu_items):
        """
        add even handlers to the menu items
        """
        window_methods = [method_name for method_name in dir(self) if callable(getattr(self, method_name))]
        tkinter_methods = [method_name for method_name in dir(tk.Tk) if callable(getattr(tk.Tk, method_name))]
        my_methods = [method for method in set(window_methods) - set(tkinter_methods)]
        my_methods = sorted(my_methods)

        for item in menu_items:
            match = ''.join([method for method in my_methods if method.startswith(item)])
            method = getattr(self, match)
            self.menu.add_command(label=item, command=method)

    def make_panels(self):
        # the second frame window
        # definir la taille de la fenetre.
        self.frame = ttk.Frame(self)
        self.frame.pack(fill='both', expand=1)

        self.north_frame = tk.Frame(self.frame,height=60)
        self.north_frame.pack(side='top',fill='x',ipadx=15,ipady=20)

        self.south_frame = tk.Frame(self.frame)
        self.south_frame.pack(side='top',fill='both',expand=True)

        self.south_frame_left = tk.Frame(self.south_frame)
        self.south_frame_left.pack(side='left',fill='both',expand=True)

        ttk.Separator(self.south_frame,orient='vertical').pack(side='left',fill='y',padx=5,pady=10)

        self.south_frame_right = tk.Frame(self.south_frame)
        self.south_frame_right.pack(side='left',fill='both',expand=True,ipadx=10)


        self.file_name = tk.StringVar()
        play_btn = ttk.Button(self.north_frame, text='Play', command=self.read_file)
        self.filename_label = ttk.Label(self.north_frame, textvariable=self.file_name, font=('Poppins', '20', 'bold'))
        # pack the label and the button in the same line with space between them
        self.filename_label.pack(side='left', padx=16)
        play_btn.pack(side='right', padx=20)

        ttk.Label(self.south_frame_left,text='Transcripted Text',font=("Ubuntu Nerd Font",18)).grid(row=0,column=0,pady=10,sticky='we',padx=20)



        self.transcripted_text = tk.Text(self.south_frame_left, height=10, width=30, font=("Ubuntu Nerd Font", 12))
        self.transcripted_text.grid(row=1, column=0, pady=10, padx=20, ipadx=10, ipady=10, sticky='nswe')
        self.transcripted_text.insert('1.0', 'We\'re waiting for the transcription ...')
        self.transcripted_text.config(state='disabled')


        ttk.Label(self.south_frame_right, text="Translated Text", font=("Ubuntu Nerd Font", 18)).grid(row=0, column=0, pady=10, columnspan=2)
        ttk.Label(self.south_frame_right,text="Please select a Language:").grid(row=1, column=0, pady=10, padx=20)


        self.selected_language = tk.StringVar()
        comboBox = ttk.Combobox(self.south_frame_right, textvariable=self.selected_language)
        comboBox['values'] = [format for format in ["EN", "AR", "FR", "ES","IT"]] #type: ignore
        comboBox['state'] = 'readonly'
        comboBox.current(0)
        comboBox.grid(row=1, column=1)
        # comboBox.bind("<<ComboboxSelected>>", lambda x: self.translate())
        ttk.Button(self.south_frame_right, text= "Translate" , command=self.translate).grid(row=2, column=0, pady=10, padx=20, columnspan=2, sticky='we')



        self.translated_text = tk.Text(self.south_frame_right ,height=10, width=30, font=("Ubuntu Nerd Font", 12))
        self.translated_text.insert('1.0', 'Select a language to translate the speech')
        self.translated_text.config(state='disabled')
        self.translated_text.grid(row=3, column=0, pady=10, padx=20, ipadx=10, ipady=10, sticky='nswe', columnspan=2)

        self.update()
        self.minsize(self.winfo_width(),self.winfo_height())


    def make_panels_record(self):
    # the third frame window
    # define the size of the window.
        self.geometry("700x400")
        self.frame = tk.Frame(self, background='white')
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.north_frame = tk.Frame(self.frame, height=80)
        self.north_frame.grid(row=0, column=0, sticky="nsew")  # Use grid for both frames


        record_btn = ttk.Button(self.north_frame, text='Record', command=self.record_spec)
        self.filename_label = tk.Label(self.north_frame, text="Vous avez 7 secondes", font=('Poppins', '20', 'bold'), bg='#eeeeee')
        self.filename_label.grid(row=5, column=0, padx=10)
        record_btn.grid(row=5, column=1, padx=10)

    def read_file(self):
        # read the audio file
        audio_file = AudioSegment.from_file(self.filepath)
        if audio_file:
            audio = AudioSegment.from_file(self.filepath)
            play(audio)
    
    def show_info(self):
        # updating the file information with the name without the path and the extension
        self.file_name.set(os.path.basename(self.filepath).split('.')[0])
        # self.file_name.set(os.path.basename(self.filepath))



    def transcript(self):
        # Todo: transcript the audio file
        # Todo: use another thread to not block the main thread
        try:
            audio_data, sample_rate = torchaudio.load(self.filepath)

            # Effacer le contenu existant dans self.transcripted_text
            self.transcripted_text.config(state='normal')
            self.transcripted_text.delete('1.0', 'end')

            # Insérer la nouvelle transcription dans self.transcripted_text
            self.transcripted_text.insert('1.0', trc.transcript(audio_data, sample_rate))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during transcription: {str(e)}")

        finally:
            self.transcripted_text.config(state='disabled')



    def translate(self):
        try:
            # Effacer le contenu existant dans self.translated_text
            self.translated_text.config(state='normal')
            self.translated_text.delete('1.0', 'end')

            # Insérer la nouvelle traduction dans self.translated_text
            self.translated_text.insert('1.0', trs.translate_text(self.transcripted_text.get('1.0', 'end'), self.selected_language.get()))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during translation: {str(e)}")

        finally:
            self.translated_text.config(state='disabled')

        


    def record_spec(self):
        import sounddevice as sd
        from scipy.io.wavfile import write
        #import wavio as wv
        fs = 44100
        second = 7
        print("start recording")
        # record your voice
        record_voice = sd.rec(int(second * fs), samplerate=fs, channels=2)
        sd.wait()
        print("end recording")
        write('output.wav', fs, record_voice)
        #wv.write("output.wav", record_voice, fs, sampwidth=2)
        self.filepath = "output.wav"
        self.destroy_widget()
        self.make_menu()
        self.make_panels()
        self.show_info()
        self.transcript()
        self.translate()



        


