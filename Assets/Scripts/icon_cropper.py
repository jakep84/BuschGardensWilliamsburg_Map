# icon_cropper.py
import cv2
import os

img = cv2.imread('bgw2025_map1.png')
clone = img.copy()
folder = 'icons'
os.makedirs(folder, exist_ok=True)
ref_points = []
count = 0

def click_and_crop(event, x, y, flags, param):
    global ref_points, count

    if event == cv2.EVENT_LBUTTONDOWN:
        ref_points = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP:
        ref_points.append((x, y))
        x1, y1 = ref_points[0]
        x2, y2 = ref_points[1]
        roi = clone[y1:y2, x1:x2]
        cv2.imshow("Cropped Icon", roi)
        filename = f'{folder}/icon_{count}.png'
        cv2.imwrite(filename, roi)
        print(f"Saved: {filename}")
        count += 1

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", click_and_crop)

while True:
    cv2.imshow("Image", clone)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
