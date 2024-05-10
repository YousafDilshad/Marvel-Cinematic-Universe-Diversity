#Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import seaborn as sns

#Importing data
mcu_data = pd.read_csv("mcu_filtered_final.csv")

#Assuming mcu_data is your DataFrame
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
plt.show()

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
plt.savefig('top_20_characters_race_specific_colors.png')  # Save the figure as an image file
plt.show()



#Scatterplots for Gender Diversity by Box Office and Critical Success
mcu_final_data = pd.read_csv('mcu_box_office_with_diversity.csv')

#Converting to numeric
mcu_final_data['worldwide_box_office'] = pd.to_numeric(mcu_final_data['worldwide_box_office'].str.replace(',', ''), errors='coerce')


# Create a custom palette from red to yellow (reversed)
custom_palette = sns.color_palette("autumn", as_cmap=True)

# Create the scatter plot
plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(x='gender_diversity', y='movie_title', size='worldwide_box_office', hue='audience_score',
                          palette=custom_palette, sizes=(50, 500), size_order=mcu_final_data['worldwide_box_office'].sort_values().unique(),
                          data=mcu_final_data)

# Reverse the y-axis
plt.gca().invert_yaxis()

# Set labels and title
scatter.set_xlabel('Gender Diversity')
scatter.set_ylabel('Movie Title')
scatter.set_title('Gender Diversity vs. Movie Title with Box Office Size and Audience Score')

# Create separate legends for size and color
scatter.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Audience Score', markerscale=0.5)
plt.legend(title='Legend', loc='center left', bbox_to_anchor=(1, 0.25), markerscale=0.5)

# Show plot
plt.tight_layout()
plt.show()
plt.savefig('gender_diversity_scatterplot.png')

# Create the scatter plot
plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(x='racial_diversity', y='movie_title', size='worldwide_box_office', hue='audience_score',
                          palette=custom_palette, sizes=(50, 500), size_order=mcu_final_data['worldwide_box_office'].sort_values().unique(),
                          data=mcu_final_data)

# Reverse the y-axis
plt.gca().invert_yaxis()

# Set labels and title
scatter.set_xlabel('Racial Diversity')
scatter.set_ylabel('Movie Title')
scatter.set_title('Racial Diversity vs. Movie Title with Box Office Size and Audience Score')

# Create separate legends for size and color
scatter.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Audience Score', markerscale=0.5)
plt.legend(title='Legend', loc='center left', bbox_to_anchor=(1, 0.25), markerscale=0.5)

# Show plot
plt.tight_layout()
plt.show()
plt.savefig('racial_diversity_plot.png')