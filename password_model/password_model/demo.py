
import torch
import string

from base_func.base_func import *
from model import PasswordModel
def char_to_index(character, alphabet):
    return alphabet.find(character)


def one_hot_encode(seq, alphabet, max_length=30):
    X = torch.zeros(len(alphabet), max_length)
    for index_char, char in enumerate(seq[::-1]):
        if char_to_index(char, alphabet) != -1:
            X[char_to_index(char, alphabet)][index_char] = 1.0
    return X


def predict(text, model, max_length, alphabet, cuda=False):
    assert isinstance(text, str)
    with torch.no_grad():
        model.eval()
        x = one_hot_encode(text, alphabet, max_length)
        x = torch.unsqueeze(x, 0)
        if cuda:
            x = x.cuda()
        output = model(x)
        # print(torch.exp(output))
        _, predicted = torch.max(output, 1)
        return predicted, torch.exp(output)


def predict_finetuned(text, model, max_length, alphabet, cuda=False):
    assert isinstance(text, str)
    with torch.no_grad():
        model.eval()
        x = one_hot_encode(text, alphabet, max_length)
        x = torch.unsqueeze(x, 0)
        if cuda:
            x = x.cuda()
        output = model(x)
        prob = torch.exp(output)[0]
        if prob[0] > 0.2:
            pred = 0
        else:
            if prob[1] > prob[2]:
                pred = 1
            else:
                pred = 2
        return pred, prob


    
    


    return filtered
if __name__ == '__main__':
    alphabet = string.ascii_letters + string.digits + string.punctuation
    model = PasswordModel(len(alphabet))
    max_length = 30
    checkpoint = torch.load("./password_model/password/model_best.pth.tar",map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['state_dict'])
    model.eval()
    password="quest"
    predicted, exp=predict(password[:30],model, max_length, alphabet, cuda=False)
    print(predicted.item())

#随机字符：0 人工密钥：1  机械密钥：2