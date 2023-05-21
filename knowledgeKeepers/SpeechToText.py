#!/usr/bin/env python
# coding: utf-8

# In[8]:


#!pip install speechrecognition
#!pip install pyttsx3
#!pip install pyaudio


# In[6]:


import speech_recognition as sr


# In[15]:


r = sr.Recognizer()
with sr.Microphone() as source:
    audio = r.listen(source)
    


# In[13]:


try:
    text = r.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, I could not understand what you said.")
except sr.RequestError as e:
    print("Sorry, an error occurred while making a request to Google Speech Recognition:", e)

