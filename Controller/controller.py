from openai import OpenAI
from flask import jsonify, Flask
from Keys.authKeys import keys
import os
import re
import json
from datetime import datetime

# laoding prompts file
from Data_Values.prompts import prompts
# from Data_Values.roles import roles
from Data_Values.roles import get_role
# loading database
from Database.database_config import (
    collection_by_type,
    collection_by_topic,
    collection_of_conversation,

    sort_orders
)


os.environ["OPENAI_API_KEY"] = keys["openAI"]  # Replace with your actual key

client = OpenAI()

# Helper function to format MongoDB documents
def format_document(doc):
    doc['_id'] = str(doc['_id'])
    return doc

####################################################################################
# =============================Database Functions==================================#
####################################################################################

def savePromptinDB(system_prompt, user_prompt, username, user_time, user_value, check, logger):
    user_prompt_command = ''

    if check == 'by_type' or check == 'by_topic':
        prompt = user_value
        logger.debug('User Value is : ', user_value)
    elif check == 'ai_chat':
        prompt = user_value
        logger.debug(f'User Prompt is : {user_prompt}')
        user_prompt_command = user_prompt

    json_data ={
        "username":username,
        "category": check,
        "search_value":prompt,
        "user_prompt_command":user_prompt_command,
        "user_prompt_time":user_time,
        "system_prompt":system_prompt,
        "system_response_time":datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    }

    if check == 'by_type':
        result = collection_by_type.insert_one(json_data)
    elif check == 'by_topic':
        result = collection_by_topic.insert_one(json_data)
    elif check == "ai_chat":
        result = collection_of_conversation.insert_one(json_data)
    
    print('Saved Data Id: ==> %s', str(result.inserted_id))

####################################################################################
# =================================Functions=======================================#
####################################################################################

def genAIfunction(system_role, prompt, app, logger, username, user_time, user_value, check):
    with app.app_context():
        try:
            completion = client.chat.completions.create(
                        model="gpt-3.5-turbo-0125",
                        messages=[
                            {
                                "role": "system",
                                "content": system_role,
                            },
                            {
                                "role": "user",
                                "content": prompt,
                            },
                        ],
                    )
            completed_data = completion.choices[0].message.content
            savePromptinDB(completed_data, prompt, username, user_time, user_value, check, logger)
            return {"flag": True, "completion_data": completed_data}

        except BaseException as e:
            logger.error('1... Exception thrown in GenAIfunction = %s', str(e))
            print(f"1... In GenAIfunction exception is = {e}")
            return {"flag": False, "completion_data": ""}


def genAIfunctionStream(system_role, prompt, app, logger, username, user_time, user_value, check):
    with app.app_context():
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {
                        "role": "system",
                        "content": system_role,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                stream=True
            )
            
            #all data will be stored in this variable to store in database
            complete_data=''
            
            sentence=''
            for chunk in stream:
                data = chunk.choices[0].delta.content
                #if data is completed and response reaches to end, IF statement will work
                if data is None and sentence != "":
                    complete_data += sentence
                    yield sentence
                if data is not None:
                    if ']' not in data:
                        sentence += data
                    else:
                        data = data.replace(']','')
                        print('replaced data====>', data)
                        sentence += data
                        complete_data += '\n'
                        sentence = sentence.replace('\n','')
                        sentence = sentence.replace('[','')

                        if sentence != "":
                            # Remove trailing whitespace
                            sentence = sentence.rstrip()
                            # Check if the last character is a comma and remove it
                            if sentence.endswith(','):
                                sentence = sentence[:-1]
                            complete_data += sentence
                            yield sentence
                            yield '\n'
                        sentence=''
            
            if username != "":
                savePromptinDB(complete_data, prompt, username, user_time, user_value, check, logger)

        except BaseException as e:
            logger.error("1... Exception thrown in GenAIfunctionstream = %s", str(e))
            print(f"1... In GenAIfunctionstream exception is = {e}")
            yield ""

####################################################################################
# ==========================AI Conversations with Poets============================#
####################################################################################


