import os
import json
import numpy as np
import torch
import torch.nn.functional as F
from torch.nn import Embedding, Transformer, Linear, Conv2d, ZeroPad2d
import torch.utils.data as Data
import warnings
from flask import current_app

from api.model import Net
from .log import LogManager
 
warnings.filterwarnings("ignore")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('device', device)

base_dir = os.path.dirname(os.path.abspath(__file__))
word2id_path = os.path.join(base_dir, '..', 'src', 'word2id.npz')
word2behavior_path = os.path.join(base_dir, '..', 'src', 'word2behavior.npz')
behavior2id_path = os.path.join(base_dir, '..', 'src', 'behavior2id.npz')

word2id = np.load(word2id_path, allow_pickle=True)['word2id'].item()
word2behavior = np.load(word2behavior_path, allow_pickle=True)['word2behavior'].item()
behavior2id = np.load(behavior2id_path, allow_pickle=True)['behavior2id'].item()

def api_extraction(tracker_id):
    REPORT_FOLDER = current_app.config['REPORT_FOLDER']
    report_path = os.path.join(REPORT_FOLDER, f"{tracker_id}.json")
    report_list = []
    api_num = []
    n = 0

    if os.path.exists(report_path):
        with open(report_path, 'r') as load_f:
            try:
                report_dict = {}
                call_list = []
                load_dict = json.load(load_f)
                
                if 'behavior' not in load_dict:
                    print(tracker_id + "_notexist")
                    return
                
                if load_dict['strings'][0] == "This program must be run under Win32":
                    print(tracker_id + "_mustInWin32")
                    return
                
                report_dict['md5'] = load_dict['target']['file']['md5']
                
                for process in load_dict['behavior']['processes']:
                    if len(process['calls']) != 0:
                        for call in process['calls']:
                            if (len(call_list) == 0 or call_list[-1] != call['api']):
                                call_list.append(call['api'])
                                # Statistics API
                                if call['api'] not in api_num:
                                     api_num.append(call['api'])
                
                report_dict['call_list'] = call_list
                report_list.append(report_dict)
            
            except Exception as e:
                print(tracker_id + "_error", e)

    return api_num

def input_generate(tracker_id):
    data = api_extraction(tracker_id)

    additional_data = {
        "API calls" : data
    }
    with current_app.app_context():
        log_manager = LogManager(tracker_id)
        log_manager.update_log_stage("Model analyzing", additional_data)

    data_x_name = []
    data_x_semantic = []
    data_y = []
    md5 = []

    api_sequence = []
    semantic_sequence = []
    
    while len(data) < 1000:
        data.append("_PAD_")
    count = 0
    
    for api in data:
        if count == 1000:
            break
        api_id = word2id.get(api)
        api_sequence.append(api_id)

        behavior = word2behavior.get(api)
        semantic_ids = [behavior2id.get(b) for b in behavior]
        semantic_sequence.extend(semantic_ids)
        count += 1

    data_x_name.append(api_sequence)
    data_x_semantic.append(semantic_sequence)
    data_y.append(int(0))

    data_x_name = np.array(data_x_name)
    data_x_semantic = np.array(data_x_semantic)
    data_y = np.array(data_y).reshape(-1, 1)

    return data_x_name, data_x_semantic, data_y
    
def predict(loader):
    model.eval()
    with torch.no_grad():
        for step, (b_x, b_y) in enumerate(loader):
            b_x = b_x.to(device)
            pred = model(b_x)
            pred = torch.where(pred >= 0.5, torch.ones_like(pred), torch.zeros_like(pred))

        return pred.to('cpu').detach().numpy().tolist()[0]

model = Net().to(device)
model_path = os.path.join(base_dir, '..', 'src', 'model.pkl')
torch.save(model, model_path)

def get_result(tracker_id):
    input_x_name, input_x_semantic, input_y = input_generate(tracker_id)

    input_x = np.concatenate([input_x_name, input_x_semantic], axis=1)

    input_xt = torch.from_numpy(input_x)
    input_yt = torch.from_numpy(input_y.astype(np.float32))

    input_dataset = Data.TensorDataset(input_xt, input_yt)

    input_loader = Data.DataLoader(
        dataset=input_dataset,
        batch_size=1,
        num_workers=1,
    )

    if not hasattr(model, 'transformer'):
        model.transformer = Transformer(d_model=512, nhead=4, num_encoder_layers=2, num_decoder_layers=0, dim_feedforward=512, dropout=0.2)
        model.transformer = model.transformer.to(device)

    prediction = predict(input_loader)
    # print(prediction)
    return prediction