import pandas as pd
import openai

#Setting API key
api_key = "sk-proj-v6comklbJcwj7wX75eJfT3BlbkFJFUNpDGwR1ORsj1D5IKPY"
openai.api_key = api_key

#Loading data
mcu_filtered = pd.read_csv("mcu_screentime_filtered.csv")

#Defining function to generate gender
def get_gender(character_name):
    prompt = f"What is the gender of the character {character_name} in the Marvel Cinematic Universe? Provide a one word answer between Male and Female"
    #Sending a request to OpenAI API 
    response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}]
        )
    #Printing API esponse
    print(response)    
    
    #Extracting answer
    return response.choices[0].message.content


#Defining function to generate race
def get_race(character_name):
    prompt = f"What is the race of the character {character_name} in the Marvel Cinematic Universe? Provide a one/two word answer from the following list: Caucasian, Asian, African-American, Middle Eastern, Hispanic."
    #Sending a request to OpenAI API 
    response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}]
        )
    #Printing API esponse
    print(response)    
    
    #Extracting answer
    return response.choices[0].message.content


#Applying API response to create gender and race columns in dataframe
mcu_filtered["gender"] = mcu_filtered["character_name"].apply(get_gender)
mcu_filtered["race"] = mcu_filtered["character_name"].apply(get_race)

# Save the updated dataframe
mcu_filtered.to_csv("mcu_filtered_with_gender_and_race.csv", index=False)
