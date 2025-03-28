import numpy as np

data = np.load('./data_demo.npz')

x_name = data['x_name']
x_semantic = data['x_semantic']
y = data['y']

keep = np.where(y != 1)[0]

x_name_filtered = x_name[keep]
x_semantic_filtered = x_semantic[keep]
y_filtered = y[keep]

np.savez_compressed('./data_demo_goodware.npz', x_name = x_name_filtered, x_semantic = x_semantic_filtered, y = y_filtered)
print("Done!")