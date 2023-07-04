import streamlit as st
from st_clickable_images import clickable_images
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration, VideoProcessorBase, WebRtcMode
import av
class detect_sign(VideoTransformerBase):
    
    
    def recv(self, frame):
        
        global sequence,sentence, threshold, res, prev, fff_res, l
        frame = frame.to_ndarray(format="bgr24")
        
        return av.VideoFrame.from_ndarray(frame, format="bgr24")

webrtc_streamer(key="example",mode=WebRtcMode.SENDRECV,
                        
                        media_stream_constraints={"video": True, "audio": False},
                        video_processor_factory=detect_sign,
                        )
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

if(clicked > -1):
        print(chr(97+clicked))