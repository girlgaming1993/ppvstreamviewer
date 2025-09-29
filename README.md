if you want to remake .exe on windows:

make sure you have python installed (currently using 3.13.7 for this)
CMD in folder with app.py in it:
  py -m pip install --upgrade pip
  py -m pip install flask requests pyinstaller
  py -m PyInstaller app.py --name StreamsViewer --onefile --add-data "templates;templates"

then use .exe in "dist\StreamsViewer.exe"




IN CASE OF ERRORS:::

-make sure the website (ppv.to) is up, if not, look for alternative ppv site
-make sure port 5000 is open
-make sure the api hasn't changed. pasted below:
thats all i got lol


~~~~~~~~~~~~~~ppv api~~~~~~~~~~~~~~~~~

GET /api/streams
Response structure
The response from this endpoint provides detailed information about various streams within their categories, structured like the below:

success (boolean): Indicates if the request was successful.
timestamp (integer): Unix timestamp of when the response was generated.
READ_ME (string): A message prompting interested parties to contact for further API usage details.
performance (float): A performance metric, possibly indicating API response time or efficiency.
streams (array): An array containing objects for different categories:
Stream category object
category (string): Name of the category (e.g., "Basketball", "Combat Sports").
id (integer): Unique identifier for the category.
always_live (integer): Flag to indicate if this category is always live (0 = no, 1 = yes).
streams (array): List of individual stream objects within the category:
Stream object
id (integer): Unique identifier for the stream.
name (string): Name or title of the event or stream.
tag (string): A tag or broadcaster label for the stream.
poster (string): URL for the promotional image of the stream.
uri_name (string): URL-friendly name used in the stream's URI.
starts_at (integer): Unix timestamp indicating when the stream starts.
ends_at (integer): Unix timestamp indicating when the stream ends.
always_live (integer): Indicates if the stream is always live (0 = no, 1 = yes).
category_name (string): The category name this stream belongs to.
iframe (string): The iframe you will use to embed. In this case, contacting specific stream endpoint is not required. If this value isn't present, we have not added it yet.
allowpaststreams (integer): Indicates if past streams are allowed to be viewed (0 = no, 1 = yes).
Example response

  {
    "success": true,
    "timestamp": 1734299469,
    "READ_ME": "Interested in using our API? Contact us for more information.",
    "performance": 3.15,
    "streams": [
      {
        "category": "Basketball",
        "id": 37,
        "always_live": 0,
        "streams": [
          {
            "id": 2940,
            "name": "Pelicans at Pacers",
            "tag": "Local Broadcast",
            "poster": "https://cdn.nba.com/manage/2024/12/nop-@-ind-12_15_2024-game-card-16_9.png",
            "uri_name": "nba-reg/week-8/nop-ind",
            "starts_at": 1734300000,
            "ends_at": 1734310800,
            "always_live": 0,
            "category_name": "Basketball",
            "allowpaststreams": 0
          },
          // ... Additional streams
        ]
      },
      // ... Additional categories
    ]
  }
 
Notes
The always_live and allowpaststreams fields are binary indicators where 1 means true and 0 means false.
Time-related fields (starts_at, ends_at, timestamp) are in Unix timestamp format.
The uri_name should be used to construct URLs for accessing specific streams or for API calls related to that stream.
Usage
Use the uri_name to fetch detailed information or access specific streams.
For real-time or scheduled streams, ensure your client application can handle timestamp conversions if needed. The ideal timing to poll this endpoint for changes is every 1 minute.
The poster URL can be used to display promotional images in user interfaces.
Limits
Can be used on other sites (Access-Control-Allow-Origin: *)
Can be used on a backend/server side generated webpage. Do not poll the endpoint each time your site is loaded. Setup caching within your local application to avoid hammering our API.
And cannot alter the functionality of our embeds, including advertisements from our embed platform. Infringers will be blocked. Includes sandboxing attempts. We will rape you.
This documentation outlines the structure and expected use of the response from the /api/streams endpoint. Remember to handle the API response appropriately in your application, particularly with regards to time management and image handling.
