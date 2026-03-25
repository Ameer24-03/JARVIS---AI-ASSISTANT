import time
import cv2


def AuthenticateFace():

    flag = 0

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('engine\\auth\\trainer\\trainer.yml')

    cascadePath = "engine\\auth\\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX

    names = ['', 'Ameer']

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    start_time = time.time()

    while True:

        ret, img = cam.read()

        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            id, accuracy = recognizer.predict(gray[y:y+h, x:x+w])

            confidence = round(100 - accuracy)

            if accuracy < 70:

                name = names[id]

                cv2.putText(img, name, (x+5, y-5),
                            font, 1, (255, 255, 255), 2)

                cv2.putText(img, str(confidence) + "%",
                            (x+5, y+h-5),
                            font, 1, (0, 255, 0), 2)

                flag = 1

            else:

                cv2.putText(img, "Unknown",
                            (x+5, y-5),
                            font, 1, (0, 0, 255), 2)

                cv2.putText(img, str(confidence) + "%",
                            (x+5, y+h-5),
                            font, 1, (0, 0, 255), 2)

        cv2.imshow("Jarvis Face Authentication", img)

        key = cv2.waitKey(1) & 0xff

        # scan for 4 seconds
        if time.time() - start_time > 4:
            break

        if key == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

    return flag


if __name__ == "__main__":
    result = AuthenticateFace()
    print("Authentication Result:", result)