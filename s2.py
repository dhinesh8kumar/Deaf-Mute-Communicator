import numpy as np
import streamlit as st
from AudioRecorder import audiorecorder
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration, VideoProcessorBase, WebRtcMode
from s2t import *
import base64
import speech_recognition
import soundfile
import os.path
import av
from s2e import *
import time
import threading
from gtts import gTTS
from PIL import Image
from st_clickable_images import clickable_images

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities


RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

sequence = []
sentence = []
threshold = 0.8
prev = ""
l = []


class detect_sign(VideoTransformerBase):
    
    
    def recv(self, frame):
        
        global sequence,sentence, threshold, res, prev, l
        fff_res = ""
        try:
            with open('f_res.txt') as f:
                fff_res = f.readlines()
            fff_res = fff_res[0]
        except:
            fff_res = ""
        
        
        frame = frame.to_ndarray(format="bgr24")
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            image, results = mediapipe_detection(frame, holistic)
            draw_styled_landmarks(image, results)
            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]
            
            if len(sequence) == 30:
                result = model.predict(np.expand_dims(sequence, axis=0),verbose=None)[0]
                pred = actions[np.argmax(result)]
                
                if len(l) >= 50:
                    
                    l.pop(0)
                    l.append(pred)
                    res = {}
                    for i in l:
                        
                        if i in res.keys():
                            res[i]+=1
                        else:
                            res[i] = 1
                    
                    sorted_dict = sorted(res.items(), key= lambda x:x[1], reverse=True)
                    sorted_dict = dict(sorted_dict)
                    
                    f_res = str(list(sorted_dict.keys())[0])
                    
                    if f_res != prev:
                        print(f_res)
                        fff_res += ' '
                        fff_res += f_res
                        prev = f_res
                        
                else:
                    
                    l.append(pred)
                
                
        font = cv2.FONT_HERSHEY_SIMPLEX
  
        
        org = (30, 450)
        
        
        fontScale = 0.7
        
        
        color = (255, 255, 255)
        cv2.rectangle(img=image, pt1=(0,430), pt2=(640,500),color=[0, 0, 0], thickness=-1)
        
        thickness = 2
        
        
        if len(fff_res) > 0:
            image = cv2.putText(image,fff_res, org, font, 
                        fontScale, color, thickness, cv2.LINE_AA)
            old = ""
            try:
                with open('f_res.txt') as f:
                    old = f.readlines()
                    old = old[0]
            except:
                old = ""
            
            with open('f_res.txt', 'w') as f:
                f.write(old + ' ' +fff_res)
        return av.VideoFrame.from_ndarray(image, format="bgr24")

    
    
    
def main():
    # Face Analysis Application #
    global fff_res
    st.title("Deaf-Mute communicator")
    activiteis = ["Home","Sign Language Recognistion", "Speech to Sign Language"]
    choice = st.sidebar.selectbox("Select Activity", activiteis)
    
    if choice == "Home":
        html_temp_home1 = """<div style="background-color:#6D7B8D;padding:10px">
                                            <h4 style="color:white;text-align:center;">
                                            Face Emotion detection application using OpenCV, Deep Learning and Streamlit.</h4>
                                            </div>
                                            </br>"""
        st.markdown(html_temp_home1, unsafe_allow_html=True)
        st.write("""
                 The application has two functionalities.
                 1. Convert Sign Language to English.
                 2. COnvert english to sign Language.
                 """)
    elif choice == "Sign Language Recognistion":
        st.header("Webcam Live Feed")
        st.write("Click on start to use webcam and detect your face emotion")
        cont = st.container()
        webrtc_streamer(key="example",mode=WebRtcMode.SENDRECV,
                        rtc_configuration=RTC_CONFIGURATION,
                        media_stream_constraints={"video": True, "audio": False},
                        video_processor_factory=detect_sign,
                        )
        
        
        if st.button('Convert to Sound'):
            
            
            lines = ""
            with open('f_res.txt') as f:
                lines = f.readlines()
            
            open('f_res.txt', 'w').close()
            mytext = lines[0]
            
            language = 'en'
            myobj = gTTS(text=mytext, lang=language, slow=False)
            myobj.save("convert.mp3")
            

            st.audio('convert.mp3')
        
        clicked = clickable_images(
        [
            
                'a.jpg',
                'b.jpg',
                'c.jpg',
                'd.jpg',
                'e.jpg',
                'f.jpg',
                'g.jpg',
                'h.jpg',
                'i.jpg',
                'j.jpg',
                'k.jpg',
                'l.jpg',
                'm.jpg',
                'n.jpg',
                'o.jpg',
                'p.jpg',
                'q.jpg',
                'r.jpg',
                's.jpg',
                't.jpg',
                'u.jpg',
                'v.jpg',
                'w.jpg',
                'x.jpg',
                'y.jpg',
                'z.jpg',
                
                
            ],
            titles=[f"{str(chr(i+97))}" for i in range(26)],
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"margin": "5px", "height": "200px"},
            )
        if clicked > -1:
            fff_res = ""
            try:
                with open('f_res.txt') as f:
                    fff_res = f.readlines()
                    fff_res = fff_res[0]
            except:
                fff_res = ""
            
            with open('f_res.txt', 'w') as f:
                    f.write(fff_res+chr(clicked+97))

    elif choice == "Speech to Sign Language":
        st.subheader("Speech to Sign Language")
        html_temp_about1= """<div style="background-color:#6D7B8D;padding:10px">
                                    <h4 style="color:white;text-align:center;">
                                    Click on Record Button to start recording audio
                                    </div>
                                    </br>"""
        st.markdown(html_temp_about1, unsafe_allow_html=True)
        #record audio
        audio = audiorecorder("Click to record", "Recording...")
        if len(audio) > 0:
    
            st.audio(audio.tobytes())
            
            #save audio
            wav_file = open("speech.wav", "wb")
            wav_file.write(audio.tobytes())
            data, samplerate = soundfile.read('speech.wav')
            soundfile.write('sp.wav', data, samplerate, subtype='PCM_16')
        
        
        if st.button('Convert to Sign Languague'):
            
            text = recognize()
            text_tokens = word_tokenize(text)
            tokens_without_sw = [word for word in text_tokens if not word in stopwords]
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

            letters = ['you','hello','q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
            tokens_without_sw = lemmatized_sentence
            for t in tokens_without_sw:
                if t in letters:
                    continue
                pathjpg = 'images/'+t+'.jpg'
                pathgif = 'images/'+t+'.gif'
                present_file_jpg = os.path.isfile(pathjpg)
                present_file_gif = os.path.isfile(pathgif)
                if not present_file_gif and not present_file_jpg:
                    get_gif(t)
            
            for t in tokens_without_sw:
                if t == 'I' or t == 'i' or t == 'me':
                    t = 'my'
                st.write(t)
                try:
                    file_ = open('images/'+t+'.gif', "rb")
                    contents = file_.read()
                    data_url = base64.b64encode(contents).decode("utf-8")
                    file_.close()

                    st.markdown(
                        f'<img src="data:image/gif;base64,{data_url}" alt="">',
                        unsafe_allow_html=True)
                except:
                    try:
                        st.image('images/'+t+'.jpg',width = 720)
                    except:
                        letters = list(t)
                        
                        for i in letters:
                            st.image('images/'+i+'.jpg',width = 720)
                st.markdown("***")
    else:
        pass


if __name__ == "__main__":
    main()