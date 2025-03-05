import cv2
import numpy as np
import face_recognition
import os
import sqlite3
from datetime import datetime
import pickle

path = r"Training_images"
images = []
classNames = []
encoding_file = "face_encodings.pkl"

# Load training images from the specified folder
myList = os.listdir(path)  # Get the list of image file names in the folder
print(f"Training images: {myList}")
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])  # Extract and store the name (without file extension)

print(f"Class names: {classNames}")


if os.path.exists(encoding_file):
    print("Loading encodings from file...")
    with open(encoding_file, 'rb') as f:
        # Load encodings and class names from the file
        encodeListKnown, classNames = pickle.load(f)
    print("Encodings loaded successfully.")
else:
    print("Encoding faces...")
    # Function to find face encodings for a list of images
    def findEncodings(images):
        encodeList = []  # List to store encodings
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image to RGB
            try:
                encode = face_recognition.face_encodings(img)[0]  # Get face encoding
                encodeList.append(encode)  # Add encoding to the list
            except IndexError:
                print("Face not detected in one of the images. Skipping...")
        return encodeList

    encodeListKnown = findEncodings(images)  # Generate face encodings
    print('Encoding Complete')

    # Save encodings and class names to a file for future use
    with open(encoding_file, 'wb') as f:
        pickle.dump((encodeListKnown, classNames), f)
    print("Encodings saved to file.")

# Initialize database connection
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS ATTENDANCE (
    ID INTEGER,
    Name TEXT,
    Date TEXT,
    Time TEXT,
    Status TEXT
)
""")
conn.commit()  #

# Initialize webcam
cap = cv2.VideoCapture(0)  # Access the default webcam
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

attendance_log = {}  # Dictionary to log attendance records

while True:
    success, img = cap.read()  # Capture a frame from the webcam
    if not success:
        print("Failed to grab frame.")
        break

    # Resize and preprocess the frame
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Resize for faster processing
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # Convert to RGB

    # Detect and encode faces in the frame
    facesCurFrame = face_recognition.face_locations(imgS)  # Get face locations
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)  # Get encodings for the faces

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.5)  # Compare with known faces
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)  # Calculate distances
        matchIndex = np.argmin(faceDis)  # Find the best match index

        if matches[matchIndex] and faceDis[matchIndex] < 0.5:  # Check if a match is found
            user_id = int(classNames[matchIndex])  # Assume ID is the image name (as an integer)

            # Fetch the student's name from the database
            cursor.execute("SELECT Name FROM STUDENTS WHERE Id = ?", (user_id,))
            result = cursor.fetchone()
            if result:
                name = result[0]  # Retrieve the name from the database
            else:
                name = f"Unknown ({user_id})"  # Fallback if ID is not found in the database

            current_time = datetime.now()  # Get the current time
            date_str = current_time.strftime("%Y-%m-%d")  # Format the date
            time_str = current_time.strftime("%H:%M:%S")  # Format the time

            # Check if the user has already been marked present today
            cursor.execute("SELECT * FROM ATTENDANCE WHERE ID = ? AND Date = ?", (user_id, date_str))
            existing_record = cursor.fetchone()

            if not existing_record:  # If no record exists for today
                # Insert attendance into the database
                conn.execute("INSERT INTO ATTENDANCE (ID, Name, Date, Time, Status) VALUES (?, ?, ?, ?, ?)",
                             (user_id, name, date_str, time_str, "Present"))
                conn.commit()  # Save the attendance record
                print(f"Attendance marked for {name} on {date_str}")
            else:
                print(f"{name} has already been marked present today.")

            # Draw bounding box and name on the detected face
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scale up the coordinates
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw rectangle around the face
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)  # Draw filled rectangle below
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)  # Add name

    # Display the webcam feed
    cv2.imshow('Webcam', img)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Release the webcam
cv2.destroyAllWindows()  # Close all OpenCV windows
conn.close()  # Close the database connection
