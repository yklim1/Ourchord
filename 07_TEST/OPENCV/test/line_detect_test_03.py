import cv2
import numpy as np

img = cv2.imread('file_path')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel_size = 5
blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

low_threshold = 50
high_threshold = 150
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

rho = 1     # distance resolution in pixels of the Hough grid
theta = np.pi / 180     # angular resolution in radians of the Hough grid
threshold = 15          # minimum number of votes (intersections in Hough grid cell)
min_line_length = 500    # minimum number of pixels making up a line
max_line_gap = 20       # maximum gap in pixels between connectable line segments
line_image = np.copy(img) * 0   # creating a blank to draw lines on

# lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
lines = cv2.HoughLinesP(edges,1,np.pi/180,650,min_line_length,max_line_gap)
# print(lines)

y = []
ylist = []
demensions = img.shape

for line in lines:
    x1,y1,x2,y2 = line[0]
    if(y2 - y1 == 0):
        y.append(y1)
    # cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
y = list(set(y))
y.sort()

for i in range(len(y)):
    if(i == len(y)):
        break
    elif(y[i+1] - y[i] <= 5):
        y.pop(i + 1)
    else:
        print("I dont't know")

for index, value in enumerate(y):
    print(index + 1, ": ", value)

print("length: ", len(y))

for a in y:
    cv2.line(img, (0, a + 1), (img.shape[1], a + 1), (255, 0, 0), 1)
    
cv2.imshow('edges', edges)
cv2.imshow('result', img)
cv2.waitKey()
cv2.destroyAllWindows()