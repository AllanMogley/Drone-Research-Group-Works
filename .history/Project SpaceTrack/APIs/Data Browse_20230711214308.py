# =============================================================================
#  USGS/EROS Inventory Service Example
#  Python - JSON API
# 
#  Script Last Modified: 1/24/2022
#  Note: This example does not include any error handling!
#        Any request can throw an error, which can be found in the errorCode proprty of
#        the response (errorCode, errorMessage, and data properies are included in all responses).
#        These types of checks could be done by writing a wrapper similiar to the sendRequest function below
#  Usage: python scene_search.py -u username -p password
# =============================================================================

import json
import requests
import sys
import time
import argparse

# Send http request
def sendRequest(url, data, apiKey = None):  
    json_data = json.dumps(data)
    
    if apiKey == None:
        response = requests.post(url, json_data)
    else:
        headers = {'X-Auth-Token': apiKey}              
        response = requests.post(url, json_data, headers = headers)    
    
    try:
      httpStatusCode = response.status_code 
      if response == None:
          print("No output from service")
          sys.exit()
      output = json.loads(response.text)	
      if output['errorCode'] != None:
          print(output['errorCode'], "- ", output['errorMessage'])
      if  httpStatusCode == 404:
          print("404 Not Found")
          sys.exit()
      elif httpStatusCode == 401: 
          print("401 Unauthorized")
          sys.exit()
      elif httpStatusCode == 400:
          print("Error Code", httpStatusCode)
          sys.exit()
    except Exception as e: 
          response.close()
          print(e)
          sys.exit()
    response.close()
    
    return output


