# **Query SQL database using natural language**

## **Overview**

In today’s data-driven world, professionals across various industries often need to extract insights from large SQL databases. Traditionally, this process involved writing complex SQL queries, performing extensive data manipulation, and creating visual dashboards to interpret results. These tasks can be time-consuming and require a high level of technical expertise.

![bird_image](./images/bird.png)


However, with advancements in natural language processing and AI technologies, querying SQL databases has become much more intuitive and accessible. Imagine being able to ask questions like, “What are the sales trends for the past year?” or “Which products have the highest return rates?” and instantly receive detailed, visualized responses. This guided project guides you through setting up an agent that lets you query a MySQL database using natural language, simplifying the data analysis process.


## **Objective**

In the project, I will:

- **Integrate natural language processing**: I'll use tools like Langchain and large language models (LLM) to interpret natural language queries.

- **Execute SQL queries from natural language**: Translate natural language questions into SQL queries to fetch relevant data from the MySQL database.


## **Set up a virtual environment**

Begin by creating a virtual environment. Using a virtual environment help me manage dependencies for different projects separately, avoiding conflicts between package versions. To replicate this project, kindly follow the steps below:

1. **Create and activate a virtual environment using `pipenv`:**

```sh
pip install virtualenv 
virtualenv sql_lang   # Create a virtual environment named sql_lang
source sql_lang/bin/activate    # activates sql_lang

```
<u>***Note:***</u> You can use any environment manager of you choice to achieve this same result.


2. **Install the necessary libraries within the `pipenv` environment:**

To ensure a seamless execution of the scripts, and considering that certain functions within these scripts rely on external libraries, it’s essential to install some prerequisite libraries before you begin.

- **`ibm-watsonx-ai` and `ibm-watson-machine-learning`**: The IBM Watson Machine Learning package integrates powerful IBM LLM models into the project.
- *`langchain`, `langchain-ibm`, and `langchain-experimental`**: This library is used for relevant features from Langchain.
- **`mysql-connector-python`**: This library is used as a MySQL database connector.

Run the following commonds in your terminal (with the `pipenv` prefix) to install the packages.

```sh
pipenv install ibm-watsonx-ai==1.0.4 \
ibm-watson-machine-learning==1.0.357 \
langchain==0.2.1 \
langchain-ibm==0.1.7 \
langchain-experimental==0.0.59 \
mysql-connector-python==8.4.0

```

3. **Activate the `pipenv` shell:

```sh
pipenv shell

```


## **Instantiate a MySQL database**

Because this project focuses on querying a MySQL database using natural language, you must instantiate a MySQL server, and then create a sample database in the server.

### **Create MySQL server**

To create a MySQL server in Cloud IDE, click the following button.

 Open and Start MySQL in IDE

After you click the button, you see that there is a MySQL service on the right. Click Start to start the MySQL server.

indexing

It might take approximately 10-15 seconds. When it’s showing active, it means that the server is ready to be used. If you see any error messages, please refresh the page and try again.

indexing

You have created a MySQL server. Let’s test it to see if it can run successfully.

Click MySQL CLI so that you can interact with the server in the terminal. It opens a new tab in the terminal showing something similar to the following image with the mysql prefix at the front.

indexing

THis means that you have successfully connected with the server. Now, let’s input an SQL query to test it. For example, the following command shows all databases in the server.

1
SHOW DATABASES;
Copied!
To run it, press enter/return on your keyboard. If it runs successcully, it returns an output like shown in the following image.

indexing

Congratulations, the server is working correctly. Now, let’s create a sample database to use.

### **Create Chinook database**

In this project, I'll use the ![Chinook](https://docs.yugabyte.com/preview/sample-data/chinook/) database as an example. The database can be forund on this ![repo](https://github.com/yugabyte/yugabyte-db/tree/master/sample).

#### **Introduction to the Chinook database**

The Chinook data model represents a digital media store, including tables for artists, albums, media tracks, invoices, and customers.

- Media-related data was created by using real data from an Apple iTunes library.
- Customer and employee information was created by using fictitious names and addresses that can be located on Google maps, and other well-formatted data (phone, fax, email, and so on).
- Sales information was auto generated using random data for a four-year period.

**The Chinook sample database includes:**

- 11 tables
- A variety of indexes, primary and foreign key constraints
- Over 15,000 rows of data

For details, the following image shows the entity relationship diagram of the Chinook data model.

#### **Install the Chinook sample database**

