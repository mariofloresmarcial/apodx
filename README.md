# APODx (Astronomy Photo of the Day Extended)

A microservice written in Python with the [Flask micro framework](https://flask.palletsprojects.com/en/2.3.x/). A SQL database holds [APOD](https://apod.nasa.gov/apod/astropix.html) entries.


## Docs
### Endpoint: `/<version>/apod`
There is only one endpoint in this service which takes 16 optional fields as parameters to a http GET request. A JSON dictionary is returned. 
#### URL Search Params | quey string parameters
- `api_key` A key needed to access the service. Can be saved locally or in a database.
- `search_term` A string containing the term to be searched. Can be omitted to search all entries.
- `search_title` A boolean `True|False` whether to search the `search_term` in the title field of an APOD entry.  Will default to `True` if omitted.
- `search_expl` A boolean `True|False` whether to search the `search_term` in the explanation field of an APOD entry. Will default to `False` if omitted.
- `search_copyright` A boolean `True|False` whether to search the `search_term` in the copyright field of an APOD entry. Will default to `False` if omitted.
 - `search_keywords` A boolean `True|False` whether to search the `search_term` in the keywords field of an APOD entry. Will default to `False` if omitted.
 - `search_inst` A boolean `True|False` whether to search the `search_term` in the instrument field of an APOD entry. Will default to `False` if omitted.
- `img_width` A positive integer, determines the minimum width of an image to search. Defaults to `0` if omitted.
- `img_height` A positve integer, determines the minimum height of an image to search. Defaults to `0` if omitted.
- `img_width2` A positive integer, determines the maximum width of an image to search. Defaults to `9999` if omitted.
- `img_height2` A positve integer, determines the maximum height of an image to search. Defaults to `9999` if omitted.
- `date` A string in YYYY-MM-DD format indicating the date of the APOD entry (example: 2022-12-25). Defaults to today's date if omitted. Must be between 1995-06-16 and today.
- `date_rec` A boolean `True|False` whether to return all recurring dates in database. Must be used with `date`.
- `start_date` A string in YYY-MM-DD format indicating the start of a date range date. All entries in the range from `start_date` to `end_date` will be returned in a JSON array. Cannot be used with `date`.
- `end_date` A string in YYYY-MM-DD format indicating the end of a date range. If `start_date` is specified without an `end_date` then `end_date` will default to today's date. 
- `media_type` A string `image|video` indicating the media type of APOD entries to search.
- `count` A positive integer, no greater than 365. If this is specified, returns `count` number of random APOD entries. Cannot be used with any other parameter.

**Returned fields**

- `apod_copyright` The name of the copyright holder.
- `apod_date` Date of the APOD entry.
- `apod_explanation` The supplied text explanation of the entry.
- `apod_hd_img` The URL for any high-resolution image for that day.
- `apod_img` The URL of the APOD image or video of the day.
- `apod_img_height` The image height in pixels.
- `apod_img_type` The image format type.
- `apod_img_width` The image width in pixels.
- `apod_media_type` The type of media returned. May be 'image' or video'
- `apod_title` The title of the APOD entry.
- `apod_version` The service version used.
- `instrument_name` The name of the instrument used to capture the APOD image. Will be 'none' if not determined.
- `word1` First keyword associated with the APOD entry.
- `word2` Second keyword associated with the APOD entry.
- `word3` Third keyword associated with the APOD entry.
- `word4` Fourth keyword associated with the APOD entry.

**Example** 

```bash
localhost:5000/v1/apod?api_key=DEMO_KEY&date=2022-12-25
```
<details><summary>See Return Object</summary>
<p>

```jsoniq
[
	{
		"apod_copyright":"Chuck Derus","apod_date":"Sun, 25 Dec 2022 00:00:00 GMT",
		"apod_explanation":"Asteroid 3200 Phaethon's annual gift to planet Earth always arrives in December. 	Otherwise known as the Geminid meteor shower, the source of the meteroid stream is dust shed along the orbit of the mysterious asteroid. Near the December 13/14 peak of the shower's activity, geminid meteors are captured in this night skyscape, composited from 22 images of starry sky taken before the moon rose over Monument Valley in the American southwest. The bright stars near the position of the shower's radiant are the constellation Gemini's twin stars Castor (blue) and Pollux (yellow). As Earth sweeps through the dusty stream, the parallel meteor trails appear to radiate from a point on the sky in Gemini due to perspective, and so the yearly shower is named for the constellation. From the camera's perspective, this view of three prominent buttes across Monument Valley also suggests appropriate names for two of them. The third one is called Merrick Butte.",
		"apod_hd_img":"https://apod.nasa.gov/apod/image/2212/J7A6402-Edit-copy-sharpened.jpg",
		"apod_img":"https://apod.nasa.gov/apod/image/2212/J7A6402-Edit-copy-sharpened1024.jpg",
		"apod_img_height":1365,
		"apod_img_type":"jpg",
		"apod_img_width":2048,
		"apod_media_type":"image",
		"apod_title":"Geminids and the Mittens",
		"apod_version":"v1",
		"instrument_name":"Unknown",
		"word1":"shower",
		"word2":"perspective",
		"word3":"gemini",
		"word4":"constellation"
	}
]
```

</p>
</details>
