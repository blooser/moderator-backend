from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from django.core.files import File
from django.http import FileResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from rest_framework import status

from pymongo import MongoClient

from .meeting import Meeting, Voting, Feedback, PDF

import logging
import base64

logger = logging.getLogger("moderator")


@api_view(["POST"])
def login(request):
    data = request.data
 
    username = data['username']
    password = data['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        return Response({
            "username": username,
            "password": password
        })

    return Response({
        "User not authenticated": "You are not allowed enter the page"
    }, status=status.HTTP_401_UNAUTHORIZED)


class Store:
    meeting = Meeting()
    voting = Voting()
    feedback = Feedback()


@api_view(["POST"])
def meeting_update(request):
    data = request.data

    try:
        Store.meeting.update(data)

        logger.info("Meeting updated")

        return Response({
            "OK": "Meeting was updated"
        })

    except Exception as err:
        return Response({
            "Error": str(err)
        })


@api_view(["GET"])
def meeting(request):
    return Response(
        Store.meeting.json()
    )


def get_by_index(collection, index):
    try:
        return collection[index]
    except IndexError:
        return False


@api_view(["POST"])
def speaker(request):
    data = request.data

    index = int(data["number"]) - 1

    if speaker := get_by_index(Store.meeting.speakers, index):
        return Response({
            "speaker": speaker
        })
    
    return Response({
        "speaker": f"No speaker found at index={index}"
    }, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET"])
def speakers(request):
    return Response({
        "speakers": Store.meeting.speakers
    })


@api_view(["POST"])
def feedback_update(request):
    data = request.data

    speaker = data["speaker"]
    answers = data["answers"]

    Store.feedback.update(speaker, answers)

    return Response({"Success": f"Feedback sent"})
    

@api_view(["GET"])
def feedback(request):
    return Response(
        Store.feedback.json()
    )


@api_view(["POST"])
def feedback_pdf(request):
    data = request.data

    speaker = data["speaker"]
    feedback = data["feedback"]

    pdf = PDF(speaker, feedback).get()
    data = base64.b64encode(pdf)

    return Response({
        "filename": f"{speaker}.pdf",
        "file": data
    })


@api_view(["POST"])
def voting_update(request):
    data = request.data

    attr = data["attr"]
    value = data["value"]

    Store.voting.update(attr, value)

    return Response({
        "Success": f"Voted successfully"
    })


@api_view(["GET"])
def voting(request):
    return Response(
        Store.voting.json()
    )
    

@api_view(["GET"])
def test(request):
    return Response({
        "OK": "Hello, from server!"
    })
