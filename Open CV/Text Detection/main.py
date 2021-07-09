import cv2.cv2 as cv2
import numpy as np


class TextEdgeDetect:
    def __init__(self, kernel):
        """
        initialize
        :param kernel: kernel size
        :type kernel: int
        """
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel, kernel))

    @staticmethod
    def __read_images(path):
        """
        read image from file
        :param path: path of target image
        :type path: string
        :return: image
        :rtype: np.ndarray
        """
        img = cv2.imread(path)
        return img

    @staticmethod
    def __convert_color_space(img):
        """
        convert bgr image to gray scale image
        :param img: raw image that need to convert
        :type img: np.ndarray
        :return: new image in gray scale
        :rtype: np.ndarray
        """
        new_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return new_img

    @staticmethod
    def __canny_edge_detector(img_after_cvt_gray, blur_ksize=5, threshold1=100, threshold2=200):
        """
        edges detect for objects in image
        :param img_after_cvt_gray: gray scale image that need to detect edge
        :type img_after_cvt_gray: np.ndarray
        :param blur_ksize: gaussian kernel size
        :type blur_ksize: int
        :param threshold1: min threshold
        :type threshold1: int
        :param threshold2: max threshold
        :type threshold2: int
        :return: image that contains only edges
        :rtype: np.ndarray
        """
        img_gaussian = cv2.GaussianBlur(img_after_cvt_gray, (blur_ksize, blur_ksize), 0)
        img_canny = cv2.Canny(img_gaussian, threshold1, threshold2)
        return img_canny

    def __morphology_ex(self, edge):
        """
        morphological transformations for better detect edge
        :param edge: image after apply canny detector
        :type edge: np.ndarray
        :return: dilation
        :rtype: np.ndarray
        """
        morph = cv2.morphologyEx(edge, cv2.MORPH_DILATE, self.kernel)
        return morph

    @staticmethod
    def __get_only_text(contours):
        """
        get only contour of text, not include pictures or boxes in image
        :param contours: old contours
        :type contours: list of vectors
        :return: new contours
        :rtype: list of vectors
        """
        new_contour = filter(lambda contour: cv2.boundingRect(contour)[1] > 100
                             and cv2.boundingRect(contour)[3] < 100
                             and cv2.contourArea(contour) > 100, contours)
        return new_contour

    @staticmethod
    def __get_only_answer_boxes(contours):
        """
        get only contours of answer boxes
        :param contours: old contours
        :type contours: list of vectors
        :return: new contours
        :rtype: list of vectors
        """
        new_contour = filter(lambda contour: cv2.boundingRect(contour)[1] > 100
                             and cv2.boundingRect(contour)[2] > 500
                             and cv2.boundingRect(contour)[3] > 100
                             and cv2.contourArea(contour) > 1000, contours)
        return new_contour

    @staticmethod
    def __draw_mask(mask, contours):
        """
        draw solid white mask on detected contours in order to take it easier to extract objects later
        :param mask: matrix that we want to color it white
        :type mask: np.ndarray
        :param contours: detected contours
        :type contours: list of vectors
        :return: solid white mask
        :rtype: np.ndarray
        """
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            x2, y2 = x + w, y + h
            points = np.array([[x, y], [x, y2], [x2, y2], [x2, y]])
            cv2.fillPoly(mask, pts=[points], color=(255, 255, 255))
        return mask

    @staticmethod
    def __draw_bounding_rect(img, contours):
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

    def text_detect(self, path):
        """
        detect text in image
        :param path: path of image
        :type path: string
        :return: image with bounding box for detected text
        :rtype: np.ndarray
        """
        image = self.__read_images(path)
        gray_image = self.__convert_color_space(image)
        image_edge = self.__canny_edge_detector(gray_image)
        morph = self.__morphology_ex(image_edge)
        contours, hierarchy = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        new_contours = self.__get_only_text(contours)
        white_mask_for_text_area = np.zeros_like(morph)
        white_mask_for_text_area = self.__draw_mask(white_mask_for_text_area, new_contours)
        mask_morph = self.__morphology_ex(white_mask_for_text_area)
        contours, hierarchy = cv2.findContours(mask_morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.__draw_bounding_rect(image, contours)
        return image

    def answer_boxes_detect(self, path):
        """
        detect answer boxes in image
        :param path: image path
        :type path: string
        :return: image with bounding box for detected boxes
        :rtype: np.ndarray
        """
        image = self.__read_images(path)
        gray_image = self.__convert_color_space(image)
        image_edge = self.__canny_edge_detector(gray_image)
        morph = self.__morphology_ex(image_edge)
        contours, hierarchy = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        new_contours = self.__get_only_answer_boxes(contours)
        white_mask_for_boxes_area = np.zeros_like(morph)
        white_mask_for_boxes_area = self.__draw_mask(white_mask_for_boxes_area, new_contours)
        mask_morph = self.__morphology_ex(white_mask_for_boxes_area)
        contours, hierarchy = cv2.findContours(mask_morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.__draw_bounding_rect(image, contours)
        return image

    @staticmethod
    def __random_generate_tic_toe(image):
        """
        This method used to random generate tic toe to the image with defined positions
        :param image: image to work with
        :type image: np.ndarray
        :return: image with random tic toe
        :rtype: np.ndarray
        """
        positions = [(np.random.randint(100, 1700), np.random.randint(200, 2700)) for i in range(10)]
        for pos in positions:
            cv2.drawMarker(image, pos, (0, 0, 255), markerType=cv2.MARKER_TILTED_CROSS, markerSize=50,
                           thickness=3, line_type=cv2.LINE_AA)
        return image, positions

    def answer_boxes_with_tic_toe_detect(self, path):
        """
        detect only answer box that has tic toe marker
        :param path: image path
        :type path: string
        :return: image with bounding box for detected object
        :rtype: np.ndarray
        """
        image = self.__read_images(path)
        image_edge = self.__canny_edge_detector(image)
        morph = self.__morphology_ex(image_edge)
        contours, hierarchy = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        answer_box_contours = self.__get_only_answer_boxes(contours)
        white_mask_for_boxes_area = np.zeros_like(morph)
        white_mask_for_boxes_area = self.__draw_mask(white_mask_for_boxes_area, answer_box_contours)
        mask_morph = self.__morphology_ex(white_mask_for_boxes_area)
        contours, hierarchy = cv2.findContours(mask_morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        image_with_tic_toe, positions = self.__random_generate_tic_toe(image)
        new_contours = []
        for contour in contours:
            distances = [cv2.pointPolygonTest(contour, pos, False) for pos in positions]
            for dist in distances:
                if dist > 0:
                    new_contours.append(contour)
                    break
        cv2.drawContours(image_with_tic_toe, new_contours, -1, (0, 255, 0), 3)
        return image_with_tic_toe

    @staticmethod
    def write_image(path, img):
        """
        save image to file
        :param path: directory to save image
        :type path: string
        :param img:
        :type img:
        :return:
        :rtype:
        """
        cv2.imwrite(path, img)

    @staticmethod
    def show_image(img):
        """
        show image
        :param img: image to show
        :type img: np.ndarray
        :return:
        :rtype:
        """
        cv2.imshow("Image", img)
        cv2.waitKey(0)
