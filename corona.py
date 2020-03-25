import numpy as np
import pandas as pd
import os
import json
from tqdm import tqdm
import re
import matplotlib.pyplot as plt
from matplotlib import style

style.use("ggplot")


dirs = ["biorxiv_medrxiv","comm_use_subset","custom_license","noncomm_use_subset"]
docs = []
for d in dirs:
    print(d)
    for file in tqdm(os.listdir(f"{d}/{d}")):
        file_path = f"{d}/{d}/{file}"
        j = json.load(open(file_path, "rb"))
        title = j['metadata']['title']
        
        try:
            abstract = j['abstract'][0]
        except:
            abstract = ""
              
        full_text = ""
        
        for text in j['body_text']:
            #print(text['text])
            full_text += text['text']+'\n\n'
            
               
        #print(full_text)
        docs.append([title, abstract, full_text])
        
df = pd.DataFrame(docs,columns=['title','abstract','full_text'])
#print(df.head())

incubation = df[df['full_text'].str.contains('incubation')]
#print(incubation.head())

texts = incubation['full_text'].values

incubation_times = []

for t in texts:
    for sentence in t.split(". "):
        if "incubation" in sentence:
            single_day = re.findall(r" \d{1,2} day", sentence)
            
            if len(single_day) == 1:
                #print(single_day[0])
                #print(sentence)
                num = single_day[0].split(" ")
                incubation_times.append(float(num[1]))
                
print(incubation_times)
print(len(incubation_times))

print(f"The mean projected incubation time is {np.mean(incubation_times)} days")
plt.hist(incubation_times, bins=10)
plt.ylabel("bin counts")
plt.xlabel("incubation time (days)")
plt.show()