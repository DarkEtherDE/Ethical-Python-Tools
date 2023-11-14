import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

#Load dataset and create object
diabetes_data = datasets.load_diabetes()
#using one feature
X = diabetes_data.data[:, np.newaxis, 2]
#Split to train and test sets
X_train = X[:-35]
X_test = X[-35:]
#Splitting the target into training and testing sets
y_train = diabetes_data.target[:-35]
y_test = diabetes_data.target[-35:]
#Create linear regression object
SLR_reg = linear_model.LinearRegression()
#Training the model
SLR_reg.fit(X_train, y_train)
#Predictions
y_pred = SLR_reg.predict(X_test)
#Print regression coefficient, mean squared error(MSE), variance score. Also plot the regression line and labels on it
print('Coefficients: \n', SLR_reg.coef_)
print("Mean squared error: %.2f"%mean_squared_error(y_test, y_pred))
print('Variance score: %.2f' % r2_score(y_test,y_pred))
plt.scatter(X_test, y_test, color = 'red')
plt.plot(X_test, y_pred, color='green', linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()