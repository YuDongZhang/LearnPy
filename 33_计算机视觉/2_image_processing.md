# 2. 图像处理基础

## OpenCV简介

OpenCV 是最流行的计算机视觉库：C++ 实现、提供 Python 接口，覆盖图像处理、摄像头、特征检测。

```bash
pip install opencv-python
pip install opencv-python-headless  # 无GUI版本
```

## 图像读取和保存

```python
import cv2

img = cv2.imread("image.jpg")                      # 彩色（BGR）
img_gray = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)

print(img.shape)   # (height, width, channels)
print(img.size)    # 像素总数
cv2.imwrite("output.jpg", img)
```

OpenCV 与 PIL 互转：

```python
from PIL import Image
import numpy as np

img_pil = Image.open("image.jpg")
img_cv = np.array(img_pil)                                  # PIL → OpenCV
img_pil2 = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
```

## 图像基本操作

```python
# 裁剪: img[y1:y2, x1:x2]
roi = img[100:300, 200:400]

# 缩放
resized = cv2.resize(img, (224, 224))
resized = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)  # 缩放一半

# 旋转
rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# 翻转
flipped = cv2.flip(img, 1)   # 1 水平 / 0 垂直 / -1 双向
```

## 颜色空间转换

OpenCV 默认使用 **BGR** 顺序（不是 RGB）：

```python
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
```

颜色分割示例——提取蓝色物体：

```python
mask = cv2.inRange(hsv, np.array([100, 50, 50]), np.array([130, 255, 255]))
result = cv2.bitwise_and(img, img, mask=mask)
```

## 绘制图形

```python
img = np.zeros((500, 500, 3), dtype=np.uint8)

cv2.line(img, (0, 0), (500, 500), (0, 255, 0), 2)          # 线
cv2.rectangle(img, (50, 50), (200, 200), (255, 0, 0), 2)   # 矩形, -1 填充
cv2.circle(img, (250, 250), 50, (0, 0, 255), -1)           # 圆
cv2.putText(img, "Hello CV", (50, 250),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)  # 文字
```

## 图像滤波

| 滤波 | 函数 | 用途 |
|------|------|------|
| 均值滤波 | `cv2.blur(img, (5,5))` | 平滑 |
| 高斯滤波 | `cv2.GaussianBlur(img, (5,5), 0)` | 更自然的去噪 |
| 中值滤波 | `cv2.medianBlur(img, 5)` | 去除椒盐噪声 |
| 双边滤波 | `cv2.bilateralFilter(img, 9, 75, 75)` | 保边缘的平滑 |
| 锐化 | 自定义卷积核 | 增强边缘 |

```python
# 锐化卷积核
kernel_sharpen = np.array([[-1, -1, -1],
                           [-1,  9, -1],
                           [-1, -1, -1]])
sharpened = cv2.filter2D(img, -1, kernel_sharpen)

# 边缘检测
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
edges = cv2.Canny(gray, 50, 150)
```

## 形态学操作

先做二值化，再在二值图像上进行：

| 操作 | 说明 |
|------|------|
| 腐蚀 | 去除小的白色噪点 |
| 膨胀 | 扩大白色区域 |
| 开运算 | 先腐蚀后膨胀，去除噪声 |
| 闭运算 | 先膨胀后腐蚀，填补空洞 |
| 梯度 | 膨胀 − 腐蚀 = 轮廓 |

```python
kernel = np.ones((5, 5), np.uint8)
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
```

## 阈值处理

```python
# 固定阈值
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 自适应阈值（光照不均时）
thresh = cv2.adaptiveThreshold(gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Otsu 自动寻找最优阈值
_, thresh = cv2.threshold(blur, 0, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

## 轮廓检测

```python
contours, _ = cv2.findContours(binary, cv2.RETR_TREE,
                               cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

for contour in contours:
    area = cv2.contourArea(contour)              # 面积
    perimeter = cv2.arcLength(contour, True)     # 周长
    x, y, w, h = cv2.boundingRect(contour)       # 外接矩形
```

## 图像变换

```python
# 仿射变换（三点确定）
M = cv2.getAffineTransform(pts1, pts2)
affine = cv2.warpAffine(img, M, (cols, rows))

# 透视变换（四点确定，如文档矫正）
M = cv2.getPerspectiveTransform(pts1, pts2)
perspective = cv2.warpPerspective(img, M, (cols, rows))
```

## 图像拼接

```python
grid = np.vstack([np.hstack(images[0:2]), np.hstack(images[2:4])])  # 2x2

# 全景拼接
stitcher = cv2.Stitcher_create()
status, panorama = stitcher.stitch([img1, img2, img3])
```

## 视频处理

```python
cap = cv2.VideoCapture(0)          # 0 表示摄像头, 也可传 "video.mp4"

while True:
    ret, frame = cap.read()
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

保存视频：`cv2.VideoWriter("output.mp4", fourcc, 30.0, (640, 480))`。

## 摄像头人脸检测

```python
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                      minNeighbors=5, minSize=(30, 30))
for (x, y, w, h) in faces:
    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
```

## 代码

讲解对应的示例代码见 `2_image_processing.py`。
