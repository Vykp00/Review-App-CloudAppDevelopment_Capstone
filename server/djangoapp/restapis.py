from cgitb import text
from ensurepip import version
from unicodedata import name
from unittest import result
from unittest.mock import sentinel
from urllib import response
import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        requests.get(url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('YPJu9jZZL_JQUVssKlFp1CqgX0ewT-koORI7O3q7uKZd', api_key))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print("POST to {url}")
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("An error occurred while making POST request.")
    status_code = response.status_code
    print("With status {status_code}")

    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dbs"]["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Perform a GET request with the specified dealer id
    json_result = get_request(url, dealerId = dealer_id)

    if json_result:
        # Get all review data from the response
        reviews = json_result["body"]["data"]["docs"]
        # For each review in the response
        for review in reviews:
            # Create a DealerReview object from the data
            review_content = review["review"]
            id = review["_id"]
            name = review["name"]
            purchase = review["purchase"]
            dealership = review["dealerships"]

            try:
                # These values may be missing
                car_make = review["car_make"]
                car_model = review["car_model"]
                car_year = review["car_year"]
                purchase_date = review["purchase_date"]

                # Create a review object with values in 'doc' object
                review_obj = DealerReview(
                    dealership=dealership, id=id, name=name, purchase=purchase, 
                    review=review_content, car_make=car_make, car_model=car_model, 
                    car_year=car_year, purchase_date=purchase_date
                    )
            except KeyError:
                print("Something missing from this review. Using default values.")
                # Create review object with default values
                review_obj = DealerReview(
                    dealership=dealership, id=id, name=name, purchase=purchase,
                    review=review_content
                    )
            # Analyze sentiment of the review text and save it to sentiment attribute
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print("sentiment: {review_obj.sentiment}")

            # Save review object to the list result
            results.append(review_obj)

    return results
# Requires the dealer_id parameter with only a single value
def get_dealer_by_id(url, dealer_id):
    # Call get_request with the dealer_id param
    json_result = get_request(url,dealer_id=dealer_id)
    print(json_result)
    # Create a CarDealer object from response
    dealer = json_result["entries"]
    dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                           id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                           short_name=dealer["short_name"],
                           st=dealer["st"], zip=dealer["zip"])

    return dealer_obj


# Gets all dealers in the specified state from the Cloudant DB with the Cloud Function get-dealerships
def get_dealers_by_state(url, state):
    results = []
    # Call get_request with the state param
    json_result = get_request(url, state=state)
    dealers = json_result["body"]["docs"]
    # For each dealer in the response
    for dealer in dealers:
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                               id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                               short_name=dealer["short_name"],
                               st=dealer["st"], zip=dealer["zip"])
        results.append(dealer_obj)

    return results
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(dealerreview):
    # Watson NLU configuration
    api_key = "YPJu9jZZL_JQUVssKlFp1CqgX0ewT-koORI7O3q7uKZd"
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/e80a3b85-c701-42df-9ee5-72b24b591c5e"
    version = '2022-04-07'
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(version=version, authenticator=authenticator)
    nlu.set_service_url(url)

    # get sentiment for the review
    try:
        response.nlu.analyze(
            text=dealerreview, 
            features = Features(sentiment=SentimentOptions())).get_result()
        print(json.dump(response))
        sentiment_label = response["sentiment"]["document"]["label"]
    except:
        print("Review is too short for sentiment analysis. Assigning default sentiment value 'neutral' instead")
        sentiment_label = "neutral"
    # print(sentiment_score)
    print(sentiment_label)

    return sentiment_label



