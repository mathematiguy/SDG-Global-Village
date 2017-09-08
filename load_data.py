import numpy as np
import pandas as pd

indicators_by_topic = pd.read_csv("data/indicators_by_topic.csv", 
								  sep = "\t", encoding = "utf-8")

topics = (indicators_by_topic.topic
			.sort_values()
			.unique())

simple_wiki = pd.read_csv("data/simple_wiki.csv")