The Chinook SQL scripts can be found in the sample directory of the YugabyteDB [GitHub](https://github.com/yugabyte/yugabyte-db) repository. The following files will be used for this exercise:

- chinook_ddl.sql — Creates the tables and constraints
- chinook_genres_artists_albums.sql — Loads artist and album information
- chinook_songs.sql — Loads individual song information


Follow the steps here to install the Chinook sample database.


Retrieve the database creation code
The database creation code has been prepared for you. Run the following code in the terminal to retrieve the SQL file from the remote.
Note: Run the code in the terminal with the (my_env) prefix instead of the mysql prefix.

1
wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/Mauh_UvY4eK2SkcHj_b8Tw/chinook-mysql.sql
Copied!Executed!
After it runs successfully, you see an SQL file called PROJECT.

indexing

Run the sql file
Now, you must excute the SQL file to create the database.

At the terminal with the mysql prefix, enter the following command.

1
SOURCE chinook-mysql.sql;
Copied!
After it’s finished, test to see if the database was created successfully by entering the following command.

1
SHOW DATABASES;
Copied!
If the database was successfully created, you see the Chinook database in your list of databases.

indexing

Let’s run some sample SQL commands to interact with the Chinook database. For example, suppose that you want to know how many albums the Chinook database contains. To find this information, you could run the following SQL command.

1
2
USE Chinook;
SELECT COUNT(*) FROM Album;
Copied!
The previous command, when copied and pasted into the terminal with the mysql prefix should give you an answer of 347.

indexing





## **Instantiate an LLM**

This section guides you through the process of instantiating an LLM by using the watsonx.ai API. This section uses the **`mistralai/mixtral-8x7b-instruct-v01` model**. To find other foundational models that are available on `watsonx.ai`, refer to ![Foundation model library](https://www.ibm.com/products/watsonx-ai/foundation-models?utm_source=skills_network&utm_content=in_lab_content_link&utm_id=Lab-chat+with+SQL+data_v1_1718403341#Foundation+model+library) and ![fm_model](https://ibm.github.io/watsonx-ai-python-sdk/fm_model.html).

### **Creating the LLM**

The code to craete the LLM object can be founf in the `sql_agent.py` file.

```python
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

model_id = 'mistralai/mixtral-8x7b-instruct-v01'

parameters = {
    GenParams.MAX_NEW_TOKENS: 256,  # This controls the maximum number of tokens in the generated output
    GenParams.TEMPERATURE: 0.5, # This randomness or creativity of the model's responses
}

credentials = {
    "url": "https://us-south.ml.cloud.ibm.com"
}

project_id = "skills-network"

model = ModelInference(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=project_id
)

mixtral_llm = WatsonxLLM(model = model)

print(mixtral_llm.invoke("What is the capital of Ontario?"))

```
The code above creates an LLM object by using the watsonx.ai API.


<u>***Note***:</u> In addition to creating the LLM object, the `sql_agent.py` also  includes the sample query `‘What is the capital of Ontario?’.` This query was included to test whether the model is being correctly loaded by the script.


### **Test the model**

Run the following command in the terminal with the `sql_lang` prefix.

```python
python3 sql_agent.py
```

You should see a response in the terminal that’s similar to the following response"

![Image of response](link_to_respose.jpg)

<u>***Note:***</u> You will likely not get an identical response because the LLM was instantiated with a `temperature` of **0.5** ensuring that there is quite a bit of **randomness** in the model’s responses.


**Great, the LLM is ready to be used!**


## **Building the database connector**

Building the database connector is simple. It requires just two lines of code:

```python
mysql_uri = 'mysql+mysqlconnector://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{database_name}'
db = SQLDatabase.from_uri(mysql_uri)

```


However, from the code, you see that there are some MySQL server-related parameters that are missing. 
Specifically, you must define a `mysql_username`, a `mysql_password`, a `mysql_host`, a `mysql_port`, and a `database_name`.


Replace the connection information in the following code with the values that you get from your MySQL server.

```sql
mysql_username = 'root'  # Replace with your server connect information
mysql_password = 'zQTLH3HB0q3ahCuAaDcAwdlb' # Replace with your server connect information
mysql_host = '172.21.52.20' # Replace with your server connect information
mysql_port = '3306' # Replace with your server connect information
database_name = 'Chinook'
mysql_uri = f'mysql+mysqlconnector://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{database_name}'
db = SQLDatabase.from_uri(mysql_uri)

```

You should add above code, with the connection information replaced by the values of your MySQL server, by appending them to the `sql_agent.py` file.

Also, delete the following line from the sql_agent.py file. This was the last line in the file prior to appending the two lines previously.

1
print(mixtral_llm.invoke("What is the capital of Ontario?"))
Copied!
After adding the two lines for the database connector and deleting the print() line, save sql_agent.py.

The following code is the complete code until now. Note that you should amend the mysql_uri = line as necessary.


# Use this section to suppress warnings generated by your code:
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
warnings.filterwarnings('ignore')
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
model_id = 'mistralai/mixtral-8x7b-instruct-v01'
parameters = {
    GenParams.MAX_NEW_TOKENS: 256,  # this controls the maximum number of tokens in the generated output
    GenParams.TEMPERATURE: 0.5, # this randomness or creativity of the model's responses
}
credentials = {
    "url": "https://us-south.ml.cloud.ibm.com"
}
project_id = "skills-network"
model = ModelInference(
    model_id=model_id,
    params=parameters,
    credentials=credentials,
    project_id=project_id
)
mixtral_llm = WatsonxLLM(model = model)
mysql_uri = 'mysql+mysqlconnector://root:zQTLH3HB0q3ahCuAaDcAwdlb@172.21.52.20:3306/Chinook'
db = SQLDatabase.from_uri(mysql_uri)