import cv2
import mediapipe as mp
import numpy as np
#import ssl
# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose
# Initializing mediapipe drawing class.
mp_drawing = mp.solutions.drawing_utils 

import pandas as pd
from sklearn.model_selection import train_test_split
df = pd.read_csv('csvs_out.csv')
X = df.drop('class', axis=1) #features
y = df['class'] #target value
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234)
from sklearn.pipeline import make_pipeline 
from sklearn.preprocessing import StandardScaler

#using logisticregression, ridgeclassifier, randomforestclassifier, gradientboostingclassifier
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

pipelines = {
    'lr':make_pipeline(StandardScaler(), LogisticRegression()),
    'rc':make_pipeline(StandardScaler(), RidgeClassifier()),
    'rf':make_pipeline(StandardScaler(), RandomForestClassifier()),
    'gb':make_pipeline(StandardScaler(), GradientBoostingClassifier()),
}

#4 models inside the fit_models
fit_models = {}
for algo, pipeline in pipelines.items():
    model = pipeline.fit(X_train, y_train)
    fit_models[algo] = model


#testing with model
#fit_models['rc'].predict(X_test)

from sklearn.metrics import accuracy_score # Accuracy metrics 
import pickle 
for algo, model in fit_models.items():
    yhat = model.predict(X_test)
    print(algo, accuracy_score(y_test, yhat))
#fit_models['rf'].predict(X_test)

with open('pose_detection.pkl', 'wb') as f:
    #export the best model and dump it down
    pickle.dump(fit_models['rf'], f)

with open('pose_detection.pkl', 'rb') as f:
    model = pickle.load(f)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    #get image
    image = cv2.imread('./test_pic/Unknown.jpeg')
        
    #blurring image
    factor = 20
    kW = int(image.shape[1] / factor)
    kH = int(image.shape[0] / factor)
    #ensure the shape of the kernel is odd
    if kW % 2 == 0: kW = kW - 1
    if kH % 2 == 0: kH = kH - 1
    image = cv2.GaussianBlur(image, (kW, kH), 0)  
        
    # Make Detections
    results = pose.process(image)

    # Draw landmarks
    mp_drawing.draw_landmarks(image, landmark_list=results.pose_landmarks, connections=mp_pose.POSE_CONNECTIONS)

    # Export coordinates
    try:
        # Extract Pose landmarks
        pose_mark = results.pose_landmarks.landmark
        pose_row = list(np.array([[landmark.x, landmark.y, landmark.z] for landmark in pose_mark]).flatten())

        X = pd.DataFrame([pose_row])
        body_language_class = model.predict(X)[0]
        body_language_prob = model.predict_proba(X)[0]
        print(body_language_class, body_language_prob)

        # Get status box
        cv2.rectangle(image, (0,0), (250, 60), (245, 117, 16), -1)

        # Display Class
        cv2.putText(image, 'CLASS', (95,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, body_language_class.split(' ')[0], (90,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Display Probability
        cv2.putText(image, 'PROB', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)],2)), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    except:
        pass
    
    #save image
    cv2.imwrite('./result_pic/save.jpg', image)
    