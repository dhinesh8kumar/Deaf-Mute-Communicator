import speech_recognition
from nltk.tokenize import word_tokenize
import os
import requests
import urllib
import urllib.request
from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

lemmatizer = WordNetLemmatizer()
def pos_tagger(nltk_tag):
	if nltk_tag.startswith('J'):
		return wordnet.ADJ
	elif nltk_tag.startswith('V'):
		return wordnet.VERB
	elif nltk_tag.startswith('N'):
		return wordnet.NOUN
	elif nltk_tag.startswith('R'):
		return wordnet.ADV
	else:		
		return None
if not os.path.exists('images/'):
    os.mkdir('images/')
spath = 'images/'

# Get env variables
DK = 'AIzaSyDOonMrAlbxiNhzNutjGuAEqFLmLlcaxeA'
CX = '1723d9a3e6f374592'



letters = ['you','hello','q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
def get_img(searchfor):

    uri = 'https://res.cloudinary.com/spiralyze/image/upload/f_auto,w_auto/BabySignLanguage/DictionaryPages/'+searchfor+'.svg'
    with open('images/'+searchfor+'.jpg', 'wb') as f:
        f.write(requests.get(uri).content)
    
    if os.path.getsize('images/'+searchfor+'.jpg') !=  0:
        print('down',searchfor)
        return
    else:
        os.remove('images/'+searchfor+'.jpg')
        print('cant down',searchfor)
        return
    
    


def get_gif(word):
    baseUrl = requests.get('https://www.lifeprint.com/asl101/pages-signs/'+word[0]+'/'+word+'.htm')
    soup = BeautifulSoup(baseUrl.text, 'html.parser')

    allImgs = soup.findAll('img')

    imgCounter = 1

    for img in allImgs:
        newImg = img.get('data-src')
        if newImg == None:
            newImg = img.get('src')

        if newImg[6:10] != 'gifs':
            continue

        extension = '.gif'
        if '.gif' in newImg:
            extension = '.gif'

        nl = 'https://www.lifeprint.com/asl101'+newImg[5:]
        imgFile = open('images/'+str(word) + extension, 'wb')
        imgFile.write(urllib.request.urlopen(nl).read())
        imgCounter = imgCounter + 1
        imgFile.close()
        break
    
        
        
        
    if imgCounter == 1:
        get_img(word)



stopwords = ['am', 'is','to', 'are', 'was', 'were', 'be', 'been', 'being',  'a', 'an', 'and', 'if', 'as', 'until', 'while', 'of', 'at', 'by', 'with', 'through', 'during', 'further', 'then', 'once', 'any', 'each',  'such',  'only', 'own', 'so', 'than', 'too',   'just', 'don', 'should', "should've",  'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", "won't", 'wouldn', "wouldn't"]
def recognize():
    rec = speech_recognition.Recognizer()
    with speech_recognition.AudioFile('sp.wav') as mic:
        print('l')
        audio = rec.listen(mic)
        text = rec.recognize_google(audio)
        return text



'''
def show_img(file):
    
    class ImageLabel(tk.Label):
        
        def load(self, im):
            if isinstance(im, str):
                im = Image.open(im)
            self.loc = 0
            self.frames = []

            try:
                for i in count(1):
                    self.frames.append(ImageTk.PhotoImage(im.copy()))
                    im.seek(i)
            except EOFError:
                pass

            try:
                self.delay = im.info[50]
            except:
                self.delay = 50

            if len(self.frames) == 1:
                self.config(image=self.frames[0])
            else:
                self.next_frame()

        def unload(self):
            self.config(image="")
            self.frames = None

        def next_frame(self):
            if self.frames:
                self.loc += 1
                self.loc %= len(self.frames)
                self.config(image=self.frames[self.loc])
                self.after(self.delay, self.next_frame)

    root = tk.Tk()
    root.geometry('1000x1000')
    lbl = ImageLabel(root)

    lbl.pack()
    try:
        lbl.load('images/'+file+'.gif')
    except:
        try:
            lbl.load('images/'+file+'.jpg')
        except:
            letters = list(file)
            
            for i in letters:
                lbl.load('images/'+i+'.jpg')
    root.after(3000,lambda:root.destroy())
    root.mainloop()

text = recognize()
text_tokens = word_tokenize(text)
print(text_tokens)
tokens_without_sw = [word for word in text_tokens if not word in stopwords]
print(tokens_without_sw)
sentence = ""
for t in tokens_without_sw:
    t = t.lower()
    sentence = sentence + t + " "

pos_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))

lemmatized_sentence = []
for word, tag in wordnet_tagged:
	if tag is None:
		# if there is no available tag, append the token as is
		lemmatized_sentence.append(word)
	else:	
		# else use the tag to lemmatize the token
		lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))

print(lemmatized_sentence)
tokens_without_sw = lemmatized_sentence

for t in tokens_without_sw:
    if t in letters:
        continue
    get_gif(t)

for t in tokens_without_sw:
    show_img(t)
'''






        
    