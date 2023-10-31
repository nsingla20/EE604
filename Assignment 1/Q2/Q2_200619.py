import cv2
import numpy as np
import librosa

def solution(audio_path):
    ############################
    ############################
    class_name = ''

    y, sr = librosa.load(audio_path, sr=None)
    n_fft = 2048
    hop_length = 512
    spec = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, fmax=22000)
    db  = librosa.power_to_db(spec, ref=np.max)
    db = db - np.min(db)
    db = db*255/np.max(db)

    kernel = np.array([[-1/3, 1/3, 1/3],
                      [-1/3, 1/3, 1/3],
                      [-1/3, 1/3, 1/3]])

    filt = cv2.filter2D(src=db, ddepth=-1, kernel=kernel)
    ret, filt = cv2.threshold(filt, 200, 255, cv2.THRESH_BINARY)

    for i in range(10):
        filt = cv2.filter2D(src=filt, ddepth=-1, kernel=kernel)
        ret, filt = cv2.threshold(filt, 200, 255, cv2.THRESH_BINARY)

    if np.max(np.average(filt, axis=0)) > 125:
        class_name = 'metal'
    else :
        class_name = 'cardboard'


    ############################
    ############################
    ## comment the line below before submitting else your code wont be executed##
    # pass
    # class_name = 'cardboard'
    return class_name

