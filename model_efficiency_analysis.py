
# --------------------------------------------------------#
#   该文件用于模型的计算效率分析
# --------------------------------------------------------#
import torch
from fvcore.nn import FlopCountAnalysis, ActivationCountAnalysis, flop_count_table


from torchsummary import summary

# from 1.ACCoNet.ACCoNet_Res_models import ACCoNet_Res
# from 1.ACCoNet.ACCoNet_VGG_models import ACCoNet_VGG
# from 1.CorrNet.CorrNet_models import CorrelationModel_VGG
# from 1.EMFINet.EMFINet import EMFINet
# from 1.ERPNet.ERPNet import ERPNet
# from 1.ERPNet.ERPNet_VGG import ERPNet_VGG
# from 1.GSANet.MyNet import MyNet
# from 1.GeleNet.GeleNet_models import GeleNet
# from 1.MCCNet.MCCNet_models import MCCNet_VGG

device = 'cuda'

model = MyNet().to(device)  # 加载需要的模型
model.eval()
inputs = torch.randn(1, 3, 256, 256).to(device)
# out1, out2, out3, out4 = CorrNet(inputs)
# print(out1.shape)
# print(out2.shape)
# print(out3.shape)
# print(out4.shape)
print('模型性能测试')
flops = FlopCountAnalysis(model, inputs)
param = sum(p.numel() for p in model.parameters() if p.requires_grad)
acts = ActivationCountAnalysis(model, inputs)

print(f"total flops : {flops.total()}")
print(f"total activations: {acts.total()}")
print(f"number of parameter: {param}")
print(flop_count_table(flops, max_depth=1))


