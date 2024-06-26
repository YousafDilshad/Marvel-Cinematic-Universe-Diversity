#Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import seaborn as sns
plt.rcParams['figure.dpi'] = 300


#Importing data
mcu_data = pd.read_csv("mcu_filtered_final.csv")

#Selecting top 20 characters
top_20_characters = mcu_data.sort_values('total_time_mins', ascending=False).head(20)

#Plot for gender
plt.figure(figsize=(12, 8))
bars_gender = plt.bar(top_20_characters['character_name'], top_20_characters['total_time_mins'], color=top_20_characters['gender'].map({'Male': 'red', 'Female': 'orange'}))
plt.xticks(rotation=45, ha='right')
plt.xlabel('Character Name')
plt.ylabel('Total Screen Time (minutes)')
plt.title('Top 20 Characters by Total Screen Time (Color-coded by Gender)')

#Create custom legend for gender
legend_elements_gender = [Patch(facecolor='red', label='Male'), Patch(facecolor='orange', label='Female')]
plt.legend(handles=legend_elements_gender, title='Gender', loc='upper right')

#Add number labels to bars for gender
for i, bar in enumerate(bars_gender):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10, str(int(bar.get_height())), ha='center', va='bottom')

plt.tight_layout()
plt.savefig('top_20_characters_gender.png')  # Save the figure as an image file

#Define colors for each race category
race_colors = {
    'Caucasian': 'red',
    'Alien': 'orange',
    'Asian': 'yellow',
    'Black': 'brown'
}

#Plot for race
plt.figure(figsize=(12, 8))
bars_race = plt.bar(top_20_characters['character_name'], top_20_characters['total_time_mins'], color=top_20_characters['race'].map(race_colors))
plt.xticks(rotation=45, ha='right')
plt.xlabel('Character Name')
plt.ylabel('Total Screen Time (minutes)')
plt.title('Top 20 Characters by Total Screen Time (Color-coded by Race)')

#Create custom legend for race
from matplotlib.patches import Patch
legend_elements_race = [Patch(facecolor=color, label=race) for race, color in race_colors.items()]
plt.legend(handles=legend_elements_race, title='Race', loc='upper right')

#Add number labels to bars for race
for i, bar in enumerate(bars_race):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10, str(int(bar.get_height())), ha='center', va='bottom')

plt.tight_layout()
plt.savefig('top_20_characters_race.png')  # Save the figure as an image file

#Scatterplots for Gender Diversity by Box Office and Critical Success
mcu_final_data = pd.read_csv('mcu_box_office_with_diversity.csv')

#Converting to numeric
mcu_final_data['worldwide_box_office'] = pd.to_numeric(mcu_final_data['worldwide_box_office'].str.replace(',', ''), errors='coerce')

#Create a custom palette from red to yellow (reversed)
custom_palette = sns.color_palette("autumn", as_cmap=True)

#Create the scatter plot for gender diversity
plt.figure(figsize=(12, 8))
scatter_gender = sns.scatterplot(x='gender_diversity', y='movie_title', size='worldwide_box_office', hue='audience_score',
                                 palette=custom_palette, sizes=(50, 500), size_order=mcu_final_data['worldwide_box_office'].sort_values().unique(),
                                 data=mcu_final_data)
plt.gca().invert_yaxis()
scatter_gender.set_xlabel('Gender Diversity')
scatter_gender.set_ylabel('Movie Title')
scatter_gender.set_title('Gender Diversity with Box Office Revenue and Audience Score')
scatter_gender.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Audience Score', markerscale=0.5)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.25), markerscale=0.5)
plt.tight_layout()
plt.savefig('scatter_gender_diversity.png')

#Create the scatter plot for racial diversity
plt.figure(figsize=(12, 8))
scatter_race = sns.scatterplot(x='racial_diversity', y='movie_title', size='worldwide_box_office', hue='audience_score',
                               palette=custom_palette, sizes=(50, 500), size_order=mcu_final_data['worldwide_box_office'].sort_values().unique(),
                               data=mcu_final_data)
