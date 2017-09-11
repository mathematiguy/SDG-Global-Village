from google import google, images
import numpy as np
import pandas as pd
import re
import hashlib
from urllib.parse import urlparse

data_dir = "../../data/"
countries = pd.read_csv(data_dir + "country_metadata.csv", encoding="ansi")
topics = pd.read_csv(data_dir + "topics.csv")
search_results = pd.read_csv(data_dir + "search_results.csv")

# search for both countries and regions
countries = np.unique(
	np.concatenate(
		[countries.nickname.unique(), 
		 countries.region_member_of.unique()]))

# setting default settings for image search
def reset_options():
	options = images.ImageOptions()
	options.color_type = 'color'
	options.license = 'f'
	options.larger_than = images.LargerThan.MP_12
	return options

def write_to_file(results, results_file):
	print("writing to file...")
	colnames = ['index', 'country', 'topic', 'query_name', 'query', 'link', 'hash', 'downloaded', 'domain', 'filename', 'filepath']
	result_df = pd.DataFrame(results, columns = colnames)
	result_df.to_csv(results_file, header = False, index = None)
	results = []
	return results

def hash_link(link):
    sha1 = hashlib.sha1()
    sha1.update(link.encode("utf-8"))
    return sha1.hexdigest()

def get_domain(link):
    domain = urlparse(link).hostname
    pattern = ['', 'co', 'ac', 'org', 'com', 'gov']
    pattern = "|".join(["[^\\.]+\\.%s\\.?[A-z]*$" % p for p in pattern])
    if domain is not None:
        search_result = re.search(pattern, domain)
        if search_result is not None:
            return search_result.group(0)

with open("search_results.csv", "a") as results_file:
	result_count = 0
	past_queries = list(search_results['query'].unique())
	results = []
	for i, country in enumerate(countries):
		for j, topic in topics.iterrows():
			options = reset_options()

			if 'face' in topic['query']:
				options.image_type = images.ImageType.FACE

			query = '{} {}'.format(country, topic['query'])

			result_count += 1

			if query in past_queries:
				continue

			query_name = "{} {}".format(country, topic['name'])

			print("Searching for: %s (%d out of %d)" \
					%(query, result_count, len(topics) * len(countries)))

			image_results = google.search_images(query)

			results += [
				{'index': image_result.index,
				 'country': country,
				 'topic': topic['name'],
				 'query_name': query_name,
				 'query': query,
				 'link': image_result.link,
				 'hash': hash_link(image_result.link),
				 'downloaded': False,
				 'domain': get_domain(image_result.link),
				 'filename': np.nan,
				 'filepath': np.nan,
				} for image_result in image_results]

			if result_count % 10 == 0:
				results = write_to_file(results, results_file)

	# write remaining results to file
	results = write_to_file(results, results_file)