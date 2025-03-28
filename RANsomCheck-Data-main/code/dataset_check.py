import numpy as np

file_names = [
    './data_demo_goodware.npz',
    './ransomware_dataset.npz',
    './ransomware_dataset_1000.npz',
    './ransomware_dataset_2000.npz',
    './ransomware_dataset_3000.npz',
    './ransomware_dataset_4000.npz',
    './ransomware_dataset_5000.npz',
    './ransomware_dataset_6000.npz',
    './ransomware_dataset_7000.npz'
]

total_samples = 0
total_ransomware = 0
total_goodware = 0

for file_name in file_names:
    data = np.load(file_name, allow_pickle=True)
    y = data['y']

    num_samples = len(y)
    total_samples += num_samples

    num_ransomware = np.sum(y == 1)
    num_goodware = np.sum(y == 0)

    total_ransomware += num_ransomware
    total_goodware += num_goodware

    if_all_zeros = np.all(y == 0)
    if_all_ones = np.all(y == 1)


    if if_all_zeros:
        print(f"{file_name}: All are goodware!")
    elif if_all_ones:
        print(f"{file_name}: All are ransomware!")
    else:
        print(f"{file_name}: Mix of goodware and ransomware!")

    num_samples = len(y)
    print(f"Sample count: {num_samples}")
    print("--------------------------")

print("Total sample count:", total_samples)
print("Total ransomware count:", total_ransomware)
print("Total goodware count:", total_goodware)