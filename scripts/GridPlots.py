import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

"""
# Lagrange basis function in 1D
def lagrange_basis_1d(order, i, x):
    xi = np.linspace(0, 1, order + 1)
    L = np.ones_like(x)
    for j in range(order + 1):
        if j != i:
            L *= (x - xi[j]) / (xi[i] - xi[j])
    return L

# Plot 1D Lagrange basis functions for orders 1 to 3
x_plot = np.linspace(0, 1, 500)
orders_1d = [1, 2, 3]

for order in orders_1d:
    plt.figure(figsize=(6, 4))
    xi = np.linspace(0, 1, order + 1)
    cmap = cm.get_cmap("tab10")

    plt.plot([0, 1], [0, 0], 'k-', linewidth=1)  # Edge

    for i in range(order + 1):
        y = lagrange_basis_1d(order, i, x_plot)
        color = cmap(i % 10)
        plt.plot(x_plot, y, label=fr"$b_h^{{{i}}}(x)$", color=color)
        plt.plot(xi[i], lagrange_basis_1d(order, i, xi[i]), 'o', color=color)  # DoF point
        plt.plot(xi[i], 0, 'o', color=color)

    plt.title(f"Lagrange Basis Functions (Order {order})")
    plt.xticks(xi)
    plt.grid(False)
    plt.tight_layout()
    plt.savefig(f"lagrange_basis_order_{order}_1d.png")
    plt.close()

# 2D Tensor-product basis functions
def tensor_product_basis(order, i, j, X, Y):
    bx = lagrange_basis_1d(order, i, X)
    by = lagrange_basis_1d(order, j, Y)
    return np.outer(bx, by).T 

orders_2d = [1, 2, 3]
x_plot_2d = np.linspace(0, 1, 100)
X, Y = np.meshgrid(x_plot_2d, x_plot_2d)

for order in orders_2d:
    dof_points = np.linspace(0, 1, order + 1)
    for i in range(order + 1):
        for j in range(order + 1):
            # Plot 

            Z = tensor_product_basis(order, i, j, x_plot_2d, x_plot_2d)
            plt.figure(figsize=(5, 4))
            cs = plt.contourf(X, Y, Z, levels=50, cmap="viridis")
            plt.colorbar(cs)
            # All DoFs
            for m in range(order + 1):
                for n in range(order + 1):
                    color = 'red' if (m == i and n == j) else 'black'
                    plt.plot(dof_points[m], dof_points[n], 'o', color=color)
            plt.xlabel("x")
            plt.ylabel("y")
            plt.axis("equal")
            plt.tight_layout()
            plt.savefig(f"tensor_basis_order_{order}_dof_{i}_{j}.png")
            plt.close()

# Add 3D surface plots for tensor-product basis functions
for order in orders_2d:
    dof_points = np.linspace(0, 1, order + 1)
    for i in range(order + 1):
        for j in range(order + 1):
            Z = tensor_product_basis(order, i, j, x_plot_2d, x_plot_2d)

            fig = plt.figure(figsize=(6, 5))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor='k', linewidth=0.3, alpha=0.9)

            # Mark all DoFs
            for m in range(order + 1):
                for n in range(order + 1):
                    x = dof_points[m]
                    y = dof_points[n]
                    z = 0
                    color = 'red' if (m == i and n == j) else 'black'
                    ax.scatter(x, y, z, color=color, s=30)

            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_zlabel("b(x, y)")
            ax.view_init(elev=30, azim=-60)
            plt.tight_layout()
            plt.savefig(f"tensor_basis_order_{order}_dof_{i}_{j}_3d.png")
            plt.close()
"""

