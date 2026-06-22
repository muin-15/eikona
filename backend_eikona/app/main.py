import cv2


image = cv2.imread('luffy.jpeg')


gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred_bw = cv2.GaussianBlur(gray, (5, 5), 0)
gaussian_bw = cv2.GaussianBlur(gray, (5, 5), 0)
mean_bw=cv2.boxFilter(gray, -1, (5, 5))
blurred_color = cv2.GaussianBlur(image, (5, 5), 0)
gaussian_color = cv2.GaussianBlur(image, (5, 5), 0)
mean_color=cv2.boxFilter(image, -1, (5, 5))
edges = cv2.Canny(blurred_bw, 100, 200)

cv2.imwrite('edges.jpg', edges)
cv2.imwrite('grayscale.jpg', gray)
cv2.imwrite('blurred_bw.jpg', blurred_bw)
cv2.imwrite('gaussian_bw.jpg', gaussian_bw)
cv2.imwrite('mean_bw.jpg', mean_bw)
cv2.imwrite('blurred_color.jpg', blurred_color)
cv2.imwrite('gaussian_color.jpg', gaussian_color)
cv2.imwrite('mean_color.jpg', mean_color)