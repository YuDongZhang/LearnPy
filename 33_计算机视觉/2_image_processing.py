"""
图像处理基础
==========

介绍使用 OpenCV 和 PIL 进行图像处理的基础技术。
由于环境中未安装 opencv-python，以下为示例代码展示。
"""

print("=" * 60)
print("1. OpenCV 基础")
print("=" * 60)

print("""
OpenCV (Open Source Computer Vision Library):

  • 最流行的计算机视觉库
  • C++ 实现，提供 Python 接口
  • 图像处理、摄像头、特征检测

安装:
  pip install opencv-python
  pip install opencv-python-headless  # 无GUI版本
""")

print()
print("=" * 60)
print("2. 图像读取和保存")
print("=" * 60)

print('''
import cv2
import numpy as np
from PIL import Image

# 2.1 读取图像
img = cv2.imread("image.jpg")  # 彩色图像
img_gray = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)

# 2.2 获取图像信息
print(f"Shape: {img.shape}")  # (height, width, channels)
print(f"Size: {img.size}")   # 像素总数
print(f"Dtype: {img.dtype}") # 数据类型

# 2.3 保存图像
cv2.imwrite("output.jpg", img)
cv2.imwrite("output.png", img)

# 2.4 使用 PIL
img_pil = Image.open("image.jpg")
img_gray_pil = img_pil.convert("L")

# PIL 转 OpenCV
img_cv = np.array(img_pil)
# OpenCV 转 PIL
img_pil2 = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
''')

print()
print("=" * 60)
print("3. 图像基本操作")
print("=" * 60)

print('''
import cv2
import numpy as np

# 3.1 创建图像
# 黑色图像
black = np.zeros((480, 640, 3), dtype=np.uint8)

# 白色图像
white = np.ones((480, 640, 3), dtype=np.uint8) * 255

# 指定颜色
blue = np.full((480, 640, 3), (255, 0, 0), dtype=np.uint8)

# 3.2 裁剪图像
# img[y1:y2, x1:x2]
roi = img[100:300, 200:400]

# 3.3 缩放图像
resized = cv2.resize(img, (224, 224))
resized = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)  # 缩放一半

# 3.4 旋转图像
# 旋转 90 度
rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# 任意角度旋转
def rotate_image(img, angle):
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    return rotated

# 3.5 翻转图像
flipped = cv2.flip(img, 1)  # 水平翻转
flipped = cv2.flip(img, 0)  # 垂直翻转
flipped = cv2.flip(img, -1) # 水平垂直翻转
''')

print()
print("=" * 60)
print("4. 颜色空间转换")
print("=" * 60)

print('''
import cv2
import numpy as np

# 4.1 颜色空间
# BGR (OpenCV 默认)
# RGB
# Gray (灰度)
# HSV (色相、饱和度、亮度)
# LAB

# 4.2 BGR 转 RGB
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 4.3 BGR 转灰度
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 4.4 BGR 转 HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 4.5 灰度转 BGR
bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

# 4.6 颜色分割示例 - 提取蓝色物体
# 定义蓝色范围
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

# 创建掩码
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# 应用掩码
result = cv2.bitwise_and(img, img, mask=mask)
''')

print()
print("=" * 60)
print("5. 绘制图形")
print("=" * 60)

print('''
import cv2
import numpy as np

# 创建空白图像
img = np.zeros((500, 500, 3), dtype=np.uint8)

# 5.1 画线
cv2.line(img, (0, 0), (500, 500), (0, 255, 0), 2)

# 5.2 画矩形
cv2.rectangle(img, (50, 50), (200, 200), (255, 0, 0), 2)
cv2.rectangle(img, (50, 50), (200, 200), (255, 0, 0), -1)  # 填充

# 5.3 画圆
cv2.circle(img, (250, 250), 50, (0, 0, 255), -1)

# 5.4 画椭圆
cv2.ellipse(img, (250, 250), (100, 50), 0, 0, 360, (255, 255, 0), 2)

# 5.5 画多边形
pts = np.array([[100, 100], [200, 100], [150, 200]], np.int32)
cv2.polylines(img, [pts], True, (255, 0, 255), 2)

# 5.6 添加文字
cv2.putText(img, "Hello CV", (50, 250),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# 5.7 绘制关键点 (for SIFT/ORB)
keypoints = [cv2.KeyPoint(100, 100, 10)]
img_with_kp = cv2.drawKeypoints(img, keypoints, None)
''')