# Top-view grid with DOFs marked for orders 1 to 5
def plot_dofs_on_grid(order, grid_size=4, vertexgrid=True, edgegrid_x=True, edgegrid_y=True, facegrid=True):
    gridtype = "none"
    element_edges = np.linspace(0, 1, grid_size + 1)
    h = 1 / grid_size
    h_dof = 1 / (grid_size * order)
    local_dofs = np.linspace(0, 1, order + 1)
    global_dofs = []

    for i in range(grid_size):
        for j in range(grid_size):
            x0, y0 = element_edges[i], element_edges[j]
            for lx in local_dofs:
                for ly in local_dofs:
                    gx = x0 + h * lx
                    gy = y0 + h * ly
                    global_dofs.append((gx, gy))

    # Grid lines
    for i in range(grid_size + 1):
        x = i / grid_size
        plt.plot([x, x], [0, 1], 'k-', linewidth=0.5)
        plt.plot([0, 1], [x, x], 'k-', linewidth=0.5)

    # Plot all DOFs
    global_dofs = np.array(global_dofs)
    # Classify and plot DOFs by type (vertex, edge, face, interior)
    grid_points = np.linspace(0, 1, grid_size + 1)
    for gx, gy in global_dofs:
        # Count how many coordinates are on the boundary (0 or 1 of the grid)
        on_boundary = sum([
            np.isclose(gx, grid_points).any(),
            np.isclose(gy, grid_points).any()
        ])

        if on_boundary == 2 and vertexgrid:
            color = 'red'      # Vertex
            plt.plot(gx, gy, 'o', color=color, markersize=5)
        elif on_boundary == 1 and (np.isclose(gx % h, 0) or np.isclose(gx % h, 0.2)) and edgegrid_x:
            color = 'blue'   # Edge
            plt.plot(gx, gy, 'o', color=color, markersize=5)
        elif on_boundary == 1 and (np.isclose(gy % h, 0) or np.isclose(gy % h, 0.2)) and edgegrid_y:
            color = 'orange'   # Edge
            plt.plot(gx, gy, 'o', color=color, markersize=5)
        elif on_boundary == 0 and facegrid:
            color = 'green'    # Interior
            plt.plot(gx, gy, 'o', color=color, markersize=5)

    plt.axis("equal")
    plt.xticks([])
    plt.yticks([])
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"dofs_grid_order_{order}_{gridtype}.png")
    plt.close()

    plt.figure(figsize=(6, 6))

