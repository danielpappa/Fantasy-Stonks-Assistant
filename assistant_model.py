import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import vector_search
import mongo_db

tokenizer = AutoTokenizer.from_pretrained('google/gemma-2b-it')
model = AutoModelForCausalLM.from_pretrained('google/gemma-2b-it') # for GPU: , device_map = 'auto')

def augmented_llm(query, history):
  source_information = vector_search.get_search_result(query, mongo_db.get_collection())
  combined_information = (
      f"Query: {query}\n\nI'm answering based on the following potential match\n{source_information}\nLLM:"
  )
  input_ids = tokenizer(combined_information, return_tensors="pt") # for GPU: .to("cuda")
  response = model.generate(**input_ids, max_new_tokens=500)
  answer = tokenizer.decode(response[0]).split("LLM:")[-1]
  return answer
