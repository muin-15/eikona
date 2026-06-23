import cv2


image = cv2.imread('luffy.jpeg')
width_d = int(image.shape[1] *0.5)
height_d = int(image.shape[0] *0.5)
image_rd = cv2.resize(image, (width_d, height_d))
cv2.imwrite('luffy_resizedDownscaled.jpg', image_rd)
width_d = int(image.shape[1] *2)
height_d = int(image.shape[0] *2)
image_ru = cv2.resize(image, (width_d, height_d))
cv2.imwrite('luffy_resizedUpscaled.jpg', image_ru)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gaussian_filter = cv2.GaussianBlur(image, (5, 5), 0)
mean_filter=cv2.boxFilter(image, -1, (5, 5))
median_filter=cv2.medianBlur(image, 5)
laplacian_filter=cv2.Laplacian(image, cv2.CV_64F,ksize=3)
edges = cv2.Canny(gray, 100, 200)

"""cv2.imwrite('edges.jpg', edges)
cv2.imwrite('grayscale.jpg', gray)
cv2.imwrite('gaussian_color.jpg', gaussian_filter)
cv2.imwrite('mean_color.jpg', mean_filter)
cv2.imwrite('median_color.jpg',median_filter)"""
#cv2.imwrite('Laplacian_color.jpg',laplacian_filter)