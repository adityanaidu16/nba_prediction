from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import numpy as np

def userInput(regr):
    print("FOR HOME TEAM INPUT THE FOLLOWING:")
    fg = int(input("FG:"))
    fga = int(input("FGA:"))
    fg3 = int(input("FG3:"))
    fg3a = int(input("FG3A:"))
    ft = int(input("FT:"))
    fta = int(input("FTA:"))
    orb = int(input("ORB:"))
    drb = int(input("DRB:"))
    ast = int(input("AST:"))
    stl = int(input("STL:"))
    blk = int(input("BLK:"))
    tov = int(input("TOV:"))
    pf = int(input("PF:"))
    pts = int(input("PTS:"))
    wins = int(input("WINS:"))
    gp = int(input("GAMES PLAYED:"))
    print("\nFOR AWAY TEAM INPUT THE FOLLOWING:")
    oppfg = int(input("FG:"))
    oppfga = int(input("FGA:"))
    oppfg3 = int(input("FG3:"))
    oppfg3a = int(input("FG3A:"))
    oppft = int(input("FT:"))
    oppfta = int(input("FTA:"))
    opporb = int(input("ORB:"))
    oppdrb = int(input("DRB:"))
    oppast = int(input("AST:"))
    oppstl = int(input("STL:"))
    oppblk = int(input("BLK:"))
    opptov = int(input("TOV:"))
    opppf = int(input("PF:"))
    opppts = int(input("PTS:"))
    oppwins = int(input("WINS:"))
    oppgp = int(input("GAMES PLAYED:"))

    score = regr.predict([[fg,fga,fg3,fg3a,ft,fta,orb,drb,ast,stl,blk,tov,pf,pts,wins,gp,oppfg,oppfga,oppfg3,oppfg3a,oppft,oppfta,opporb,oppdrb,oppast,oppstl,oppblk,opptov,opppf,opppts,oppwins,oppgp]])

    print(int(score[0][0]), end='')
    print('-', end='')
    print(int(score[0][1]))

def main():
    stats = pd.read_csv('nbascrape.csv')

    X = stats[['fg', 'fga', 'fg3', 'fg3a', 'ft', 'fta', 'orb', 'drb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'wins', 'gp', 'oppfg', 'oppfga', 'oppfg3', 'oppfg3a', 'oppft', 'oppfta', 'opporb', 'oppdrb', 'oppast', 'oppstl', 'oppblk', 'opptov', 'opppf', 'opppts', 'oppwins', 'oppgp']]
    y = stats[['finalpoints', 'oppfinalpoints']]

    testsize = 500
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=testsize, random_state=1)

    # identify outliers in the training dataset
    iso = IsolationForest(contamination=0.1)
    yhat = iso.fit_predict(X_train)

    # train without outliers
    mask = yhat != -1
    X_train, Y_train = X_train.iloc[mask, :], Y_train.iloc[mask]


    regr = MLPRegressor(random_state=0, max_iter=500).fit(X_train, Y_train)

    #expected_y  = Y_test
    #predicted_y = regr.predict(X_test)
    #print(metrics.r2_score(expected_y, predicted_y))
    #print(metrics.mean_squared_error(expected_y, predicted_y))

    testAccuracy(regr, testsize, X_test, Y_test)

    userInput(regr)

def testAccuracy(regr, testsize, X_test, Y_test):
    correctwinners = 0
    closescore = 0
    # find probability of winner
    for row in range(testsize):
        arr = (X_test.iloc[row]).to_numpy()
        arr_2d = np.reshape(arr, (1,32))
        prediction = regr.predict(arr_2d)

        # find probabilty of score within 8-pt range
        if (abs(prediction[0][0] - Y_test.iloc[row][0]) < 10 and abs(prediction[0][1] - Y_test.iloc[row][1]) < 10):
            closescore+=1

        if (prediction[0][0] > prediction[0][1] and Y_test.iloc[row][0] > Y_test.iloc[row][1]):
            correctwinners += 1
        elif (prediction[0][0] < prediction[0][1] and Y_test.iloc[row][0] < Y_test.iloc[row][1]):
            correctwinners += 1
        else:
            #print(prediction)
            #print(Y_test.iloc[row])
            pass
    print("{0:.0%}".format(correctwinners/testsize) + " Accuracy in predicting winner")
    print("{0:.0%}".format(closescore/testsize) + " Accuracy in predicting relative score")


if __name__ == '__main__':
    main()