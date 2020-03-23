import numpy
import cv2

class GaussianBlur5x5:

    def __init__(self, surface_, shape_):

        # ядро 5x5
        self.kernel_v = numpy.array(([1 / 16, 4 / 16, 6 / 16, 4 / 16, 1 / 16]))  # вертикальный вектор
        self.kernel_h = numpy.array(([1 / 16, 4 / 16, 6 / 16, 4 / 16, 1 / 16]))  # горизонтальный вектор

        self.kernel_half = 2
        self.surface = surface_
        self.shape = shape_
        self.source_array = numpy.zeros((self.shape[0], self.shape[1], 3))

    # горизонталь
    def convolution_h(self):

        for y in range(0, self.shape[1]):

            for x in range(0, self.shape[0]):
                r, g, b = 0, 0, 0

                for kernel_offset in range(-self.kernel_half, self.kernel_half + 1):
                    try:
                        xx = x + kernel_offset
                        k = self.kernel_h[kernel_offset + self.kernel_half]
                        color = self.surface[xx,y]
                        r += color[0] * k
                        g += color[1] * k
                        b += color[2] * k

                    except IndexError:
                        k = self.kernel_h[kernel_offset + self.kernel_half]
                        r += 128 * k
                        g += 128 * k
                        b += 128 * k

                self.source_array[x][y] = (r, g, b)

        return self.source_array

    # вертикаль
    def convolution_v(self):

        for y in range(0, self.shape[1]):

            for x in range(0, self.shape[0]):
                r, g, b = 0, 0, 0
                for kernel_offset in range(-self.kernel_half, self.kernel_half + 1):
                    try:
                        yy = y + kernel_offset
                        color = self.surface[x, yy]
                        k = self.kernel_v[kernel_offset + self.kernel_half]
                        r += color[0] * k
                        g += color[1] * k
                        b += color[2] * k

                    except IndexError:
                        k = self.kernel_v[kernel_offset + self.kernel_half]
                        r += 128 * k
                        g += 128 * k
                        b += 128 * k

                self.source_array[x][y] = (r, g, b)

        return self.source_array

    def convolutions(self):
        print(self.shape[0])
        print(self.shape[1])
        vertical_convo = self.convolution_v()
        self.surface = vertical_convo
        return self.convolution_h()


if __name__ == '__main__':
    img = cv2.imread('m1.jpg')
    pyrup_opencv = cv2.pyrUp(img,borderType=cv2.BORDER_REFLECT_101)
    cv2.imwrite("OpenCV.jpg", pyrup_opencv)

    img1 = img[:, :].repeat(2, axis=0).repeat(2, axis=1)
    w, h, c = img1.shape

    Gauss = GaussianBlur5x5(img1, img1.shape)
    array = Gauss.convolutions()

    cv2.imwrite('my.jpg', array)
    cv2.imwrite('output_diff1.jpg', array - pyrup_opencv)
