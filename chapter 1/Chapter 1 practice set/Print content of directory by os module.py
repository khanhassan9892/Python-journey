import os
# Provide the direcotry path if not use '..'
directory = '/'
# List of files in specific direcetry
for item in os.listdir(directory):
    print(item)
