import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey

# Example data
categories = ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
flows = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1]

# Create a Sankey diagram
sankey = Sankey()
sankey.add(flows=flows, labels=categories)
sankey.finish()

plt.show()