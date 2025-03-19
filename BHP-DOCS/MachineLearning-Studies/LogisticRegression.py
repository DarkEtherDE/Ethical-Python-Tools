#Importing necessary packages
import numpy as np
import matplotlib.pyplot as plt

#Download data
from sklearn.datasets import load_digits
digits_data = load_digits()
#Print images and labels in the datasets
print(digits_data.data.shape)
print(digits_data.target.shape)
plt.figure(figsize=(20,4))
for index, (image, label) in enumerate(zip(digits_data.data[0:10], digits_data.target[0:10])):
    plt.subplot(1, 10, index + 1)
    plt.imshow(np.reshape(image, (8,8)), cmap=plt.cm.gray)
    plt.title('Training: %i\n' % label, fontsize = 20)
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(digits_data.data, digits_data.target, test_size = .30, random_state = 0)#Set test size to 30%, train percent goes to %70
from sklearn.linear_model import LogisticRegression
#Import the logistic regression class from sklearn and use the fit method to train the model
LogRegression = LogisticRegression()
LogRegression.fit(x_train,y_train)
#Prediction for images
LogRegression.predict(x_test[0].reshape(1,-1))
LogRegression.predict(x_test[0:10])
y_pred = LogRegression.predict(x_test)
#Calculate performance metrics
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
print("Output data")
#Print confusion Matrix
print('Confusion Matrix:-\n', confusion_matrix(y_test, y_pred))
#Classification report
print('Classification Report:-\n', classification_report(y_test, y_pred))
#Accuracy score
print('Accuracy:-\n', accuracy_score(y_test, y_pred))