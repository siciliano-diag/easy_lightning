import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import numpy as np

#https://github.com/AlanChou/Truncated-Loss
class GCELoss(nn.Module):

    def __init__(self, q=0.7, k=0.5, trainset_size=50000):
        super(GCELoss, self).__init__()
        self.q = q
        self.k = k
        self.weight = torch.nn.Parameter(data=torch.ones(trainset_size, 1), requires_grad=False)
             
    def forward(self, logits, targets, indexes):
        p = F.softmax(logits, dim=1)
        Yg = torch.gather(p, 1, torch.unsqueeze(targets, 1))

        loss = ((1-(Yg**self.q))/self.q)*self.weight[indexes] - ((1-(self.k**self.q))/self.q)*self.weight[indexes]
        loss = torch.mean(loss)

        return loss

    def update_weight(self, logits, targets, indexes):
        p = F.softmax(logits, dim=1)
        Yg = torch.gather(p, 1, torch.unsqueeze(targets, 1))
        Lq = ((1-(Yg**self.q))/self.q)
        Lqk = ((1-(self.k**self.q))/self.q) * torch.ones_like(targets, dtype=torch.float)
        Lqk = torch.unsqueeze(Lqk, 1)
    
        condition = torch.gt(Lqk, Lq)
        self.weight[indexes] = condition.float().to(logits.device)

        
