# SIMPLE CRUD API WITH DJANGO REST FRAMEWORK
[Django REST framework](http://www.django-rest-framework.org/) is a powerful and flexible toolkit for building Web APIs.


In our case, we have one single resource, `boxes`, so we will use the following URLS - `/boxes/` and `/boxes/<id>` for collections and elements, respectively:

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`box` | GET | READ | Get all boxes
`boxes/:id` | GET | READ | Get a single box
`boxes`| POST | CREATE | Create a new box
`boxes/:id` | PUT | UPDATE | Update a box
`boxes/:id` | DELETE | DELETE | Delete a box
`my-boxes/` | GET | GET | get all my boxes

## Create users and Tokens

First we need to create a user, so we can log in
```
http POST https://spinny-dnui.onrender.com/auth/register/ email="email@email.com" username="USERNAME" password1="PASSWORD" password2="PASSWORD" is_staff = "True"/"False"
```

After we create an account we can use those credentials to get a token

To get a token first we need to request
```
http https://spinny-dnui.onrender.com/auth/token/ username="username" password="password"
```
after that, we get the token
```
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNjI5MjMyMSwianRpIjoiNGNkODA3YTlkMmMxNDA2NWFhMzNhYzMxOTgyMzhkZTgiLCJ1c2VyX2lkIjozfQ.hP1wPOPvaPo2DYTC9M1AuOSogdRL_mGP30CHsbpf4zA",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjA2MjIxLCJqdGkiOiJjNTNlNThmYjE4N2Q0YWY2YTE5MGNiMzhlNjU5ZmI0NSIsInVzZXJfaWQiOjN9.Csz-SgXoItUbT3RgB3zXhjA2DAv77hpYjqlgEMNAHps"
}
```
We got two tokens, the access token will be used to authenticated all the requests we need to make, this access token will expire after some time.
We can use the refresh token to request a need access token.

requesting new access token
```
http https://spinny-dnui.onrender.com/auth/token/refresh/ refresh="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYxNjI5MjMyMSwianRpIjoiNGNkODA3YTlkMmMxNDA2NWFhMzNhYzMxOTgyMzhkZTgiLCJ1c2VyX2lkIjozfQ.hP1wPOPvaPo2DYTC9M1AuOSogdRL_mGP30CHsbpf4zA"
```
and we will get a new access token
```
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE2MjA4Mjk1LCJqdGkiOiI4NGNhZmMzMmFiZDA0MDQ2YjZhMzFhZjJjMmRiNjUyYyIsInVzZXJfaWQiOjJ9.NJrs-sXnghAwcMsIWyCvE2RuGcQ3Hiu5p3vBmLkHSvM"
}
```


The API has some restrictions:
-   The boxes are always associated with a creator (user who created it).
-   Only authenticated users may create and see boxes.
-   Only the creator of a boxes may update or delete it.
-   The API doesn't allow unauthenticated requests.




### Commands
```
Get all boxes
http https://spinny-dnui.onrender.com/api/boxes/ "Authorization: Bearer {YOUR_TOKEN}" 
Get a single box
http GET https://spinny-dnui.onrender.com/api/boxes/{box_id}/ "Authorization: Bearer {YOUR_TOKEN}" 
Create a new box
http POST https://spinny-dnui.onrender.com/api/boxes/ "Authorization: Bearer {YOUR_TOKEN}" length=12 breadth=12
Full update a box
http PUT https://spinny-dnui.onrender.com/api/boxes/{box_id}/ "Authorization: Bearer {YOUR_TOKEN}" length=12 breadth=12
Delete a box
http DELETE https://spinny-dnui.onrender.com/api/boxes/{box_id}/delete "Authorization: Bearer {YOUR_TOKEN}"
Get all myBoxes
http GET https://spinny-dnui.onrender.com/api/my-boxes/ "Authorization: Bearer {YOUR_TOKEN}"
```

### Filters
The API supports filtering, you can filter by the attributes of a boxes like this
```
http https://spinny-dnui.onrender.com/api/boxes/?area__gt=43 "Authorization: Bearer {YOUR_TOKEN}"
http https://spinny-dnui.onrender.com/api/boxes/?volume__gt=432 "Authorization: Bearer {YOUR_TOKEN}"
http https://spinny-dnui.onrender.com/api/boxes/?length__lte=4 "Authorization: Bearer {YOUR_TOKEN}"
http https://spinny-dnui.onrender.com/api/boxes/?breadth__gt=423 "Authorization: Bearer {YOUR_TOKEN}"
```