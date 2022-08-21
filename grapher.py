from tkinter import X
import matplotlib.pyplot as plt

def plot_graph(results):
    xValues = x_values(results)
    yValues = y_values(results)
    
    plt.plot(xValues, yValues)
    plt.xticks(rotation = 90)
    plt.show()


def x_values(results):
    values = []
    for result in results:
        values.append(result.date)
    
    return values

def y_values(results):
    values = []
    for result in results:
        values.append(result.balance)
    
    return values
