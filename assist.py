from tkinter import *    #GUI tkinter 
import speech_recognition as sr    
import tkinter.filedialog 
from PIL import Image,ImageTk
import pyaudio
import speech_recognition as sr
from tkinter.filedialog import askopenfilename   
import pyttsx3 
import time
import pytesseract
from PIL import *
import warnings
warnings.filterwarnings('ignore')

root=Tk()
root.title('The 3 Modules')
root.geometry('1000x900')
root.resizable(width = FALSE ,height= FALSE)

Image_open = Image.open('41.jpg').convert()
image = ImageTk.PhotoImage(Image_open)
logo = Label(root,image=image,bg='Black')
logo.place(x=0,y=0,bordermode="outside")
lb=Label(root,text="The 3 Modules",font=('bold',20),fg='black')
lb.place(x=20,y=80)

#Speech to Text

def STT():
        
    

    r = sr.Recognizer()
    m = sr.Microphone()

    try:
        print("A moment of silence, please...")
        with m as source: r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        while True:
            print("Say something!")
            with m as source: audio = r.listen(source)
            print("Got it! Now to recognize it...")
            try:
                value = r.recognize_google(audio)
                print(value)
              
                if str is bytes:
                    print(u"You said {}".format(value).encode("utf-8"))
                    
                else:
                    print("You said {}".format(value))
                    
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:        pass


#Image to Speech
    
def imgspeech():
    t = Tk()
    t.title("input-screen")
    t.geometry('900x600')
    t.configure(bg='blue')
    t.resizable(width = FALSE ,height= FALSE)
   
    def browse():        
        path1=tkinter.filedialog.askopenfilename()  
        e2.delete(0, END)      
        e2.insert(0, path1)

    e2 = Entry(t,bd=5,text='')  #Entry box
    e2.place(x =50 ,y=150)

    def nw():
        import pyttsx3       
        path1 = e2.get()
        global Path1
        #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
        a=(pytesseract.image_to_string(path1))
        #print (a)

        engine = pyttsx3.init()
        engine.say(a)        
        print(a)
        
        engine.runAndWait()

    browse = Button(t, text='browse',width=5,height=1,relief=RAISED,overrelief=RIDGE,command=browse)
    browse.place(x =250 ,y=150)
    browse = Button(t, text='ok',width=5,height=1,relief=RAISED,overrelief=RIDGE,command=nw)
    browse.place(x =100 ,y=350)
        
    t.mainloop()    

#Text to Speech 
def CheckLogin():
    t = Tk()
    t.title("input-screen")
    t.geometry('900x700')
    t.configure(bg='blue')
    t.resizable(width = FALSE ,height= FALSE)
    
    e1 = Entry(t,bd=5,text='')   #Entry box 
    e1.place(x=50 ,y=150)

    path = e1.get()     

    #Text to Speech
    def TTS():
        import pyttsx3  #text to speech 
        path = e1.get() #to import text from the Entry box 
        global Path    
        print (path)   #prints the same text in the python shell

        engine = pyttsx3.init()  #object creation 
        engine.say(path)    #speech input          
        engine.runAndWait() #speech output

    browse = Button(t, text='Input',width=5,height=1,relief=RAISED,overrelief=RIDGE,command=TTS)
    browse.place(x =250 ,y=150)
            
    t.mainloop()


#*******************************************************************************#
    
loginbt = Button(root,text = "TextToSpeech",width=15,height=2,bg="Dodger Blue",fg="black",font="5",relief=RAISED,overrelief=RIDGE,command=CheckLogin)
loginbt.place(x =30 ,y=200)
loginbt = Button(root,text = "SpeechToText",width=15,height=2,bg="Dodger Blue",fg="black",font="5",relief=RAISED,overrelief=RIDGE,command=STT)
loginbt.place(x =200 ,y=200)
loginbt = Button(root,text = "ImageTospeech",width=15,height=2,bg="Dodger Blue",fg="black",font="5",relief=RAISED,overrelief=RIDGE,command=imgspeech)
loginbt.place(x =370 ,y=200)

root.mainloop()

#*******************************************************************************#




