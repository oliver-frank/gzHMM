import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# Generate data for Green Cluster
mean_green = [3.1, 3.5]
cov_green = [[0.3, 0.1], [0.1, 0.3]]
green_dots = np.random.multivariate_normal(mean_green, cov_green, 100)

# Generate data for Red Cluster
mean_red = [3.0, 4.0]
cov_red = [[0.3, 0.1], [0.1, 0.3]]
red_dots = np.random.multivariate_normal(mean_red, cov_red, 100)

# Create the plot
fig, ax = plt.subplots(figsize=(7, 6))

fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Plot the data points
ax.scatter(green_dots[:, 0], green_dots[:, 1], color='green', alpha=0.8, edgecolors='none', label='Class 1')
ax.scatter(red_dots[:, 0], red_dots[:, 1], color='red', alpha=0.8, edgecolors='none', label='Class 2')

# Define and plot the decision line 
x_vals = np.linspace(1.0, 6.0, 100)
y_vals = 0.9 * x_vals + 1.2  # Positive slope configuration
ax.plot(x_vals, y_vals, color='black', linestyle='--', linewidth=2)

ax.set_xlim(1.0, 6.0)
ax.set_ylim(0.5, 6.5)

ax.set_ylabel('PC1')
ax.set_xlabel('PC2')

ax.grid(False)

plt.show()

