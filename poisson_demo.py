"""Simple demo of a 2D poisson problem"""

import matplotlib.pyplot as plt
from poisson_solver import solve_poisson_problem

# Define the size of the grid
nx, ny = 101, 101

# Solve the Poisson equation on this grid
u, x, y, residual = solve_poisson_problem(nx, ny, source_value=1.0)

print("2D Poisson solve with sparse matrix assembly")
print(f"Grid Size: {nx} x {ny}")
print(f"Calculation Residual: {residual:.3e}")
print(f"Solution Range: [{u.min():.6f}, {u.max():.6f}]")

# Plot the solution
fig, ax = plt.subplots()
p = ax.pcolormesh(x, y, u)
c = plt.colorbar(p)
ax.set_aspect("equal")
ax.set_xlabel("x  [dimensonless]")
ax.set_ylabel("y  [dimensonless]")
c.set_label("z  [dimensonless]")
ax.set_title("2D Poisson Problem")
fig.savefig("poisson_demo.png")