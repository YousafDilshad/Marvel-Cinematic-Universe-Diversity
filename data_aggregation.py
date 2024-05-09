#Importing Libraries
import pandas as pd

#Importing Data
mcu_data = pd.read_csv("mcu_filtered_with_gender_and_race.csv")

print(mcu_data.head())

# Replace NaN with '00:00'
mcu_data.iloc[:, :27] = mcu_data.iloc[:, :27].fillna('00:00')

# Replace 'x:00' with '0:00'
def replace_x_with_zero(value):
    return value.replace('x:00', '0:00')

mcu_data.iloc[:, :27] = mcu_data.iloc[:, :27].applymap(replace_x_with_zero)


# Convert all values to strings
mcu_data = mcu_data.astype(str)

# Remove ':' from the strings
mcu_data = mcu_data.applymap(lambda x: x.replace(':', ''))

def convert_to_minutes(value):
    value = value.zfill(6)  # Ensure value has at least 6 digits
    seconds = int(value[4:])
    minutes = int(value[2:4])
    hours = int(value[:2])
    total_minutes = hours + minutes + (seconds / 60)
    return total_minutes

# Convert first 27 columns to minutes
mcu_data.iloc[:, :27] = mcu_data.iloc[:, :27].applymap(convert_to_minutes)



print(mcu_data.head(20))