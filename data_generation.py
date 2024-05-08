import pandas as pd
import openai

# Set your API key
api_key = "sk-proj-v6comklbJcwj7wX75eJfT3BlbkFJFUNpDGwR1ORsj1D5IKPY"
openai.api_key = api_key

# Load your dataframe
mcu_filtered = pd.read_csv("mcu_screentime_filtered.csv")

# Define a function to generate gender for a given character name
def get_gender(character_name):
    prompt = f"What is the gender of the character {character_name} in the Marvel Cinematic Universe? Provide a one word answer between Male and Female"
    # Make a request to the OpenAI API using the specified model and prompt
    response = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}]
        )
    # Print the API response to console for debugging purposes
    print(response)    
    
    # Extract the summary from the API response and return it
    return response.choices[0].message.content


# Apply the function to create a new column called 'gender'
mcu_filtered["gender"] = mcu_filtered["character_name"].apply(get_gender)

# Save the updated dataframe
mcu_filtered.to_csv("mcu_filtered_with_gender.csv", index=False)
