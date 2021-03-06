from torch.autograd import Variable
import torch
import torchvision
import matplotlib.pyplot as plt
import numpy as np
import torchvision.transforms as transforms
import utils
class Train():
    """Performs the training of ``model`` given a training dataset data
    loader, the optimizer, and the loss criterion.
    Keyword arguments:
    - model (``nn.Module``): the model instance to train.
    - data_loader (``Dataloader``): Provides single or multi-process
    iterators over the dataset.
    - optim (``Optimizer``): The optimization algorithm.
    - criterion (``Optimizer``): The loss criterion.
    - metric (```Metric``): An instance specifying the metric to return.
    - use_cuda (``bool``): If ``True``, the training is performed using
    CUDA operations (GPU).
    """

    def __init__(self, model, data_loader, optim, criterion, metric, use_cuda):
        self.model = model
        self.data_loader = data_loader
        self.optim = optim
        self.criterion = criterion
        self.metric = metric
        self.use_cuda = use_cuda

    def run_epoch(self, iteration_loss=False):
        """Runs an epoch of training.
        Keyword arguments:
        - iteration_loss (``bool``, optional): Prints loss at every step.
        Returns:
        - The epoch loss (float).
        """
        epoch_loss = 0.0
        self.metric.reset()
        self.model.train()
        for step, batch_data in enumerate(self.data_loader):
            inputs, labels = batch_data 
            # print(inputs.size())                       
            # inputs, labels = Variable(inputs), Variable(labels)
            # utils.imshow_batch(inputs, labels)

            if self.use_cuda:
                inputs = inputs.cuda()
                labels = labels.cuda()
            # Forward propagation
            outputs = self.model(inputs)
            # Loss computation
            loss = self.criterion(outputs, labels)
            # Backpropagation
            self.optim.zero_grad()
            loss.backward()
            self.optim.step()
            # Keep track of loss for current epoch
            epoch_loss += loss.item()
            # Keep track of the evaluation metric
            self.metric.add(outputs.data, labels.data)
            if iteration_loss:
                print("[Step: %d] Iteration loss: %.4f" % (step, loss.item()))

        return epoch_loss / len(self.data_loader), self.metric.value()
