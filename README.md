# soc_network

# **This repo provides api of social network**

##Installation
`git clone git@github.com:PJeys/soc_network_api.git`

export application name to env

`export FLASK_APP=soc_network`

create secret key in file .env (example provided in soc_network folder)

install requirements

`pip3 install -r requirements.txt `

and then you can run an app

Endpoints:

New user registration:

`/api/register?email=EMAIL&password=PASSWORD`

email should be correct, and password length between 6 and 18 symbols

User login:

`/api/login?email=EMAIL&password=password`

response provides token, that should be passed in marked (token-required) requests in header as 'x-access-token'
token exp time = 30 minutes

Create post:

`/api/create_post?text=TEXT&media=MEDIA`

media - is not necessary field

Like post:

`/api/like_post?post_id=POST_ID`

Unlike post:

`/api/unlike_post?post_id=POST_ID`

Get stats about likes in some date period:

`/api/like_stats?date_from=DATE_FROM&date_to=DATE_TO`

date format is year-month-day

Get last user login and request:

`/api/user_stats?user_id=USER_ID`

you need to provide user public id to get response
