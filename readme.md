# Introduction to FastAPI ⚡
# What is an API? 
An API, or **Application Programming Interface**, is a set of rules and protocols that allows different software applications to communicate with each other. It defines the methods and data formats that applications can use to request and exchange information.

Think of it as an interface between your service and the outside world.

```
USERS <--> API <--> SERVICE
```

APIs are the backbone of most modern internet services.

**Examples of APIs:**
*   Sending sensors data from IoT devices to a server
*   Booking a flight ticket or hotel online
*   Retrieving weather information from an app
*   Accessing social media platforms
*   ...

APIs can range from very simple (like a calculator API) to highly complex (like the API for a major social media platform).

# FastAPI
FastAPI is a modern, high-performance web framework for building APIs with Python.

*   **Easy to learn:** Designed to be intuitive and straightforward.
*   **Fast to code:** Increases development speed significantly.
*   **High performance:** One of the fastest Python frameworks available, thanks to its asynchronous capabilities.

# 1. Installation
To get started, you need to install FastAPI and a server to run your application.

Open your terminal and run the following command:

```bash
pip install "fastapi[all]"
```

> **Note:** This command installs FastAPI, Uvicorn (a server to run your application), and other optional dependencies that are useful for production and development.

# 2. Create Your First App
Create a new Python file named `main.py` and add the following code:

```python
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# Define a route for the root URL ("/")
@app.get("/")
def read_root():
    return {"message": "Hello, World! :)"}
```

This code creates a simple API with a single endpoint (`/`) that responds to `GET` requests with a JSON message.

*   A `GET` request is used to retrieve data from the server. If you want to send data to the server, you typically use a `POST` request.
*   An endpoint is a specific URL where an API can be accessed by a client application (in this case, the root URL `/`).
*   JSON (JavaScript Object Notation) is a lightweight data-interchange format that is easy for humans to read and write, and easy for machines to parse and generate.

# 3. Run the Development Server
To run your app, use the Uvicorn server installed with FastAPI. In your terminal, navigate to the directory containing `main.py` and run:

```bash
uvicorn main:app --reload
```

*   `main`: The name of your Python file (`main.py`).
*   `app`: The `FastAPI` instance you created inside the file.
*   `--reload`: Automatically restarts the server whenever you make changes to the code.

You will see output similar to this, indicating the server is running:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [131532] using StatReload
INFO:     Started server process [133940]
INFO:     Application startup complete.
```

Since the server is running locally, you get a local IP address (`127.0.0.1`). For others to access your API, you would need to deploy it to a public server and provide them with the appropriate URL.

**Exercise:** Open your web browser and navigate to `http://127.0.0.1:8000` (or the IP address shown in the terminal). You should see the message: `{"message":"Hello, World! :)"}`.

# 4. Building a Shopping List API
Let's expand our application into a simple shopping list. We'll add endpoints to create, view, and retrieve items.

First, update `main.py` to include a shopping list to store our items.

```python
# List to store our shopping items
items = []
```

> [!IMPORTANT]
> Refreshing the server will reset the list because it is stored in memory. For persistent data, you could use a database.

### Create Items (POST)
To add a new item, we use the `POST` method. This endpoint will receive an item as a query parameter and add it to our list.

```python
@app.post("/items")
def create_item(item: str) -> list[str]:
    """Create a new item and add it to the items list."""
    items.append(item)
    return items
```

You can test this endpoint with a tool like `curl`. Curl is a command-line tool for making HTTP requests and is available on most operating systems. Type the following command in your terminal:

```bash
curl -X POST "http://127.0.0.1:8000/items?item=apple"
```

This command sends a `POST` request to the `/items` endpoint with a **query parameter** `item` set to `apple`. Query parameters are appended to the URL with a `?`. Multiple parameters can be added after each other using the `&` symbol.

This adds "apple" to the shopping list. The server should respond with the updated list of items as a JSON array: `["apple"]`. Due to the typehinting added to the `create_item` function, FastAPI will automatically validate that the `item` parameter is a string.

**Exercise:**
1. Add more items to the shopping list.
2. What happens if you send a number?
3. Set the typehints to `int` and try sending a string value. What happens?

### List All Items (GET)
To view all items, we'll create a `GET` endpoint that returns the entire list:

```python
@app.get("/items")
def list_items():
    """List all items in the items list."""
    return items
```
Then, test the endpoint:
```bash
curl "http://127.0.0.1:8000/items"
```

