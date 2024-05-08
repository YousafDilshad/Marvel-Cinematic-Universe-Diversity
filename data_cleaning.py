#Importing libraries
import pandas as pd

#Importing data
mcu_box_office = pd.read_csv('mcu_box_office.csv')
mcu_screentime = pd.read_csv('meu_screentime.csv')

#Display the shape of each database (rows, columns)
print("MCU Box Office Database Shape:", mcu_box_office.shape)
print("MCU Screentime Database Shape:", mcu_screentime.shape)

#Display basic information about each database (data types, non-null values)
print("\nMCU Box Office Database Info:")
print(mcu_box_office.info())
print("\nMCU Screentime Database Info:")
print(mcu_screentime.info())

#Display summary statistics for numerical columns in each database
print("\nMCU Box Office Database Summary Statistics:")
print(mcu_box_office.describe())
print("\nMCU Screentime Database Summary Statistics:")
print(mcu_screentime.describe())

#Display the first few rows of each database
print("\nMCU Box Office Database Sample:")
print(mcu_box_office.head())
print("\nMCU Screentime Database Sample:")
print(mcu_screentime.head())

#Replace character_name with alternate_name where possible
mcu_screentime['character_name'] = mcu_screentime.apply(lambda x: x['alternate_name'] if pd.notnull(x['alternate_name']) else x['character_name'], axis=1)

#List of Movies/Shows in mcu_screentime
print(mcu_screentime.columns.tolist())

#Checking for consistency in movie titles across two dataframes
box_office_movie_titles = mcu_box_office['movie_title'].unique()
screentime_columns = set(mcu_screentime.columns)
non_matching_columns = [title for title in box_office_movie_titles if title not in screentime_columns]
print("Columns in mcu_box_office that don't match column names in mcu_screentime:")
for column in non_matching_columns:
    print(column)

#Renaming non-matching column names
mcu_screentime = mcu_screentime.rename(columns={
    'Avengers: Endgame': 'Avengers: End Game',
    'Spider-Man: Far from Home': 'Spider-Man: Far From Home'
})

#Rechecking for consistency to confirm
box_office_movie_titles = mcu_box_office['movie_title'].unique()
screentime_columns = set(mcu_screentime.columns)
non_matching_columns = [title for title in box_office_movie_titles if title not in screentime_columns]
print("Columns in mcu_box_office that don't match column names in mcu_screentime:")
for column in non_matching_columns:
    print(column)

#Dropping shows/movies not in mcu_boxoffice from mcu_screentime and alternate_name column
box_office_movie_titles = mcu_box_office['movie_title'].unique()
matching_columns = [col for col in mcu_screentime.columns if col in box_office_movie_titles]
columns_to_keep = matching_columns + mcu_screentime.columns[-2:].tolist()
mcu_screentime_filtered = mcu_screentime[columns_to_keep]
mcu_screentime_filtered = mcu_screentime_filtered.drop('alternate_name', axis=1)

#Dropping rows with non-appearing characters
initial_row_count = mcu_screentime_filtered.shape[0]
mcu_screentime_filtered = mcu_screentime_filtered.dropna(subset=[col for col in mcu_screentime_filtered.columns if col != 'character_name'], how='all')
final_row_count = mcu_screentime_filtered.shape[0]
print(f"Row count before dropping NaN values: {initial_row_count}")
print(f"Row count after dropping NaN values: {final_row_count}")

#Inspecting for confirmation
print(mcu_screentime_filtered.head())

#Savingto file and printing final data summary
mcu_screentime_filtered.to_csv('mcu_screentime_filtered.csv', index=False)
print(f"Final Data Summary: After data cleaning, the datasets provide information on {len(mcu_box_office['movie_title'])} movies, recording screen time in minutes for {len(mcu_screentime_filtered)} characters.")
