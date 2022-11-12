# -*- coding: utf-8 -*-
"""Binary_Text_Classification_Conspiracy-COMP400.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YsLpM_A8VCIrru4sq6_At4tRAlX-Hac-
"""

import gradio as gr
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from transformers import TrainingArguments, Trainer
from datasets import load_dataset
import torch
from torch import nn
from torch.nn import functional as F
import numpy as np
import torchmetrics
from torchmetrics.classification.f_beta import F1Score

# import the dataset into a dataset class
dataset = load_dataset("csv", data_files="dataset_balanced.csv", split="train")

# summarize dataset
size = len(dataset["text"])
print(f"Found {size} examples to train on")
print("Schema:")
print(dataset)

split_dataset = dataset.train_test_split(test_size=0.2, shuffle=True)

train_ds = split_dataset["train"]
test_ds = split_dataset["test"]

max_length = 100

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-cased")

def tokenize_function(examples):
  return tokenizer(examples["text"], padding='max_length', truncation=True, max_length=max_length)

train_ds = train_ds.map(tokenize_function)
test_ds = test_ds.map(tokenize_function)

model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-cased",
                                                            num_labels=2)

# set up the training args (where to keep checkpoints + when to evaluate)
training_args = TrainingArguments(output_dir="test_trainer", 
                                  evaluation_strategy="steps",
                                  eval_steps=100,
                                  num_train_epochs=30,
                                  logging_steps=100,
                                  learning_rate=5e-7)

#
#define metrics to compute on each epoch
f1 = torchmetrics.classification.BinaryF1Score()
acc = torchmetrics.classification.BinaryAccuracy()
def compute_metrics(eval_pred):
  f1.reset()
  acc.reset()
  logits, labels = eval_pred
  logits = torch.tensor(logits)
  labels = torch.tensor(labels)
  acc(logits, F.one_hot(labels, num_classes=2))
  f1(logits, F.one_hot(labels, num_classes=2))
  return {"Accuracy": acc.compute(), "F1 score": f1.compute() }

# trainer class that handles the model training loops
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=test_ds,
    compute_metrics=compute_metrics,
)

trainer.train()

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-cased")
max_length = 512

def predict(inputs):
  tokenized_input = tokenizer(inputs,
                              padding='max_length',
                              truncation=True,
                              max_length=max_length, return_tensors="pt")
  #print(tokenized_input)
  preds = model(input_ids=tokenized_input["input_ids"].to("cuda"), attention_mask=tokenized_input["attention_mask"].to("cuda"))
  pred = torch.argmax(preds["logits"], dim=-1)
  print(preds["logits"])
  return "Conspiracy" if pred == 1 else "Not Conspiracy"
  print(preds)

predict("Flashback: There is no one in the White House tasked specifically to oversee a coordinated government-wide response in the event of a pandemic, since the post of senior director for global health security and biothreats on the NSC was eliminated last May. https://t.co/kOQK8XVI9j")

demo = gr.Interface(fn=predict, inputs="text", outputs="text")

demo.launch()