def ai_conversation(app, data, logger):
    
    with app.app_context():
        username = data["username"]
        user_prompt_time = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

        prompt = data["prompt"]
        number =''
        poetname = data['poet_name']

        if poetname == 'Ustad':
            poetname = 'Urdu Scholar'

        if poetname in ['Urdu Scholar', 'Male', 'Female']:
            number ='3'
        elif poetname == 'Competitor':
            number = '4'
        else:
            number ='2'

        system_role = get_role(app, number, poetname)
        
        
        try:
            AI_data = genAIfunction(system_role, prompt, app, logger, username, user_prompt_time, poetname, "ai_chat")

            print('getting ai data===========++++++++++',AI_data)
            if AI_data['flag']:
                completed_data = AI_data['completion_data']
                print("Data Completion============>", completed_data)
                return {"flag": True, "completion_data": completed_data}
            else:
                logger.error('8... No data returned from GenAI function')
                return {"flag": False, "completion_data": ""}

        except BaseException as e:
            logger.error('8... Exception thrown in ai_conversation function = %s', str(e))
            print(f"8... In ai_conversation exception is = {e}")
            return {"flag": False, "completion_data": ""}


def ai_conversation_with_poets(app, data, returned_data, logger):
    with app.app_context():
        
        acquired_data = ai_conversation(app, data, logger)

        if acquired_data["flag"]:
            # data is found and processed before sending to client
            data = acquired_data["completion_data"]
            returned_data["response"] = data
        else:
            # data not found, exception was thrown, blank array is returned to client
            logger.error('9... Empty Response from API: []')
            returned_data["response"] = []

####################################################################################
####################################################################################
##############             Streaming Poetry by Topic                  ##############
####################################################################################
####################################################################################

#Stream by Topic
def stream_poetry_by_topic(app, data, logger):
    print('====>>In stream_poetry_by_topic function')
    
    # Loading Prompt
    prompt = prompts["4"].format(poetry_topic=data["poetry_topic"])
    # Loading Role
    system_role = get_role(app, "1", "")
    username = data["username"]
    user_prompt_time = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    user_value = data["poetry_topic"]

    print('====>>In stream_poetry_by_topic function')
    return genAIfunctionStream(
        system_role, 
        prompt, 
        app, 
        logger, 
        username, 
        user_prompt_time,
        user_value,
        "by_topic"
    )

#Stream by Type
def stream_poetry_by_type(app, data, logger):
    print('====>>In stream_poetry_by_type function')
    
    # Loading Prompt
    prompt = prompts["5"].format(poetry_type=data["poetry_type"])
    # Loading Role
    system_role = get_role(app, "1", "")
    username = data["username"]
    user_prompt_time = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    user_value = data["poetry_type"]
    
    print('====>>In stream_poetry_by_type function')
    return genAIfunctionStream(
        system_role, 
        prompt, 
        app, 
        logger, 
        username, 
        user_prompt_time,
        user_value,
        "by_type"
        )


####################################################################################
####################################################################################
##############              Shayaris with Database                    ##############
####################################################################################
####################################################################################

def get_chat_history(app, data,returned_data, logger):
    with app.app_context():
        username = data['username']
        if data.get('page'):
            page = int(data['page'])
        else:
            page = 1

        print(page)
        limit = 2
        skip = (page - 1) *limit

        items = []

        if data.get('poetry_topic'):
            topic = data['poetry_topic']
            print(topic)
            items = collection_by_topic.find({'username':username, 'search_value':topic})
        elif data.get('poetry_type'):
            type = data['poetry_type']
            print(type)
            items = collection_by_type.find({'username':username, 'search_value':type})
        elif data.get('character'):
            character = data['character']
            print(character)
            items = collection_of_conversation.find({'username':username, 'search_value':character}).sort("user_prompt_time", sort_orders[1]).skip(skip).limit(limit)
    
        returned_data['items']= []
        for item in items:
            # Convert ObjectId to string if necessary
            if '_id' in item:
                item['_id'] = str(item['_id'])
            returned_data['items'].insert(0,item)

# def save_shayari_by_topic(app, data, returned_data, logger):
#     print('Save shayari_by_topic')
#     json_data = data["data"]
#     result = collection_by_topic.insert_one(json_data)
#     print('Saved Data Id: ==> %s', str(result.inserted_id))
    
