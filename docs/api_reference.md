# API Reference Documentation

## Overview
This document provides a comprehensive guide to the API endpoints available in the app. It covers endpoints in users, bikes, parkings, and rentals including methods, query parameters and response formats.

## Authentication
**Endpoint:** `POST /users/login`

**Description:**  
Authenticate a user using their email and password. On a successful login, a server-side session is established and session cookie is set in the client’s browser

> [!TIP]
> Setting a `SESSION_COOKIE_SECURE=True` in `settings.py` will increase security even more

**Request:**
```json
{
  "email": "user@example.com",
  "password": "Examplepassword123"
}
```
`200 OK` *Successful authentication*

```json
{
  "detail": "Successfully logged in"
}
```

`400 Bad Request` *Invalid credentials provided (email or password)*

```json
{
  "detail": "Invalid credentials"
}
```

`403 Forbidden` *Account is not active (pending admin activation)*

```json
{
  "detail": "Your account needs to be activated by an admin"
}
```

If a user creates his account, verifies email and tries to log in API will return a 403 Forbidden response.

Cause:
The user's `is_active` status is set to `FALSE` in the database, preventing new *(unknown)* users from accessing map with bike locations

Fix:
Admin must manually activate the account by setting `is_active = TRUE` in the user management system.

## User Endpoints

### 1. Register User

**Endpoint:** `POST /users/register/`

**Description:**  
Create a new user account. After registration, the user must verify their email.
The server sends a mail with verification link formatted as `FRONTEND_URL/UID/TOKEN`. The frontend should parse it on its own.

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "ExamplePassword123",
  "confirmed_password": "ExamplePassword123"
}
```

**Response:**

`201 Created` *Account created successfully; verification email sent*  
  ```json
  {
    "detail": "Account created. Please verify your email."
  }
  ```

`400 Bad Request` *When user with provided email exists or passwords doesn't match*  
  ```json
  {
    "email": "Email already exists"
  }
  ```

`500 Internal Server Error` *Mail sending failed*  
  ```json
  {
    "detail": "Mail sending failed"
  }
  ```

---

### 2. Verify Email

**Endpoint:** `POST /users/verify-email/`

**Description:**  
Verifies user's email address using the provided token.

**Request:**
```json
{
  "uid": "base64-encoded-uid",
  "token": "verification-token"
}
```

**Response:**

`200 OK` *Account verified successfully*  
  ```json
  {
    "detail": "Account verified successfully"
  }
  ```

`400 Bad Request` *If UID or Token are invalid*  


---

### 3. Reset Password Request

**Endpoint:** `POST /users/reset-password-request/`

**Description:**  
Sends a password reset link to the user's email.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**

`200 OK` *Password reset link sent*  
  ```json
  {
    "detail": "Your password reset link has been sent"
  }
  ```

`404 Not Found`  *User with this email does not exist*

`500 Server Error` *Mail sending failed*  
  ```json
  {
    "detail": "Mail sending failed"
  }
  ```

---

### 4. Reset Password

**Endpoint:** `PUT /users/reset-password-check/`

**Description:**  
Resets the user's password using the token from the password reset email.
Similarly to email verification link is structured as `FRONTEND_URL/UID/TOKEN` and frontend should take care of parsing it and eventually send request as below.

**Request:**
```json
{
  "uid": "base64-encoded-uid",
  "token": "reset-token",
  "password": "NewPassword123",
  "confirmed_password": "NewPassword123"
}
```

**Response:**

`200 OK` *Password changed successfully*  
  ```json
  {
    "detail": "Your password has been changed successfully"
  }
  ```

  `400 Bad Request` *If UID or Token are invalid*

---
## User Management Endpoints

User Management system is only available for admins. In case a non privileged user ( with `is_staff=False` ) tries to fetch some data the access is denied and `403 Forbidden` status code is returned. In case you use django admin panel for management it might be a good idea to deactivate the endpoints below

### 1. List Users

**Endpoint:** `GET /users/`

**Description:**  
Retrieve a list of all users.

**Response:**

`200 OK`
  ```json
  [
    {
      "id": 4,
      "email": "activeuser@sociale.com",
      "first_name": "Active",
      "last_name": "User",
      "is_verified": true,
      "is_active": true,
      "is_staff": false
    },
    ...
  ]
  ```
---
### 2. User Detail

**Endpoint:** `GET /users/<user_id>/`

**Description:**  
Retrieve detailed information for a specific user by their ID.

**Response:**

`200 OK` *User was successfully retrieved*
  ```json
  {
    "id": 13,
    "email": "user@sociale.com",
    "first_name": "User",
    "last_name": "Sociale",
    "is_verified": true,
    "is_active": false,
    "is_staff": false
  }
  ```
`404 Not Found`  *User with this ID does not exist*

---

### 3. User Create

**Endpoint:** `POST /users/create/`

**Description:**  
Creates an user. The user won't get any verification mail as admin can choose whether to give him permissions or not.

**Request**
```json
{
  "email": "newuser@example.com",
  "first_name": "NewName",
  "last_name": "TheLastName",
  "is_verified": false,
  "is_active": true,
  "is_staff": false
}

```
**Response:**

`200 OK` *User was successfully created*

`400 Bad Request`  *User with this ID does not exist*

---

### 4. Update User

**Endpoint:** `PUT /users/<user_id>/update/`

**Description:**  
Update a user by his ID. Only the fields provided in the request will be updated.

**Request Example:**
```json
{
  "first_name": "NewName",
  "last_name": "TheLastName"
}
```

**Response:**

`200 OK` *User was updated*

`400 Bad Request` *When provided email already exists or field has incorrect type* 
```json
{
  "email": "Email already exists"
}
```

`404 Not Found`  *User with this ID does not exist*

---

### 5. Delete User

**Endpoint:** `DELETE /users/<user_id>/delete/`

**Description:**  
Delete a user account. 

**Response:**

`204 No Content` *User was deleted*

`404 Not Found`  *User with this ID does not exist*

---

## Bike Endpoints
