# Project Userify

A Django based backend implementation of a login system which can be interacted with through an JSON based rest-api.

## API Guide

* getusers/                     -> [Admin Authenticated] An admin accisble url to get info of all users. [HTTP: GET]
* signup/                       -> A url used to create new user. [HTTP: POST]
* send-otp/                     -> A url used to send otp to the user email for given user. [HTTP: POST]
* verify-otp/                   -> A url to verify the above sent otp (validity = 300 seconds). [HTTP: POST]
* login/                        -> A url used to login and start session for a user.
* logout/                       -> A url used to logout from a session.
* update-user/<str:username>/   -> [User Authenticated] A url used to update the information for a user. [HTTP: PUT]
* get-user/<str:username>/      -> [User Authenticated] A url used to get user information for a user. [HTTP: GET]
* del-user/<str:username>/      -> [User Authenticated] A url used to delete a user. [HTTP: DELETE]
* token/refresh/                -> A url used to refresh access tokens for a session.

## Environment Setup Instructions

Please use a gmail address which has less [secure apps](https://support.google.com/a/answer/6260879) turned on and add the email and password to environment variables DEV_MAIL and DEV_MAIL_PASS for the otp system to work.
