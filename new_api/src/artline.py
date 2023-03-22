from PIL import Image
import requests
import numpy as np
import urllib.request
from urllib.request import urlretrieve
import PIL.Image
import torchvision.transforms as T
import fastai
from fastai.vision import *
from fastai.utils.mem import *
from PIL import Image
import numpy as np
from io import BytesIO

class FeatureLoss(nn.Module):
    def __init__(self, m_feat, layer_ids, layer_wgts):
        super().__init__()
        self.m_feat = m_feat
        self.loss_features = [self.m_feat[i] for i in layer_ids]
        self.hooks = hook_outputs(self.loss_features, detach=False)
        self.wgts = layer_wgts
        self.metric_names = ['pixel',] + [f'feat_{i}' for i in range(len(layer_ids))
              ] + [f'gram_{i}' for i in range(len(layer_ids))]
 
    def make_features(self, x, clone=False):
        self.m_feat(x)
        return [(o.clone() if clone else o) for o in self.hooks.stored]
    
    def forward(self, input, target):
        out_feat = self.make_features(target, clone=True)
        in_feat = self.make_features(input)
        self.feat_losses = [base_loss(input,target)]
        self.feat_losses += [base_loss(f_in, f_out)*w
                             for f_in, f_out, w in zip(in_feat, out_feat, self.wgts)]
        self.feat_losses += [base_loss(gram_matrix(f_in), gram_matrix(f_out))*w**2 * 5e3
                             for f_in, f_out, w in zip(in_feat, out_feat, self.wgts)]
        self.metrics = dict(zip(self.metric_names, self.feat_losses))
        return sum(self.feat_losses)
    
    def __del__(self): self.hooks.remove()

path = Path("./models")
learn=load_learner(path, 'ArtLine_650.pkl')

from PIL import Image,ImageOps
import requests
from io import BytesIO

import fastai
from fastai.vision import *
from fastai.utils.mem import *
from fastai.vision import open_image, load_learner, image, torch,Image
import numpy as np
import urllib.request
import PIL.Image
from io import BytesIO
import torchvision.transforms as T

def add_margin2(img, size=650, color=(255, 255, 255)):
    width, height = img.size
    new_width = ((width - 1) // size + 1) * size
    new_height = ((height - 1) // size + 1) * size
    left = (new_width - width) // 2
    top = (new_height - height) // 2
    right = new_width - width - left
    bottom = new_height - height - top
    return ImageOps.expand(img, border=(left, top, right, bottom), fill=color)
def add_margin(img, size=650, color=(255, 255, 255)):
    width, height = img.size
    max_dim = max(width, height)
    new_dim = ((max_dim - 1) // size + 1) * size
    h_pad = (new_dim - height) // 2
    w_pad = (new_dim - width) // 2
    border = (w_pad, h_pad, w_pad, h_pad)
    return ImageOps.expand(img, border=border, fill=color)
def predict(url):
    response = requests.get(url)
    img = PIL.Image.open(BytesIO(response.content)).convert("RGB")
    img_with_margin = add_margin(img)
    #img_with_margin.save("test2.png")

    img_t = T.ToTensor()(img_with_margin)
    img_fast = Image(img_t)
    p,img_hr,b = learn.predict(img_fast)
  
    x = np.minimum(np.maximum(image2np(img_hr.data*255), 0), 255).astype(np.uint8)
    img_hr = PIL.Image.fromarray(x)
    img_hr = img_hr.resize(img_with_margin.size)  
  
    # Remove margin from the high-resolution image
    width, height = img.size
    left = (img_with_margin.size[0] - width) // 2
    top = (img_with_margin.size[1] - height) // 2
    img_hr = img_hr.crop((left, top, left + width, top + height))
  
    img_hr.save("test.png")

def predict2(url):
  response = requests.get(url)
  input = PIL.Image.open(BytesIO(response.content)).convert("RGB")
  size = input.size
  img_t = T.ToTensor()(input)
  img_fast = Image(img_t)
  p,img_hr,b = learn.predict(img_fast)
  x = np.minimum(np.maximum(image2np(img_hr.data*255), 0), 255).astype(np.uint8)
  img = PIL.Image.fromarray(x)
  #im = img.resize(size)
  img.save("test.png")