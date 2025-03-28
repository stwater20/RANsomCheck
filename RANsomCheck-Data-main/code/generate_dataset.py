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

# merge the dataset
merged_data = {}

for file_name in file_names:
    dataset = np.load(file_name, allow_pickle=True)
    
    for key in dataset.keys():
        if key not in merged_data:
            merged_data[key] = []
        
        merged_data[key].append(dataset[key])

for key in merged_data.keys():
    merged_data[key] = np.concatenate(merged_data[key])

# random the dataset
indices = np.arange(len(merged_data['x_name']))
np.random.shuffle(indices)

for key in merged_data.keys():
    merged_data[key] = merged_data[key][indices]
    # print(merged_data[key])

# split the dataset
dataset_train = {}
dataset_val = {}
dataset_test = {}
dataset_length = len(merged_data['x_name'])
dataset_train_length = int(0.6 * dataset_length)
dataset_val_length = int(0.2 * dataset_length)
dataset_test_length = dataset_length - dataset_train_length - dataset_val_length

for key in merged_data.keys():
    dataset_train[key] = merged_data[key][:dataset_train_length]
    dataset_val[key] = merged_data[key][dataset_train_length:dataset_train_length + dataset_val_length]
    dataset_test[key] = merged_data[key][dataset_train_length + dataset_val_length:]

np.savez('./final_dataset_train_1.npz', x_name=dataset_train['x_name'], x_semantic=dataset_train['x_semantic'], y=dataset_train['y'])
np.savez('./final_dataset_val_1.npz', x_name=dataset_val['x_name'], x_semantic=dataset_val['x_semantic'], y=dataset_val['y'])
np.savez('./final_dataset_test_1.npz', x_name=dataset_test['x_name'], x_semantic=dataset_test['x_semantic'], y=dataset_test['y'])

# count
train_goodware_count = np.sum(dataset_train['y'] == 0)
train_ransomware_count = np.sum(dataset_train['y'] == 1)
val_goodware_count = np.sum(dataset_val['y'] == 0)
val_ransomware_count = np.sum(dataset_val['y'] == 1)
test_goodware_count = np.sum(dataset_test['y'] == 0)
test_ransomware_count = np.sum(dataset_test['y'] == 1)

total_goodware_count = train_goodware_count + val_goodware_count + test_goodware_count
total_ransomware_count = train_ransomware_count + val_ransomware_count + test_ransomware_count

print("Training dataset class counts:")
print(f"Goodware: {train_goodware_count}")
print(f"Ransomware: {train_ransomware_count}")

print("\nValidation dataset class counts:")
print(f"Goodware: {val_goodware_count}")
print(f"Ransomware: {val_ransomware_count}")

print("\nTesting dataset class counts:")
print(f"Goodware: {test_goodware_count}")
print(f"Ransomware: {test_ransomware_count}")

print("\nTotal class counts:")
print(f"Goodware: {total_goodware_count}")
print(f"Ransomware: {total_ransomware_count}")