---
layout: post
published: true
title: Website labeling tool in 50 lines of Python
tags: [streamlit, machine-learning, python, data-science]
---

## What
Machine learning is 
Very often, part of the machine learning job is to collect 
Doing it in python
Simplicity 
## Screenshots

## Setup

Install streamlit with pip
```bash
pip install streamlit
```

Lets create simple `app.py` file, that just prints "Hello world!"

```python
print("Hello World!")
```

Now, lets run `streamlit`
```bash
streamlit run app.py
```

... and voila! This should start a local server and open the browser tab with our app running! Currently it would be just a blank page. Don't worry we would soon have rest of our components in there!

As a note, the terminal window should have a sharable URL on local network as well. Super useful if you want to share your app with your colleagues.

```bash

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.4:8501
```  

## Website Labeler

Now, lets add the code for website labeling.

We are going to assume that 
1. You have a csv file where you have a list of websites you want to label.
2. You want to store the output of labeling in a csv file.

### Reading input

Lets read the input file with URLs to be labeled `websites.csv` and put them into a list.

```python
import csv

websites = []
with open('websites.csv', newline='') as csvfile:
  for temp in csv.reader(csvfile):
    websites.append(temp[0])  
```

### Displaying labeling tools

Lets add our websites to the UI. Let's start 

```python
import streamlit as st

st.markdown(f'## [{websites[0]}]({websites[0]})')
```
This should give you a simple clickable markdown link to the first website in the list.

TODO: screenshot-website-link

Now lets add buttons for each of labels. We will be using streamlit button component for this. 

```python
labels = ["safe","unsafe","social","educational"]
label_buttons = []

def insert_button(columns,labels,i,label_buttons):
  with columns[i]:
    b = st.button(l)
    label_buttons.append(b)
```

```python
```

### Keeping count

```python
def update_count(count):
  with open("counter", "w") as f:
    f.truncate()
    f.write(f"{count}")

with open("counter", "r") as f:
  count = int(f.readline())


```
### Writing the output

```python
def write_label(w,label,notes,count):
  with open('labeled-dataset.csv','a') as fd:
    fd.write(f"{w},{label},{notes},{count}\n")
```
### Celebrations and Reset
```python

```



## Optimization
Now that we have the app working, we can optimize a few things.
First since streamlit will run the whole application each time, we should avoid repeating things which are not going to change between runs.

In our case, for example, if you assume, the list of websites, we can add the `@st.cache` annotation. This way it will be cached automatically between run.

```python
@st.cache
def load_data(filename='websites.csv'):
  with open(filename, newline='') as csvfile:
    for temp in csv.reader(csvfile):
      websites.append(temp[0])
```

```
if count<len(websites):
  w = websites[count]
  if w=="DONE":
      st.balloons()
      if st.button("Reset"):
        update_count(1) 
  else:    
    st.markdown(f'## [{w}]({w})')
    columns = st.beta_columns(len(labels))

    for i,l in enumerate(labels):
        insert_button(columns,labels,i,label_buttons)

    notes=st.text_input("notes")

    for i,b in enumerate(label_buttons):
      if b:
        write_label(websites[count-1],labels[i],notes,count-1)
        count += 1
        update_count(count)
```

Here is the full code for app.py, as promised under 50 lines!

Streamlit also allows you to run the app file directly from github! So you can use the following command to get the app running locally!
```bash
stremlit run https://raw.githubusercontent.com/dharmeshkakadia/website_labeler/master/app.py
```

The full source code is available on [my github](https://github.com/dharmeshkakadia/website_labeler)