plt.gca().invert_yaxis()
scatter_race.set_xlabel('Racial Diversity')
scatter_race.set_ylabel('Movie Title')
scatter_race.set_title('Racial Diversity with Box Office Revenue and Audience Score')
scatter_race.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Audience Score', markerscale=0.5)
plt.legend( loc='center left', bbox_to_anchor=(1, 0.25), markerscale=0.5)
plt.tight_layout()
plt.savefig('scatter_racial_diversity.png')


#Convert movie_title to a categorical variable for proper ordering
mcu_final_data['movie_title'] = pd.Categorical(mcu_final_data['movie_title'], categories=mcu_final_data['movie_title'].unique(), ordered=True)

#Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 6))

#Plot racial diversity
sns.lineplot(x='movie_title', y='racial_diversity', data=mcu_final_data, color='red', label='Racial Diversity', ax=ax)

#Plot gender diversity
sns.lineplot(x='movie_title', y='gender_diversity', data=mcu_final_data, color='orange', label='Gender Diversity', ax=ax)

#Set labels and title
ax.set(xlabel='Movie Title', ylabel='Diversity', title='Trend of Racial and Gender Diversity Over Movies')

#Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

#Add lines for mcu_phase changes
last_phase = mcu_final_data['mcu_phase'].iloc[0]
for i, phase in enumerate(mcu_final_data['mcu_phase']):
    if phase != last_phase:
        plt.axvline(x=i, color='gray', linestyle='--', linewidth=0.5)
        last_phase = phase

#Saving Plot
plt.legend()
plt.tight_layout()
plt.savefig('diversity_lineplot.png')

#Create a custom palette from red to yellow (reversed)
custom_palette = sns.color_palette("autumn", as_cmap=True)

#Create the scatter plot for gender diversity
fig, axes = plt.subplots(1, 2, figsize=(18, 8), sharey=True)
scatter_gender = sns.scatterplot(ax=axes[1], x='gender_diversity', y='movie_title', size='worldwide_box_office', hue='audience_score',
                                 palette=custom_palette, sizes=(50, 500), size_order=mcu_final_data['worldwide_box_office'].sort_values().unique(),
                                 data=mcu_final_data)

scatter_gender.set_xlim(0, 100)
scatter_gender.set_xlabel('Gender Diversity')
scatter_gender.set_ylabel('Movie Title',ha='right')
scatter_gender.set_title('Gender Diversity vs. Movie Title with Box Office Size and Audience Score')
scatter_gender.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Audience Score', markerscale=0.5)
scatter_gender.legend(loc='center left', bbox_to_anchor=(1, 0.25), markerscale=0.5)
scatter_gender.invert_yaxis()  # Invert the y-axis

#Create the scatter plot for racial diversity (flipped horizontally)
scatter_race = sns.scatterplot(ax=axes[0], x='racial_diversity', y='movie_title', size='worldwide_box_office', hue='audience_score',
                               palette=custom_palette, sizes=(50, 500), size_order=mcu_final_data['worldwide_box_office'].sort_values().unique(),
                               data=mcu_final_data)
scatter_race.invert_xaxis()
scatter_race.set_xlim(100, 0)
scatter_race.set_xlabel('Racial Diversity')
scatter_race.set_ylabel('')
scatter_race.set_title('Racial Diversity vs. Movie Title with Box Office Size and Audience Score')
scatter_race.legend_.remove()
scatter_race.invert_yaxis()  # Invert the y-axis

#Create a mapping of movie titles to y-axis positions
title_positions = {title: i for i, title in enumerate(mcu_final_data['movie_title'])}

#Add lines for mcu_phase changes
phase_positions = mcu_final_data.groupby('mcu_phase')['movie_title'].last().map(title_positions).tolist()
for pos in phase_positions:
    for ax in axes:
        ax.axhline(y=pos, color='gray', linestyle='--', linewidth=1)
        
plt.tight_layout()

plt.savefig('scatter_plots_side_by_side.png')