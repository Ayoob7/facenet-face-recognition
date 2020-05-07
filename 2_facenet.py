from keras import backend as K
import time
from multiprocessing.dummy import Pool
K.set_image_data_format('channels_first')
import cv2
import os
import glob
import numpy as np
from numpy import genfromtxt
import tensorflow as tf
from dir_util.fr_utils import *
from dir_util.inception_blocks_v2 import *
import win32com.client as wincl

normalize_image_borders = 50
assert_detect_identity = True
speak_welcome_message = wincl.Dispatch("SAPI.SpVoice")
font = cv2.FONT_HERSHEY_SIMPLEX
facial_recognition_model = faceRecoModel(input_shape=(3, 96, 96))

'''
The loss function from the thesis implement here.
FaceRecoModel was ported and optimised to run on average computing resources.
'''
def own_loss_function(y_true, y_pred, alpha = 0.3):
    
    differential, pos, neg = y_pred[0], y_pred[1], y_pred[2]
    
    # Step 1: Reduce distance between the differential and positive
    positive_distance = tf.reduce_sum(tf.square(tf.subtract(differential, pos)), axis=-1) # axis -1 IMPORTANT
    # Step 2: Reduce distance between the differential and negative
    negative_distance = tf.reduce_sum(tf.square(tf.subtract(differential, neg)), axis=-1) # axis -1 IMPORTANT
    # Step 3: get the difference and add alpha
    intermediate_pooling_loss = tf.add(tf.subtract(positive_distance, negative_distance), alpha)
    # Step 4: Argmax of basic loss and 0
    final_loss = tf.reduce_sum(tf.maximum(intermediate_pooling_loss, 0.0))
    
    return final_loss

facial_recognition_model.compile(optimizer ='adam', loss = own_loss_function, metrics = ['accuracy'])

load_weights_from_FaceNet(facial_recognition_model)

def prepare_dictionary():
    person_dictionary = {}

    # Load training data
    for image in glob.glob("images/*"):
        person_id = os.path.splitext(os.path.basename(image))[0]
        person_dictionary[person_id] = img_path_to_encoding(image, facial_recognition_model)

    return person_dictionary

def webcam_video_feed(database):
    global assert_detect_identity

    cv2.namedWindow("preview")
    video_feed = cv2.VideoCapture(0)

    face_detectors = cv2.CascadeClassifier('dir_util/haarcascade_frontalface_default.xml')
    
    while video_feed.isOpened():
        _, video_frame = video_feed.read()
        img = video_frame

        # Securely detect single faces.
        if assert_detect_identity:
            img = process_frame(img, video_frame, face_detectors)
        
        key = cv2.waitKey(100)
        cv2.imshow("preview", img)

        if key == 27:
            break
    cv2.destroyWindow("preview")

def process_frame(img, frame, face_cascade):
    """
    Find whether people from the database is in the video frame.
    """
    global assert_detect_identity
    remove_color_channel = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_list = face_cascade.detectMultiScale(remove_color_channel, 1.3, 5)

    # Loop faces
    identities = []
    for (x, y, w, h) in faces_list:
        x_new = x - normalize_image_borders
        y_new = y - normalize_image_borders
        x2_new = x + w + normalize_image_borders
        y2_new = y + h + normalize_image_borders

        img = cv2.rectangle(frame,(x_new, y_new),(x2_new, y2_new),(255,0,0),2)

        person_id = find_person_identity(img, frame, x_new, y_new, x2_new, y2_new)

        if person_id is not None:
            identities.append(person_id)
            id_split = person_id.split("_")
            print(id_split)
            #filename = output('attendance', 'class1', int(id_split[1]), id_split[0], 'yes')

    if identities != []:
        #cv2.imwrite('example.png',img)
        assert_detect_identity = False
        thread_pool = Pool(processes=1)
        # Thread pools are created to run some processes concurrently through asynchronous calls
        thread_pool.apply_async(welcome_users, [identities])
    return img

def find_person_identity(img, frame, x1_new, y1_new, x2_new, y2_new):

    h_max, w_max, color_channels = frame.shape
    # Display the bounding box
    part_video_frame = frame[max(0, y1_new):min(h_max, y2_new), max(0, x1_new):min(w_max, x2_new)]
    
    return who_is_the_person(img, part_video_frame, database, facial_recognition_model, x1_new, y1_new)

def who_is_the_person(frame, image, database, facenet, x1, y1):
    encoding = img_to_encoding(image, facenet)
    
    minimum_distance = 100
    persons_id = None
    
    # for each name in database
    for (name, database_encoding) in database.items():
        
        # calculate euclidean distance
        encoding_distance = np.linalg.norm(database_encoding - encoding)
        cv2.putText(frame, name, (x1 + 30, y1 - 10), font, 1, (120, 255, 120), 2, 1)
        print('distance for %s is %s' %(name, encoding_distance))

        # If this distance is less than the min_dist, then set min_dist to dist, and identity to name
        if encoding_distance < minimum_distance:
            minimum_distance = encoding_distance
            persons_id = name
    
    if minimum_distance > 0.49:
        return None
    else:
        return str(persons_id)

def welcome_users(identity_matrix):
    global assert_detect_identity
    enter_message = 'Welcome '

    if len(identity_matrix) == 1:
        enter_message += '%s, you may enter.' % identity_matrix[0]
    else:
        for identity_id in range(len(identity_matrix) - 1):
            enter_message += '%s, ' % identity_matrix[identity_id]
        enter_message += 'and %s, ' % identity_matrix[-1]
        enter_message += 'you may enter'

    speak_welcome_message.Speak(enter_message)

    # Rerun any unused threads
    assert_detect_identity = True

if __name__ == "__main__":
    database = prepare_dictionary()
    webcam_video_feed(database)

