import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create a figure and axis
fig, ax = plt.subplots()

# Add a square (starting at x=1, y=1 with side length 2)
square = patches.Rectangle((1, 1), 2, 2, linewidth=2, edgecolor='blue', facecolor='lightblue')
ax.add_patch(square)
square = patches.Rectangle((3, 1), 2, 2, linewidth=2, edgecolor='blue', facecolor='lightblue')
ax.add_patch(square)

# Set the limits of the plot
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal', adjustable='box')  # Keep the aspect ratio equal

# Show the plot
plt.title("aquifer")
plt.show()
