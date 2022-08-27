import torch

class Pegasus():
  # source: https://huggingface.co/docs/transformers/main/model_doc/pegasus#examples
  def __init__(self):
    print("Pegasus model loading...")
    from transformers import PegasusForConditionalGeneration, PegasusTokenizer
    self.model_name = "google/pegasus-xsum"
    self.device = "cuda" if torch.cuda.is_available() else "cpu"
    self.tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
    self.model = PegasusForConditionalGeneration.from_pretrained(self.model_name).to(self.device)

  def summarize(self, src_text):
    print("\nPegasus model:")
    batch = self.tokenizer(src_text, truncation=True, padding="longest", return_tensors="pt").to(self.device)
    translated = self.model.generate(**batch)
    tgt_text = self.tokenizer.batch_decode(translated, skip_special_tokens=True)
    return tgt_text

class Facebook_bart_large_cnn():
  # source https://huggingface.co/facebook/bart-large-cnn
  def __init__(self):
    print("facebook_bart_large_cnn model loading...")
    self.model_name = "facebook_bart_large_cnn mode"
    from transformers import pipeline
    self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

  def summarize(self, src_text):
    print("\nFacebook_bart_large_cnn model:")
    tgt_text = self.summarizer(src_text, max_length=130, min_length=30, do_sample=False)
    tgt_text = tgt_text[0]['summary_text']
    return tgt_text

class Philschmid_bart_large_cnn_samsum():
  # source https://huggingface.co/philschmid/bart-large-cnn-samsum
  def __init__(self):
    print("\nPhilschmid_bart_large_cnn_samsum loading...")
    self.model_name = "Philschmid_bart_large_cnn_samsum"
    from transformers import pipeline
    self.summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum")

  def summarize(self, src_text):
    print("model Philschmid_bart_large_cnn_samsum:")
    tgt_text = self.summarizer(src_text, truncation=True)
    tgt_text = tgt_text[0]['summary_text']
    return tgt_text

class MT5_multilingual_XLSum():
  # source: https://huggingface.co/csebuetnlp/mT5_multilingual_XLSum
  def __init__(self):
    print("MT5_multilingual_XLSum loading...")
    import re
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

    self.WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))
    self.model_name = "csebuetnlp/mT5_multilingual_XLSum"
    self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
    self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)

  def summarize(self, src_text):
    print("MT5_multilingual_XLSum:")
    input_ids = self.tokenizer(
        [self.WHITESPACE_HANDLER(src_text)],
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512)["input_ids"]

    output_ids = self.model.generate(
        input_ids=input_ids,
        max_length=84,
        no_repeat_ngram_size=2,
        num_beams=4)[0]

    summary = self.tokenizer.decode(
        output_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False)
    return summary

class Small2bert_cnn_daily_mail():
  def __init__(self):
    print("small2bert_cnn_daily_mail loading...")
    self.model_name = "small2bert_cnn_daily_mail"

    from transformers import BertTokenizerFast, EncoderDecoderModel
    self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    self.tokenizer = BertTokenizerFast.from_pretrained('mrm8488/bert-small2bert-small-finetuned-cnn_daily_mail-summarization')
    model = EncoderDecoderModel.from_pretrained('mrm8488/bert-small2bert-small-finetuned-cnn_daily_mail-summarization').to(self.device)

    def summarize(self, src_text):
      inputs = self.tokenizer([text], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
      input_ids = inputs.input_ids.to(self.device)
      attention_mask = inputs.attention_mask.to(self.device)
      output = self.model.generate(input_ids, attention_mask=attention_mask)
      return self.tokenizer.decode(output[0], skip_special_tokens=True)