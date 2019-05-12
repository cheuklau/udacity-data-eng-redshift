# Data Warehouse

## Purpose

A music streaming startup, Sparkify, has their data in Amazon S3. The data is contained in two directories:
1. Directory of JSON metadata for the songs in their app, and
2. Directory of JSON logs on user activity in their app.

The goal of this project is to build an ETL pipeline to:
- Extract data from S3,
- Stage data in Redshift, and
- Transform data into a set of dimensional tables in Redshift.

The final tables will be used by Sparkify's analytics team to gain insight into the songs that their users are listening to.

## Dataset

The first [dataset](s3://udacity-dend/song_data) contains the song data in JSON format. Files are partitioned by first three letters of each song's track ID e.g. `song_data/A/B/C/TRABCEI128F424C983.json`. Example of a single song file:
```
{
    "num_songs": 1, 
    "artist_id": "ARJIE2Y1187B994AB7", 
    "artist_latitude": null, 
    "artist_longitude": null, 
    "artist_location": "", 
    "artist_name": "Line Renaud", 
    "song_id": "SOUPIRU12A6D4FA1E1", 
    "title": "Der Kleine Dompfaff", 
    "duration": 152.92036, 
    "year": 0
}
```

The second [dataset](s3://udacity-dend/log_data) contains the log metadata. The log files are paratitioned by year and month e.g., `log_data/2018/11/2018-11-12-events.json`. Example entry in a log file:
```
{
    "artist": "Pavement",
    "auth": "Logged in",
    "firstName": "Sylvie",
    "gender": "F",
    "iteminSession": 0,
    "lastName": "Cruz",
    "length": 99.16036,
    "level": "free",
    "location": "Kiamath Falls, OR",
    "method": "PUT",
    "page": "NextSong",
    "registration": 1.540266e+12,
    "sessionId": 345,
    "song": "Mercy: The Laundromat",
    "status": 200,
    "ts": 1541990258796,
    "userAgent": "Mozzilla/5.0...",
    "userId": 10
}
```

## Schema for Song Play Analysis

The Redshift table we will create for the analytics team will be a star schema which is optimized for queries on song play analysis. The star schema contains the following fact and dimension tables:
1. `songplay` (fact) - records event data for each song play
    + `songplay_id`
    + `start_time`
    + `user_id`
    + `level`
    + `song_id`
    + `artist_id`
    + `session_id`
    + `location`
    + `user_agent`
2. `users` (dimension) - users in the app
    + `user_id`
    + `first_name`
    + `last_name`
    + `gender`
    + `level`
3. `song` (dimension) - songs in music database
    + `song_id`
    + `title`
    + `artist_id`
    + `year`
    + `duration`
4. `artist` (dimension) - artists in music database
    + `artist_id`
    + `name`
    + `location`
    + `lattitude`
    + `longtitude`
5. `time` (dimension) - timestamps of records in `songplays`
    + `start_time`
    + `hour`
    + `day`
    + `week`
    + `month`
    + `year`
    + `weekday`

## Redshift Cluster Description

Redshift cluster properties:
- Node type: `dc2.large`
- Number of nodes: 2
- Cluster identifier: `udacity-redshift`
- Database name: `dev`
- Database port: 5439
- Master username: `awsuser`
- IAM role: `myRedshiftRole`
    * Allows Redhshift to communicate with S3 with `AmazonS3ReadOnlyAccess` role
- Default VPC: `vpc-86cf25fe`
- Security group: `redshift_security_group`
    * Opens TCP port for all incoming traffic in order to connect with database

## ETL Pipeline

1. Create staging and final tables in Redshift: `python create_tables.py`
2. Copy data from s3 into Redshift staging tables: `python etl.py`
3. Insert data from staging into final tables in Redshift (already performed by running `etl.py` in step 2)
4. Verify final tables have correct data using Redshift query editor (see next section).

### Final Tables Verificaiton

We verified the final tables contain the correct data using Redshift query editor. Sample entries in `songplay`:
```
songplay_id,start_time,user_id,level,song_id,artist_id,session_id,location,user_agent
6,1543256734796,92,free,SONQBUB12A6D4F8ED0,ARFCUN31187B9AD578,938,Palestine, TX,Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0
22,1542824952796,97,paid,SOSMXVH12A58A7CA6C,AR6PJ8R1187FB5AD70,817,Lansing-East Lansing, MI,"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"
```

Sample entries in `users`:
```
user_id,first_name,last_name,gender,level
66,Kevin,Arellano,M,free
15,Lily,Koch,F,paid
```

Sample entries in `song`:
```
song_id,title,artist_id,year,duration
SOZCTXZ12AB0182364,Setanta matins,AR5KOSW1187FB35FF4,0,269.58322
SOBYAKJ12AB017C6E2,Broken (LP Version),ARAO91X1187B98CCA4,2002,259.91791
```

Sample entries in `artist`:
```
artist_id,name,location,latitude,longitude
ARL26PR1187FB576E5,Camera Obscura,Glasgow, Scotland,,
AR0WQ0N1187FB3AAB9,The Accüsed,,,
```

Sample entries in `time`:
```
start_time,hour,day,week,month,year,weekday
2018-11-02 01:25:34.000000,1,2,44,11,2018,2
2018-11-02 02:42:48.000000,2,2,44,11,2018,2
```