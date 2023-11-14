import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model, metrics

#Load dataset and create object
boston_data = datasets.fetch_california_housing()
#Defining feature matrix X and response vector Y
X = boston_data.data
y = boston_data.target
#split data into train/test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.6, random_state = 1)
#Create regression object, train model
MLR_reg = linear_model.LinearRegression()
MLR_reg.fit(X_train, y_train)
#Printing regression coefficient, variance score, plot regression line and labels on it
print('Coefficients: \n', MLR_reg.coef_)
print('Variance score: {}'.format(MLR_reg.score(X_test, y_test)))
plt.style.use('bmh')
plt.scatter(MLR_reg.predict(X_train),MLR_reg.predict(X_train) - y_train, color = "green", s = 20, label = 'Train_data')
plt.hlines(y=0, xmin = 0, xmax = 60, color = 'red', linewidth = 1.25)
plt.legend(loc = 'upper right')
plt.title("Residual errors(eo)")
plt.show()