print()
print("=" * 60)
print("6. 图像滤波")
print("=" * 60)

print('''
import cv2
import numpy as np

# 6.1 均值滤波 (平滑)
blur = cv2.blur(img, (5, 5))

# 6.2 高斯滤波 (更自然的平滑)
gaussian = cv2.GaussianBlur(img, (5, 5), 0)

# 6.3 中值滤波 (去除椒盐噪声)
median = cv2.medianBlur(img, 5)

# 6.4 双边滤波 (保持边缘的平滑)
bilateral = cv2.bilateralFilter(img, 9, 75, 75)

# 6.5 自定义滤波器
kernel = np.ones((5, 5), np.float32) / 25
filtered = cv2.filter2D(img, -1, kernel)

# 6.6 锐化
kernel_sharpen = np.array([
    [-1, -1, -1],
    [-1,  9, -1],
    [-1, -1, -1]
])
sharpened = cv2.filter2D(img, -1, kernel_sharpen)

# 6.7 边缘检测 - Sobel
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

# 6.8 边缘检测 - Laplacian
laplacian = cv2.Laplacian(gray, cv2.CV_64F)

# 6.9 边缘检测 - Canny
edges = cv2.Canny(gray, 50, 150)
''')

print()
print("=" * 60)
print("7. 形态学操作")
print("=" * 60)

print('''
import cv2
import numpy as np

# 创建二值图像
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 7.1 腐蚀 (去除小的白色区域)
kernel = np.ones((5, 5), np.uint8)
eroded = cv2.erode(binary, kernel, iterations=1)

# 7.2 膨胀 (扩大白色区域)
dilated = cv2.dilate(binary, kernel, iterations=1)

# 7.3 开运算 (先腐蚀后膨胀 - 去除噪声)
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

# 7.4 闭运算 (先膨胀后腐蚀 - 填补空洞)
closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

# 7.5 梯度运算 (膨胀 - 腐蚀 = 轮廓)
gradient = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)

# 7.6 顶帽 (原图 - 开运算)
tophat = cv2.morphologyEx(binary, cv2.MORPH_TOPHAT, kernel)

# 7.7 黑帽 (闭运算 - 原图)
blackhat = cv2.morphologyEx(binary, cv2.MORPH_BLACKHAT, kernel)
''')

print()
print("=" * 60)
print("8. 图像阈值处理")
print("=" * 60)

print('''
import cv2
import numpy as np

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 8.1 固定阈值
_, thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 8.2 自适应阈值 - 均值
thresh2 = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY, 11, 2
)

# 8.3 自适应阈值 - 高斯
thresh3 = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 11, 2
)

# 8.4 Otsu's 阈值 (自动寻找最优阈值)
_, thresh4 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 8.5 大津法结合高斯模糊
blur = cv2.GaussianBlur(gray, (5, 5), 0)
_, thresh5 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
''')

print()
print("=" * 60)
print("9. 轮廓检测")
print("=" * 60)

