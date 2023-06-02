
The Traffic Manager

## Setup

To set up the Traffic Management System, follow the steps below:

1. Clone the repository:
```
git clone https://github.com/danrigoli/traffic-manager
```
2. Navigate to the project directory
```
cd traffic-manager
```
3. Install the required dependencies:
```
pip install -r api/requirements.txt
```
4. Navigate to the Darknet directory and build darknet:
> :warning: **You need to have g++ and gcc installed**
```
cd darknet
make
```
5. Run the app
```
cd ..
run api/app.py
```

-------

If you want to run darknet by itself:
```
./darknet detect cfg/yolov3.cfg yolov3.weights data/traffic.jpg
```

## Usage

### Detect Objects API

This API endpoint allows you to detect objects in an image. It accepts a POST request with an image file and returns the detected objects with their respective confidences.

**Endpoint:** `/detect-objects`
**Method:** POST

#### Request

- Form Data:
  - `image`: Image file to be processed (JPEG, PNG, or similar formats)

#### Response

The response will be in JSON format and include the following information:

- `bus`: A list of detected buses.
- `car`: A list of detected cars.
- `motorbike`: A list of detected motorbikes.
- `truck`: A list of detected trucks.

### Trigger API

This API endpoint lets you know if a semaphore should be triggered by its ID. It accepts a POST request with the semaphore ID and performs the calculations to manage the traffic light.

**Endpoint:** `/trigger-semaphore/{id}`
**Method:** POST

#### Request

- Path Parameter:
  - `id`: ID of the semaphore to trigger (integer)

#### Response

The response will be a message confirming if the semaphore with the specified ID should triggered.
