import numpy as np
import pandas as pd

sdg_data = pd.read_csv("data/sdg_data.csv", low_memory = False)

selected_indicators = pd.read_csv("data/selected_indicators.csv")

image_data = pd.read_csv("data/search_results.csv")

country_data = pd.read_csv("data/country_metadata.csv")

indicators_by_topic = pd.read_csv("data/indicators_by_topic.csv", 
                                  sep = "\t", encoding = "utf-8")

topics = (indicators_by_topic.topic
          .sort_values()
          .unique())

simple_wiki = pd.read_csv("data/simple_wiki.csv")

# set percentage bounds and text
perc_data = pd.DataFrame(
    {'lower_bound': [0.00, 0.05, 0.34, 0.68, 0.95, 1.00],
     'upper_bound': [0.05, 0.34, 0.68, 0.95, 1.00, np.infty],
     'text'  : ["almost none","some","about half",
                "many","almost all", "all"]})

# set comparison bounds and text
comp_data = pd.DataFrame(
    {'lower_bound': [-np.infty, -1.0, -0.2, -0.1, 0.1, 0.2, 1.0],
     'upper_bound': [-1, -0.2, -0.1,  0.1, 0.2, 1.0, np.infty],
     'text'  : ["very much lesser", "much lesser", "lesser", 
                "about the same", "greater", "much greater", 
                "very much greater"]})