# -*- coding: utf-8 -*-
"""Minor_Project_final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ijRMmeW9pvRejmN-nclQliKf5jU56Is4

# **General**
"""

# Imports
import numpy as np
import pandas as pd
import sklearn
import seaborn as sns
import matplotlib.pyplot as plt

"""# **Laoading data from local drive**

# **Read Data**
"""

fd = pd.read_csv('Fertilizer.csv')
td = pd.read_csv('final_temperature.csv')
rd = pd.read_csv('final_rainfall.csv')
ytr= pd.read_csv('Final_Dataset_after_temperature.csv')

"""# **Data Preparation**

## **Fertilizer Data**
"""

fd

fd.info()

fd.describe()

# Number of crops
len(fd['Crop'].unique())

"""## **Temperature Data**"""

td

td.info()

td.describe()

# Number of Indian States and Union Territories
len(td['States'].unique())

td.shape

# Number of crops
len(fd['Crop'].unique())

"""## **Rainfall Data**"""

rd

rd.info()

rd.describe()

rd.shape

"""## **Crop Yield Data Using Temperature and Rainfall**"""

ytr

ytr.info()

ytr.describe()

ytr.shape

ytr

# Number of crops
len(ytr['Crop'].unique())

"""# **Data Exploration**

## **Tempertaure Data**
"""

td

temp_data = td.groupby('States')['yearly_temp'].mean()  # Group by 'States' and get mean of 'yearly_temp'

# Plot data
fig, ax = plt.subplots(figsize=(15, 9))
fig.suptitle('Mean Yearly Temperature (°C) Across States')

temp_data.plot(ax=ax, kind='bar')  # Plot as bar graph (adjust 'kind' for different plot types)

ax.set_ylabel('Mean Yearly Temperature (°C)')
ax.set_xlabel('States')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability with many states

plt.show()

td=td.corr(numeric_only=True)
td

#sns.heatmap(td,annot=True,cbar=True,cmap="coolwarm")

sns.distplot(td['yearly_temp'])
plt.show()

"""## **Rainfall Data**"""

rd=rd.corr()
rd

sns.heatmap(rd,annot=True,cbar=True,cmap="coolwarm")

sns.distplot(rd['yearly_rainfall'])
plt.show()

"""## **Final Crop Yield**"""

ytr

ytr.boxplot()

# Group by 'State_Name' and get mean of 'Yield_ton_per_hec'
crop_data_by_state = ytr.groupby('State_Name')['Yield_ton_per_hec'].mean()
crop_data_by_state

crop_data_by_state = ytr.groupby('State_Name')['Yield_ton_per_hec'].mean()

# 1. Scatter Plot using matplotlib:
plt.figure(figsize=(15, 9))
plt.scatter(crop_data_by_state.index, crop_data_by_state.values)
plt.xlabel('State Name')
plt.ylabel('Mean Yield (tons per hectare)')
plt.title('Mean Yield per State (Scatter Plot)')
plt.xticks(rotation=45)  # Rotate x-axis labels for readability
plt.show()

# 2. Box Plot using matplotlib:
plt.figure(figsize=(15, 9))
plt.boxplot(
    [ytr[ytr['State_Name'] == state]['Yield_ton_per_hec'] for state in ytr['State_Name'].unique()],
    labels=ytr['State_Name'].unique(),
    vert=False  # Horizontal box plot for better readability with many states
)
plt.xlabel('Yield (tons per hectare)')
plt.ylabel('State Name')
plt.title('Distribution of Yield per State (Box Plot)')
plt.show()

ytr1=ytr.corr(numeric_only=True)
ytr1

sns.heatmap(ytr1,annot=True,cbar=True,cmap="coolwarm")

sns.distplot(ytr1['Yield_ton_per_hec'])
plt.show()

"""# **Data Preprocessing**

## **Removal of Outliers(Box Plot)**
"""

ytr.boxplot(column='Production_in_tons')
plt.show()

def remove_outlier(col):

   sorted(col)

   q1,q3=col.quantile([0.25,0.75])

   IQR=q3-q1

   lwr_bound= q1-(1.5*IQR)

   upr_bound =q3+(1.5*IQR)

   return lwr_bound, upr_bound

low, high=remove_outlier(ytr["Production_in_tons"])

ytr["Production_in_tons"]=np.where(ytr["Production_in_tons"]>high, high, ytr["Production_in_tons"])

ytr["Production_in_tons"]=np.where (ytr["Production_in_tons"]<low, low, ytr ["Production_in_tons"])

