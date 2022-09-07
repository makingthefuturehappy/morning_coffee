import torch

class bart_large_mnli():
    # source https://huggingface.co/facebook/bart-large-mnli
    def __init__(self):
        print("\nbart_large_mnli loading...")
        self.model_name = "bart_large_mnli"
        self.round = 2
        from transformers import pipeline
        self.classifier = pipeline("zero-shot-classification",
                              model="facebook/bart-large-mnli")

    def zero_shot(self, text:str, labels:list):
        zero_shot_list = []

        try:
            z_result = self.classifier(text,
                                       labels,
                                       # multi_class=True
                                       )
            #round up
            scores = []
            for score in z_result['scores']:
                scores.append(round(score, 2))
            z_result['scores'] = scores

            zero_shot_list = []
            for i in range(0, len(labels)):
                zero_shot_list.append(
                    str(z_result['labels'][i]) + ": " + str(z_result['scores'][i]))

        except:
            print("zero_shot error")
            zero_shot_list = []

        return zero_shot_list
