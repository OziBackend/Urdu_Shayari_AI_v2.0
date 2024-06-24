from flask import jsonify, request, Response

# from helpers import some_helper_function
from Controller.controller import (
    ai_conversation_with_poets,
    
    stream_poetry_by_topic,
    stream_poetry_by_type,

    get_chat_history
    # save_shayari_by_topic
)
import threading
import re
import time

from Extra_Modules.logging import get_logger
#Get configured logger
logger = get_logger()

semaphores = threading.Semaphore(30)


def setup_routes(app):
    @app.route("/urdu-shayari/ai")
    def index():
        return "Hello, world!"

    #==========================================================================#
    # Shayari Routes: Urdu Shayari APIs using ChatGPT
    #==========================================================================#
    
    @app.route("/urdu-shayari/ai/ai_conversation_with_poets", methods=["POST"])
    def ai_conversation():
        print("CHat GPT AI funtion to ai_conversation_with_poets called")

        # reading body parameters
        data = request.json
        print("<----------------------------------------->", data)
        # Process the recieved data
        if data is None:
            print("-------------Prompt Missing------------")
            return (jsonify({"message": "Bad Request, no prompt found"}), 400)

        query_params = {}
        for key, value in request.args.items():
            query_params[key] = value

        if not query_params or not query_params["poet_name"]:
            print("--------Parameters missing--------")
            return (
                jsonify(
                    {"message": "Bad Request, no query found or parameters missing"}
                ),
                400,
            )
        
        logger.info(f"Calling API 'ai_conversation' for {query_params["poet_name"]}")
        logger.info(f"Calling API 'ai_conversation' with prompt = {data.get("prompt")}")

        return_data = {}
        additional_data = {
            "prompt": data.get("prompt"),
            "poet_name": query_params["poet_name"],
        }

        # Acquire Semaphore
        print("Acquiring a Semaphore")
        semaphores.acquire()

        t = threading.Thread(
            target=ai_conversation_with_poets, args=(app, additional_data, return_data, logger)
        )
        t.start()
        t.join()

        # Processing on response
        print(return_data)

        # Release Semaphore
        print("Releasing a Semaphore")
        semaphores.release()

        if not return_data:
            return jsonify({"response": [] })

        return jsonify(return_data)
    

    #==========================================================================#
    # Streaming Route: Get poetry by topic
    #==========================================================================#
    @app.route("/urdu-shayari/ai/stream_poetry_by_topic", methods=["GET"])
    def poetry_by_topic_stream():
        print("Chat GPT AI function to stream_poetry_by_topic called")
        query_params = {}
        for key, value in request.args.items():
            query_params[key] = value

        if not query_params or not query_params.get("poetry_topic") or not query_params.get("username"):
            logger.critical("--------Parameters missing--------")
            print("--------Parameters missing--------")
            return (
                jsonify(
                    {"message": "Bad Request, no query found or parameters missing"}
                ),
                400,
            )
        
        logger.info(f"{query_params['username']} Called API 'stream_poetry_by_topic' for {query_params['poetry_topic']}")
        additional_data = query_params


        return Response(stream_poetry_by_topic(app, additional_data, logger), mimetype='application/json')

    @app.route("/urdu-shayari/ai/stream_poetry_by_type", methods=["GET"])
    def poetry_by_type_stream():
        print("Chat GPT AI function to stream_poetry_by_type called")
        query_params = {}
        for key, value in request.args.items():
            query_params[key] = value

        if not query_params or not query_params.get("poetry_type"):
            logger.critical("--------Parameters missing--------")
            print("--------Parameters missing--------")
            return (
                jsonify(
                    {"message": "Bad Request, no query found or parameters missing"}
                ),
                400,
            )
        
        logger.info(f"{query_params['username']} Called API 'stream_poetry_by_type' for {query_params['poetry_type']}")
        additional_data = query_params


        return Response(stream_poetry_by_type(app, additional_data, logger), mimetype='application/json')


    #==========================================================================#
    # Database connected Routes
    #==========================================================================#

    @app.route("/urdu-shayari/ai/get_chat_history", methods=['GET'])
    def get_chat_history_main():
        print("Function to get_chat_history called")
        query_params = {}
        for key, value in request.args.items():
            query_params[key] = value

        
        logger.info(f"{query_params['username']} Called API 'get_chat_history'")
        additional_data = query_params

        return_data ={}

        # Acquire Semaphore
        print("Acquiring a Semaphore")
        semaphores.acquire()

        t = threading.Thread(
            target=get_chat_history, args=(app, additional_data, return_data, logger)
        )
        t.start()
        t.join()


        # Processing on response
        print(return_data)

        # Release Semaphore
        print("Releasing a Semaphore")
        semaphores.release()

        if not return_data:
            return jsonify({"response": [] })

        return jsonify(return_data)

    # @app.route("/urdu-shayari/v2.0/save_poetry_by_topic", methods=["GET"])
    # def save_to_db_by_topic():
    #     print('1')
    #     query_params = {}
    #     for key, value in request.args.items():
    #         query_params[key] = value

    #     if not query_params or not query_params["poetry_topic"]:
    #         print("--------Parameters missing--------")
    #         return (
    #             jsonify(
    #                 {"message": "Bad Request, no query found or parameters missing"}
    #             ),
    #             400,
    #         )
    #     data = request.json

    #     logger.info(f"Calling API 'get_poetry_by_topic' for {query_params["poetry_topic"]}")

    #     return_data = {}
    #     additional_data = {
    #         "query_params": query_params,
    #         "data": data}

    #     save_shayari_by_topic(app, additional_data, return_data, logger)

    #     return jsonify({"message": "Data is saved in database (X)"})