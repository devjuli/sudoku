#Finds weights for each number given an image and the positions of each numbers. 0's are used to represent empty spaces.

from PIL import Image
import numpy as np
import Neuron



#Get's positions including 0's

def get_positions():
    positions = []
    for i in range(10):
        ith_position = []
        for j in range(len(sudoku)):
            if int(sudoku[j]) == i:
                ith_position.append(j)
        positions.append(ith_position)
    return positions

def get_num(img,numpos):
    data = list(img.getdata())
    numbervals = []
    dat = []
    for i in range(numpos//9 * 111,numpos//9 * 111 + 111):
        for j in range((numpos)%9*78, (numpos)%9*78+78):
            numbervals.append(data[i*img.width+j][0])
            dat.append(data[i*img.width+j])
    img2 = Image.new("RGB", (78,111), "white")
    img2.putdata(dat)
    img2.show()
    return numbervals

def get_labels(num):
    #Get positions of num without 0's
    positions = []
    sdk = sudoku.replace("0","")
    for i in range(len(sdk)):
        if int(sdk[i]) == num:
            positions.append(i)
    #Set labels to be 1 at positions of num
    labels = [0] * len(sdk)
    for position in positions:
        labels[position] = 1

    return labels

def greatest(li):
    greatest = 0
    waschanged = False
    for i in li:
        if(i> greatest):
            greatest = i
            waschanged = True
    if waschanged: return li.index(greatest) +1
    else: return 0

#Solves sudoku by brute force

def solve(sudoku):
  emptypos = sudoku.find("0")
  if emptypos == -1:
    return sudoku
  not_num = set()
  for j in range(81):
    if emptypos//9 == j//9 or emptypos%9 == j%9 or (emptypos//27 == j//27 and emptypos%9//3 == j%9//3) :
      not_num.add(sudoku[j])
  for num in "123456789":
    if num not in not_num:
      solution = solve(sudoku[:emptypos]+num+sudoku[emptypos+1:])
      if solution: return solution
  return False


def analyze(f,sudoku):
    #initialize
    img = Image.open(f)
    positions = get_positions()

    #create and typecast X's and y's

    numbers = []
    for i in range(1,10):
        for j in range(len(positions[i])):
            numbers.append(get_num(img,positions[i][j]))

    ys = [get_labels(i) for i in range(10)]
    X = np.array(numbers)
    #Setup and train "Neurons"

    ns = [Neuron.Neuron(n_iter=1000,eta=0.001) for i in range(10)]
    for i in range(1,10):
        ns[i].fit(X,ys[i])




    #Test on Training set
    #TODO: SPLIT TRAINING FROM TESTING DATA IN ORDER TO AVOID OVERFITTING!!!
    #TODO: ADD PREDICTIONS FOR POSITIONS OF 0's

    prediction = ""
    for i in range(len(sudoku)-len(positions[0])):
        preds = []
        for j in range(1,10):
            preds.append(ns[j].net_input(X[i]))
        print(preds)
        prediction += str(greatest(preds))

    #Print out results

    print(prediction)
    print(ys[7])

if __name__ == "__main__":
    sudoku = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    analyze("imgpsh_fullsize.jpg",sudoku)
