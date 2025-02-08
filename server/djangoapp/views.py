from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data["status"] = "Authenticated"
    return JsonResponse(data)


def logout_request(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"success": True, "message": "Logoutsuccessfully"})
    return JsonResponse({"success": False, "error": "Invalid "}, status=400)


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]
    username_exist = User.objects.filter(username=username).exists()
    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"username": username, "error": "Already Registered"})


def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail["review"])
            review_detail["sentiment"] = (
                response.get("sentiment", "neutral") if response else "neutral"
            )
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_cars(request):
    if CarMake.objects.count() == 0:
        initiate()
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in CarModel.objects.select_related("car_make")
    ]
    return JsonResponse({"CarModels": cars})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as err:
            logger.error(f"Error in posting review: {err}")
            return JsonResponse({"status": 401, "message": "Error posting"})
    return JsonResponse({"status": 403, "message": "Unauthorized"})
