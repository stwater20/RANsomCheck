import numpy as np
import torch
import torch.nn.functional as F
from torch.nn import Embedding, Transformer, Linear, Conv2d, ZeroPad2d
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score, accuracy_score
import torch.utils.data as Data
import wandb

import warnings
warnings.filterwarnings("ignore")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('device', device)

class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.embedder1 = Embedding(num_embeddings=316, embedding_dim=16)
        self.embedder2 = Embedding(num_embeddings=289, embedding_dim=8)

        self.cnn1_1 = Conv2d(in_channels=1, out_channels=128, kernel_size=(3, 16), stride=1, padding=(1, 0))
        self.cnn1_2 = Conv2d(in_channels=1, out_channels=128, kernel_size=(4, 16), stride=1)
        self.cnn1_3 = Conv2d(in_channels=1, out_channels=128, kernel_size=(5, 16), stride=1, padding=(2, 0))

        self.cnn2 = Conv2d(in_channels=1, out_channels=128, kernel_size=(4, 8), stride=4)

        self.transformer = Transformer(d_model=512, nhead=4, num_encoder_layers=2, num_decoder_layers=0, dim_feedforward=512, dropout=0.2)

        self.lin1 = Linear(512, 64)
        self.lin2 = Linear(64, 32)
        self.lin3 = Linear(32, 1)

    def forward(self, data):
        x_name, x_behavior = data.split([1000, 4000], 1) 

        x_name = self.embedder1(x_name)
        x_behavior = self.embedder2(x_behavior)

        x_name = x_name.unsqueeze(1)
        x_behavior = x_behavior.unsqueeze(1)

        pad = ZeroPad2d(padding=(0, 0, 2, 1))
        x_name_pad = pad(x_name)

        x_name_cnn1 = F.relu(self.cnn1_1(x_name)).squeeze(-1).permute(0, 2, 1)
        x_name_cnn2 = F.relu(self.cnn1_2(x_name_pad)).squeeze(-1).permute(0, 2, 1)
        x_name_cnn3 = F.relu(self.cnn1_3(x_name)).squeeze(-1).permute(0, 2, 1)

        x_behavior = F.relu(self.cnn2(x_behavior)).squeeze(-1).permute(0, 2, 1)

        x = torch.cat([x_name_cnn1, x_name_cnn2, x_name_cnn3, x_behavior], dim=-1)

        x = self.transformer.encoder(x)

        x, max_index = torch.max(x, dim=1)
        
        x = F.relu(self.lin1(x))
        x = F.dropout(x, p=0.2, training=self.training)
        x = F.relu(self.lin2(x))
        x = F.dropout(x, p=0.2, training=self.training)
        x = F.sigmoid(self.lin3(x))

        return x
    
def train(epoch, loader):
    model.train()
    loss_all = 0
    for step, (b_x, b_y) in enumerate(loader):
        b_x = b_x.to(device)
        b_y = b_y.to(device)
        optimizer.zero_grad()
        output = model(b_x)
        loss = F.binary_cross_entropy(output, b_y)
        loss.backward()
        loss_all += b_x.size(0) * loss.item()
        optimizer.step()

        wandb.log({"Step Loss": loss.item()})
    return loss_all / len(loader.dataset)

def test(loader):
    model.eval()
    label_list = []
    pred_list = []
    with torch.no_grad():
        for step, (b_x, b_y) in enumerate(loader):
            b_x = b_x.to(device)
            pred = model(b_x)
            pred = torch.where(pred >= 0.5, torch.ones_like(pred), torch.zeros_like(pred))

            label_list.extend(b_y.to('cpu').detach().numpy().tolist())
            pred_list.extend(pred.to('cpu').detach().numpy().tolist())

    y_true = np.asarray(label_list)
    y_pred = np.asarray(pred_list)
    _val_confusion_matrix = confusion_matrix(y_true, y_pred)
    _val_acc = accuracy_score(y_true, y_pred)
    _val_precision = precision_score(y_true, y_pred)
    _val_recall = recall_score(y_true, y_pred)
    _val_f1 = f1_score(y_true, y_pred)

    return _val_confusion_matrix, _val_acc, _val_precision, _val_recall, _val_f1

wandb.init(project="model_Transformer", config={
    "learning_rate": 0.0001,
    "architecture": "Net",
    "dataset": "Custom",
    "epochs": 50,
})

# Load datasets
train_data = np.load('../../dataset/final_dataset_train_1.npz', allow_pickle=True)
val_data = np.load('../../dataset/final_dataset_val_1.npz', allow_pickle=True)
test_data = np.load('../../dataset/final_dataset_test_1.npz', allow_pickle=True)

train_x_name = train_data['x_name']
train_x_semantic = train_data['x_semantic']
train_y = train_data['y']

val_x_name = val_data['x_name']
val_x_semantic = val_data['x_semantic']
val_y = val_data['y']

test_x_name = test_data['x_name']
test_x_semantic = test_data['x_semantic']
test_y = test_data['y']

# Combine features
train_x = np.concatenate([train_x_name, train_x_semantic], axis=1)
val_x = np.concatenate([val_x_name, val_x_semantic], axis=1)
test_x = np.concatenate([test_x_name, test_x_semantic], axis=1)

# Convert to PyTorch tensors
train_xt = torch.from_numpy(train_x)
val_xt = torch.from_numpy(val_x)
test_xt = torch.from_numpy(test_x)
train_yt = torch.from_numpy(train_y.astype(np.float32))
val_yt = torch.from_numpy(val_y.astype(np.float32))
test_yt = torch.from_numpy(test_y.astype(np.float32))

# Create DataLoaders
train_dataset = Data.TensorDataset(train_xt, train_yt)
val_dataset = Data.TensorDataset(val_xt, val_yt)
test_dataset = Data.TensorDataset(test_xt, test_yt)

train_loader = Data.DataLoader(
    dataset=train_dataset,
    batch_size=64,
    shuffle=True,
    num_workers=1,
)

val_loader = Data.DataLoader(
    dataset=val_dataset,
    batch_size=64,
    num_workers=1,
)

test_loader = Data.DataLoader(
    dataset=test_dataset,
    batch_size=64,
    num_workers=1,
)

model = Net().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=wandb.config.learning_rate)

for epoch in range(1, wandb.config.epochs + 1):
    loss = train(epoch, train_loader)
    con, acc, precision, recall, f1 = test(val_loader)
    print(f'Epoch: {epoch:03d}, Loss: {loss:.5f}, Train Acc: {acc:.5f}, Train Precision: {precision:.5f}, Train Recall: {recall:.5f}, Train F1: {f1:.5f}')
    wandb.log({"Epoch": epoch, "Loss": loss, "Train Accuracy": acc, "Train Precision": precision, "Train Recall": recall, "Train F1": f1})

con, acc, precision, recall, f1 = test(test_loader)
print("==================================")
print('Test result:')
print('Accuracy:', acc)
print('Precision:', precision)
print('Recall:', recall)
print('F1 Score:', f1)
print(con)

torch.save(model, './model_wandb_1007.pkl')
wandb.finish()