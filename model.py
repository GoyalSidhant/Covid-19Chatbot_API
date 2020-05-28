import io
import random
import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
import pandas as pd
nltk.download('popular', quiet=True) # for downloading packages
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
import re


# uncomment the following only the first time
""" nltk.download('punkt') # first-time use only
nltk.download('wordnet') # first-time use only """

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)



# dataset coronavirus WHO
pd.set_option('max_colwidth', 100)  # Increase column width
data = pd.read_excel("WHO_FAQ.xlsx", encoding='utf8')



def preprocess_sentences(input_sentences):
    return [re.sub(r'(covid-19|covid)', 'coronavirus', input_sentence, flags=re.I) 
            for input_sentence in input_sentences]
        
# Load module containing USE
print("loading module")
module = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual-qa/3')
print("loaded model")
# Create response embeddings
response_encodings = module.signatures['response_encoder'](
        input=tf.constant(preprocess_sentences(data.Answer)),
        context=tf.constant(preprocess_sentences(data.Context)))['outputs']

test_questions = []
print(type(test_questions))
def responsive(user_response):
  test_questions.append(user_response)
  question_encodings = module.signatures['question_encoder'](
    tf.constant(preprocess_sentences(test_questions))
)['outputs']
  test_responses = data.Answer[np.argmax(np.inner(question_encodings, response_encodings), axis=1)]
  test_responses=test_responses.values.tolist()
  test_questions.clear()
  return (test_responses[0])
  
def response(user_response):
  print("ROBO: My name is . I will answer your queries about Chatbots. If you want to exit, type Bye!")
  user_response=user_response.lower()
  if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            return "ROBO: You are welcome.."
        else:
            if(greeting(user_response)!=None):
                return "ROBO: "+greeting(user_response)
            else:
                
                return "ROBO:"+ responsive(user_response)
  else:
        return "ROBO: Bye! take care.."