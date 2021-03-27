import torch.nn as nn
from model.component.depthwise_separable_conv2d import DepthwiseSeparableConv2d

class DownsamplerEncoder(nn.Module):
    def __init__(self, dim_in, dim_out):
        super(DownsamplerEncoder, self).__init__()

        self.downsampler1 = nn.Sequential(            
            DepthwiseSeparableConv2d(dim_in, dim_out, kernel_size = 4, stride = 2, padding = 1, bias = False),
            nn.ReLU(),
            DepthwiseSeparableConv2d(dim_in, dim_out, kernel_size = 4, stride = 2, padding = 1, bias = False),
            nn.ReLU()
        )
        self.downsampler2 = nn.Sequential(
            DepthwiseSeparableConv2d(dim_in, dim_out, kernel_size = 8, stride = 4, padding = 2, bias = False),
            nn.ReLU()
        )

        self.bn = nn.BatchNorm2d(dim_out)

    def forward(self, x):        
        x1      = self.downsampler1(x)
        x2      = self.downsampler2(x)

        xout    = self.bn(x1 + x2)
        return xout