# Top-view grid with DOFs marked for orders 1 to 5 with MPI regions
def plot_dofs_on_grid_MPI(order, grid_size=4, vertexgrid=False, edgegrid_x=False, edgegrid_y=False, facegrid=False, MPI=True):
    gridtype = ""
    element_edges = np.linspace(0, 1, grid_size + 1)
    h = 1 / grid_size
    h_dof = 1 / (grid_size * order)
    local_dofs = np.linspace(0, 1, order + 1)
    global_dofs = []

    for i in range(grid_size):
        for j in range(grid_size):
            x0, y0 = element_edges[i], element_edges[j]
            for lx in local_dofs:
                for ly in local_dofs:
                    gx = x0 + h * lx
                    gy = y0 + h * ly
                    global_dofs.append((gx, gy))

    plt.figure(figsize=(6, 6))

    if MPI:
        if vertexgrid:
            x_start = - h / 4
            y_start = - h / 4
            side_length = h / 4 + 0.5 - h_dof / 2
            square = plt.Rectangle((x_start, y_start), side_length, side_length, color='blue', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length], [y_start, y_start], color='blue', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length], [y_start + side_length, y_start + side_length], color='blue', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length], color='blue', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length, x_start + side_length], [y_start, y_start + side_length], color='blue', alpha=1, linewidth=0.5, zorder=2)

            x_start = 0.5 + h_dof / 2
            y_start = - h / 4
            square = plt.Rectangle((x_start, y_start), side_length, side_length, color='red', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length], [y_start, y_start], color='red', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length], [y_start + side_length, y_start + side_length], color='red', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length], color='red', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length, x_start + side_length], [y_start, y_start + side_length], color='red', alpha=1, linewidth=0.5, zorder=2)

            x_start = - h / 4
            y_start = 0.5 + h_dof / 2
            square = plt.Rectangle((x_start, y_start), side_length, side_length, color='orange', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length], [y_start, y_start], color='orange', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length], [y_start + side_length, y_start + side_length], color='orange', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length], color='orange', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length, x_start + side_length], [y_start, y_start + side_length], color='orange', alpha=1, linewidth=0.5, zorder=2)

            x_start = 0.5 + h_dof / 2
            y_start = 0.5 + h_dof / 2
            square = plt.Rectangle((x_start, y_start), side_length, side_length, color='green', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length], [y_start, y_start], color='green', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length], [y_start + side_length, y_start + side_length], color='green', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length], color='green', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length, x_start + side_length], [y_start, y_start + side_length], color='green', alpha=1, linewidth=0.5, zorder=2)

        elif edgegrid_x:
            x_start = - h / 4
            y_start = - h / 4
            side_length_x = h / 4 + 0.5 - h_dof / 2
            side_length_y = h / 4 + 0.5 + h_dof / 4
            square = plt.Rectangle((x_start, y_start), side_length_x, side_length_y, color='blue', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length_x], [y_start, y_start], color='blue', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length_x], [y_start + side_length_y, y_start + side_length_y], color='blue', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length_y], color='blue', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length_x, x_start + side_length_x], [y_start, y_start + side_length_y], color='blue', alpha=1, linewidth=0.5, zorder=2)

            x_start = 0.5 + h_dof / 2
            y_start = - h / 4
            square = plt.Rectangle((x_start, y_start), side_length_x, side_length_y, color='red', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length_x], [y_start, y_start], color='red', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length_x], [y_start + side_length_y, y_start + side_length_y], color='red', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length_y], color='red', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length_x, x_start + side_length_x], [y_start, y_start + side_length_y], color='red', alpha=1, linewidth=0.5, zorder=2)

            x_start = - h / 4
            y_start = 0.5 + 3 * h_dof / 4
            side_length_y = h / 4 + 0.5 - 3 * h_dof / 4
            square = plt.Rectangle((x_start, y_start), side_length_x, side_length_y, color='orange', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length_x], [y_start, y_start], color='orange', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length_x], [y_start + side_length_y, y_start + side_length_y], color='orange', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length_y], color='orange', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length_x, x_start + side_length_x], [y_start, y_start + side_length_y], color='orange', alpha=1, linewidth=0.5, zorder=2)

            x_start = 0.5 + h_dof / 2
            y_start = 0.5 + 3 * h_dof / 4
            square = plt.Rectangle((x_start, y_start), side_length_x, side_length_y, color='green', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length_x], [y_start, y_start], color='green', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length_x], [y_start + side_length_y, y_start + side_length_y], color='green', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length_y], color='green', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length_x, x_start + side_length_x], [y_start, y_start + side_length_y], color='green', alpha=1, linewidth=0.5, zorder=2)

        elif edgegrid_y:
            x_start = - h / 4
            y_start = - h / 4
            side_length_x = h / 4 + 0.5 + h_dof / 4
            side_length_y = h / 4 + 0.5 - h_dof / 2
            square = plt.Rectangle((x_start, y_start), side_length_x, side_length_y, color='blue', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length_x], [y_start, y_start], color='blue', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length_x], [y_start + side_length_y, y_start + side_length_y], color='blue', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length_y], color='blue', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length_x, x_start + side_length_x], [y_start, y_start + side_length_y], color='blue', alpha=1, linewidth=0.5, zorder=2)

            x_start = - h / 4
            y_start = 0.5 + h_dof / 2
            square = plt.Rectangle((x_start, y_start), side_length_x, side_length_y, color='orange', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length_x], [y_start, y_start], color='orange', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length_x], [y_start + side_length_y, y_start + side_length_y], color='orange', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length_y], color='orange', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length_x, x_start + side_length_x], [y_start, y_start + side_length_y], color='orange', alpha=1, linewidth=0.5, zorder=2)

            x_start = 0.5 + 3 * h_dof / 4
            y_start = - h / 4
            side_length_x = h / 4 + 0.5 - 3 * h_dof / 4
            square = plt.Rectangle((x_start, y_start), side_length_x, side_length_y, color='red', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length_x], [y_start, y_start], color='red', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length_x], [y_start + side_length_y, y_start + side_length_y], color='red', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length_y], color='red', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length_x, x_start + side_length_x], [y_start, y_start + side_length_y], color='red', alpha=1, linewidth=0.5, zorder=2)

            x_start = 0.5 + 3 * h_dof / 4
            y_start = 0.5 + h_dof / 2
            square = plt.Rectangle((x_start, y_start), side_length_x, side_length_y, color='green', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length_x], [y_start, y_start], color='green', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length_x], [y_start + side_length_y, y_start + side_length_y], color='green', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length_y], color='green', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length_x, x_start + side_length_x], [y_start, y_start + side_length_y], color='green', alpha=1, linewidth=0.5, zorder=2)

        elif facegrid:
            x_start = - h / 4
            y_start = - h / 4
            side_length_x = h / 4 + 0.5 + h_dof / 4
            side_length_y = h / 4 + 0.5 + h_dof / 4
            square = plt.Rectangle((x_start, y_start), side_length_x, side_length_y, color='blue', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length_x], [y_start, y_start], color='blue', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length_x], [y_start + side_length_y, y_start + side_length_y], color='blue', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length_y], color='blue', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length_x, x_start + side_length_x], [y_start, y_start + side_length_y], color='blue', alpha=1, linewidth=0.5, zorder=2)

            x_start = - h / 4
            y_start =  0.5 + 3 * h_dof / 4
            side_length_y = h / 4 + 0.5 - 3 * h_dof / 4
            square = plt.Rectangle((x_start, y_start), side_length_x, side_length_y, color='orange', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length_x], [y_start, y_start], color='orange', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length_x], [y_start + side_length_y, y_start + side_length_y], color='orange', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length_y], color='orange', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length_x, x_start + side_length_x], [y_start, y_start + side_length_y], color='orange', alpha=1, linewidth=0.5, zorder=2)

            x_start = 0.5 + 3 * h_dof / 4
            y_start = - h / 4
            side_length_x = h / 4 + 0.5 - 3 * h_dof / 4
            side_length_y = h / 4 + 0.5 + h_dof / 4
            square = plt.Rectangle((x_start, y_start), side_length_x, side_length_y, color='red', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length_x], [y_start, y_start], color='red', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length_x], [y_start + side_length_y, y_start + side_length_y], color='red', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length_y], color='red', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length_x, x_start + side_length_x], [y_start, y_start + side_length_y], color='red', alpha=1, linewidth=0.5, zorder=2)

            x_start = 0.5 + 3 * h_dof / 4
            y_start = 0.5 + 3 * h_dof / 4
            side_length_y = h / 4 + 0.5 - 3 * h_dof / 4
            square = plt.Rectangle((x_start, y_start), side_length_x, side_length_y, color='green', alpha=0.2, zorder=1)
            plt.gca().add_patch(square)
            # Add border lines with alpha=1 and same color
            plt.plot([x_start, x_start + side_length_x], [y_start, y_start], color='green', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start + side_length_x], [y_start + side_length_y, y_start + side_length_y], color='green', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start, x_start], [y_start, y_start + side_length_y], color='green', alpha=1, linewidth=0.5, zorder=2)
            plt.plot([x_start + side_length_x, x_start + side_length_x], [y_start, y_start + side_length_y], color='green', alpha=1, linewidth=0.5, zorder=2)

    # Grid lines
    for i in range(grid_size + 1):
        x = i / grid_size
        plt.plot([x, x], [0, 1], 'k-', linewidth=0.5)
        plt.plot([0, 1], [x, x], 'k-', linewidth=0.5)

    # Plot vertex grid
    if (vertexgrid):
        gridtype = gridtype + "vertexgrid"
        for i in range(grid_size + 1):
            x = i / grid_size
            plt.plot([x, x], [0, 1], color='red', linestyle='-', linewidth=2)
            plt.plot([0, 1], [x, x], color='red', linestyle='-', linewidth=2)

    # Plot edge grid (x-direction)
    if (edgegrid_x):
        gridtype = gridtype + "edgegrid_x"
        x_start = 0
        x_end = 1

        y_start = h / 2
        y_end = 1 - h / 2

        for i in range(grid_size+1):
            x = x_start + i * h
            y = y_start + i * h
            plt.plot([x, x], [y_start, y_end], color='blue', linestyle='-', linewidth=2)
            if y < 1:
                plt.plot([x_start, x_end], [y, y], color='blue', linestyle='-', linewidth=2)

    # Plot edge grid (y-direction)
    if (edgegrid_y):
        gridtype = gridtype + "edgegrid_y"
        x_start = h / 2
        x_end = 1 - h / 2

        y_start = 0
        y_end = 1

        for i in range(grid_size+1):
            x = x_start + i * h
            y = y_start + i * h
            if x < 1:
                plt.plot([x, x], [y_start, y_end], color='orange', linestyle='-', linewidth=2)
            plt.plot([x_start, x_end], [y, y], color='orange', linestyle='-', linewidth=2)

    # Plot face grid
    if (facegrid):
        gridtype = gridtype + "facegrid"
        x_start = h / 2
        x_end = 1 - h / 2

        y_start = h / 2
        y_end = 1 - h / 2

        for i in range(grid_size):
            x = x_start + i * h
            y = y_start + i * h
            plt.plot([x, x], [y_start, y_end], color='green', linestyle='-', linewidth=2)
            plt.plot([x_start, x_end], [y, y], color='green', linestyle='-', linewidth=2)

    # Plot all DOFs
    global_dofs = np.array(global_dofs)
    # Classify and plot DOFs by type (vertex, edge, face, interior)
    grid_points = np.linspace(0, 1, grid_size + 1)
    for gx, gy in global_dofs:
        # Count how many coordinates are on the boundary (0 or 1 of the grid)
        on_boundary = sum([
            np.isclose(gx, grid_points).any(),
            np.isclose(gy, grid_points).any()
        ])
        if on_boundary == 2 and vertexgrid:
            color = 'red'      # Vertex
            plt.plot(gx, gy, 'o', color=color, markersize=5)
        elif on_boundary == 1 and (np.isclose(gx % h, 0) or np.isclose(gx % h, 0.2)) and edgegrid_x:
            color = 'blue'   # Edge
            plt.plot(gx, gy, 'o', color=color, markersize=5)
        elif on_boundary == 1 and (np.isclose(gy % h, 0) or np.isclose(gy % h, 0.2)) and edgegrid_y:
            color = 'orange'   # Edge
            plt.plot(gx, gy, 'o', color=color, markersize=5)
        elif on_boundary == 0 and facegrid:
            color = 'green'    # Interior
            plt.plot(gx, gy, 'o', color=color, markersize=5)

    plt.axis("equal")
    plt.xticks([])
    plt.yticks([])
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.tight_layout()
    plt.savefig(f"dofs_grid_order_{order}_{gridtype}_{MPI}.png")
    plt.close()

