## Group 1 - Basic functionality

### Configuration:
Run service without any data.

### Scenario 1 - No data at start
1. Send GET request for endpoint '/bear' -> Empty list is returned.

### Scenario 2 - 'Info' works fine
1. Send GET request for endpoint '/info' -> Service returns clear help page

### Scenario 3 - Add new bear **(?)**
1. Send POST request for endpoint '/bear' with data _"{"bear_type" : "BLACK" , "bear_name" : "Semen" , "bear_age" : 17.5}"_ -> No errors from the service and in the service logs.
1. Send GET request for endpoint '/bear' -> Servie returned list with same data, as you sent to the service plus 'bear_id' field **(?)**

**Actual result:** Service returned name in upper case: "SEMEN". But I added "Semen". But, looks like it is expected.

### Scenario 4 - Get list of bears
1. Send POST request for endpoint '/bear' with data _"{"bear_type" : "BROWN" , "bear_name" : "Boris" , "bear_age" : 16}"_ -> No errors from the service and in the service logs.
1. Send GET request for endpoint '/bear' -> Service returned list with data of two bears. Data should be the same, as we added it plus 'bear_id' field.

### Scenario 5 - Get one special bear **(?)**
1. Send GET request for endpoint '/bear/:1' -> Sevice returned data for bear Semen
1. Send GET request for endpoint '/bear/:2' -> Sevice returned data for bear Boris

**(?)** Info or interface is incorrect. I should send the request to the endpoint "/bear/1", without ':'.

### Scenario 6 - Update bear **(x)**
1. Send PUT request for endpoint '/bear/:2' with data _"{"bear_type" : "BROWN" , "bear_name" : "Boris" , "bear_age" : 17}"_ -> No errors from the service and in the service logs.
1. Send GET request for endpoint '/bear/:2' -> Sevice returned data for bear Boris with age 17 **(x)**
1. Send PUT request for endpoint '/bear/:2' with data _"{"bear_type" : "BROWN" , "bear_name" : "Boris Britva" , "bear_age" : 17}"_ -> No errors from the service and in the service logs.
1. Send GET request for endpoint '/bear/:2' -> Sevice returned data for bear with name 'Boris Britva'
1. Send PUT request for endpoint '/bear/:2' with data _"{"bear_type" : "POLAR" , "bear_name" : "Boris Britva" , "bear_age" : 17}"_ -> No errors from the service and in the service logs.
1. Send GET request for endpoint '/bear/:2' -> Sevice returned data for bear with type "POLAR" **(x)**

**Actual result:** bear's age and bear's type has not been modified, but requests are not failed

### Scenario 7 - Delete special bear
1. Send DELETE request for endpoint '/bear/:2' -> No errors from the service and in the service logs.
1. Send GET request for endpoint '/bear' -> Service returned list with bear Semen only.

### Scenario 8 - Delete all bears
1. Send DELETE request for endpoint '/bear' -> No errors from the service and in the service logs.
1. Send GET request for endpoint '/bear' -> Empty list is returned.

### Scenario 9 - Add bears of all available types **(x)**
1. Send POST request for endpoint '/bear' with data _"{"bear_type" : "BLACK" , "bear_name" : "Semen" , "bear_age" : 17.5}"_ -> No errors from the service and in the service logs.
1. Send POST request for endpoint '/bear' with data _"{"bear_type" : "BROWN" , "bear_name" : "Boris" , "bear_age" : 16}"_ -> No errors from the service and in the service logs.
1. Send POST request for endpoint '/bear' with data _"{"bear_type" : "POLAR" , "bear_name" : "Viktor" , "bear_age" : 13}"_ -> No errors from the service and in the service logs.
1. Send POST request for endpoint '/bear' with data _"{"bear_type" : "GUMMY" , "bear_name" : "Rita" , "bear_age" : 11}"_ -> No errors from the service and in the service logs.
1. Send GET request for endpoint '/bear' -> Service return list with 4 bears. Bears data are correct. **(x)**

**Actual result:** Data is corrupted for the bear "GUMMY"

## Group 2 - Error handling

### Configuration:
Run service without any data.

Restart service before every test scenario.

### Scenario 1 - incorrect endpoint
1. Add several bears to the service; 
1. Send GET request for endpoint '/wrong' -> Request failed, service returned '404 Not found' and wrote information to the log;
1. Send POST request for endpoint '/wrong' -> Request failed, service returned '404 Not found' and wrote information to the log;
1. Send PUT request for endpoint '/wrong' -> Request failed, service returned '404 Not found' and wrote information to the log;
1. Send DELETE request for endpoint '/wrong' -> Request failed, service returned '404 Not found' and wrote information to the log;
1. Send GET request for endpoint '/bear' -> Bears from the step #1 has not been corrupted; 

### Scenario 2 - Get unexisting bear
1. Send GET request for endpoint '/bear/:1' -> Service return string "EMPTY";
1. Add some bear to the service;
1. Send GET request for endpoint '/bear/:2' -> Service return string "EMPTY";
1. Add one more bear to the service;
1. Delete bear #1;
1. Send GET request for endpoint '/bear/:1' -> Service return string "EMPTY";
1. Send GET request for endpoint '/bear/:2' -> Service return correct data about bear #2;

### Scenario 3 - Update unexisting bear
1. Send PUT request for endpoint '/bear/:1' with some data -> Request failed, service returned error '500' and wrote information to the log (**(?)** I see NullPointrException. Maybe it is not good.)
1. Add some bear to the service;
1. Send PUT request for endpoint '/bear/:2' with some data -> Request failed, service returned error '500' and written information to the log;
1. Add one more bear to the service;
1. Delete bear #1;
1. Send PUT request for endpoint '/bear/:1' with some data -> Request failed, service returned error '500' and written information to the log;
1. Send PUT request for endpoint '/bear/:2' with some data -> Request failed, service returned error '500' and written information to the log;
1. Get list of bears -> service contains data about second updated bear only;

