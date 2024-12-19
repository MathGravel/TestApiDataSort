# TestAPIDataSort

   TestAPIDataSort is a Python web server using the FASTAPI library for data sorting. Project made in order to fufill
   a technical test, the codebase takes a plain text file sent as a web request, or from memory, and sort the data to 
   return the identifiers of the most prominent data.

   The project was made to showcase general project and coding baselines. Thus, the architecture was made 
   in a minimalist, modular way, in order for the code to easily integrate in other FastAPI projects, without causing
   redundancies in authentification, deployment and security modules.


# Installation


   To install TestAPIDataSort on an Unix machine (Please note that the script should be modicied on MacOsx and Windows machine to modify the Anaconda library executable.):
    
    ```bash
    $ chmod +x installer.sh
    $ sh installer.sh
    ```

The installer shell script will install Anaconda to your machien and create a ready to use
    environnement for TestAPIDataSort.

If you wish to use the project without an Anaconda environement:

    ```bash
    $ pip install -r requirements.txt
    ```

Please take note that the project supports Python 3.11+

# Usage

(Please note that the usage shown here is for a local deployment. For deployment on Google cloud,
    please check their [`documentation`](https://cloud.google.com/sdk/gcloud/reference/app/deploy) for more details.)

    ```bash
    $ fastapi run 
    ```

The project loads a default database on startup, and its API can be contacted at the following routes:
- GET https:localhost:8000/**health**
    Simple route to confirm the app is correctly running.
- GET https:localhost:8000/**getValues/{nValues}**
    Route to return the top nValues from the currently loaded dataset.
- POST https:localhost:8000/**replaceDataset**
    Route to replace the current in memory dataset.
    The body content of the request must be a **.txt** file.
- POST https:localhost:8000/**uploadAndTreatFile/{nResponses}**
    Route to return the top nValues from the file sent in request, without replacing the dataset in memory.
    The body content of the request must be a **.txt** file.

# Tests

## Usage

The project uses the [`pyTest`](https://pytest.org) library for testing.

    ```bash
    $ pytest 
    ```

## Generate new tests

New test files can be generated using the **generator.py** module in the testFiles folder.

    ```console
    usage : python3 generator.py [nInstances] [BytesId] [BytesValue]

    positional arguments:
        nInstances          The number of key_value instances to generate in the test file.
        BytesId             The number of bytes used for the length of the random Id generation.
        BytesValue          The number of bytes used for the length of the random Value generation.
    ```
generator.py will save the test file generated as *test_(nInstances)_date_(current datetime).txt*

# Profiling

The project calls can be profiled using the **pyInstrument** library

    ```bash
    $ pyinstrument -m fastapi run 
    $ pyinstrument -m pytest 
    ```

Individual profiling calls for inner functions were chosen to be left out of the codebase at this stage of the project lifecycle, in order to keep the structure easy to read. An example of function profiling can be found as an extras in main.py by swapping the PROFILER global variable to True in **config.yaml**, which start a profiler at the level of each route.

# Project complexity

## Temporal complexity


- GET https:localhost:8000/**health**
    The route is done in O(1), since the call intercept the request and return an response without additional calculations.
- GET https:localhost:8000/**getValues/{nValues}**
    The route is done in O(C * mlogm), C being the number of cached files calculated at the start of the web server, or during the last call to **replaceDataset**, and m being the size of *nValues*. Since the program sort each sub-arrays of the dataset and simply retrieve the highest nValues of each file, and C being a fixed value of 10 in the current implementation, the temporal complexity is bounded by m and can be simplified to O(mlogm) when m is bigger than 10.

    Detailed explanation :
    The call receives the request and does request parameters validation, which are considered O(1). The program then call *default_data_treatment.get_Data(...)*, which can either return directly an response if the in-memory dataset was small O(1), or it calls *data_from_files(...)*. This call open an FileReader on each of the 10 cached sub-files, and reads nValues key_value pairs, which are stocked in an Heapq. The Heapq size is bounded to m, and each of its call is O(logm), which give us a global loop of O(mlogm).

- POST https:localhost:8000/**replaceDataset**
    The route is done in O(C * nlogn), with n being the number of elements in the dataset, and C being the number of sub-files created to stock the data. Since C is bounded to the range of {0..9}, as long as n is significatly higher than 10, we can simplify the complexity to O(nlogn).

    Detailed explanation :
    The call receives the request and does request parameters validation, which are considered O(1). The program then call *default_data_treatment.process_data(...)*, which can branch into two different functions, depending on the length of the file.
     The first one, process_entire_file(...), called when the file is small enough to be kept in memory, opens an file writer that read the entire file in linear O(n) time, and then transform the list into a heap, also in linear O(n) time. O(2n) = O(n)
     The second function, process_data_per_chunk(...), create C sub-files (with C bounded to 10), and iterate on the dataset file on O(n) to stock each key_value pair into an individual sub-files, based on their hash. The function then pass on each sub-files and apply a sort, done in O(nlogn), which gives us a complexity of O(n + C*nlogn) = O(c*nlogn)
     From the two branches, O(n) is bounded by O(c*nlogn), and thus the function is in O(C*nlogn)
- POST https:localhost:8000/**uploadAndTreatFile/{nResponses}**
    The route is done in O(nlogm), with n being the number of elements in the dataset, and m being the size of *nResponses*.

    Detailed explanation :
    The call receives the request and does request parameters validation, which are considered O(1). The program then create a new NumericalStructure class and then call *analysis.get_Data(...)* and process_entire_file(...) .
    process_entire_file does an iteration on the entire dataset in the input file, which is done in n operations. During this loop, the function input the current key_value pair inside a priority_queue with an max size of m. This maximum size makes it that each call to the queue is bounded in O(logm), since its spatial size cannot become bigger than m. Thus, the entire looping function is done on O(nlogm).
     
## Spatial complexity

- GET https:localhost:8000/**health**
    The route is done in O(1), since the call intercept the request and return an response without additional calculations.
- GET https:localhost:8000/**getValues/{nValues}**
    The route is done in O(m),m being the size of *nValues*. 

    Detailed explanation :
    The call receives the request and does request parameters validation, which are considered O(1). The program then call *default_data_treatment.get_Data(...)*, which can either return directly an response if the in-memory dataset size was small enough (Which then bounded the spatial memory to O(m), being the size of the sub-array returned), or it calls *data_from_files(...)*. This call open an FileReader on each of the 10 cached sub-files, and reads nValues key_value pairs, which are stocked in an Heapq. Since the reading of the file is done line per line, the memory usage is constant, with only the heapQ taking additional space holding the m values to be returned. Since the heapq is bounded to only keep at most m values at any times, the spatial memory of the fonction, and thus the entire call, is bounded by O(m).

- POST https:localhost:8000/**replaceDataset**
    The route is done in O(n), with n being the number of elements in the dataset.
    Detailed explanation :
    The call receives the request and does request parameters validation, which are considered O(1). The program then call *default_data_treatment.process_data(...)*, which can branch into two different functions, depending on the length of the file.
     The first one, process_entire_file(...), called when the file is small enough to be kept in memory, opens an file writer that read the entire file and then transform it into a heap to be stocked in memory. Each one of these calls will take O(n) space, which gives us O(3n) = O(n)
     The second function, process_data_per_chunk(...), create C sub-files (with C bounded to 10), and iterate on the dataset file on O(n) to stock each key_value pair into an individual sub-files, based on their hash, before sorting them. Since n is split to each instance of C, the calculation is brought back to taking O(n) space, and the conventional python list sort is considered to run in O(n) space.
     Since each branch takes O(n) space, each call to the function will run on O(n) space.
- POST https:localhost:8000/**uploadAndTreatFile/{nResponses}**
    The route is done in O(m), with n being the number of elements in the dataset, and m being the size of *nResponses*.

    Detailed explanation :
    The call receives the request and does request parameters validation, which are considered O(1). The program then create a new NumericalStructure class and then call *analysis.get_Data(...)* and process_entire_file(...) .
    process_entire_file does an iteration on the entire dataset in the input file, while only keeping the current line in memory O(1) space. During this loop, the function input the current key_value pair inside a priority_queue with an max size of m. This maximum size makes it that we do not keep more than m items in memory at any time during the execution, which bounds it to O(m). Thus this function is bounded to O(m) space.


# Future works
- Modify NumericalData getter functions to add more memoization caching.
- Add unit testing to NumericalStructure functions.
