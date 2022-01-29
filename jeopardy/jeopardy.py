import pandas as pd
import string
import re

pd.set_option('display.max_colwidth', -1)
#Load the data into a DataFrame and investigate its contents.
df = pd.read_csv("jeopardy.csv", header=[0] )

#print(df.head())

#inspect the dataframe attributes
firstrow_list = df.columns.tolist()

#print(firstrow_list)

#Rename the columns 
df.columns = ['Show_Number', 'Air_Date', 'Round', 'Category', 'Value', 'Question', 'Answer']

#print(df.head())

#print(df.Question.head())

df1 = df.loc[:, 'Question']
testList = ["King", "England"]
df2 = df1.tolist()

# Write a function that filters the dataset for questions that contains all of the words in a list of words
def filter_question(data, words, sensitive=False, separated=False):
    """This function filters the dataset for questions that contains all of the words in a list of words.

    Args:
        data, words: List of words in question coulumn

    Returns:
        [type]: Dataframe 
    """
    yes_sens = lambda x: x if sensitive == True else x.lower()
    yes_sep = lambda x: "\\b"+x+"\\b" if separated == True else x
    filter = lambda x: all(re.search(yes_sep(yes_sens(word)), yes_sens(x)) for word in words)
    #filter = lambda x: all(word.lower() in x.lower() for word in words)
    return data.loc[data["Question" ].apply(filter)]

#print(filter_dataset_questions(df,testList))

df3 = df[df.loc[:,"Question"].str.contains('King','England')]
#print(df3)

#create new column with without the dollar sign

df['new_Value'] = df.Value.str.strip('$')
#print(df.head(25))

# In addition to string with 'None' value, there are values with coma to clean before converting to type float
distinct_dtr_values = []
for i in range(len(df['new_Value'])):
    if (len(df['new_Value'].iloc[i]) > 4) & (df['new_Value'].iloc[i] not in distinct_dtr_values):
        distinct_dtr_values.append(df['new_Value'].iloc[i])

#print(distinct_dtr_values)

# Clean the dataset by removing the comma in the string values with punctuation and by replacing the None value by 0.
df['new_Value'] = df['new_Value'].apply(lambda v: v.translate(v.maketrans('','', string.punctuation)) if v != 'None' else 0 )

# Convert the new_Value column values to floats
df['new_Value'] = df['new_Value'].astype(float)

#print(df['new_Value'])

#Write a function that returns the count of the unique answers to all of the questions in a dataset.

def get_answer_count_unique(data, word, col_label1, col_label2):
    """This function filters the dataset for all the questions that contain the given word and returns the count of the unique answers to all of the questions in a dataset

    Args:
        dataset, word: List of words in question coulumn

    Returns:
        [type]: Dataframe 
    """
    indice_list = []
    answer_list = []
    question_list = []
    
    for i in data.index:
        if data.loc[i, col_label1].find(word) == True:
            indice_list.append(i)
    
    for j in indice_list:
        question_list.append(data.loc[j, col_label1])
        answer_list.append(data.loc[j, col_label2])
            
    # return  a Series containing counts of unique rows in the DataFrame of Answer_list
    unique_answer = pd.DataFrame(answer_list, question_list).reset_index()
    
    # rename the columns
    unique_answer.columns = ['question', 'answer']
    
    #count unique values
    val_counts = unique_answer.value_counts()
    
    #converting to DataFrame and assigning the column names.
    df_val_counts = pd.DataFrame(val_counts).reset_index()
    df_val_counts.columns = ['question', 'answer', 'unique_value']
                                      
    return df_val_counts 
    
#print(get_answer_count_unique(df,'King', 'Question', 'Answer'))

# get most common answer for questions selected by words from a list
def get_most_frequente_answer(words_list):
    filtered = filter_question(df, words_list)
    answers = filtered.groupby('Answer').Show_Number.count().reset_index()
    most_selected = answers[answers.Show_Number == answers.Show_Number.max()]
    return most_selected

#print(get_most_frequente_answer(['King']))
#print(get_most_frequente_answer(['Computer']))
#print(get_most_frequente_answer(testList))

#define decades
def decades(mydate):
    mydate =pd.to_numeric(mydate)
    decade70s =  (1970 <= mydate < 1980 and '1970s') 
    decade80s =  (1980 <= mydate < 1990 and '1980s') 
    decade90s =  (1990 <= mydate < 2000 and '1990s')
    decade00s =  (2000 <= mydate < 2010 and '2000s')
    decade10s =  (2010 <= mydate < 2020 and '2010s')
    return decade70s  or decade80s  or decade90s  or decade00s  or decade10s

