#Importing Libraries
import pandas as pd

#Importing Data
mcu_data = pd.read_csv("mcu_filtered_with_gender_and_race.csv")

#Inspecting Data
print(mcu_data.head())

#Replacing empty values
mcu_data.iloc[:, :27] = mcu_data.iloc[:, :27].fillna('00:00')

#Replace 'x:00' with '0:00'
def replace_x_with_zero(value):
    return value.replace('x:00', '0:00')

mcu_data.iloc[:, :27] = mcu_data.iloc[:, :27].applymap(replace_x_with_zero)


#Converting values to strings
mcu_data = mcu_data.astype(str)

#Removing ':'s from strings
mcu_data = mcu_data.applymap(lambda x: x.replace(':', ''))

#Setting up function to convert time to minutes
def convert_to_minutes(value):
    value = value.zfill(6)  #Ensuring value has at least 6 digits
    seconds = int(value[4:])
    minutes = int(value[2:4])
    hours = int(value[:2])
    total_minutes = hours + minutes + (seconds / 60)
    return total_minutes

#Applying function to first 27 columns
mcu_data.iloc[:, :27] = mcu_data.iloc[:, :27].applymap(convert_to_minutes)

#Reinspecting data for confirmation
print(mcu_data.head(20))

#Summing time per character in minutes
mcu_data['total_time_mins'] = mcu_data.iloc[:, :27].sum(axis=1)

#Saving to file
mcu_data.to_csv('mcu_filtered_final.csv', index=False)