print('''
import cv2

# 9.1 查找轮廓
contours, hierarchy = cv2.findContours(
    binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
)

# 9.2 绘制轮廓
contour_img = img.copy()
cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)

# 9.3 绘制单个轮廓
cv2.drawContours(contour_img, [contours[0]], -1, (0, 255, 0), 2)

# 9.4 轮廓特征
for contour in contours:
    # 面积
    area = cv2.contourArea(contour)

    # 周长
    perimeter = cv2.arcLength(contour, True)

    # 外接矩形
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(contour_img, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # 最小外接矩形
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(contour_img, [box], 0, (255, 0, 0), 2)

    # 最小外接圆
    (x, y), radius = cv2.minEnclosingCircle(contour)
    center = (int(x), int(y))
    radius = int(radius)
    cv2.circle(contour_img, center, radius, (255, 255, 0), 2)

# 9.5 轮廓近似
epsilon = 0.01 * perimeter
approx = cv2.approxPolyDP(contour, epsilon, True)
''')

print()
print("=" * 60)
print("10. 图像变换")
print("=" * 60)

print('''
import cv2
import numpy as np

# 10.1 仿射变换
# 定义三个点
pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
pts2 = np.float32([[10, 100], [200, 50], [100, 250]])

M = cv2.getAffineTransform(pts1, pts2)
affine = cv2.warpAffine(img, M, (cols, rows))

# 10.2 透视变换
pts1 = np.float32([[0, 0], [cols-1, 0], [0, rows-1], [cols-1, rows-1]])
pts2 = np.float32([[0, 0], [cols-1, 0], [0, rows-1], [cols-1, rows-1]])
# 修改 pts2 实现变形效果

M = cv2.getPerspectiveTransform(pts1, pts2)
perspective = cv2.warpPerspective(img, M, (cols, rows))

# 10.3 极坐标变换
polar = cv2.linearPolar(img, center, maxRadius, cv2.WARP_FILL_OUTLIERS)

# 10.4 Log -polar
log_polar = cv2.logPolar(img, center, maxRadius, cv2.WARP_FILL_OUTLIERS)
''')

print()
print("=" * 60)
print("11. 图像拼接")
print("=" * 60)

print('''
import cv2
import numpy as np

# 11.1 水平拼接
hstack = np.hstack([img1, img2])

# 11.2 垂直拼接
vstack = np.vstack([img1, img2])

# 11.3 使用 OpenCV 拼接
concat_h = cv2.hconcat([img1, img2])
concat_v = cv2.vconcat([img1, img2])

# 11.4 批量图像拼接
images = [img1, img2, img3, img4]
# 2x2 网格
row1 = np.hstack(images[0:2])
row2 = np.hstack(images[2:4])
grid = np.vstack([row1, row2])

# 11.5 Stitcher (全景拼接)
stitcher = cv2.Stitcher_create()
status, panorama = stitcher.stitch([img1, img2, img3])
''')

print()
print("=" * 60)
print("12. 视频处理")
print("=" * 60)

print('''
import cv2

# 12.1 读取视频
cap = cv2.VideoCapture("video.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 处理帧
    cv2.imshow("Video", frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# 12.2 摄像头读取
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# 12.3 保存视频
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("output.mp4", fourcc, 30.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)

out.release()

# 12.4 视频属性
fps = cap.get(cv2.CAP_PROP_FPS)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
''')

print()
print("=" * 60)
print("13. 摄像头人脸检测")
print("=" * 60)

print('''
import cv2

# 加载预训练模型
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# 也可以检测眼睛
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 检测人脸
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # 在人脸区域检测眼睛
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
''')

print()
print("=" * 60)
print("14. 图像处理总结")
print("=" * 60)

print("""
图像处理核心操作:

✓ 基础操作:
  • 读取、保存、显示
  • 裁剪、缩放、旋转

✓ 颜色处理:
  • 颜色空间转换
  • 颜色分割

✓ 滤波:
  • 平滑 (均值、高斯、中值)
  • 边缘检测 (Canny, Sobel)

✓ 形态学:
  • 腐蚀、膨胀
  • 开运算、闭运算

✓ 轮廓:
  • 检测、绘制
  • 特征提取

✓ 变换:
  • 仿射、透视
  • 极坐标

✓ 视频:
  • 读取、保存
  • 摄像头处理
""")