"""
for order in range(1, 6):
    plot_dofs_on_grid(order)
"""

plot_dofs_on_grid(1, grid_size=4)
plot_dofs_on_grid(2, grid_size=4)
plot_dofs_on_grid(3, grid_size=4, vertexgrid=True, edgegrid_x=False, edgegrid_y=False, facegrid=False)
plot_dofs_on_grid_MPI(1, grid_size=5)
plot_dofs_on_grid_MPI(2, grid_size=5)
plot_dofs_on_grid_MPI(2, facegrid=True, grid_size=5)
plot_dofs_on_grid_MPI(2, edgegrid_x=True, grid_size=5)
plot_dofs_on_grid_MPI(2, edgegrid_y=True, grid_size=5)
plot_dofs_on_grid_MPI(2, vertexgrid=True, grid_size=5)
plot_dofs_on_grid_MPI(1, grid_size=4, MPI=False)
plot_dofs_on_grid_MPI(2, grid_size=4, MPI=False)
plot_dofs_on_grid_MPI(2, facegrid=True, grid_size=4, MPI=False)
plot_dofs_on_grid_MPI(2, edgegrid_x=True, grid_size=4, MPI=False)
plot_dofs_on_grid_MPI(2, edgegrid_y=True, grid_size=4, MPI=False)
plot_dofs_on_grid_MPI(2, vertexgrid=True, grid_size=4, MPI=False)

