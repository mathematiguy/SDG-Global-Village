import random
import numpy as np
import pandas as pd

from load_data import *

def summarise_indicators(user_name, user_sex, user_country, target_country, target_topic):

    summary_text = []

    def get_country_nickname(country, country_data):
        '''Returns the nickname of a country using country_data'''
        return country_data.loc[
                    country_data.country == country,
                    'nickname'].iloc[0]

    user_country_nickname = get_country_nickname(user_country, country_data)

    target_country_nickname = get_country_nickname(target_country, country_data)

    # derive child name and population from user data
    country_child_name = country_data.loc[
        country_data.country == target_country, user_sex + "_name"]\
        .iloc[0]

    target_population = country_data.loc[
        country_data.country == target_country, 'population']\
        .iloc[0]

    def select_indicators(selected_indicators, target_country, target_topic):

        # use user data to select indicators
        indicator_selection = selected_indicators[
            selected_indicators.topic == target_topic]

        # select the indicator with the highest priority
        indicator_selection = indicator_selection[
            indicator_selection.priority == indicator_selection.priority.min()]

        # use user data to subset sdg_data
        sdg_selection = sdg_data[
            np.logical_and(
                sdg_data.country == target_country,
                sdg_data.topic == target_topic)]

        if len(sdg_selection) > 0:
        	# there is data, so continue on to merge
            # subset sdg_selection based on selected indicators
            sdg_selection = sdg_selection.merge(indicator_selection, 
                on = ['goal', 'priority', 'indicator_id', 'topic', 
                      'series', 'location', 'age_group', 'unit', 'sex', 
                      'value_type'],
                how = 'inner')

        return indicator_selection, sdg_selection

    indicator_selection, sdg_selection = select_indicators(selected_indicators, 
        target_country, target_topic)

    if len(sdg_selection) == 0:
        summary_text += [
            "Hi {}, I am interested in {} too.".format(
                user_name, target_topic),
            "I hope that {} and {} can be friends.".format(
                user_country_nickname, target_country_nickname)]
        return ' '.join(summary_text)

    else:
        perc_text = perc_data.loc[
            np.logical_and(
                sdg_selection.value.max() >= perc_data.lower_bound,
                sdg_selection.value.max() < perc_data.upper_bound),
            'text'].iloc[0]

        comparison_text = comp_data.loc[
            np.logical_and(
                sdg_selection.value.max() >= comp_data.lower_bound,
                sdg_selection.value.max() < comp_data.upper_bound),
            'text'].iloc[0]

        summary_text.append('Hi {}! My name is {}.\n'\
                    .format(user_name, country_child_name))

        def millify(n):
            '''
            Converts a number into human readable text.
            e.g. 12345 -> 12 thousand
            '''
            millnames = ['', 'thousand', 'million', 'billion', 
            			 'trillion']
            n = float(n)
            millidx = max(0,
                min(len(millnames)-1,
                int(np.floor(0 if n == 0 else np.log10(abs(n))/3))))

            return '{:.0f} {}'.format(n / 10**(3 * millidx), 
                millnames[millidx])

        summary_text.append(
            '{}, did you know that {} people live in {}?'\
            .format(
                user_name,
                millify(target_population),
                target_country_nickname))

        percent_value = sdg_selection.loc[
            sdg_selection.year == sdg_selection.year.max(),
            'value'].iloc[0] * 100

        summary_text += [
             '{}, did you know that in {} in {:d},'.format(
                user_name, target_country_nickname, sdg_selection.year.max()),

             '{} ({:.1f}%) {}'.format(
                perc_text, percent_value,
                indicator_selection.indicator_text.iloc[0]
                ),
            ]

        if len(sdg_selection.year.unique()) > 1:
        	summary_text.append('This is {} as in {}'.format(
        		comparison_text, sdg_selection.year.min()))

        return ' '.join(summary_text)

# uncomment this block for testing

# Get user data
# user_name = "Sam"
# user_sex = "female"

# # select user country at random (for testing)
# user_country = country_data.country.sample().iloc[0]

# # select target country at random (for testing)
# target_country = country_data.country.sample().iloc[0]

# # select topic at random (for testing)
# target_topic = random.choice(sdg_data.topic.unique())

# # select user country at random (for testing)
# user_country = "Saint Kitts and Nevis"

# # select target country at random (for testing)
# target_country = "Jamaica"

# # select topic at random (for testing)
# target_topic = "plants"

# print("User data:", user_name, user_sex, user_country, target_country, target_topic)

# print(summarise_indicators(user_name, user_sex, user_country, target_country, target_topic))