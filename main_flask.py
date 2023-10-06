from flask import Flask, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import colors
from matplotlib.colors import ListedColormap
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from dotenv import dotenv_values,load_dotenv
import os

from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist

app = Flask(__name__)
data_global = {}

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/load_data')
def load_data():
    ENV = dotenv_values(".env")
    load_dotenv(override=False)
    data = pd.read_csv(os.environ['DATASETS_PATH'] + '/marketing_campaign.csv', sep="\t")
    data=data.dropna()
    data["Age"] = 2023-data["Year_Birth"]
    data["Spent"] = data["MntWines"]+ data["MntFruits"]+ data["MntMeatProducts"]+ data["MntFishProducts"]+ data["MntSweetProducts"]+ data["MntGoldProds"]
    data["Marital_Status"]=data["Marital_Status"].replace({"Married":"1", "Together":"1", "Absurd":"0", "Widow":"0", "YOLO":"0", "Divorced":"0", "Single":"0", "Alone":"0"})
    data["Children"]=data["Kidhome"]+data["Teenhome"]
    data["Fam_with_children"] = np.where(data.Children> 0, 1, 0)
    data["Education"]=data["Education"].replace({"Basic":"0","2n Cycle":"1", "Graduation":"2", "Master":"3", "PhD":"3"})
    data["Education"]=pd.to_numeric(data['Education'])
    data=data.rename(columns={"MntWines": "Wines","MntFruits":"Fruits","MntMeatProducts":"Meat","MntFishProducts":"Fish","MntSweetProducts":"Sweets","MntGoldProds":"Gold"})
    to_drop = ["Marital_Status", "Dt_Customer", "Z_CostContact", "Z_Revenue", "Year_Birth", "ID"]
    data = data.drop(to_drop, axis=1)
    data_global = pd.DataFrame(data)
    data = pd.DataFrame.to_json(data)
    return data