ytr.boxplot(column="Production_in_tons")

ytr.boxplot(column='Area_in_hectares')
plt.show()

low, high=remove_outlier(ytr["Area_in_hectares"])

ytr["Area_in_hectares"]=np.where(ytr["Area_in_hectares"]>high, high, ytr["Area_in_hectares"])

ytr["Area_in_hectares"]=np.where (ytr["Area_in_hectares"]<low, low, ytr ["Area_in_hectares"])

ytr.boxplot(column="Area_in_hectares")

ytr.boxplot(column='Yield_ton_per_hec')
plt.show()

low, high=remove_outlier(ytr["Yield_ton_per_hec"])

ytr["Yield_ton_per_hec"]=np.where(ytr["Yield_ton_per_hec"]>high, high, ytr["Yield_ton_per_hec"])

ytr["Yield_ton_per_hec"]=np.where (ytr["Yield_ton_per_hec"]<low, low, ytr ["Yield_ton_per_hec"])

ytr.boxplot(column="Yield_ton_per_hec")

low, high=remove_outlier(ytr["rainfall"])

ytr["rainfall"]=np.where(ytr["rainfall"]>high, high, ytr["rainfall"])

ytr["rainfall"]=np.where (ytr["rainfall"]<low, low, ytr ["rainfall"])

ytr.boxplot(column="rainfall")

ytr.boxplot(column="temperature")

low, high=remove_outlier(ytr["temperature"])

ytr["temperature"]=np.where(ytr["temperature"]>high, high, ytr["temperature"])

ytr["temperature"]=np.where (ytr["temperature"]<low, low, ytr ["temperature"])

ytr.boxplot()

"""## **Test-Train Dataset Split**"""

ytr.shape

ytr

X=ytr.drop("Yield_ton_per_hec",axis=1)
y=ytr["Yield_ton_per_hec"]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

X_train.shape

y_train.shape

X_test.shape

y_test.shape

X_train

X_train.head(1)

"""## **One Hot Encoding and Standard Scaling**"""

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
ohe = OneHotEncoder(drop='first')
scale = StandardScaler()

preprocesser = ColumnTransformer(
        transformers = [
            ('StandardScale', scale, [3, 4, 5, 6]),
            ('OHE', ohe, [0, 1, 2]),
        ],
        remainder='passthrough'
)

preprocesser

X_train_dummy = preprocesser.fit_transform(X_train)
X_test_dummy = preprocesser.transform(X_test)

X_train_dummy

X_test_dummy

ytr.shape

ytr.shape

"""## **Modeling**"""

#linear regression
from sklearn.linear_model import LinearRegression,Lasso,Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error,r2_score


models = {
    'lr':LinearRegression(),
    'lss':Lasso(),
    'Rid':Ridge(),
    'Dtr':DecisionTreeRegressor(),
    'gbr' : GradientBoostingRegressor()
}
for name, md in models.items():
    md.fit(X_train_dummy,y_train)
    y_pred = md.predict(X_test_dummy)

    print(f"{name} : mae : {mean_absolute_error(y_test,y_pred)} score : {r2_score(y_test,y_pred)}")

"""## **Select Model**"""

dtr = DecisionTreeRegressor()
dtr.fit(X_train_dummy,y_train)
dtr.predict(X_test_dummy)

X_train

ytr

"""## **Prediction**"""

def prediction(State_Name,Crop_Type,	Crop,	rainfall,	temperature,Area_in_hectares,Production_in_tons):
    # Create an array of the input features
    features = np.array([[State_Name,	Crop_Type,	Crop,	rainfall,	temperature,	Area_in_hectares,	Production_in_tons]], dtype=object)

    # Transform the features using the preprocessor
    transformed_features = preprocesser.transform(features)

    # Make the prediction
    predicted_yield = dtr.predict(transformed_features).reshape(1, -1)

    return predicted_yield[0]

State_Name= 'andhra pradesh'
Crop_Type= 'kharif'
Crop= 'Arhar/Tur'
rainfall= 654.34
temperature= 29.266667
Area_in_hectares= 14320.0
Production_in_tons= 2600.0

result = prediction(State_Name,Crop_Type,Crop,rainfall,temperature,	Area_in_hectares,	Production_in_tons)

result

import pickle
pickle.dump(dtr,open('dtr.pkl','wb'))
pickle.dump(preprocesser,open('preprocessor.pkl','wb'))

import sklearn
print(sklearn.__version__)
