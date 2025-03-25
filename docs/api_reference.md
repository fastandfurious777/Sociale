## API Reference Documentation

<h2 id="overview">Overview</h2>
This document provides a comprehensive guide to the API endpoints available in the app. It covers endpoints in users, bikes, parkings, and rentals including methods, query parameters and response formats.

- [API Reference Documentation](#api-reference-documentation)
- [User Management Endpoints](#user-management-endpoints)
  - [1. List Users](#1-list-users)
  - [2. User Detail](#2-user-detail)
  - [3. User Create](#3-user-create)
  - [4. Update User](#4-update-user)
  - [5. Delete User](#5-delete-user)
- [Bike Endpoints](#bike-endpoints)
  - [1. List Bikes](#1-list-bikes)
  - [2. Bike Detail](#2-bike-detail)
  - [3. Create Bike](#3-create-bike)
  - [4. Update Bike](#4-update-bike)
  - [5. Delete Bike](#5-delete-bike)


<h2 id="authentication">Authentication</h2>

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

<h2 id="user-endpoints">User Endpoints</h2>

<h3 id="register-user">1. Register User</h3>

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

<h3 id="verify-email">2. Verify Email</h3>

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

<h3 id="reset-password-request">3. Reset Password Request</h3>

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

<h3 id="reset-password">4. Reset Password</h3>

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

These endpoints allow you to manage bikes in the system. Note that endpoints for getting , creating, editing and deleting a specific bike are restricted for admins only. Non-admin users attempting to access admin-only endpoints will receive a `403 Forbidden` response.

---

### 1. List Bikes

**Endpoint:** `GET /bikes/`

**Description:**  
Lists bikes available for rental. Only users with <u>eligible accounts</u> (i.e. those with verified emails and activated by an admin) or admin users can access this endpoint.

- **Default Behavior:**  
  Only bikes that are available (not currently rented or hidden by admins) are included in the response.
  
- **Admin Feature:**  
  Admin users can include bikes that are not available with the query parameter `include_unavailable=true`
  
- **Access Restriction:**  
  Eligible users (non-admin) are not permitted to view unavailable bikes. If an eligible user attempts to use the `include_unavailable=True`, a `403 Forbidden` error is returned.


**Query Parameters:**

- **include_unavailable** (optional, boolean):  already discussed before

**Response:**

**200 OK**  *Retrieve a list of bikes*  
  ```json
  [
    {
      "name": "Moongoose",
      "lon": 19.941945,
      "lat": 50.060453
    },
    {
      "name": "Mountain Explorer",
      "lon": 19.946589,
      "lat": 50.051214
    }
  ]
  ```

**403 Forbidden**  *When a non-admin user attempts to include unavailable bikes*  
  ```json
  {
    "detail": "Forbidden: You cannot include unavailable bikes"
  }
  ```

---

### 2. Bike Detail

**Endpoint:** `GET /bikes/<bike_id>/`

**Description:**  
Retrieve detailed information for a specific bike by its ID. *(Admin only)*

**Response:**

**200 OK**  *Bike was successfully retrieved*  
  ```json
  {
    "name": "Moongoose",
    "lon": 19.941945,
    "lat": 50.060453,
    "qr_code": "30ebf6b5-4848-4e90-88ad-f80f59083508",
    "is_available": true,
    "last_taken_by": 5,
    "last_updated": "2023-03-23T12:00:00Z"
  }
  ```

**404 Not Found**  *Bike with provided ID does not exist*  

---

### 3. Create Bike

**Endpoint:** `POST /bikes/create/`

**Description:**  
Create a new bike entry. *(Admin only)*

**Request:**
```json
{
  "name": "Moongoose",
  "lon": 19.941945,
  "lat": 50.060453,
  "code": 123456,
  "is_available": true,
  "last_taken_by": null
}
```

**Response:**

**201 Created**  *Bike was successfully created*  

**400 Bad Request** *Provided data is invalid*  
  ```json
  {
    "field_name": ["error description"]
  }
  ```

---

### 4. Update Bike

**Endpoint:** `PUT /bikes/<bike_id>/update/`

**Description:**  
Updates a specific bike. Only the fields provided in the request will be updated. *(Admin only)*

**Request Example:**
```json
{
  "name": "Updated Moongoose",
  "is_available": false
}
```

**Response:**

**200 OK**  *Bike was updated successfully*  

**400 Bad Request**  *Provided data is invalid*
  ```json
  {
    "field_name": ["error description"]
  }
  ```

**404 Not Found**  *Bike with the provided ID does not exist*  

---

### 5. Delete Bike

**Endpoint:** `DELETE /bikes/<bike_id>/delete/`

**Description:**  
Delete a bike from the system. *(Admin only)*


**Response:**

**200 OK**  *Bike was deleted successfully*  


**404 Not Found**  *Bike with the provided ID does not exist*  

---

<h2 id="parkings">Parkings Endpoints </h2>
Rental area can cover an entire country or even globe, but it is recommended to limit it to smaller regions, such as city. To enforce this, admins can define a special parking area called a "boundary".

This can be done by sending a <a href="create-parking">POST request</a> with the following data (coordinates should be adjusted to match your specific location):
 
  ```json
  {
  "name": "boundary",
  "geometry": { 
    "type": "Polygon", 
    "coordinates": [
      [
        [19.850, 50.100], 
        [19.950, 50.100], 
        [20.050, 50.050], 
        [19.950, 49.950], 
        [19.850, 49.950], 
        [19.850, 50.100]
      ]
    ] 
  }
  }
  ```

The geometry attribute follows the GEOJSON format, so make sure to familiarize yourself with GEOJSON documentation:

* https://geojson.org/geojson-spec.html
* https://www.ibm.com/docs/en/db2/11.5?topic=formats-geojson-format
  
<h3 id="list-parkings">List Parkings</h3>


**Endpoint:**  `GET /parkings/`

**Description:**  
Retrieve a list of all parkings.
- **Default Behavior:** Only active parkings are returned by default.
- **Admin Feature:** Admin users can include inactive parkings by appending the query parameter `include_inactive=true`.
- **Access Restriction:** Non-admin (eligible) users are not allowed to use `include_inactive`. If attempted, a `403 Forbidden` error is returned.

**Query Parameters:**  
- `include_inactive` (optional, boolean): When set to `true` by an admin, both active and inactive parkings are included.

**Responses:**

**200 OK** *Retrieve a list of parkings*
  ```json
  [
    {
      "name": "Central Parking",
      "coords": { "type": "Polygon", "coordinates": [ [ [ 19.941945, 50.060453 ], [ ... ] ] ] },
      "capacity": 150
    },
    {
      "name": "Bronx Parking",
      "coords": { "type": "Polygon", "coordinates": [ [ [ 19.946589, 50.051214 ], [ ... ] ] ] },
      "capacity": 100
    },
    ...
  ]
```


<h3 id="parking-detail">Parking Detail</h3>

**Endpoint:**  `GET /parkings/<parking_id>/`

**Description:**  
Retrieve detailed information for a specific parking by its ID.  *(Admin only)*

**Responses:**

**200 OK** *Retrieve parking by ID*
  ```json
  {
    "name": "Central Parking",
    "coords": { "type": "Polygon", "coordinates": [ [ [ 19.941945, 50.060453 ], [ ... ] ] ] },
    "capacity": 150
  }
  ```

**404 Not Found** *Parking ID does not exist*

<h3 id="create-parking">Create Parking</h3>

**Endpoint:**  `POST /parkings/`

**Description:**  
Create a new parking with provided details. *(Admin only)*

**Request Body:**
```json
{
  "name": "New Parking Lot",
  "coords": { "type": "Polygon", "coordinates": [ [ [ 19.941945, 50.060453 ], [ ... ] ] ] },
  "capacity": 200
}
```

**Responses:**

**201 Created** *Parking created successfully*

**400 Bad Request**  *Provided data is invalid*
  ```json
  {
    "capacity": "Capacity must be greater than zero"
  }
  ```

<h3 id="update-parking">Update Parking</h3>

**Endpoint:**  `PUT /parkings/<parking_id>/`

**Description:**  
Update parking by ID. *(Admin only)*

**Request Body:**
```json
{
  "name": "Updated Parking Name",
  "capacity": 180
}
```

**Responses:**

**200 OK** *Parking updated successfully*

**400 Bad Request**  *Provided data is invalid*
  ```json
  {
    "capacity": "Capacity must be greater than zero"
  }
  ```

**404 Not Found** *Parking with given ID does not exist*

<h3 id="delete-parking">Delete Parking</h3>

**Endpoint:**  `DELETE /parkings/<parking_id>/`

**Description:**  
Delete an existing parking entry by its ID. *(Admin only)*

**Responses:**

**204 No Content** *Parking deleted successfully*

**404 Not Found** *Parking with given ID does not exist*

<h2 id="rentals">Rental Endpoints </h2>

<h3 id="rental-list">Rental List</h3>

**Endpoint:** `GET /rentals/`

**Description:**  
Retrieve a list of rental records. *( Admin only )*

**Query Parameters:**  
- **user_id** (optional, integer): Filter rentals by the ID of the u .
- **status** (optional, string): Filter rentals by their status (`"started"`, `"finished"`, `"canceled"`).  

**Response:**

`200 OK` *Retrieve a list of rentals*
```json
[
  {
    "id": 1,
    "user": 3,
    "bike": 5,
    "status": "started",
    "started_at": "2023-03-23T12:00:00Z",
    "finished_at": null,
  },
  {
    "id": 2,
    "user": 4,
    "bike": 8,
    "status": "finished",
    "started_at": "2023-03-22T11:00:00Z",
    "finished_at": "2023-03-22T12:00:00Z",
  }
]
```

`400 Bad Request` *Invalid query parameters*

`403 Forbidden` *Access forbidden*

---

<h3 id="rental-detail">Rental Detail</h3>

**Endpoint:** `GET /rentals/<rental_id>/`

**Description:**  
Retrieve a specific rental record by its ID. *( Admin only)*

**Response:**

`200 OK` *Rental details retrieved successfully*
```json
{
  "id": 1,
  "user": 3,
  "bike": 5,
  "status": "started",
  "started_at": "2023-03-23T12:00:00Z",
  "finished_at": null,
}
```

`404 Not Found` *Rental with the provided ID does not exist*

---

<h3 id="rental-start">Rental Start</h3>

**Endpoint:** `POST /rentals/start/`

**Description:**  
Start a new rental by user. A code for bike locker is returned on success. Endpoint is restricted for elibible and admin users.

**Request Body:**

```json
{
  "bike": 5
}
```
**Response:**

`201 Created` *Rental was started successfully*
```json
{
  "code": 5132 
}
```

`400 Bad Request` *Invalid request data (e.g., bike already rented, user has an ongoing rental)*
```json
{
  "detail": "Bike is not available"
}
```
---

<h3 href="rentals-finish">Finish Rental </h3>


**Endpoint:**  `POST /rentals/finish/`

**Description:**  
Finishes a rental, similarly to `rental/start` user has to be verified and active in order to access this endpoint.

**Request Body:**  
```json
{
  "lon": 34.0522,
  "lat": -118.2437
}
```
**Response:**

`200 OK` *Rental finished successfully*

`400 Bad Request` *Invalid request data (e.g. user is not in parking location)*

```json
{
  "detail": "Bike is not in a parking location"
}
```

---

<h3 href="rentals-update">Update Rental </h3>

**Endpoint:**  `PUT /rentals/{rental_id}/update/`

**Description:**  
Allows updating rental details such as `status`, `started_at`, `finished_at` *( Admin Only )*

**Request Body:**  
```json
{
  "status": "finished",
  "finished_at": "2025-03-24T16:00:00Z"
}
```

**Response:**

`200 OK` *Rental updated successfully*


`400 Bad Request` *Invalid request data*
```json
{
  "status": "Invalid status value"
}
```
`404 Not Found` *Rental wasn't found*