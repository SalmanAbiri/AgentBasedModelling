import cv2
import numpy as np

class Shape:
    coordinates = []
    color = (255, 0, 0)
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

def draw_agents(shapes):
        # Create a blank image (black background)
        img = np.zeros((500, 500, 3), dtype=np.uint8)
        for shape in shapes:
            shape.draw_closed_shape(img)
        # Show the image
        cv2.imshow("Closed Shape", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()    
# Example usage:
# points = [(100, 100), (200, 100), (200, 200), (100, 200)]  # Points of a rectangle
# draw_closed_shape(points, color=(255, 0, 0))  # Red color
