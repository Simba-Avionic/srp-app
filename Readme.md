**Introduction**  
Application based on SimBa software fork of this library [https://chrizog.github.io/someipy/](https://chrizog.github.io/someipy/) .   
Allowing you to communicate with your ECUs via SOME/IP protocol. The application is designed to steer the engine and communicate with the computers of SimLE’s Orzeł 7 rocket. It is going to be used in the rocket’s static tests.

**Requirements:**

- Ubuntu  
- Python 3.12  
- Android Studio Dart and Flutter to make changes to the interface  
- Adjusting local network as said in someipy library, remember to do accordingly with the desired state

*sudo ip addr add 224.224.224.245 dev lo autojoin*

- If you want to run two application on the local machine: add another addresses to localhost interface  
  sudo ip addr add 127.0.0.2/24 dev lo




**General Information**  
Application is based on 3 layers each one is responsible for a different part of the communication allowing for robust data transmission.

### **1\. Proxy (Communicates with ECUs via SOME/IP):**

* **Role**: The Proxy interacts with the ECUs (Electronic Control Units) using the SOME/IP protocol. It sends requests and receives responses from ECUs over a network.  
    
* **Technology**: It communicates using **SOME/IP** (Scalable service-Oriented Middleware over IP) which is designed for automotive systems to allow distributed communication.  
    
* **Responsibilities**:  
  * Handles the SOME/IP protocol specifics.  
  * Interfaces with ECUs, making requests and handling responses.

  ### **2\. Server (Bridge between Proxy and User Interface):**

* **Role**: The Server acts as an intermediary between the Proxy and the User Interface (UI), providing an abstraction layer for easier communication. It ensures that the UI can interact with the Proxy without needing to understand the details of the underlying SOME/IP protocol.  
    
* **Technology**: The Server exposes a set of REST APIs for communication and utilizes **Socket.IO** for event-driven communication.  
    
  * **REST API**: The Server exposes **RESTful APIs** to handle synchronous communication with the UI. These are used for calling SOME/IP methods  
      
  * **Socket.IO**: The Server uses **Socket.IO** for asynchronous event-driven communication. This is used for handling SOME/IP events.  
      
* **Responsibilities**:  
  * Manages requests from the UI and forwards them to the Proxy using SOME/IP for method calls (via REST).  
  * Manages events from the Proxy (via SOME/IP) and communicates them to the UI using Socket.IO.

### **3\. User Interface (UI):**

Created with Flutter and Dart.

* The UI communicates with the Server using REST APIs for method calls and Socket.IO for real-time event communication.  
* It receives responses or events from the Server and presents them to the user.

**Parsing json files**  
Application is designed to be auto generated on the base of JSON files .In order to achieve auto-generated result files go to proxy/parsers and generate desired files:

**1\. Generating dataclasses:**   
Go to json\_to\_dataclass.py, verify that the path to system definition is right. Generate all the files automatically. In case of an issue generate each file by one one. Go to files after generation to verify if there are not any errors. Especially import errors

**2\.  Generating services:**  
	Analogically as dataclasses in every aspect. Remember to verify for errors

**3\. Generating apis:**  
Step 1: Go to gen\_api.py and generate each file one by one through manager import. Step 2: Verify for any potential errors in the created files.  
Step 3: Inside app.py import all generated: routers, socketio registers and initializers from the service files as in:

*from api.engineservice.socketio import register\_engineservice\_socketio*  
*from api.engineservice.router import router as engine\_router*   
*NAME THE ROUTER*  
*from proxy.app.services.engineservice import initialize\_engineservice*

	Step 4: Include new routers as in:  
app.include\_router(engine\_router)

Step 5: Register socketio namespaces as in:  
	*register\_engineservice\_socketio(sio)*

Step 6: Register manager runners:  
*async def run\_engine\_service\_manager(sd):*  
  	  *await initialize\_engineservice(sd)*

Step 7: Run managers as background tasks inside lifespan function:  
 *asyncio.create\_task(run\_engine\_service\_manager(sd\_instance))*

**4\. Adjusting frontend for changes**

1. Go to generate/generate\_data.dart and pass the correct file path.  
2. Run THE FILE, not the project  
3. Copy the output from the console  
4. Go to home.dart and paste the copied data  
       final Map\<String, dynamic\> engineService \= {  
         "serviceName": "Engine Service",  
         "serviceId": 518,  
         "methods": \[  
           {"name": "Start", "id": 1, "in\_type": "void"},  
           {"name": "SetMode", "id": 2, "in\_type": "uint8"},  
         \],  
         "events": \[  
           {"name": "CurrentMode", "id": 32769},  
         \],  
       };  
     
5. Create a new service widget and add it to the home widget. Max two per row, separate rows with sizedbox of height 10px

                ServiceWidget(  
                  serviceName: engineService\['serviceName'\],  
                  serviceId: engineService\['serviceId'\],  
                  methods: engineService\['methods'\],  
                  events: engineService\['events'\],  
                ),

**Adjusting server**

- Create virtual environment in srp-app directory, activate it and install requirements.txt  
- To assign ports and ip address go to config.jsons  
- Verify server and desktop app are communicating via the same IP address

**Running application**  
After successfully adjusting the server. Run the server and the desktop application separately

**Additional informations:**  
Saved data is in desktop/data/csv/data.csv . Verify it is saving correctly, as saving is done as a background task with yield so data shall appear already while saving.

To perform testing go to app/testing. Only tests for engine and env are added. Run server, test files and desktop. 

Remember there is no type checking for method’s input so pay attention.

