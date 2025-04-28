# a.py
import requests

class GetAns:
    def trimword(self, word):
        newWord = ''
        for char in word:
            if char.isalnum():
                newWord += char
            elif char in ('/', '-'):
                newWord += '-'
        return newWord

    def getValue(self, prompt):
        words = prompt.split(' ')
        cleaned = [self.trimword(w) for w in words]
        slug = '-'.join(cleaned)
        baseUrl = (
            f"https://www.espncricinfo.com/ask/_next/data/"
            f"Y23c3yFF7-wh3NNz_Usz7/cricket-qna/{slug}%26tournament%3Dipl.json"
            f"?results=cricket-qna&results={slug}%26tournament%3Dipl"
        )
        headers = {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/134.0.0.0 Safari/537.36"),
            "Accept": "application/json",
        }
        resp = requests.get(baseUrl, headers=headers)
        try:
            return resp.json()
        except:
            return {}














# import requests

# class GetAns:
#     def trimword(self,word):
#         newWord = '';
#         for char in word:
#             if char.isalnum():
#                 newWord += char
#             elif(char=='/' or char=='-'): newWord += '-'
#         return newWord

#     def getValue(self,prompt):

#         userInputList = prompt.split(' ')
#         newUserInputList = [self.trimword(item) for item in userInputList];
#         userPrompt = '-'.join(newUserInputList)

#         baseUrl = f"https://www.espncricinfo.com/ask/_next/data/Y23c3yFF7-wh3NNz_Usz7/cricket-qna/{userPrompt}%26tournament%3Dipl.json?results=cricket-qna&results={userPrompt}%26tournament%3Dipl"

#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
#             "Accept": "application/json",
#         }

#         response = requests.get(baseUrl, headers=headers)

#         print("URL:", baseUrl)
#         print("Status Code:", response.status_code)

#         try:
#             data = response.json()
#             print(data)
#             return data
#         except Exception as e:
#             print("Could not parse JSON:", e)
#             return {}









# import requests
# import pandas as pd

# # Function to clean up words for URL
# def trimword(word):
#     newWord = ''
#     for char in word:
#         if char.isalnum():
#             newWord += char
#         elif char == '/' or char == '-': 
#             newWord += '-'
#     return newWord;

# # Function to generate table from JSON data
# def generate_table_from_json(data):
#     try:
#         # Extract the relevant data for table creation
#         parsed_data = data['pageProps']['parsedData']['scrappedData']['data']['cmpData']['parsedData']
        
#         # Create a DataFrame from the extracted data (key-value pairs)
#         df = pd.DataFrame(parsed_data)
        
#         # Render the table to the user
#         return df
#     except KeyError as e:
#         return f"Error processing data: {e}"

# # Main execution logic
# def main():
#     userInput = input("Enter the prompt: ")
#     userInputList = userInput.split(' ')
#     newUserInputList = [trimword(item) for item in userInputList]
#     userPrompt = '-'.join(newUserInputList)

#     baseUrl = f"https://www.espncricinfo.com/ask/_next/data/Y23c3yFF7-wh3NNz_Usz7/cricket-qna/{userPrompt}%26tournament%3Dipl.json?results=cricket-qna&results={userPrompt}%26tournament%3Dipl"

#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
#         "Accept": "application/json",
#     }

#     response = requests.get(baseUrl, headers=headers)

#     print("URL:", baseUrl)
#     print("Status Code:", response.status_code)

#     try:
#         data = response.json()

#         # Check for query type and handle accordingly
#         if 'head-to-head' in userPrompt:
#             # For head-to-head or match queries, render the table
#             table = generate_table_from_json(data)
#             print(table)

#         elif 'RCB won' in userPrompt or 'Orange Cap' in userPrompt or 'six' in userPrompt:
#             # Handle queries for top scores, Orange Cap, sixes etc.
#             table = generate_table_from_json(data)
#             print(table)

#         elif 'lowest total score' in userPrompt or 'most dismissals' in userPrompt:
#             # Handle queries related to scores or dismissals
#             table = generate_table_from_json(data)
#             print(table)

#         elif 'most ducks' in userPrompt:
#             # Handle queries related to most ducks
#             table = generate_table_from_json(data)
#             print(table)

#         else:
#             # Handle cases where the query type is not recognized but we still need to display a table
#             print("Unknown query type or unhandled case.")

#     except Exception as e:
#         print("Could not parse JSON:", e)

# # Run the main function
# if __name__ == "__main__":
#     main()