import cv2


image = cv2.imread('luffy.jpeg')


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gaussian_filter = cv2.GaussianBlur(image, (5, 5), 0)
mean_filter=cv2.boxFilter(image, -1, (5, 5))
median_filter=cv2.medianBlur(image, 5)
edges = cv2.Canny(gray, 100, 200)

cv2.imwrite('edges.jpg', edges)
cv2.imwrite('grayscale.jpg', gray)
cv2.imwrite('gaussian_color.jpg', gaussian_filter)
cv2.imwrite('mean_color.jpg', mean_filter)
cv2.imwrite('median_color.jpg',median_filter)