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
Application is designed to be auto generated on the base of JSON files. In order to achieve auto-generated result files go to `proxy/parsers` and generate desired files.

### Dodawanie nowego serwisu (package)

Nowy „package” w tym projekcie to **nowy serwis SOME/IP** zdefiniowany w `system_definition/`. Na jego podstawie generowany jest kod backendu (proxy + API) i dane frontendu (Flutter).

#### Krok 1 — Definicja w `system_definition`

Utwórz katalog z plikami JSON, wzorując się na istniejących serwisach, np. `system_definition/someip/engine_service/`.

**`service.json`** — główna definicja serwisu:

```json
{
    "include": [],
    "package": "srp.apps",
    "someip": {
        "EngineService": {
            "service_id": 518,
            "major_version": 1,
            "minor_version": 0,
            "methods": { ... },
            "events": { ... }
        }
    }
}
```

| Pole | Co ustawić | Dlaczego |
|------|------------|----------|
| `package` | Namespace logiczny, np. `srp.apps`, `srp.env` | Grupuje definicje w systemie; musi być spójny z powiązanymi plikami `*_data_type.json` w tym samym obszarze (oxidizer EC, FC itd.) |
| `someip.<NazwaSerwisu>` | Unikalna nazwa klasy serwisu, np. `EngineService` | Z niej powstają pliki `engineservice.py`, `engineservice_dataclass.py`, namespace API `/engineservice` |
| `service_id` | ID z definicji ECU | Musi odpowiadać ID serwisu na docelowym komputerze — inaczej Service Discovery nie znajdzie ECU |
| `methods` / `events` | ID, typy wejścia/wyjścia | Określają REST endpointy (`POST /serwis/metoda`) i eventy Socket.IO |

Jeśli serwis używa złożonych struktur danych, dodaj też plik `*_data_type.json` w tym samym katalogu (wzór: `sys_stat_data_type.json`).

#### Krok 2 — Generowanie kodu backendu

Uruchamiaj skrypty z aktywnym venv, z katalogu głównego projektu. **Przed uruchomieniem** ustaw ścieżkę do `system_definition/someip` w bloku `if __name__ == "__main__"` każdego parsera (domyślnie w repo mogą być stare ścieżki):

```python
process_directory(Path(__file__).resolve().parent / "../../system_definition/someip")
```

**1. Generating dataclasses** (`proxy/parsers/json_to_dataclass.py`):
- generuje `proxy/app/dataclasses/<serwis>_dataclass.py` i `structs.py`
- po generacji sprawdź importy i typy

**2. Generating services** (`proxy/parsers/json_to_service_class.py`):
- generuje `proxy/app/services/<serwis>.py` (manager SOME/IP)
- **automatycznie inkrementuje `NEXT_PORT`** w `proxy/app/config.json` — każdy nowy serwis dostaje kolejny port UDP lokalny (10319, 10320, …)
- po generacji zweryfikuj przypisany port w wygenerowanym pliku

**3. Generating APIs** (`proxy/parsers/gen_api.py`):
- dodaj import nowego `*Manager` do listy `manager_classes`
- uruchom skrypt — generuje `api/<serwis>/router.py` i `api/<serwis>/socketio.py`

#### Krok 3 — Podpięcie w `api/app.py`

Dla każdego nowego serwisu:

```python
from api.<serwis>.router import router as <serwis>_router
from api.<serwis>.socketio import register_<serwis>_socketio
from proxy.app.services.<serwis> import initialize_<serwis>
```

Następnie:
1. `app.include_router(<serwis>_router)` — tylko jeśli serwis ma metody (router)
2. `register_<serwis>_socketio(sio)` — jeśli serwis ma eventy
3. Dodaj `async def run_<serwis>(sd): await initialize_<serwis>(sd)`
4. W `lifespan` dodaj `asyncio.create_task(run_<serwis>(sd_instance))` oraz obsługę `cancel` przy shutdown

#### Krok 4 — Frontend (Flutter)

1. W `desktop/lib/generate/generate_data.dart` ustaw ścieżkę do `system_definition/someip`
2. Uruchom **sam plik** (`dart run desktop/lib/generate/generate_data.dart`), nie cały projekt
3. Skopiuj wyjście z konsoli
4. Wklej mapę serwisu do `desktop/lib/views/home.dart` i dodaj `ServiceWidget`:

```dart
ServiceWidget(
  serviceName: engineService['serviceName'],
  serviceId: engineService['serviceId'],
  methods: engineService['methods'],
  events: engineService['events'],
),
```

Maksymalnie 2 widgety w rzędzie; między rzędami `SizedBox(height: 10)`.

#### Krok 5 — Docker / nginx (jeśli używasz kontenerów)

Po dodaniu serwisu z metodami lub eventami dopisz jego namespace (małymi literami) do regex w `desktop/nginx/nginx.conf.template`, np.:

