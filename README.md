# Authentication-Microservice

This microservice provides a well-rounded user authentication functionality to any application using this service. This service uses Django REST Framework for API development.

## Installation

- Clone the repository and navigate to the project root folder.
- Create an environment and install the required packages using pip.
  `pip install -r requirements.txt`
- Run the database migrations and start your server
  `python manage.py migrate
python manage.py runserver`

## API Endpoints

- `POST /user/register/`

  Registers a new user with the provided user details. Sends an OTP to the registered email address for verification.

- `POST /user/register/staff/`

  Registers a new staff or admin user with the provided details. Sends an OTP to the registered email address for verification. Staff users have additional privileges compared to regular users.

- `PUT /user/verify-otp/<int:pk>/`

  Verifies the OTP sent to the user's registered email address during the registration process.

- `POST /user/login/`

  Logs in a user with the provided email and password and returns a JWT token for authentication.

- `POST /reset-password/`

  Sends a password reset link to the user's registered email address.

- `POST /reset-password-confirm/`

  Resets the user's password and sends a confirmation email to the registered email address.

- `DELETE /user/delete-account/`

  Deletes the authenticated user account.

## API Documentation

### Register a new user

**URL:** `/user/register/`

**Method:** `POST`

**Request Body:**
`{
  "email": "user@example.com",
  "password": "password",
  "full_name": "Emmanuel John",
  "phone_number": "1234567890",
  "sex": "male"
}`

**Response Body:**
`{
  "id": 1,
  "email": "user@example.com",
  "username": "",
  "full_name": "Emmanuel John",
  "phone_number": "1234567890",
  "sex": "male",
  "otp": "123456"
}`

### Register a new staff or admin user

**URL:** `/user/register/staff/`

**Method:** `POST`

**Request Body:**
`{
  "email": "staff@example.com",
  "password": "password",
  "full_name": "Victoria Jane",
  "phone_number": "1234567890",
  "sex": "female"
}`

**Response Body:**
`{
  "id": 2,
  "email": "staff@example.com",
  "username": "",
  "full_name": "Jane Doe",
  "phone_number": "1234567890",
  "sex": "female",
  "otp": "123456"
}`

### Verify OTP

**URL:** `/user/verify-otp/<int:pk>/`

**Method:** `PUT`

**Request Body:**
`{
  "otp": "123456"
}`

**Response Body:**
`{
  "status": "success",
  "message": "your account is verified"
}`

### Login

**URL:** `/user/login/`

**Method:** `POST`

**Request Body:**
`{
  "email": "user@example.com",
  "password": "password"
}`
**Response Body:**
`{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJK
}`

### Reset Password

**URL:** `/reset-password/`

**Method:** `POST`

**Request Body:**
`{
  "email": "user@example.com"
}`

**Response Body:**
`{
  "status": "success",
  "message": "Password reset link sent to email"
}`

### Reset Password Confirmation

**URL:** `/reset-password-confirm/`

**Method:** `POST`

**Request Body:**
`{
  "password": "stringst",
  "confirm_password": "stringst",
  "token": "string"
}`
**Response Body:**
`an email is sent to the user with a link like this -  http://localhost:8000/reset-password/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyfQ.d-od5`
note that the frontend URL can be set in the environment variable.if not set, the default will be  http://localhost:8000
### Delete Account

**URL:** `/user/delete-account/`

**Method:** `DELETE`

**Request Body:**
Deletes the authenticated user account.