### Scenario 4 - Delete unexisting bear
1. Send DELETE request for endpoint '/bear/:1' -> Service returned message about error **(x)** (but service returned message OK)
1. Add some bear to the service;
1. Send DELETE request for endpoint '/bear/:2' -> Service returned message about error;
1. Get list of bears -> service still contains information about the first bear only;
1. Add one more bear to the service;
1. Send DELETE request for endpoint '/bear/:1' -> Service return "OK"
1. Send DELETE request for endpoint '/bear/:1' -> Service returned message about error;
1. Get list of bears -> service contains data about second updated bear only;

### Scenario 5 - Clean empty base
1. Send DELETE request for endpoint '/bear' -> Service returned "OK";
1. Get list of bears -> Service return empty list;

### Scenario 6 - Add bear of incorrect type
1. Send POST request for endpoint '/bear' with data _"{"bear_type" : "FLYING" , "bear_name" : "Batbear" , "bear_age" : 27}"_ -> Request is failed and returned text with error 500
1. Get list of bears -> Service return empty list;

### Scenario 7 - Add bear with unexpected fields **(x)**
1. Send POST request for endpoint '/bear' with data _"{"bear_type" : "BROWN" , "bear_name" : "Boris" , "bear_age" : 16, "gender" : "male" }"_ ->
Service stored field "gender" or request should be failed.
1. Get list of bears -> Service return bear with the field "gender" and correct other fields. **(x)**

**Actual result:** field "gender" just ignored. The service didn't save it and didn't write any warnings.

### Scenario 8 - Add bear with incorrect data type
1. Send POST request for endpoint '/bear' with data _"{"bear_type" : "BLACK" , "bear_name" : "Semen" , "bear_age" : "Very very old bear"}"_ -> 
Request failed, service returned error '500' and wrote information to the log

### Scenario 9 - Send modify request with incorrect bear type
1. Send POST request for endpoint '/bear' with data _"{"bear_type" : "BLACK" , "bear_name" : "Semen" , "bear_age" : 17.5}"_ -> No errors from the service and in the service logs.
1. Send PUT request for endpoint '/bear/1' with data _"{"bear_type" : "FLYING" , "bear_name" : "Batbear" , "bear_age" : 27}"_ -> Request is failed and returned text with error 500
1. Get list of bears -> Service return bear _"{"bear_type" : "BLACK" , "bear_name" : "Semen" , "bear_age" : 17.5}"_;

### Scenario 10 - Send modify request with unexpected fields **(x)**
1. Send POST request for endpoint '/bear' with data _"{"bear_type" : "BLACK" , "bear_name" : "Semen" , "bear_age" : 17.5}"_ -> No errors from the service and in the service logs.
1. Send PUT request for endpoint '/bear' with data _"{"bear_type" : "BROWN" , "bear_name" : "Boris" , "bear_age" : 16, "gender" : "male" }"_ ->
Service stored field "gender" or request should be failed.
1. Get list of bears -> Service return bear with field "gender" and correct other fields. **(x)**

**Actual result:** field "gender" just ignored. The service didn't save it and didn't write any warnings.

### Scenario 11 - Send modify request with incorrect data type
1. Send POST request for endpoint '/bear' with data _"{"bear_type" : "BLACK" , "bear_name" : "Semen" , "bear_age" : 17.5}"_ -> No errors from the service and in the service logs.
1. Send POST request for endpoint '/bear' with data _"{"bear_type" : "BLACK" , "bear_name" : "Semen" , "bear_age" : "Very very old bear"}"_ -> 
Request failed, service returned error '500' and wrote information to the log
1. Get list of bears -> Service return bear _"{"bear_type" : "BLACK" , "bear_name" : "Semen" , "bear_age" : 17.5}"_;

## Group 3 - Stress testing

_Improvement: We can define the speed of bears insertion (requests per second)_

### Configuration

Run service without any data.

### Scenario 1 - Add bears
1. Add at least 10000 bears through at least 10 processes without any delays -> All requests are accepted;
1. Get list of breas -> Service returned all inserted bears.

### Scenario 2 - Get bears
1. Take list of bears from the previous scenario and use 'bear_id' of these bears to get special bear by it from the service. Send request at least 50000 requests through at least 10 processes without any delays -> Service return correct bear for every request.

### Scenario 3 - Update bears
1. Take list of bears from the previous scenario and add random symbols to the names of every bear;
1. Increase or decrease age for every bear;
1. Change bear_type for every bear;
1. Send update requests through at least 10 processes for all bears -> All requests are accepted;
1. Get list of breas -> Service returned all bears with updated data.

### Scenario 4 - Update one bear
1. Take list of bears from the previous scenario and select one random bear;
1. Send all these bears as PUT request for the selected bear through at least 10 processes without any delays -> service didn't cash or hung. No errors in the logs.

 _We don't know, which update is come latest. So, we should make sure, that service is alive._

 ### Scenario 5 - Delete special bears
 1. Take half of bears from the previous scenario;
 1. Send delete requests for half of bears through at least 10 processes without any delays -> All requests are accepted;
 1. Get list of bears -> make sure that service didn't return deleted bears, but returned every remaining bear;

 ### Scenario 6 - Delete all bears
 1. Send DELETE request for endpoint '/bear' -> request is OK;
 1. Get list of bears -> Service returned empty list; 
