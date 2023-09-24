import numpy as np
import pandas as pd

def download_UCI(dataset_name, **kwargs):
	#divided in train/test
	if dataset_name in ["adult","bupa","image","monks-1","monks-2","monks-3","poker","thyroid"]:		
		data = download_UCI_divided(dataset_name)
		
	#not divided in train/test
	elif dataset_name in ["australian","breast-cancer-wisconsin","car","cleveland",
										"covtype","crx","EEG%20Eye%20State","german","glass",
										"haberman","heart","hepatitis","ionosphere","iris","sonar"]:
		data = download_UCI_united(dataset_name)
	else:
		print("IMPORT FOR ", dataset_name, "NOT ALREADY DEFINED")

	return data

def download_UCI_united(dataset_name, **kwargs):
	url = "http://archive.ics.uci.edu/ml/machine-learning-databases/"

	if dataset_name=="german":
		load_data = pd.read_csv(url + "statlog/" + dataset_name + "/" + dataset_name +".data-numeric", header=None, sep="\s+")
	elif dataset_name=="australian":
		load_data = pd.read_csv(url + "statlog/" + dataset_name + "/" + dataset_name +".dat", header=None, sep="\s+")
	elif dataset_name=="covtype":
		load_data = pd.read_csv(url + dataset_name + "/" + dataset_name + ".data.gz", header=None)
	elif dataset_name=="cleveland":
		load_data = pd.read_csv(url + "heart-disease/processed." + dataset_name + ".data", header=None)
	elif dataset_name=="crx":
		load_data = pd.read_csv(url + "credit-screening/" + dataset_name + ".data", header=None)
	elif dataset_name=="EEG%20Eye%20State":
		load_data = pd.read_csv(url + "00264/" + dataset_name + ".arff", header=None, skiprows=19)
	elif dataset_name=="heart":
		load_data = pd.read_csv(url + "statlog/" + dataset_name + "/" + dataset_name +".dat", header=None, sep="\s+")
	elif dataset_name=="sonar":
		load_data = pd.read_csv(url + "undocumented/connectionist-bench/" + dataset_name + "/" + dataset_name +".all-data", header=None)
	else:
		load_data = pd.read_csv(url + dataset_name + "/" + dataset_name + ".data", header=None)

	if dataset_name=="car":
		for col in load_data.columns[:-1]:
			load_data[col] = load_data[col].astype("category").cat.codes
	elif dataset_name=="breast-cancer-wisconsin":
		load_data.drop(0,axis=1,inplace=True)
		load_data.loc[load_data[6]=="?",6] = -1 #replace missing values
		load_data[6] = load_data[6].astype(int)
	elif dataset_name=="crx":
		app = np.where(load_data=="?")
		for i,j in zip(app[0],app[1]):
			load_data.iloc[i,j] = -1 #replace missing values
		for col in [0,3,4,5,6,8,9,11,12]:
			load_data[col] = load_data[col].astype("category").cat.codes
	elif dataset_name=="cleveland":
		for col in load_data.columns[:-1]:
			if load_data[col].dtype != float:
				load_data[col] = load_data[col].astype("category").cat.codes
	elif dataset_name=="glass":
		load_data = load_data.iloc[:,1:] #remove ID column
	elif dataset_name=="hepatitis":
		app = np.where(load_data=="?")
		for i,j in zip(app[0],app[1]):
			load_data.iloc[i,j] = -1 #replace missing values

	if dataset_name=="hepatitis": #class is first column
		x = load_data.iloc[:,1:].to_numpy()
		y = load_data.iloc[:,:1].to_numpy()
	else:
		x = load_data.iloc[:,:-1].to_numpy()
		y = load_data.iloc[:,-1:].to_numpy()

	if dataset_name=="breast-cancer-wisconsin":
		y = (y==4)*1
	elif dataset_name=="haberman":
		y = (y==2)*1

	return {"x":x, "y":y}

def download_UCI_divided(dataset_name):
	url = "http://archive.ics.uci.edu/ml/machine-learning-databases/"

	if "monks" in dataset_name:
		train_data = pd.read_csv(url + "monks-problems/" + dataset_name + ".train",sep=" ", names = ["c","a1","a2","a3","a4","a5","a6","d"])
		train_data.set_index("d", inplace=True)
		test_data = pd.read_csv(url + "monks-problems/" + dataset_name + ".test",sep=" ", names = ["c","a1","a2","a3","a4","a5","a6","d"])
		test_data.set_index("d", inplace=True)
	elif dataset_name == "poker":
		train_data = pd.read_csv(url + dataset_name + "/poker-hand-training-true.data", header=None)
		test_data = pd.read_csv(url + dataset_name + "/poker-hand-testing.data", header=None)
		#if redefine_class: #change class to delete noise
		#train_data.iloc[:,0] = monk_rules_3(train_data)*1
	elif dataset_name == "image":
		train_data = pd.read_csv(url + dataset_name + "/segmentation"+".data", skiprows=2)
		test_data = pd.read_csv(url + dataset_name + "/segmentation"+".test", skiprows=2)
	elif dataset_name=="bupa":
		load_data = pd.read_csv(url + "liver-disorders" + "/" + dataset_name + ".data", header=None)
		train_data = load_data.loc[load_data.iloc[:,-1]==1,:].iloc[:,:-1]
		test_data = load_data.loc[load_data.iloc[:,-1]==2,:].iloc[:,:-1]
	elif dataset_name=="adult":
		train_data = pd.read_csv(url + dataset_name + "/" + dataset_name + ".data", header=None)
		for col in train_data.columns[:-1]:
			if train_data[col].dtype != int:
				train_data[col] = train_data[col].astype("category").cat.codes
		test_data = pd.read_csv(url + dataset_name + "/" + dataset_name + ".test", header=None, skiprows=1)
		test_data.iloc[:,-1] = test_data.iloc[:,-1].apply(lambda x: x[:-1]) #delete last dot char
		for col in test_data.columns[:-1]:
			if test_data[col].dtype != int:
				test_data[col] = test_data[col].astype("category").cat.codes
	elif dataset_name=="thyroid":
		train_data = pd.read_csv(url + dataset_name + "-disease/ann-train.data", sep=" ",header=None).iloc[:,:-2]
		test_data = pd.read_csv(url + dataset_name + "-disease/ann-test.data", sep=" ",header=None).iloc[:,:-2]

	#divide x, y
	if "monks" in dataset_name:	#class is first column
		train_x = train_data.iloc[:,1:].to_numpy()
		train_y = train_data.iloc[:,:1].to_numpy()
		test_x = test_data.iloc[:,1:].to_numpy()
		test_y = test_data.iloc[:,:1].to_numpy()
	elif dataset_name == "image": #class is index
		train_x = train_data.to_numpy()
		train_y = train_data.index.to_numpy()[:,None]
		test_x = test_data.to_numpy()
		test_y = test_data.index.to_numpy()[:,None]
	else: #class is last column
		train_x = train_data.iloc[:,:-1].to_numpy()
		train_y = train_data.iloc[:,-1:].to_numpy()
		test_x = test_data.iloc[:,:-1].to_numpy()
		test_y = test_data.iloc[:,-1:].to_numpy()

	return {"train_x":train_x, "test_x":test_x, "train_y":train_y, "test_y":test_y}