```
location ~ ^/(engineservice|...|nowyserwis|save)(/.*)?$ {
```

Bez tego nginx nie przekieruje ruchu API/WebSocket do proxy i UI nie połączy się z nowym serwisem.

#### Krok 6 — Weryfikacja

- Uruchom backend i sprawdź logi w `logs/`
- Dla testów lokalnych bez ECU: `proxy/app/testing/` (dostępne mocki engine i env)
- Pamiętaj: **brak walidacji typów** na wejściu metod — podawaj poprawne typy zgodnie z `service.json`

---

**Adjusting server**

- Create virtual environment in srp-app directory, activate it and install requirements.txt

### Konfiguracja sieci i proxy

Proxy komunikuje się z ECU wyłącznie przez **UDP** (multicast Service Discovery + unicast metody/eventy). Konfiguracja steruje tym, na jakim interfejsie i adresach nasłuchuje proces Pythona.

#### Uruchomienie lokalne (bez Dockera)

Edytuj `proxy/app/config.json`:

| Parametr | Przykład | Co robi | Dlaczego to ustawić |
|----------|----------|---------|---------------------|
| `MULTICAST_GROUP` | `224.224.224.245` | Adres multicast SOME/IP SD | Musi być zgodny z siecią ECU i biblioteką someipy |
| `INTERFACE_IP` | `192.168.10.49` | IP interfejsu, na którym proxy binduje porty UDP (10319–10335) | **Najważniejszy parametr** — ustaw IP maszyny (np. RPi) w sieci, w której siedzą ECU |
| `INTERFACE_IP_FINAL` | `10.101.0.1` | Zarezerwowane na przyszłość | Obecnie nieużywane w kodzie, można zostawić domyślne |
| `SD_PORT` | `30490` | Port Service Discovery | Standardowy port SOME/IP SD |
| `NEXT_PORT` | `10260` | Licznik portów dla generatora serwisów | Inkrementowany automatycznie przez `json_to_service_class.py`; ręczna zmiana potrzebna tylko przy konfliktach portów |

**Przed startem** na hoście (wymagane przez someipy):

```bash
sudo ip addr add 224.224.224.245 dev lo autojoin
```

Dla testów dwóch instancji na jednej maszynie:

```bash
sudo ip addr add 127.0.0.2/24 dev lo
```

#### Uruchomienie przez Docker

Konfiguracja jest w `docker-compose.yml` (sekcja `proxy.environment`). Wartości można nadpisać plikiem `.env` w katalogu projektu:

```env
INTERFACE_IP=192.168.10.49
MULTICAST_GROUP=224.224.224.245
SD_PORT=30490
DESKTOP_PORT=8080
```

| Parametr | Domyślnie | Dlaczego |
|----------|-----------|----------|
| `INTERFACE_IP` | `192.168.10.49` | W trybie `network_mode: host` proxy używa interfejsów hosta — ustaw IP RPi w LAN ECU |
| `MULTICAST_GROUP` | `224.224.224.245` | Używany też w entrypoincie kontenera do dodania adresu na `lo` |
| `SD_PORT` | `30490` | Port SOME/IP Service Discovery |
| `NEXT_PORT` | `10260` | Dla generatorów kodu; w runtime nie jest krytyczny |
| `DESKTOP_PORT` | `8080` | Port nginx z aplikacją Flutter web |

**Dlaczego proxy ma `network_mode: host`?**  
SOME/IP wymaga UDP multicast na fizycznym interfejsie. W sieci bridge Dockera multicast do ECU zwykle nie działa poprawnie. Kontener desktop pozostaje w sieci bridge i proxuje API do `host.docker.internal:5000`.

**Wolumeny:**
- `./desktop/data/csv` — zapis danych CSV z przycisku „Save Data”
- `./logs` — logi błędów aplikacji

- Verify server and desktop app are communicating via the same address (lokalnie: `localhost:5000`; Docker: UI na porcie 8080, API proxowane przez nginx)

**Running application**

#### Lokalnie (Makefile)

```bash
# Backend + web przez nginx systemowy
make run-all

# Backend + natywna aplikacja Linux
make run-all-desktop

# Tylko backend (API na :5000)
make run-proxy
```

#### Docker

```bash
docker compose up --build -d
```

- **UI:** `http://<IP-hosta>:8080`
- **API bezpośrednio:** `http://<IP-hosta>:5000`

Aplikacja web w kontenerze łączy się z API przez nginx (ten sam origin). Przy developmencie poza Dockerem domyślny adres API to `http://localhost:5000` (`desktop/lib/services/base.dart`).


**Additional informations:**  
Saved data is in desktop/data/csv/data.csv . Verify it is saving correctly, as saving is done as a background task with yield so data shall appear already while saving.

To perform testing go to app/testing. Only tests for engine and env are added. Run server, test files and desktop. 

Remember there is no type checking for method’s input so pay attention.

