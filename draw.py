import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

class Shape:
    coordinates = []
    color = (255, 0, 0)
    area = 1.
    def __init__(self, coordinates = None, color = None):
        if coordinates != None:
            self.coordinates = coordinates
        if color != None:
            self.color = color
    @staticmethod
    def create():
        obj = Shape()
        return obj

    def draw_closed_shape(self, img, thickness=2):
            """
            Draw a closed shape using the given points.

            Args:
            points (list of tuples): List of (x, y) points.
            color (tuple): Color of the shape in BGR format (default is green).
            thickness (int): Thickness of the shape's lines (default is 2).
            """
        

            # Convert points to a numpy array
            points_array = np.array(self.coordinates, np.int32)

            # Reshape points to be in the right format for cv2.polylines (as a single list of points)
            points_array = points_array.reshape((-1, 1, 2))

            # Draw the polygon (closed shape)
            cv2.polylines(img, [points_array], isClosed=True, color=self.color, thickness=thickness)

            # Fill the polygon with color
            cv2.fillPoly(img, [points_array], color=self.color) 
      
    def calculateArea(self):
        coords = self.coordinates
        n = len(coords)
        if n < 3:
            raise ValueError("At least three coordinates are required to form a polygon.")

        area = 0
        for i in range(n):
            x1, y1 = coords[i]
            x2, y2 = coords[(i + 1) % n]  # Wrap around to the first point

            area += (x1 * y2) - (y1 * x2)

        self.area = abs(area) / 2 

def draw_agents(shapes):
        # Create a blank image (black background)
        width = 540
        height = 540
        img = np.zeros((width, height, 3), dtype=np.uint8)
        for shape in shapes:
            shape.draw_closed_shape(img)
        # Show the image
        cv2.imshow("Closed Shape", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def test():
    # Load the image
    image = cv2.imread("pics/image1.jpg")

    # Define the original image's corners (assuming it's a rectangle)
    h, w, _ = image.shape
    original_pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]])  # (top-left, top-right, bottom-right, bottom-left)

    # Define the target coordinates where the image should be placed
    x1, y1 = 100, 100
    x2, y2 = 200, 200
    target_pts = np.float32([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])

    # Compute the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(original_pts, target_pts)

    # Warp the image to fit the new coordinates
    warped_image = cv2.warpPerspective(image, matrix, (500, 500))  # Adjust output size as needed

    # Show the transformed image
    cv2.imshow("Warped Image", warped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
# Example usage:
# points = [(100, 100), (200, 100), (200, 200), (100, 200)]  # Points of a rectangle
# draw_closed_shape(points, color=(255, 0, 0))  # Red color
