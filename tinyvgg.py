from torch import nn
from torch.nn import functional as F
import torch

class TinyVGG(nn.Module):
    def __init__(self, input_channels: int, out_channels: int, hidden: int, kernel_size: int):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(input_channels, hidden, kernel_size),
            nn.ReLU(),
            nn.Conv2d(hidden, hidden, kernel_size),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(hidden, hidden, kernel_size),
            nn.ReLU(),
            nn.Conv2d(hidden, hidden, kernel_size),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten()
        )
        self.linear = nn.Linear(160, out_channels)
    
    def forward(self, X: torch.Tensor, target: torch.Tensor | None = None):
        out = self.conv(X)
        logits = self.linear(out)
        if target is None:
            loss = None
        else:
            loss = F.cross_entropy(logits, target)
        return logits, loss
    
    def predict(self, X: torch.Tensor, probs: bool = False) -> list[int] | list[list[float]]:
        if X.dim() == 3:
            X = X.unsqueeze(dim=0)
        assert X.dim() == 4
        logits, loss =self(X)
        preds = F.softmax(logits, dim=1)
        return preds.tolist() if probs else preds.argmax(dim=1).tolist()
        