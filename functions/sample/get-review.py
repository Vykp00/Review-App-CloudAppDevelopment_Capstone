from urllib import response
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(dict):
    scret={
        "COUCH_URL": "https://19a1a093-eb76-4bd7-b854-2dffa807b7a5-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "4-PnQyyuvd8ON4UvdiTLGv84UftA0HTQddgoGHASWaxA",
        "COUCH_USERNAME": "19a1a093-eb76-4bd7-b854-2dffa807b7a5-bluemix",
        }
    client = Cloudant(
        url = scret["COUCH_URL"],
        scret["IAM_API_KEY"],
        scret["COUCH_USERNAME"],
        connect = True,
    )
    my_database = client["reviews"]

    try:
        selector = {'id': {'$eq': int(dict["id"])}}
        result_by_filter = my_database.get_query_result(selector, raw_result=True)
        response= 
        return response
        print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}

# Version 2 - WORKING
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
def main(dict):
    authenticator = IAMAuthenticator('4-PnQyyuvd8ON4UvdiTLGv84UftA0HTQddgoGHASWaxA')
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://19a1a093-eb76-4bd7-b854-2dffa807b7a5-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_find(
        db='reviews',
        selector={'dealership': {'$eq': int(dict["id"])}},).get_result()
    try:
        # result_by_filter=my_database.get_query_result(selector,raw_result=True)
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        return result
    except:
        return{
            'statusCode': 404,
            'message': 'Something went wrong'
        }