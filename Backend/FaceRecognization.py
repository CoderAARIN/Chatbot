import face_recognition
import cv2
import numpy as np
import os
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Load all known faces
known_face_encodings = []
known_face_names = []

path = 'known_faces'  # Folder with known faces

for filename in os.listdir(path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image = face_recognition.load_image_file(os.path.join(path, filename))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_face_encodings.append(encoding[0])
            known_face_names.append(os.path.splitext(filename)[0])

if not known_face_encodings:
    print("No known faces found. Exiting...")
    exit()

# Start webcam
video_capture = cv2.VideoCapture(0)

process_this_frame = True
access_granted = False

while True:
    ret, frame = video_capture.read()
    
    if not ret:
        print("Failed to grab frame")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Compare faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)
            name = "Unknown"

            # Use the closest match
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

            face_names.append(name)

            if name != "Unknown" and not access_granted:
                speak(f"Welcome {name}")
                access_granted = True
            elif name == "Unknown" and not access_granted:
                speak("Unknown person detected. Access Denied!")
                access_granted = False

    process_this_frame = not process_this_frame

    # Display results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Label the name
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Show video
    cv2.imshow('Jarvis Face Recognition', frame)

    # Break with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

