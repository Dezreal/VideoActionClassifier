from torch import nn


class TCN(nn.Module):

    def __init__(self, out_channels, kernel_size, stride, padding, dropout):
        super(TCN, self).__init__()
        self.seq = nn.Sequential(
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(
                out_channels,
                out_channels,
                (kernel_size[0], 1),
                (stride, 1),
                padding,
            ),
            nn.BatchNorm2d(out_channels),
            nn.Dropout(dropout, inplace=True),
        )

    def forward(self, x):
        return self.seq(x)
