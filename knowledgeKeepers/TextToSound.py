
import sys
from gtts import gTTS

import os
  
# The text that you want to convert to audio
if __name__ == '__main__':
    # Get the input text from the command-line arguments
    mytext = sys.argv[1]
  
# Language in which you want to convert
language = 'en'
  
# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)
  
# Saving the converted audio in a mp3 file named
# welcome 
myobj.save("Test.mp3")
  
# Playing the converted file
# os.system("Test.mp3")

