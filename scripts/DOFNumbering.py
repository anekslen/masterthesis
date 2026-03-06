#!/usr/bin/env python3
"""
DOF Numbering Visualization for IPPL Finite Elements

This script creates plots showing the DOF numbering scheme used by IPPL's DOFHandler
for Lagrange elements in 1D, 2D, and 3D. The numbering follows the pattern:
- Vertices first (counter-clockwise)
- Edge DOFs (X, Y, Z directions)  
- Face DOFs (XY, XZ, YZ planes)
- Volume DOFs (interior)
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_1d_dof_numbering(order_max=4):
    """Plot 1D DOF numbering for different orders."""
    
    fig, axes = plt.subplots(1, order_max, figsize=(4*order_max, 3))
    if order_max == 1:
        axes = [axes]
    
    for order in range(1, order_max + 1):
        ax = axes[order - 1]
        
        # 1D element from 0 to 1
        x_line = np.linspace(0, 1, 100)
        y_line = np.zeros_like(x_line)
        
        # Plot the edge
        ax.plot(x_line, y_line, 'k-', linewidth=3, label='Edge')
        
        # DOF positions for 1D Lagrange elements
        dof_positions = []
        dof_labels = []
        dof_colors = []
        
        # Vertices (always at 0 and 1)
        dof_positions.extend([0.0, 1.0])
        dof_labels.extend(['0', '1'])
        dof_colors.extend(['red', 'red'])
        
        # Edge DOFs (interior points)
        if order > 1:
            for i in range(1, order):
                pos = i / order
                dof_positions.append(pos)
                dof_labels.append(str(1 + i))  # DOFs 2, 3, 4, ...
                dof_colors.append('blue')
        
        # Plot DOF points
        for i, (pos, label, color) in enumerate(zip(dof_positions, dof_labels, dof_colors)):
            ax.plot(pos, 0.0, 'o', color=color, markersize=12, markeredgecolor='black', linewidth=2)
            ax.text(pos, 0.1, label, ha='center', va='bottom', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9))
        
        ax.set_xlim(-0.1, 1.5)
        ax.set_ylim(-0.2, 0.3)
        ax.set_title(f'1D Order {order}\n({len(dof_positions)} DOFs)', fontsize=14)
        # Remove all spines and ticks
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        # Add x-axis arrow (extended)
        ax.annotate('', xy=(1.15, 0), xytext=(-0.05, 0),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        ax.text(1.18, 0, 'x', fontsize=12, ha='left', va='center')
        ax.set_aspect('equal')
    
    # Legend removed for cleaner appearance
    
    plt.tight_layout()
    plt.savefig('1D_dof_numbering.png', dpi=300, bbox_inches='tight')
    print("Saved: 1D_dof_numbering.png")
    plt.show()

def plot_2d_dof_numbering(order_max=4):
    """Plot 2D DOF numbering for different orders."""
    
    fig, axes = plt.subplots(1, order_max, figsize=(4*order_max, 4))
    if order_max == 1:
        axes = [axes]
    
    for order in range(1, order_max + 1):
        ax = axes[order - 1]
        
        # 2D element (unit square)
        square_x = [0, 1, 1, 0, 0]
        square_y = [0, 0, 1, 1, 0]
        ax.plot(square_x, square_y, 'k-', linewidth=3, label='Element boundary')
        
        # DOF positions and labels
        dof_positions = []
        dof_labels = []
        dof_colors = []
        
        dof_count = 0
        
        # Vertices (counter-clockwise: bottom-left, bottom-right, top-right, top-left)
        vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        for i, (x, y) in enumerate(vertices):
            dof_positions.append((x, y))
            dof_labels.append(str(dof_count))
            dof_colors.append('red')
            dof_count += 1
        
        if order > 1:
            # Edge DOFs - X-direction edges first, then Y-direction edges
            
            # X-direction edges (horizontal edges)
            # Bottom edge (y=0)
            for i in range(1, order):
                x = i / order
                dof_positions.append((x, 0.0))
                dof_labels.append(str(dof_count))
                dof_colors.append('blue')
                dof_count += 1
            
            # Top edge (y=1)
            for i in range(1, order):
                x = i / order
                dof_positions.append((x, 1.0))
                dof_labels.append(str(dof_count))
                dof_colors.append('blue')
                dof_count += 1
            
            # Y-direction edges (vertical edges)
            # Left edge (x=0)
            for i in range(1, order):
                y = i / order
                dof_positions.append((0.0, y))
                dof_labels.append(str(dof_count))
                dof_colors.append('blue')
                dof_count += 1
            
            # Right edge (x=1)
            for i in range(1, order):
                y = i / order
                dof_positions.append((1.0, y))
                dof_labels.append(str(dof_count))
                dof_colors.append('blue')
                dof_count += 1
            
            # Face DOFs (interior)
            if order >= 2:
                for j in range(1, order):
                    for i in range(1, order):
                        x = i / order
                        y = j / order
                        dof_positions.append((x, y))
                        dof_labels.append(str(dof_count))
                        dof_colors.append('green')
                        dof_count += 1
        
        # Plot DOF points
        for pos, label, color in zip(dof_positions, dof_labels, dof_colors):
            ax.plot(pos[0], pos[1], 'o', color=color, markersize=12, markeredgecolor='black', linewidth=2)
            # Position labels consistently to the top-right of each DOF
            offset_x = 0.1
            offset_y = 0.1
            ax.text(pos[0] + offset_x, pos[1] + offset_y, label, ha='center', va='center', 
                   fontsize=14, fontweight='bold', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        
        ax.set_xlim(-0.15, 1.25)
        ax.set_ylim(-0.15, 1.25)
        ax.set_title(f'2D Order {order}\n({len(dof_positions)} DOFs)', fontsize=14)
        # Remove all spines and ticks
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        # Add x-axis arrow (extended)
        ax.annotate('', xy=(1.2, 0), xytext=(-0.1, 0),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        ax.text(1.23, 0, 'x', fontsize=12, ha='left', va='center')
        # Add y-axis arrow
        ax.annotate('', xy=(0, 1.2), xytext=(0, -0.1),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        ax.text(0, 1.23, 'y', fontsize=12, ha='center', va='bottom')
        ax.set_aspect('equal')
    
    # Legend removed for cleaner appearance
    
    plt.tight_layout()
    plt.savefig('2D_dof_numbering.png', dpi=300, bbox_inches='tight')
    print("Saved: 2D_dof_numbering.png")
    plt.show()

def plot_2d_dof_clean(order_max=4):
    """Plot 2D DOF positions without numbers, all DOFs black, no arrows."""
    
    fig, axes = plt.subplots(4, 4, figsize=(16, 16))
    
    plot_idx = 0
    for order in range(1, order_max + 1):
        row = plot_idx // 4
        col = plot_idx % 4
        ax = axes[row, col]
        plot_idx += 1
        
        # 2D element (unit square)
        square_x = [0, 1, 1, 0, 0]
        square_y = [0, 0, 1, 1, 0]
        ax.plot(square_x, square_y, 'k-', linewidth=3, label='Element boundary')
        
        # DOF positions
        dof_positions = []
        
        dof_count = 0
        
        # Vertices (counter-clockwise: bottom-left, bottom-right, top-right, top-left)
        vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        for i, (x, y) in enumerate(vertices):
            dof_positions.append((x, y))
            dof_count += 1
        
        if order > 1:
            # Edge DOFs - X-direction edges first, then Y-direction edges
            
            # X-direction edges (horizontal edges)
            # Bottom edge (y=0)
            for i in range(1, order):
                x = i / order
                dof_positions.append((x, 0.0))
                dof_count += 1
            
            # Top edge (y=1)
            for i in range(1, order):
                x = i / order
                dof_positions.append((x, 1.0))
                dof_count += 1
            
            # Y-direction edges (vertical edges)
            # Left edge (x=0)
            for i in range(1, order):
                y = i / order
                dof_positions.append((0.0, y))
                dof_count += 1
            
            # Right edge (x=1)
            for i in range(1, order):
                y = i / order
                dof_positions.append((1.0, y))
                dof_count += 1
            
            # Face DOFs (interior)
            if order >= 2:
                for j in range(1, order):
                    for i in range(1, order):
                        x = i / order
                        y = j / order
                        dof_positions.append((x, y))
                        dof_count += 1
        
        # Plot DOF points (all black, no labels)
        for pos in dof_positions:
            ax.plot(pos[0], pos[1], 'o', color='black', markersize=12, markeredgecolor='black', linewidth=2)
        
        ax.set_xlim(-0.15, 1.15)
        ax.set_ylim(-0.15, 1.15)
        ax.set_title(f'2D Order {order}', fontsize=14)
        # Remove all spines and ticks
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        ax.set_aspect('equal')
    
    # Hide unused subplots
    for i in range(order_max, 16):
        row = i // 4
        col = i % 4
        axes[row, col].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('2D_dof_clean.png', dpi=300, bbox_inches='tight')
    print("Saved: 2D_dof_clean.png")

def plot_3d_dof_numbering(order_max=3):
    """Plot 3D DOF numbering for different orders."""
    
    fig = plt.figure(figsize=(6*order_max, 6))
    
    for order in range(1, order_max + 1):
        ax = fig.add_subplot(1, order_max, order, projection='3d')
        
        # 3D element (unit cube) - draw edges
        # Define vertices of cube
        vertices = [
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # bottom face
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]   # top face
        ]
        
        # Define edges of cube
        edges = [
            # Bottom face
            [0, 1], [1, 2], [2, 3], [3, 0],
            # Top face  
            [4, 5], [5, 6], [6, 7], [7, 4],
            # Vertical edges
            [0, 4], [1, 5], [2, 6], [3, 7]
        ]
        
        # Draw cube edges
        for edge in edges:
            points = np.array([vertices[edge[0]], vertices[edge[1]]])
            ax.plot3D(points[:, 0], points[:, 1], points[:, 2], color='gray', linewidth=1.5, alpha=0.6)
        
        # DOF positions and labels
        dof_positions = []
        dof_labels = []
        dof_colors = []
        
        dof_count = 0
        
        # Vertices (DOF 0 starts at (0,0,0), then counter-clockwise in XY at z=0, then z=1)
        vertex_positions = [
            (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),  # z=0 plane
            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)   # z=1 plane
        ]
        for pos in vertex_positions:
            dof_positions.append(pos)
            dof_labels.append(str(dof_count))
            dof_colors.append('red')
            dof_count += 1
        
        if order > 1:
            # Edge DOFs
            # X-edges (4 edges parallel to X)
            x_edges = [
                (0, 0, 0, 1, 0, 0),  # bottom-front
                (0, 1, 0, 1, 1, 0),  # bottom-back
                (0, 1, 1, 1, 1, 1),  # top-back
                (0, 0, 1, 1, 0, 1)   # top-front
            ]
            for x1, y1, z1, x2, y2, z2 in x_edges:
                for i in range(1, order):
                    t = i / order
                    x = x1 + t * (x2 - x1)
                    y = y1 + t * (y2 - y1)
                    z = z1 + t * (z2 - z1)
                    dof_positions.append((x, y, z))
                    dof_labels.append(str(dof_count))
                    dof_colors.append('blue')
                    dof_count += 1
            
            # Y-edges (4 edges parallel to Y)
            y_edges = [
                (0, 0, 0, 0, 1, 0),  # bottom-left
                (1, 0, 0, 1, 1, 0),  # bottom-right
                (1, 0, 1, 1, 1, 1),  # top-right
                (0, 0, 1, 0, 1, 1)   # top-left
            ]
            for x1, y1, z1, x2, y2, z2 in y_edges:
                for i in range(1, order):
                    t = i / order
                    x = x1 + t * (x2 - x1)
                    y = y1 + t * (y2 - y1)
                    z = z1 + t * (z2 - z1)
                    dof_positions.append((x, y, z))
                    dof_labels.append(str(dof_count))
                    dof_colors.append('blue')
                    dof_count += 1
            
            # Z-edges (4 edges parallel to Z)
            z_edges = [
                (0, 0, 0, 0, 0, 1),  # front-left
                (1, 0, 0, 1, 0, 1),  # front-right
                (1, 1, 0, 1, 1, 1),  # back-right
                (0, 1, 0, 0, 1, 1)   # back-left
            ]
            for x1, y1, z1, x2, y2, z2 in z_edges:
                for i in range(1, order):
                    t = i / order
                    x = x1 + t * (x2 - x1)
                    y = y1 + t * (y2 - y1)  
                    z = z1 + t * (z2 - z1)
                    dof_positions.append((x, y, z))
                    dof_labels.append(str(dof_count))
                    dof_colors.append('blue')
                    dof_count += 1
            
            # Face DOFs (if order >= 2)
            if order >= 2:
                # XY faces (z=0 and z=1)
                for z in [0, 1]:
                    for j in range(1, order):
                        for i in range(1, order):
                            x = i / order
                            y = j / order
                            dof_positions.append((x, y, z))
                            dof_labels.append(str(dof_count))
                            dof_colors.append('green')
                            dof_count += 1
                
                # XZ faces (y=0 and y=1) 
                for y in [0, 1]:
                    for k in range(1, order):
                        for i in range(1, order):
                            x = i / order
                            z = k / order
                            dof_positions.append((x, y, z))
                            dof_labels.append(str(dof_count))
                            dof_colors.append('green')
                            dof_count += 1
                
                # YZ faces (x=0 and x=1)
                for x in [0, 1]:
                    for k in range(1, order):
                        for j in range(1, order):
                            y = j / order
                            z = k / order
                            dof_positions.append((x, y, z))
                            dof_labels.append(str(dof_count))
                            dof_colors.append('green')
                            dof_count += 1
            
            # Volume DOFs (if order >= 2)
            if order >= 2:
                for k in range(1, order):
                    for j in range(1, order):
                        for i in range(1, order):
                            x = i / order
                            y = j / order
                            z = k / order
                            dof_positions.append((x, y, z))
                            dof_labels.append(str(dof_count))
                            dof_colors.append('orange')
                            dof_count += 1
        
        # Plot DOF points
        for pos, label, color in zip(dof_positions, dof_labels, dof_colors):
            ax.scatter(pos[0], pos[1], pos[2], c=color, s=120, edgecolors='black', linewidth=2)
            # Offset text position for better visibility
            offset_x = 0.05
            offset_y = 0.05
            offset_z = 0.08
            ax.text(pos[0] + offset_x, pos[1] + offset_y, pos[2] + offset_z, label, 
                   fontsize=14, ha='center', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9))
        
        ax.set_title(f'3D Order {order}\n({len(dof_positions)} DOFs)', fontsize=18)
        # Remove background, grid, ticks, and labels
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_zlabel('')
        # Remove background panes
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('none')
        ax.yaxis.pane.set_edgecolor('none')
        ax.zaxis.pane.set_edgecolor('none')
        # Remove all grid lines completely
        ax.xaxis._axinfo["grid"]['color'] = (1,1,1,0)
        ax.yaxis._axinfo["grid"]['color'] = (1,1,1,0)
        ax.zaxis._axinfo["grid"]['color'] = (1,1,1,0)
        # Add custom arrow axes (extended x-axis)
        ax.quiver(0, 0, 0, 1.5, 0, 0, color='black', arrow_length_ratio=0.1, linewidth=2)
        ax.quiver(0, 0, 0, 0, 1.3, 0, color='black', arrow_length_ratio=0.1, linewidth=2)
        ax.quiver(0, 0, 0, 0, 0, 1.3, color='black', arrow_length_ratio=0.1, linewidth=2)
        ax.text(1.6, 0, 0, 'x', fontsize=12)
        ax.text(0, 1.4, 0, 'y', fontsize=12)
        ax.text(0, 0, 1.4, 'z', fontsize=12)
        # View angle so (0,0,0) is at left front
        ax.view_init(elev=15, azim=-60)
    
    # Legend removed for cleaner appearance
    
    plt.tight_layout()
    plt.savefig('3D_dof_numbering.png', dpi=300, bbox_inches='tight')
    print("Saved: 3D_dof_numbering.png")
    plt.show()

def main():
    """Main function to create all DOF numbering plots."""
    print("Creating DOF numbering visualization plots...")
    
    # Create plots for different dimensions
    plot_1d_dof_numbering(order_max=4)
    plot_2d_dof_numbering(order_max=4) 
    plot_2d_dof_clean(order_max=4)  # Clean 2D plot without numbers
    plot_3d_dof_numbering(order_max=3)  # 3D gets complex at higher orders
    
    print("DOF numbering visualization complete!")

if __name__ == "__main__":
    main()