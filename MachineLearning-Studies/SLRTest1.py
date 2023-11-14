import numpy as np
import matplotlib.pyplot as plt

#Define a function for claculating values for SLR
def coef_estimation(x,y):
    n = np.size(x)                                      #Calculate number of observations n
    mean_x, mean_y = np.mean(x), np.mean(y)             #Calculate mean x and y
    cross_xy = np.sum(y*x) - n*mean_y*mean_x            #Calculate cross deviation and deviation about x
    cross_xx = np.sum(x*x)-n*mean_x*mean_x          
    reg_b_1 = cross_xy/cross_xx                         #Calculate regression coefficents
    reg_b_0 = mean_y - reg_b_1*mean_x              
    return(reg_b_0, reg_b_1)
#Plot regression line
def plot_regression_line(x,y,b):
    plt.scatter(x,y, color = "r", marker ="o", s = 20)  #Plot actual points as scatter plot
    y_pred = b[0] + b[1]*x
    plt.plot(x, y_pred, color = "g")                    #plotting the regression line and labels on it
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    

#Define main() to provide data and call preceding functions
def main():
    x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10, 11, 12, 13, 14])
    y = np.array([100, 300, 350, 500, 750, 850, 900,950, 1250, 1350,1400, 1550, 1600, 1650,1700])
    b = coef_estimation(x,y)
    print("Estimated coefficients:\nreg_b_0 = {} \nreg_b_1 = {}".format(b[0],b[1]))
    plot_regression_line(x,y,b)


if __name__ == "__main__":
    main()