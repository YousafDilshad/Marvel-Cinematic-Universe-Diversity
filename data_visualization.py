#Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch


# Importing data
mcu_data = pd.read_csv("mcu_filtered_final.csv")

# Assuming mcu_data is your DataFrame
top_20_characters = mcu_data.sort_values('total_time_mins', ascending=False).head(20)

# Plot for gender
plt.figure(figsize=(12, 8))
bars_gender = plt.bar(top_20_characters['character_name'], top_20_characters['total_time_mins'], color=top_20_characters['gender'].map({'Male': 'red', 'Female': 'orange'}))
plt.xticks(rotation=45, ha='right')
plt.xlabel('Character Name')
plt.ylabel('Total Screen Time (minutes)')
plt.title('Top 20 Characters by Total Screen Time (Color-coded by Gender)')

# Create custom legend for gender
legend_elements_gender = [Patch(facecolor='red', label='Male'), Patch(facecolor='orange', label='Female')]
plt.legend(handles=legend_elements_gender, title='Gender', loc='upper right')

# Add number labels to bars for gender
for i, bar in enumerate(bars_gender):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10, str(int(bar.get_height())), ha='center', va='bottom')

plt.tight_layout()
plt.savefig('top_20_characters_gender.png')  # Save the figure as an image file
plt.show()

# Define colors for each race category
race_colors = {
    'Caucasian': 'red',
    'Alien': 'orange',
    'Asian': 'yellow',
    'Black': 'brown'
}

# Plot for race
plt.figure(figsize=(12, 8))
bars_race = plt.bar(top_20_characters['character_name'], top_20_characters['total_time_mins'], color=top_20_characters['race'].map(race_colors))
plt.xticks(rotation=45, ha='right')
plt.xlabel('Character Name')
plt.ylabel('Total Screen Time (minutes)')
plt.title('Top 20 Characters by Total Screen Time (Color-coded by Race)')

# Create custom legend for race
from matplotlib.patches import Patch
legend_elements_race = [Patch(facecolor=color, label=race) for race, color in race_colors.items()]
plt.legend(handles=legend_elements_race, title='Race', loc='upper right')

# Add number labels to bars for race
for i, bar in enumerate(bars_race):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10, str(int(bar.get_height())), ha='center', va='bottom')

plt.tight_layout()
plt.savefig('top_20_characters_race_specific_colors.png')  # Save the figure as an image file
plt.show()

#Importing box office and critical rating data
mcu_boxoffice = pd.read_csv("mcu_box_office.csv")
print(mcu_boxoffice)

import pandas as pd

# Assuming 'gender' and 'race' columns exist in mcu_data

# Calculate total value of columns 1 to 27 by gender
gender_totals = mcu_data.groupby('gender').sum().iloc[:, :27]

# Calculate total value of columns 1 to 27 by race
race_totals = mcu_data.groupby('race').sum().iloc[:, :27]

# Calculate gender diversity for each column 1 to 27 where gender diversity = female/total
gender_diversity = {}
for column in mcu_data.columns[0:27]:
    female_total = mcu_data[mcu_data['gender'] == 'Female'][column].sum()
    total = mcu_data[column].sum()
    gender_diversity[column] = 100*female_total / total

# Calculate racial diversity for each column 1 to 27 where racial diversity = values that are not Caucasian/total
racial_diversity = {}
for column in mcu_data.columns[0:27]:
    non_caucasian_total = mcu_data[mcu_data['race'] != 'Caucasian'][column].sum()
    total = mcu_data[column].sum()
    racial_diversity[column] = 100*non_caucasian_total / total

print("Gender Totals:")
print(gender_totals)
print("\nRace Totals:")
print(race_totals)
print("\nGender Diversity:")
print(gender_diversity)
print("\nRacial Diversity:")
print(racial_diversity)

# Add gender diversity to mcu_boxoffice
mcu_boxoffice['gender_diversity'] = mcu_boxoffice['movie_title'].map(gender_diversity)
mcu_boxoffice['gender_diversity'] = mcu_boxoffice['gender_diversity'].round(2)

# Add racial diversity to mcu_boxoffice
mcu_boxoffice['racial_diversity'] = mcu_boxoffice['movie_title'].map(racial_diversity)
mcu_boxoffice['racial_diversity'] = mcu_boxoffice['racial_diversity'].round(2)




#Saving to file
mcu_boxoffice.to_csv('mcu_boxoffice_with_diversity.csv', index=False)