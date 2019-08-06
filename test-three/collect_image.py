import cv2

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    cv2.imshow('Frame', frame)
    cv2.imwrite("./img/new/filename.jpg", frame)
    if cv2.waitKey(20) & 0xff == ord('q'):
        break


# realize capture
cap.release()
cv2.destroyAllWindows()
