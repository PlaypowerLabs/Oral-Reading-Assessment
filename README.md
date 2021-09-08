#   ORAL READING ASSESSMENT

![image](https://raw.githubusercontent.com/Playpowerlabs/Oral-Reading-Assessment/master/.github/images/img_1.png)

Oral Reading Assessment app provides a way for the students' to improve their reading skills. Reading is an essential skill to become successful in any discipline.  

## Setting up the project

### 1. Clone the repo

Clone this repository for all the source code as mentioned below: 

```console
$ git clone https://github.com/PlaypowerLabs/Oral-Reading-Assessment.git
$ cd Oral-Reading Assessment
```

### 2. Installating Packages & Downloading Models

- The application is made using `Streamlit` in `Python`. Make sure that least version of python is 3.4.0 .

- Use the below command to download all the python libraries and some dependencies required for the application to run:

```console
pip install --no-cache-dir -r requirements.txt
python -m install spacy download en_core_web_sm
```

- Download models (Total Size - 2.3GB) using the below command:

```console
chmod +x data_download.sh
./data_download.sh
```

This would create `models` folder inside the `Oral-Reading-Assessment` repo. To manually download the data, click the below link:

https://oral-reading-assessment-app-models.s3.us-east-2.amazonaws.com/models.zip

## Running the Oral Reading Assessment Webapp

- Execute the python file `app.py` using streamlit:

```console
streamlit run app.py
```

- The webapp is launched in your browser and opened automatically.

- Choose the language that you want to practice speaking and click `Show Passage` button.

- Wait for the speech-to-text engine to load for the selected language and then click `record` button and start reading the passage.

- 



