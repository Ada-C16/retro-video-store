from app import db 
from flask import Blueprint, jsonify, request, make_response 
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

customers_bp = Blueprint("customers",__name__,url_prefix = "/customers") # path that gives you access to resources/endpoint
videos_bp = Blueprint("videos",__name__,url_prefix = "/videos")

@videos_bp.route("", methods=["GET"])
def handle_videos():

    videos_table = Video.query.all() # searching for all the videos in the videos table
    videos_list_response = [] # empty list 
    # if videos_table is None:
    #     return jsonify (videos_list), 200
        

    print(videos_table)
    for each_video in videos_table:
            videos_list_response.append(
            {

                "id": each_video.id,
                "title": each_video.title,
                "release_date": False,
                "total_inventory": each_video.total_inventory

            }
        )
    print (videos_list_response)
    return jsonify(videos_list_response), 200

@videos_bp.route("/<video_id>", methods=["GET"])
def handle_video(video_id):
    videos_table = Video.query.get(video_id)
    if videos_table is None:
        return {"message": "Video 1 was not found"}, 404
    elif request.method == "GET":
        return {
            "id": videos_table.id,
            "title": videos_table.title,
            "release_date": videos_table.release_date,
            "total_inventory": videos_table.total_inventory
        }, 200


        



@customers_bp.route("", methods=["GET"])
def handle_customers():

    customers_database = Customer.query.all() # searching for all the customers in the database 
    customers_list = [] # empty list 
    for each_customer in customers_database:
            customers_list.append(
                {

                "id": each_customer.id,
                "name": each_customer.name,
                "registered_at": True




            })

