import os
import json
import numpy as np

paths = ['./goodware_samples/cuckoo_report',
         './malware_samples/cuckoo_report']

dontrun = []
def api_extraction():    
    paths = ['/home/ubuntu/.cuckoo/storage/analyses']

    report_list = []
    api_num = []
    n = 0
    # with open('output.txt', 'w') as f:
    #     with contextlib.redirect_stdout(f):
    for path in paths:
        file_list = os.listdir(path)
        for file_num in file_list:
            if not(file_num == 'latest') and not(file_num in dontrun) and ((int(file_num) > 6000) and (int(file_num) < 7001)):
                print("{} / 1000".format(n))
                n = n + 1
                if os.path.exists(path + "/" + file_num + "/reports/report.json"):
                    with open(path + "/" + file_num + "/reports/report.json", 'r') as load_f:
                        try:
                            report_dict = {}
                            call_list = []
                            load_dict = json.load(load_f)
                            if 'behavior' not in load_dict:
                                print(file_num + "_notexist")
                                continue
                            if load_dict['strings'][0] == "This program must be run under Win32":
                                print(file_num + "_mustInWin32")
                                continue
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
                        except:
                            print(file_num + "_error")

        np.savez("ransomware_api_7000", report_list=report_list)
        print(len(report_list))
api_extraction()
