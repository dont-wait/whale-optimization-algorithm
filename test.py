import numpy as np
import matplotlib.pyplot as plt

# Thiết lập giới hạn và độ phân giải
xmin, xmax, ymin, ymax = -5, 5, -5, 5
resolution = 0.1

# Tạo các mảng x và y
x = np.arange(xmin, xmax + resolution, resolution)
y = np.arange(ymin, ymax + resolution, resolution)

# Tạo lưới
xx, yy = np.meshgrid(x, y, sparse=True)

# Ví dụ hàm: z = x^2 + y^2
z = xx**2 + yy**2

# Vẽ đồ thị
plt.figure()
plt.contourf(xx, yy, z, levels=50, cmap='viridis')
plt.colorbar()  # Thêm thanh màu
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Contour Plot of z = x^2 + y^2')
plt.show()