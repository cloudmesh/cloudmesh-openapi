import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import explained_variance_score

def decisiontree_model():
	df =pd.read_csv("https://raw.githubusercontent.com/cybertraining-dsc/fa20-523-327/main/project/dataset/USvideos.csv")

	#turn boolean labels into 1/0
	df["comments_disabled"] = df["comments_disabled"].astype(int)
	df["ratings_disabled"] = df["ratings_disabled"].astype(int)
	df["video_error_or_removed"] = df["video_error_or_removed"].astype(int)

	#clean publish and date
	df['publish_time'] = pd.to_datetime(df["publish_time"], format = '%Y-%m-%d')
	df['trending_date'] = pd.to_datetime(df["trending_date"], format = '%y.%d.%m')

	#create new columns
	df['td_month'] = df['trending_date'].dt.month
	df['td_day'] = df['trending_date'].dt.day
	df['td_year'] = df['trending_date'].dt.year
	df['p_month'] = df['publish_time'].dt.month
	df['p_day'] = df['publish_time'].dt.day
	df['p_year'] = df['publish_time'].dt.year

	#drop fields that cannot be ran through model or relevant
	x1 = df.drop(['trending_date','video_id', 'title', 'channel_title', 'publish_time', 'tags',
	             'thumbnail_link', 'description'], axis = 'columns')

	#model
	x1 = df[['category_id', 'likes', 'dislikes', 'comment_count', 
	         'comments_disabled', 'ratings_disabled', 'video_error_or_removed', 'td_month',
	         'td_day', 'td_year', 'p_month', 'p_day', 'p_year']]
	y1 = df["views"]
	x1_train, x1_test, y1_train, y1_test = train_test_split(x1, y1, test_size = 0.2, random_state = 68)

	#decision tree
	DecisionTree_Class_Model = DecisionTreeRegressor()

	DecisionTree_Class_Model.fit(x1_train, y1_train)
	y_pred1 = DecisionTree_Class_Model.predict(x1_test)

	score = print("The score of this model is:", explained_variance_score(y1_test, y_pred1))
 

	return score