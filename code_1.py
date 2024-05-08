import pandas as pd
import numpy as np
import re
from datetime import datetime
from plotnine import ggplot, aes, geom_point, labs, scale_x_continuous, theme_minimal, element_text, scale_color_gradient, scale_size, geom_col, geom_text, position_dodge, scale_fill_manual, scale_color_manual
from plydata import define, if_else, mutate, summarise
from plydata.tidy import gather

# Setting Directory and Importing Data
data_dir = "C:/Users/Yousaf Dilshad/Desktop/Syracuse University/Spring/Information Visualization/Final Project Data/Data/"
mcu1 = pd.read_csv(data_dir + "mcu_box_office.csv")
mcu2 = pd.read_csv(data_dir + "meu_screentime_added_variables.csv", dtype=str)

# Inspecting Data
print(mcu1.info())

# Changing character_name to alternate_name where applicable
mcu2['character_name'] = np.where(mcu2['alternate_name'] != "", mcu2['alternate_name'], mcu2['character_name'])
mcu2 = mcu2.drop(columns=['alternate_name'])

# Standardizing Race Data
mcu2['Race'] = mcu2['Race'].replace({'African.American': 'Black', 'African': 'Black',
                                     'Unknown|Alien|Skrull|Kree': 'Unknown/Alien'}, regex=True)

# Standardizing Movie Names
mcu1['movie_title'] = mcu1['movie_title'].str.replace("-", " ").str.replace("\\.", ":")
mcu2.columns = mcu2.columns.str.replace("\\.\\.", ":").str.replace("\\.", " ").str.strip()
mcu2.loc[mcu2['movie_title'] == "Avengers: Endgame", 'movie_title'] = "Avengers: End Game"
mcu2.loc[mcu2['movie_title'] == "Spider Man: Far from Home", 'movie_title'] = "Spider Man: Far From Home"

# Keeping only Movies Listed in mcu1
common_columns = mcu2.columns.intersection(mcu1['movie_title'])
mcu2 = mcu2[['movie_title'] + list(common_columns)]

# Converting Times
def convert_time(time_str):
    time_str = re.sub("^x:00$", "", time_str)
    time_parts = time_str.split(":")
    if len(time_parts) == 3:
        hours, minutes, seconds = map(int, time_parts)
        total_minutes = hours * 60 + minutes + seconds / 60
    else:
        minutes, seconds = map(int, time_parts)
        total_minutes = minutes + seconds / 60
    return total_minutes

for col in mcu2.columns[1:28]:
    mcu2[col] = mcu2[col].str.replace("^x:00$", "").str.replace("^(\\d{2}):(\\d{2}):\\d{2}$", "\\1:\\2")
    mcu2[col] = mcu2[col].apply(convert_time)

mcu2['total_time_mins'] = mcu2.iloc[:, 1:28].sum(axis=1)

mcu2 = mcu2[mcu2['total_time_mins'] != 0]

mcu2.to_csv("mcu2_modified.csv", index=False)

# Top 10 Characters
top_10 = mcu2[['character_name', 'total_time_mins']].sort_values(by='total_time_mins', ascending=False).head(10)
print(top_10)

# Aggregating by Gender
gender_agg = mcu2.groupby('Gender').agg('sum')['Iron Man'].reset_index()
print(gender_agg)

# Aggregating by Race
race_agg = mcu2.groupby('Race').agg('sum').reset_index()
race_agg.columns = ['Race'] + ['race_' + col.lower() for col in race_agg.columns[1:]]
print(race_agg)

# Merging mcu1 with aggregated_race
merged_data_race = pd.merge(mcu1, race_agg, on="movie_title", how="left")

# Merging the result with aggregated_gender
mcu_final = pd.merge(merged_data_race, gender_agg, on="movie_title", how="left")

# Sorting by date
mcu_final['release_date'] = pd.to_datetime(mcu_final['release_date'], format="%m/%d/%Y")
mcu_final = mcu_final.sort_values(by='release_date').reset_index(drop=True)

mcu_final = mcu_final.drop(columns=['race_unknown.alien', 'gender_unknown'])

# Calculate gender diversity
mcu_final['gender_diversity'] = (mcu_final['gender_Female'] / (mcu_final['gender_Male'] + mcu_final['gender_Female'])) * 100

# Calculate racial diversity (non-Caucasian)
mcu_final['racial_diversity'] = ((mcu_final['race_Asian'] + mcu_final['race_Black'] + mcu_final['race_Middle.Eastern'] + mcu_final['race_Hispanic']) /
                                 (mcu_final['race_Caucasian'] + mcu_final['race_Asian'] + mcu_final['race_Black'] + mcu_final['race_Middle.Eastern'] + mcu_final['race_Hispanic'])) * 100

mcu_final.to_csv("mcu_final.csv", index=False)

# Creating plots
# Gender Diversity
(ggplot(mcu_final, aes(x='gender_diversity', y='movie_title', color='audience_score', size='worldwide_box_office'))
 + geom_point()
 + labs(x='Gender Diversity', y=None, title='Gender Diversity vs. Movie Title')
 + scale_x_continuous(limits=[0, 100])
 + theme_minimal()
 + theme(axis_text_y=element_text(hjust=0.5))
 + scale_color_gradient(low="yellow", high="red")
 + scale_size(range=[2, 10], limits=[200000000, 3000000000]))

# Racial Diversity
(ggplot(mcu_final, aes(x='racial_diversity', y='movie_title', color='audience_score', size='worldwide_box_office'))
 + geom_point()
 + labs(x='Racial Diversity', y=None, title='Racial Diversity vs. Movie Title')
 + scale_x_continuous(limits=[0, 100])
 + theme_minimal()
 + theme(axis_text_y=element_text(hjust=0.5))
 + scale_color_gradient(low="yellow", high="red")
 + scale_size(range=[2, 10], limits=[200000000, 3000000000]))

# Slicing Data
top_20_characters = (mcu2.assign(rank=mcu2['total_time_mins'].rank(ascending=False))
                     .query('rank <= 20')
                     .sort_values('total_time_mins', ascending=False))

