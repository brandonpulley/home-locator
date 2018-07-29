## Dependencies

[Docker](https://www.docker.com/get-docker)
[docker-compose](https://docs.docker.com/compose/install/)

## Run the server

First build your image locally
```
$ docker-compose build
```

Then run your container
```
$ docker-compose up
```

## Query

When running locally you can POST to /query endpoint of localhost on port 8080
```
http://localhost:8080/query
```
body
```
{
  "visits": [
	{
		"lat": 45.12355,
		"lon": -118.12345,
		"arrival_time": "5/29/2015 7:12:35",
		"departure_time": "5/30/2015 20:12:35"
	},
	{
		"lat": 45.12355,
		"lon": -118.12345,
		"arrival_time": "6/28/2015 7:12:35",
		"departure_time": "6/30/2015 20:12:35"
	}
  ]
}
```