"""
def plot_dofs_in_hexahedron(order):
    local_dofs = np.linspace(0, 1, order + 1)
    X, Y, Z = np.meshgrid(local_dofs, local_dofs, local_dofs, indexing='ij')

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Draw hexahedron edges without aliasing
    for x in [0, 1]:
        for y in [0, 1]:
            ax.plot([x, x], [y, y], [0, 1], color='gray', linewidth=1, antialiased=False)
    for x in [0, 1]:
        for z in [0, 1]:
            ax.plot([x, x], [0, 1], [z, z], color='gray', linewidth=1, antialiased=False)
    for y in [0, 1]:
        for z in [0, 1]:
            ax.plot([0, 1], [y, y], [z, z], color='gray', linewidth=1, antialiased=False)

    # Classify and plot DOFs
    for xi in range(order + 1):
        for yi in range(order + 1):
            for zi in range(order + 1):
                x, y, z = local_dofs[xi], local_dofs[yi], local_dofs[zi]
                # Count how many coordinates are on the boundary (0 or 1)
                on_boundary = sum([
                    np.isclose(x, 0) or np.isclose(x, 1),
                    np.isclose(y, 0) or np.isclose(y, 1),
                    np.isclose(z, 0) or np.isclose(z, 1)
                ])
                if on_boundary == 3:
                    color = 'red'      # Vertex
                    marker = 'o'
                elif on_boundary == 2:
                    color = 'orange'   # Edge
                    marker = 'o'
                elif on_boundary == 1:
                    color = 'green'    # Face
                    marker = 'o'
                else:
                    color = 'blue'     # Interior
                    marker = 'o'
                ax.scatter(x, y, z, color=color, s=40, marker=marker)

    # Remove axis labels, ticks, and grid
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_zlabel("")
    ax.grid(False)

    # Hide panes and axes spines
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.line.set_color((1, 1, 1, 0))
        axis.pane.set_edgecolor((1, 1, 1, 0))
        axis.pane.set_facecolor((1, 1, 1, 0))
        axis.pane.set_alpha(0)

    # Set transparent figure background
    ax.set_facecolor((1, 1, 1, 0))
    fig.patch.set_alpha(0)

    # Set limits and view
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)
    ax.view_init(elev=30, azim=-60)

    plt.tight_layout()
    plt.savefig(f"dofs_in_hexahedron_order_{order}.png", transparent=True, dpi=300)
    plt.close()

for order in range(1, 6):
    plot_dofs_in_hexahedron(order)
"""