from fastai import data_block
import torchvision.transforms as T
import os
import sys
import torch.nn as nn
from fastai.vision import *
from fastai.utils.mem import *
from fastai.vision import load_learner
from pathlib import Path
from utils import *
from PIL import Image
import base64


import uvicorn 

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware 



# This class is very important for the prediction and it must be in the same file as the prediction 
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


#Initializing the fast API server
app = FastAPI()

origins = [

    "http://localhost.tiangolo.com",

    "https://localhost.tiangolo.com",

    "http://localhost",

    "http://localhost:8081",

    "http://localhost:3000",

    ]

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

    )

setattr(sys.modules["__main__"], 'FeatureLoss',  FeatureLoss)
learner = load_learner(Path("."), 'ArtLine_920.pkl')


def predict(img_url, learner):
    img = preprocess_img(img_url)
    _,pred, _ = learner.predict(img)
    pred = pred.detach().cpu().numpy().transpose((1, 2, 0))
    pred = (pred - pred.min())/ (pred.max() - pred.min()) * 255
    pred = pred.astype("uint8")
    pred = Image.fromarray(pred)
    return pred

@app.get("/")
async def root():
    return {"message": "I can declourize image with machine learning"}

@app.post("/decolorize")
async def decolorize_image(file: bytes = File(...)):
    img = predict(file, learner)
    pred_path = os.path.join("static", "pred_img.jpg")
    img.save(pred_path)
    with open(pred_path, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    return {my_string}


   
if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")