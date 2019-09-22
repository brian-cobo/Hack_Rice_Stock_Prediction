# -*- coding: utf-8 -*-

import torch
from torch import nn
import torch.nn.functional as F
from collections import OrderedDict
# from torchvision import datasets, transforms, models
from torch import optim
import matplotlib.pyplot as plt

dropout = 0.5;
epochs = 5;
print_every = 10;
input_size = 256;
output_size = 3 # -1, 0 , 1
hidden_layers = [128,64]


def validation(model, device, testloader, criterion):
    model.eval()
    model.to(device)
    with torch.no_grad():
        accuracy = 0
        test_loss = 0
        for images, labels in testloader:
            images, labels = images.to(device), labels.to(device)
            output = model.forward(images)
            test_loss += criterion(output, labels).item()
            ps = torch.exp(output)
            equality = (labels.data == ps.max(1)[1])
            accuracy += equality.type_as(torch.FloatTensor()).mean()
    print("Test Accuracy: {}".format(accuracy/len(testloader))) 
    return test_loss, accuracy 


def train(model, trainloader, testloader, criterion, optimizer, epochs,print_every):
    train_losses = []
    test_losses = []
    model.to(device)
    steps = 0
    running_loss = 0
    for epoch in range(epochs):
        for data, labels in trainloader:
            data, labels = data.to(device), labels.to(device)
            optimizer.zero_grad()
            output = model.forward(data)
            loss = criterion(output,labels)
            loss.backward()
            optimizer.step()
            running_loss +=loss.item()
            
            if steps % print_every ==0:
                model.eval()
                
                with torch.no_grad():
                    test_loss, accuracy = validation(model,testloader,criterion)
                train_losses.append(running_loss/len(trainloader))
                test_losses.append(test_loss/len(testloader)) 
                print(f"Epoch {epoch+1}/{epochs}.. "
                      f"Train loss: {running_loss/print_every:.3f}.. "
                      f"Test loss: {test_loss/len(testloader):.3f}.. "
                      f"Test accuracy: {accuracy/len(testloader):.3f}")
                running_loss = 0
                model.train()
    plt.plot(train_losses, label='Training loss')
    plt.plot(test_losses, label='Testing loss')
    plt.legend(frameon=False)


class model(nn.Module):
    def __init__(self, input_size, output_size, hidden_layers, dropout):
        super().__init__()
        self.hidden_layer1 = nn.Linear(input_size, hidden_layers[0])
        self.hidden_layer2 = nn.Linear(hidden_layers[0], hidden_layers[1])
        self.output = nn.Linear(hidden_layers[1], output_size)
        self.dropout = nn.Dropout(p=dropout)
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax(dim =1)
    def forward(self,x):
        x = self.hidden_layer1(x)
        x = F.relu(x)
        x = self.hidden_layer2(x)
        x = F.relu(x)
        x = self.dropout(x)
        x = self.output(x)
        x = self.softmax(x)
        return x

        
def save_checkpoint(model, training_dataset,optimizer):
    #checkpoint for cat/dog
    #notepoint for drum
    model.class_to_idx = training_dataset.class_to_idx
    checkpoint = {'input_size': 256,
                  'output_size': 3,
                  'hidden_layer_units': 128,
                  'batch_size': 64,
                  'learning_rate': 0.001,
                  'model_name': 'model',
                  'model_state_dict': model.state_dict(),
                  'optimizer' : optimizer.state_dict(),
                  'epochs': 5,
                  'class_to_idx': model.class_to_idx}

    torch.save(checkpoint, 'checkpoint.pth') 
# this is the data part... not really sure what to do
#train_transforms, test_transforms = trial.trial_transforms()
#train_dataset, test_dataset = trial.trial_datasets(data_dir, train_transforms, test_transforms)
#trainloader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)
#testloader = torch.utils.data.DataLoader(test_dataset, batch_size=64)

model = model(input_size, output_size, hidden_layers, dropout)
for param in model.parameters():
    param.requires_grad = False
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr= 0.001)
model.to(device)
train(model,device, trainloader, testloader, criterion, optimizer,epochs,print_every)
validation(model,device, testloader, criterion)
save_checkpoint_dense(model,train_dataset,optimizer)


