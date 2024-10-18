#--------------------------------------------------------#
#   该文件用于处理权重文件，包括更改Key，删除key
#--------------------------------------------------------#
from collections import OrderedDict

import torch

# 选择你的权重文件路径
old_weight_file_path = './SwiftFormer_L3.pth'
new_weight_file_path = './new_weights.pth'
# 加载权重文件
state_dict = torch.load(old_weight_file_path)['model']

# 创建一个新的状态字典用于存放更改后的键值对
new_state_dict = OrderedDict()
# 遍历原始状态字典中的键值对
for key, value in state_dict.items():
    # # 如果键以'sdi_'开头，则将'sdi_'替换为'sdem_'
    # if key.startswith('Decoder.cgm_'):
    #     new_key = key.replace('cgm_', 'ssfm_')
    # elif key.startswith('sdi_'):
    #     new_key = key.replace('sdi_', 'sdem_')
    # else:
    #     new_key = key
    if key.startswith('head') or key.startswith('dist_head'):
        continue  # 跳过这些键值对，不将它们添加到新的状态字典中
    new_key = key
    # 将键值对添加到新的状态字典中
    new_state_dict[new_key] = value

# 选择你希望保存的文件路径
new_weight_file_path = 'new_weights.pth'

# 保存更改后的权重文件
torch.save(new_state_dict, new_weight_file_path)