Now, let's add an optional query parameter `limit` that restricts the number of items returned. This can be done using the normal function parameter syntax in Python. Exchange the code for the `list_items` function with the following:

```python
@app.get("/items")
def list_items(limit: int | None = None) -> list[str]:
    """List all items in the items list. Optionally limit the number of items returned."""
    if limit is not None:
        return items[0:limit]
    return items
```

Test the endpoint with the `limit` parameter to get only a subset of items:
```bash
curl "http://127.0.0.1:8000/items?limit=2"

# It still works without the limit parameter
curl "http://127.0.0.1:8000/items"
```

### Get a Specific Item and Handle Errors
To retrieve a single item by its index, we can use a path parameter. Path parameters are part of the URL path itself.

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Get a specific item by its index."""
    return items[item_id]
```

Test the endpoint by requesting an item by its index:

```bash
# This will return the item at index 0
curl "http://127.0.0.1:8000/items/0"

# This will probably return an error, because the index is out of bounds
curl "http://127.0.0.1:8000/items/99"
```

If requesting an out-of-bounds index, FastAPI will return a `Internal Server Error`. This is not very user-friendly and does not provide useful information to the client. There are standard HTTP status codes that can indicate specific errors - take a look at them [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status). To handle this better, check if the index is valid before trying to access the item and raise a `404 Not Found` exception when the item does not exist.

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Get a specific item by its index."""
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

Try it again, and you should see a more informative error message.

# 5. Using Data and Response Models (Pydantic)
So far, we've been using simple data types like strings and integers for our items. However, in real-world applications, items often have multiple attributes. FastAPI uses Pydantic models to define complex data structures.

Let's define a model for a more detailed shopping item:

```python
from pydantic import BaseModel

class Item(BaseModel):
    """Data model for an item on a shopping list."""
    name: str
    description: str | None = None  # Optional field
    price: float
    quantity: int = 1               # Field with a default value
```

Now, let's update our `POST /items` endpoint to use this model by simply changing the function parameter to `item: Item`:

```python
@app.post("/items")
def create_item(item: Item):
    """Create a new item and add it to the items list."""
    items.append(item)
    return items
```

FastAPI will automatically parse a JSON request body and validate it against the `Item` model and enforce data types. Required fields (`name`, `price`) must be present while optional fields (`description`) can be omitted and default values (`quantity`) will be used if not provided.
To test this new endpoint, you can send a JSON payload in the request body:

```bash
curl -X POST "http://127.0.0.1:8000/items" \
-H "Content-Type: application/json" \
-d '{"name": "milk", "price": 3.50}'
```

You can also specify a `response_model` to ensure the data returned by your API conforms to a specific structure. This is useful for filtering out fields and ensuring consistent output.

Let's update our `GET /items` endpoint to specify that it returns a list of `Item` objects:

```python
# Update the list_items function signature
@app.get("/items", response_model=list[Item])
def list_items(limit: int | None = None):
    """List all items, with an optional limit."""
    if limit is not None:
        return items[0:limit]
    return items
```

# 6. Interactive Documentation
FastAPI automatically generates interactive API documentation for your application. There you can see all available endpoints, their methods, required parameters, and even test them directly from your browser. Check them out at:

*   **Swagger UI:** Navigate to `http://127.0.0.1:8000/docs`
*   **ReDoc:** Navigate to `http://127.0.0.1:8000/redoc`

These interfaces allow you to explore, test, and interact with your API endpoints directly from your browser.

# 7. Next Steps
This was just a basic introduction to FastAPI. There are many more features and capabilities to explore if you are interested, such as:

* Authentication and security
* Asynchronous programming
* Database integration
* Testing and debugging
* ...

# Exercise
Now it's your turn! Create a small project using FastAPI with a idea of your choice. Here are some suggestions/ideas:

**Project Ideas:**
*   **Book Library API:** Endpoints to add books, list books, borrow books, etc.
*   **Bank API:** Endpoints to create accounts, transfer money, check balances.
*   **Weather API:** Endpoints to get the current weather or a forecast for a city.
*   ...

**Helpful Resources:**
*   [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/)
*   [FastAPI Course for Beginners](https://www.youtube.com/watch?v=iWS9ogMPOI0)
*   [Building A Python CRUD API With FastAPI](https://www.youtube.com/watch?v=34cqrIp5ANg)
