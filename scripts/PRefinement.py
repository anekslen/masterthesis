import matplotlib.pyplot as plt
import numpy as np

# Data: (spacing, relative_error) for each order
data = {
    1: {
        'h': [0.6666666666666666, 0.2857142857142857, 0.1333333333333333,
              0.06451612903225806, 0.03174603174603174, 0.01574803149606299,
              0.007843137254901961, 0.003913894324853229, 0.001955034213098729],
        'err': [0.1147550621098495, 0.02107746038752363, 0.004590202484393618,
                0.001074709218514286, 0.0002602155603341969, 6.403345273038428e-05,
                1.588305359108783e-05, 3.955237496784459e-06, 9.868771879682533e-07],
    },
    2: {
        'h': [0.6666666666666666, 0.2857142857142857, 0.1333333333333333,
              0.06451612903225806, 0.03174603174603174, 0.01574803149606299,
              0.007843137254901961, 0.003913894324853229, 0.001955034213098729],
        'err': [9.771342284700076e-16, 1.905006379484008e-15, 4.566161067402813e-15,
                8.522359043772003e-14, 3.399824421403875e-13, 3.827108086471977e-12,
                4.523947781078101e-12, 4.549130329298167e-11, 1.220695310531624e-10],
    },
    3: {
        'h': [0.6666666666666666, 0.2857142857142857, 0.1333333333333333,
              0.06451612903225806, 0.03174603174603174, 0.01574803149606299,
              0.007843137254901961, 0.003913894324853229, 0.001955034213098729],
        'err': [3.189568735509884e-16, 1.525558747702637e-14, 2.978985652512653e-14,
                2.493295939953471e-13, 1.173340511698068e-12, 3.707775436592123e-12,
                9.363789114196559e-12, 6.070264882830908e-11, 5.839048163734056e-10],
    },
    4: {
        'h': [0.6666666666666666, 0.2857142857142857, 0.1333333333333333,
              0.06451612903225806, 0.03174603174603174, 0.01574803149606299,
              0.007843137254901961, 0.003913894324853229, 0.001955034213098729],
        'err': [2.318749780602338e-15, 1.332019469340634e-14, 5.571442931015194e-14,
                4.941607204472456e-13, 4.428804466881976e-12, 1.450716122365883e-12,
                1.998419803857779e-11, 1.315671412747996e-10, 0.07695216809721352],
    },
}

fig, ax = plt.subplots(figsize=(8, 6))

colors = {1: 'tab:blue', 2: 'tab:orange', 3: 'tab:green', 4: 'tab:red'}
markers = {1: 'o', 2: 's', 3: '^', 4: 'D'}

for order, d in data.items():
    h = np.array(d['h'])
    err = np.array(d['err'])

    if order == 1:
        label = f'Order {order}'
    else:
        # Orders 2-4 hit machine precision, skip last point for order 4 (diverged)
        if order == 4:
            h = h[:-1]
            err = err[:-1]
        label = f'Order {order}'

    ax.loglog(h, err, marker=markers[order], color=colors[order],
              linewidth=1.5, markersize=6, label=label)

# Add reference slope for O(h^2)
h_ref = np.array([0.001, 1.0])
ax.loglog(h_ref, 0.3 * h_ref**2, 'k-', alpha=0.6, linewidth=2.5, label=r'$O(h^2)$')

# Add machine precision line
h_range = ax.get_xlim()
ax.axhline(y=np.finfo(float).eps, color='gray', linestyle=':', linewidth=1, label='Machine precision')

ax.set_xlabel('Mesh spacing $h$', fontsize=12)
ax.set_ylabel('Relative error', fontsize=12)
ax.legend(fontsize=10, bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

# Only show gridlines at 10^-2 and 10^-1 on x-axis
from matplotlib.ticker import FixedLocator
ax.xaxis.set_major_locator(FixedLocator([1e-2, 1e-1]))
ax.xaxis.set_minor_locator(FixedLocator([]))
ax.grid(True, which='major', alpha=0.3)

plt.tight_layout()
plt.savefig('/home/annah/masterproject/p_refinement_plot.png', dpi=150, bbox_inches='tight')
plt.savefig('/home/annah/masterproject/p_refinement_plot.pdf', bbox_inches='tight')
print("Saved p_refinement_plot.png and p_refinement_plot.pdf")
plt.show()
