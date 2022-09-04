import torch

class bart_large_mnli():
    # source https://huggingface.co/facebook/bart-large-mnli
    def __init__(self):
        print("\nbart_large_mnli loading...")
        self.model_name = "bart_large_mnli"
        from transformers import pipeline
        self.classifier = pipeline("zero-shot-classification",
                              model="facebook/bart-large-mnli")

    def zero_shot(self, text:str, labels:list):
        try:
            z_result = self.classifier(text, labels)
        except:
            print("zero_shot error")
            z_result= {'scores': None,
                       "labels": None,
                       "sequence": None}
        return z_result
