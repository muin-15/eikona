import cv2

# Read image
image = cv2.imread('lufy.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('grayscale.jpg', gray)
edges = cv2.Canny(gray, 100, 200)
cv2.imwrite('edges.jpg', edges)