if __name__ == '__main__': 
    #NOTE :: Passing credentials over a command line arguement is not considered secure
    #        and is used only for the purpose of being example - credential parameters
    #        should be gathered in a more secure way for production usage
    #Define the command line arguements
    
    # User input    
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help='Username')
    parser.add_argument('-p', '----password', required=True, help='Password')
    
    args = parser.parse_args()
    
    username = args.username
    password = args.password     

    print("\nRunning Scripts...\n")
    
    serviceUrl = "https://m2m.cr.usgs.gov/api/api/json/experimental/"
    
    # Login
    payload = {'username' : username, 'password' : password}
    
    print("\nLogin...\n")
    
    response = sendRequest(serviceUrl + "login", payload)
    
    if response['errorCode'] == None:
        apiKey = response['data']
    else:
        sys.exit()
    
    print("API Key: " + apiKey + "\n")    
    
    # Scene-search-create - it'll return a search ID in the data field   
    searchCreatePayload = {
        "autoExecute": False, # If set to true, there is no need to call scene-search-execute
        "searchLabel": "Test Search",
        "metadataConfig": None,
        "resultsPerPage": 100,
        "compareListName": "test-compare",
        "excludeListName": "test-exclude",
        "sceneDatasetFilters": [
            {
                "datasetName": "gls_all",
                "sceneFilter": {
                    "spatialFilter": {
                        "geoJson": {
                            "type": "Point",
                            "coordinates": [-96, 43]
                        },
                        "filterType": "geojson"
                    }
                }
            },
            {
                "datasetName": "landsat_ot_c2_l1",
                "sceneFilter": {
                    "spatialFilter": {
                        "geoJson": {
                            "type": "Point",
                            "coordinates": [-100, 40]
                        },
                        "filterType": "geojson"
                    }
                }
            }
        ]
    }                  
    
    print("Creating a search request...\n")
    response = sendRequest(serviceUrl + "scene-search-create", searchCreatePayload, apiKey)
    if response['errorCode'] == None:
        searchId = response['data']
    else:
        sys.exit()
    print(f"Search {searchId} created\n")

    # Scene-search-execute - skip this step if autoExecute is true in scene-search-create
    searchExecutePayload = {
        "searchId": searchId,
        "enableSpatialAggregates": False,
        "refreshResults": True,
        "resultsPerPage": 100
    }
    
    print("Processing the search request...\n")
    response = sendRequest(serviceUrl + "scene-search-execute", searchExecutePayload, apiKey)
    if response['errorCode'] != None:
        sys.exit()

    # Scene-search-summary
    searchSummaryPayload = {
        "searchId": searchId,
        'maxWaitTime': 10,
        "temporalSummaryMask": "YYYY"
    }
    
    print("Getting the search results summary...\n")
    response = sendRequest(serviceUrl + "scene-search-summary", searchSummaryPayload, apiKey) 
    if response['errorCode'] == 'SEARCH_UNAVAILABLE':        
        retryNumber = 0
        while retryNumber < 15 and response['errorCode'] == 'SEARCH_UNAVAILABLE':
            print("Waiting for the search results summary...\n")
            time.sleep(5)
            print("Getting the search results summary...\n")            
            response = sendRequest(serviceUrl + "scene-search-summary", searchSummaryPayload, apiKey)
            retryNumber += 1
        
        if retryNumber == 15:
            print("Search was unavailable - reached max retry count\n")
            sys.exit()
            
    if response['errorCode'] != None:
        sys.exit()
        
    summary = response['data']    
    
    for datasetSummary in summary['datasetSummary']:
        print(f"Find {datasetSummary['numberResults']} products in dataset {datasetSummary['datasetName']}\n")
    
    # The details of scene-search-summary response can be found here: https://m2m.cr.usgs.gov/api/docs/reference/#scene-search-summary
    totalPages = summary['totalPages']
     
    # Iterate over every page of results
    for page in range(totalPages):       
        # Scene-search-results
        searchResultsPayload = {
            "searchId": searchId,
            'maxWaitTime': 10,
            "pageNumber": page + 1
        }
        
        print(f"\nGetting search results on page {page + 1}...\n")
        response = sendRequest(serviceUrl + "scene-search-results", searchResultsPayload, apiKey)
        if response['errorCode'] != None:
            sys.exit()        
        results = response['data']['results']
        
        for result in results:
            # The details of scene-search-results response can be found here: https://m2m.cr.usgs.gov/api/docs/reference/#scene-search-results
            print (result['entityId'])
            # TODO: get you want with the product
            
    # If update the search request
    print("\nUpdating the search request...\n")
    searchUpdatePayload = {
        "searchId": searchId,
        "autoExecute": False, # If set to true, the search will automatically execute after saving the filters (default = false)
        "clearExisting": True, # If set to true, all existing filters will be replaced by this content. If set to false, the input is appended to the current filters. (default = false)
        "metadataConfig": None,
        "resultsPerPage": 100,
        "compareListName": "test-compare",
        "excludeListName": "test-exclude",
        "sceneDatasetFilters": [
            {
                "datasetName": "gls_all",
                "sceneFilter": {
                    "spatialFilter": {
                        "geoJson": {
                            "type": "Point",
                            "coordinates": [-98, 45]
                        },
                        "filterType": "geojson"
                    }
                }
            }
        ]
    }
    
    response = sendRequest(serviceUrl + "scene-search-update", searchUpdatePayload, apiKey)
    if response['errorCode'] != None:
        sys.exit()
    
    print("Processing the search request...\n")
    sendRequest(serviceUrl + "scene-search-execute", searchExecutePayload, apiKey)

    # Scene-search-summary
    searchSummaryPayload = {
        "searchId": searchId,
        'maxWaitTime': 10,
        "temporalSummaryMask": "YYYY"
    }
    
    print("Getting the search results summary...\n")
    response = sendRequest(serviceUrl + "scene-search-summary", searchSummaryPayload, apiKey)
    if response['errorCode'] == 'SEARCH_UNAVAILABLE':        
        retryNumber = 0
        while retryNumber < 15 and response['errorCode'] == 'SEARCH_UNAVAILABLE':
            print("Waiting for the search results summary...\n")
            time.sleep(5)
            print("Getting the search results summary...\n")            
            response = sendRequest(serviceUrl + "scene-search-summary", searchSummaryPayload, apiKey)
            retryNumber += 1
        
        if retryNumber == 15:
            print("Search was unavailable - reached max retry count\n")
            sys.exit()
            
    if response['errorCode'] != None:
        sys.exit()
        
    summary = response['data'] 
    
    for datasetSummary in summary['datasetSummary']:
        print(f"Find {datasetSummary['numberResults']} products in dataset {datasetSummary['datasetName']}\n")
    
    # The details of scene-search-summary response can be found here: https://m2m.cr.usgs.gov/api/docs/reference/#scene-search-summary
    totalPages = summary['totalPages']    
     
    # Iterate over every page of results
    for page in range(totalPages):       
        #   Scene-search-results
        searchResultsPayload = {
            "searchId": searchId,
            'maxWaitTime': 10,
            "pageNumber": page + 1
        }
        
        print(f"\nGetting search results on page {page + 1}...\n")
        response = sendRequest(serviceUrl + "scene-search-results", searchResultsPayload, apiKey)
        if response['errorCode'] != None:
            sys.exit()
        results = response['data']['results']
        
        for result in results:
            # The details of scene-search-results response can be found here: https://m2m.cr.usgs.gov/api/docs/reference/#scene-search-results
            print (result['entityId']) 
            # TODO: get you want with the product
                
    # Logout so the API Key cannot be used anymore
    endpoint = "logout"  
    if sendRequest(serviceUrl + endpoint, None, apiKey) == None:        
        print("Logged Out\n")
    else:
        print("Logout Failed\n")