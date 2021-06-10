# NBA Final Score Prediction


### DESCRIPTION
Predicts final score of an NBA game based on first quarter statistcs with MLP regression.

### WEB SCRAPER
To begin, I created a python web scraper to get the necessary statistics from [www.basketball-reference.com/](https://www.basketball-reference.com/). I began by collecting the ids (aka csk) of every game from october 2016 to march 2021--over 5,000 games! Next, I accessed the box score webpages of every game with the ids that I collected earlier and parsed it using BeautifulSoup. Finally, I collected the basic box score stats after the first quarter as well as the final score and inserted these  into a csv file.

### MLP REGRESSION (NEURAL NETWORK)
After creating the csv file with all of the statistics I needed, I put it to use, using [MLP regression](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html) from the scikit learn neural network. First, I split the data into inputs, which were all of the first quarter statistics, and the outputs, which was the final score. Next, I split the data with [test_train_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) before identifying outliers in the training data with [IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) and removing them. I finally trained the MLP Regressor and tested it, being able to accurately predict the winner 70% of the time and the relative score (within 10 points) 45% of the time.

### DEMO
Lets test the recent game 2 of the Eastern Conference Semifinals: Atlanta Hawks @ Philadelphia 76ers. After entering the first quarter stats 
and regular season wins from each team, we get a prediction of 115-104, not too far off of the actual final score 118-102.

<img src="demo.gif" width="750">  <img src="demo.PNG" width="250">