# Number of questions from the 90s use the word "Computer" compared to questions from the 2000s
def filter_by_decade(words_list):
    """This function filters the dataset for all the questions that contain the givena list of strings and returns 
    the count of the questions by decade.

    Args:
       a list of strings

    Returns:
        [type]: Dataframe 
    """
    
    filtered = filter_question(df, words_list)
    
    #extract years in new column as numeric values
    filtered['Air_Date'] = filtered['Air_Date'].str.replace('-', '')
    filtered['year'] = pd.to_numeric(pd.DatetimeIndex(filtered['Air_Date']).year)
    
    # create a decades columns in the the filtered DataFrame
    filtered['decades'] = filtered.year.apply( lambda year: decades(year)  )
    
    # define decades DataFrame
    decadeDataFrame = filtered.groupby('decades').Question.count().reset_index()
    
    return decadeDataFrame

# print(filter_by_decade(['Computer']))

# Write a function that filters the dataset for questions that contains all of the words in a list of words.
def filter_category( dataframe, words_list):
    """This function filters the dataset for questions that contains all of the words in a list of words.
    Args:
        data, words: List of words in question coulumn
    Returns:
        [type]: Dataframe 
    """
    filter = lambda x: all(word.lower() in x.lower() for word in words_list)
    return dataframe.loc[dataframe["Category" ].apply(filter)]

#print(filter_category(df,["Literature"]))

def filter_by_round(words_list):
    """This function filters the dataset for all the categories that contain the given list of strings and returns 
    the count of the categories by round.

    Args:
       a list of strings

    Returns:
        [type]: Dataframe 
    """
    
    filtered = filter_category(df, words_list)
    
    
    # define decades DataFrame
    grouped_df = filtered.groupby('Round').Category.count().reset_index()
    
    return grouped_df

#print(filter_by_round(["Literature"]))


#Building a system quiz

def get_gl_knowledge_statements():
    #build a list of question-answer
    statements = []
    question_list = []
    answer_list = []
    for i in df[:10].index:
        question_list.append(df.loc[i, 'Question'])
        answer_list.append(df.loc[i, 'Answer'])

    statements = zip(question_list, answer_list)
    statements = list(zip(question_list, answer_list))
    
    return  statements

#print(get_gl_knowledge_statements())

def get_literature_statements():
    litf = filter_category(df,["Literature"])
    
    #build a list of question-answer
    statements = []
    question_list = []
    answer_list = []
    for i in litf[:10].index:
        question_list.append(litf.loc[i, 'Question'])
        answer_list.append(litf.loc[i, 'Answer'])

    statements = zip(question_list, answer_list)
    statements = list(zip(question_list, answer_list))
    
    return  statements

#print(get_literature_statements())

def play_literature_quiz():
    
    # Get literature statements
    literature_statements = get_literature_statements()
    
    # Randomise literature statements
    random.shuffle(literature_statements)
    
    # set player score to 0
    score = 0
    
    # Show tof statements using a loop
    for s in literature_statements:
        
        # present statement
        print("Literature: " + s[0])
        
        # user enter guess
        guess = input("Enter your answer: ")
        # check if guess is correct
        if guess == s[1]:
            print("Correct!")
            # update score
            score += 1
        else:
            print("Incorrect :(")
            
    # Show final score
    print("Your final score is: " + str(score))

def play_gl_knowledge_quiz():
    
    # Get general knowledge statements
    gl_knowledge_statements = get_gl_knowledge_statements()
    
    # Randomise general knowledge statements
    random.shuffle(gl_knowledge_statements)
    
    # set player score to 0
    score = 0
    
    # Show tof statements using a loop
    for s in gl_knowledge_statements:
        
        # present statement
        print("General Knowledge: " + s[0])
        
        # user enter guess
        guess = input("Enter your answer: ")
        # check if guess is correct
        if guess == s[1]:
            print("Correct!")
            # update score
            score += 1
        else:
            print("Incorrect :(")
            
    # Show final score
    print("Your final score is: " + str(score))
    
    
    
def main_menu():
    
    print("+--------------------------------+")
    print("|    Welcome to QUIZ JEOPARDY!   |")
    print("+--------------------------------+")
    print("| Please select an option:       |")
    print("|                                |")
    print("| 1. Play Literature quiz        |")
    print("| 2. Play General Knowledge quiz |")
    print("| 0. Quit                        |")
    print("+--------------------------------+")
    choice = input("Enter 1, 2, or 0: ")
    if choice == "1":
        play_literature_quiz()
    elif choice == "2":
        play_gl_knowledge_quiz()
    else:
        print("Thank for your laying!")
        quit()
    return choice

main_menu()
    