## Main Branch Test State: [![Main Branch](https://github.com/uofa-cmput404/f24-project-honeydew/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/uofa-cmput404/f24-project-honeydew/actions/workflows/django.yml)

## Table of Contents

- [Watch on YouTube](https://www.youtube.com/watch?v=-5R_JLsiuoI)
- [Node Links and Credentials](#node-links-and-credentials)
- [Running Our Application Locally](#running-our-application-locally)
- [API Documentation](#api-documentation)



[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zUKWOP3z)
CMPUT404-project-socialdistribution
===================================

CMPUT404-project-socialdistribution

See [the web page](https://uofa-cmput404.github.io/general/project.html) for a description of the project.
Make a distributed social network!

### Watch on YouTube
[![Watch the video](https://img.youtube.com/vi/-5R_JLsiuoI/maxresdefault.jpg)](https://www.youtube.com/watch?v=-5R_JLsiuoI)
[video also posted on youtube](https://www.youtube.com/watch?v=-5R_JLsiuoI).

# Node Links and Credentials

## Our Node
- **URL**: [Honeydew Node](https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/login/)
  - **Username**: `dndu_brianna_node`
  - **Password**: `dndu_brianna_node`

## Fully Connected Nodes
### Chartreuse
- **URL**: [Chartreuse Node](https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/)
  - **Username**: `honeydew-chartreuse`
  - **Password**: `honeychar`

### Fuchsia
- **URL**: [Fuchsia Node](https://f24-fuchsia-605b02c3dd87.herokuapp.com/app/)
  - **Username**: `dndu_fuschia`
  - **Password**: `dndu_fuschia`

### Papayawhip
- **URL**: [Papayawhip Node](https://c404-project-7bb630f157d0.herokuapp.com/home)
  - **Username**: `honeydewteam`
  - **Password**: `honeydewteam`

### Gold
- **URL**: [Gold Node](https://gold-d9aafb476531.herokuapp.com/login)
  - **Username**: `honeydew`
  - **Password**: `123456789`

# Running Our Application Locally

## Prerequisites
- **Python 3.11** must be installed.  
  - [Download Python 3.11 here](https://www.python.org/downloads/).  
- **pip** must be installed.

---

1) Create a Virtual Enviroment:
- ```virtualenv venv --python=python3.11 ```

2) Run the Virtual Enviroment and Install Requirements
- ```source venv/bin/activate ```
- ```python3.11 -m pip install -r requirements.txt ```

3) Create Migrations and SQL database
- ```python3.11 manage.py makemigrations ```
- ```python3.11 manage.py migrate auth ```
- ```python3.11 manage.py migrate --run-syncdb ```

4) (OPTIONAL) Run Database Tests
- ```python3.11 manage.py test ```
- If you want to run a specific test suite: ```python3 manage.py test api_tests.test_inbox.HandleInboxTests```

6) Run The Server Locally
- ```python3.11 manage.py runserver 0.0.0.0:8000 ```
  



## License

* MIT License

## Copyright

The authors claiming copyright, if they wish to be known, can list their names here...

* Alex Huo - MdzzLO
* Ben Gao
* Brett Liu - Polaris Starnor
* Brianna Stals - stalsb
* Dylan Du - DylanD03
* Shiv Chopra - Shiv Chopra





# API Documentation


All endpoints concerning Author objects. 

# `GET` `/api/authors`
## Description
API that recieves a GET request with a query defining page number and page
size. By default, this will return page 1 of size 5.

Endpoint should be used when gathering author information in bulk
(mainly communicating with other nodes)

If there is a specific author the caller would like to receive, it is
recommended to use the handle_author api instead.

## Examples
`http://host.com/api/authors`

`http://host.com/api/authors?page=2`

`http://host.com/api/authors?size=7`

`http://host.com/api/authors?page=3&size=5`

### Example with current deployment
`https://f24-honeydew-aeea8463c39c.herokuapp.com/api/authors`

## Request/Response Fields
* Request: None

* Response:
   * type (string): "authors"
   * authors (list): [{
            "type": "author",
            "id": "http://example.com/api/authors/20",
            "host": "http://example.com/api/",
            "displayName": "Donut Lover 20",
            "github": "https://github.com/donut_lover_20",
            "page": "http://example.com/authors/20"
        }]

## Response Example:
```json
{
    "type": "authors",
    "authors": [
        {
            "type": "author",
            "id": "https://c404-project-7bb630f157d0.herokuapp.com/api/authors/fbbffca4-794d-4004-9392-a1a204792558",
            "host": "https://c404-project-7bb630f157d0.herokuapp.com/api/",
            "displayName": "NoProfilePicturePeter",
            "github": "",
            "profileImage": "https://assets.techrepublic.com/uploads/2021/08/tux-new.jpg",
            "page": "https://c404-project-7bb630f157d0.herokuapp.com/authors/fbbffca4-794d-4004-9392-a1a204792558"
        },
        {
            "type": "author",
            "id": "https://c404-project-7bb630f157d0.herokuapp.com/api/authors/b63c7f01-6858-4bc3-8ab7-f6cb619e1cd0",
            "host": "https://c404-project-7bb630f157d0.herokuapp.com/api/",
            "displayName": "SmithersSimpsonsREAL",
            "github": "",
            "profileImage": "https://assets.techrepublic.com/uploads/2021/08/tux-new.jpg",
            "page": "https://c404-project-7bb630f157d0.herokuapp.com/authors/b63c7f01-6858-4bc3-8ab7-f6cb619e1cd0"
        },
        {
            "type": "author",
            "id": "https://c404-project-7bb630f157d0.herokuapp.com/api/authors/49ba081e-524b-4f81-9202-cbe6afeddfca",
            "host": "https://c404-project-7bb630f157d0.herokuapp.com/api/",
            "displayName": "Michael",
            "github": "",
            "profileImage": "https://assets.techrepublic.com/uploads/2021/08/tux-new.jpg",
            "page": "https://c404-project-7bb630f157d0.herokuapp.com/authors/49ba081e-524b-4f81-9202-cbe6afeddfca"
        },
        {
            "type": "author",
            "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/5",
            "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
            "displayName": "asfjkl",
            "github": "",
            "profileImage": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/authors/5"
        },
        {
            "type": "author",
            "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/4",
            "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
            "displayName": "q",
            "github": "",
            "profileImage": "https://fps.cdnpk.net/images/home/subhome-ai.webp?w=649&h=649",
            "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/authors/4"
        }
    ]
}
```

# `GET` `/api/authors/{author_serial}`
## Description

On a GET request. Returns data of an Author referred to locally at `serial`. Serials are integer only. Our Author Object will be in json format descrbed in `Response`.

If there is no author with a matching serial, a 404 response will be returned.

Might have to flip to Handle Author Tab in REST API View

## Examples
`http://host.com/api/authors/1`

`http://host.com/api/authors/33`

`http://host.com/api/authors/2`

### Example with current deployment
`https://f24-honeydew-aeea8463c39c.herokuapp.com/api/authors/4`

## Request/Response Fields
* Request:
   * serial (string): The serial of the author.

* Response:
   * type (string): "author",
   * id (string): "http://example.com/api/authors/1"
   * host (string): "http://example.com/api/"
   * displayName (string): "Donut Lover 1"
   * github (string): "https://github.com/donut_lover_1"
   * page (string): "http://example.com/authors/1"

## Response Example:
```json
{
    "type": "author",
    "id": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/4",
    "host": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/",
    "displayName": "Ben2222",
    "github": "",
    "profileImage": null,
    "page": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/authors/4"
}

```

# `PUT` `/api/authors/{author_serial}` `Local`
## Description
API endpoint used for authors to edit their properties on their home node. Payload should be one completed author json, such as the one above. This endpoint is not usable remotely, it is only for authors on one node to stay in their one node.


# `GET` `/api/authors/{author_fqid}`
## Description
Similar to the function above, except it will use an FQID instead of a serial in order to receive authors imported by the node.

Local authors may be handled by both this endpoint and the endpoint above.

FQID can be any string of characters, but in our case, we use URLs for our FQIDs, 

## Examples
`http://host.com/api/authors/http://example.com/api/authors/1`

`http://host.com/api/authors/http://example.com/api/authors/7`

`http://host.com/api/authors/http://example.com/api/authors/21`

`http://host.com/api/authors/http://example.com/api/authors/2`

### Example with current deployment
`https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/3`

`https://f24-honeydew-aeea8463c39c.herokuapp.com/api/authors/http://f24-honeydew-aeea8463c39c.herokuapp.com/api/authors/2`

## Request/Response Fields
* Request:
   * fqid (string): http://example.com/api/authors/1".

* Response:
   * type (string): "author",
   * id (string): "http://example.com/api/authors/1"
   * host (string): "http://example.com/api/"
   * displayName (string): "Donut Lover 1"
   * github (string): "https://github.com/donut_lover_1"
   * page (string): "http://example.com/authors/1"

## Response Example:
```json
for: GET /api/authors/https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/3
HTTP 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Vary: Accept
{
    "type": "author",
    "id": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/3",
    "host": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/",
    "displayName": "dylshiv",
    "github": "https://github.com/PolarisStarnor",
    "profileImage": "https://imgur.com/gallery/mare-foal-fhv3QDB#/t/art",
    "page": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/authors/3"
}


API for previewing follower relationships.

# `GET` `/api/authors/{author_id}/followers`
## Description
Purpose: Retrieve followers of a specific author.
* When to use: To list all followers of an author.
* Retrieves followers through filtering Follow objects.

## Examples
`http://host.com/api/authors/4/followers`

`http://host.com/api/authors/18/followers`

### Example with current deployment
`https://f24-honeydew-aeea8463c39c.herokuapp.com/api/authors/1/followers`

## Request/Response Fields
* Request:
   * author_id (string): The ID of the author. "1"

* Response:
   * type (string): "followers"
   * followers (list): A list of author objects. [{
            "type": "author",
            "id": "http://example.com/api/authors/2",
            "host": "http://example.com/api/",
            "displayName": "Donut Lover 2",
            "github": "https://github.com/donut_lover_2",
            "page": "http://example.com/authors/2"
        }]

## Response Example:
```json
For: https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/4/followers
HTTP 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Vary: Accept

{
    "type": "followers",
    "followers": [
        {
            "type": "author",
            "id": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2",
            "host": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/",
            "displayName": "Ben44",
            "github": null,
            "profileImage": "https://imgur.com/gallery/mare-foal-fhv3QDB#/t/art",
            "page": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/authors/2"
        }
    ]
}

```

# `GET` `api/authors/{author_serial}/followers/{FOREIGN_AUTHOR_FQID}`
## Description
The purpose of this request is to check if the local author designated by the serial is pointed to by the author referred to by ID. No object will be returned on a hit, instead, this endpoint will return 200 if both authors exist and the local author is following the author referred to by ID.

In any other scenario (one of the authors does not exist, local author is not following the other author), this endpoint will return a 404 NOT FOUND.

## Examples
`http://host.com/api/authors/4/followers/http://example.com/api/authors/1`

`http://host.com/api/authors/20/followers/http://example.com/api/authors/5`

### Example with current deployment
`https://f24-honeydew-aeea8463c39c.herokuapp.com/api/authors/4/followers/http://example.com/api/authors/2`

## Request/Response Fields
* Request:
     * author_serial (string): The ID of the author. "1"
     * FOREIGN_AUTHOR_FQID (string): ID of follower to check. "http://example.com/api/authors/1"

* Response:
   * Only on not following:
      * detail (string): "No Follow matches the given query." 

## Response Example:
```
HTTP 200 OK
Allow: GET, DELETE, OPTIONS, PUT
Content-Type: application/json
Vary: Accept


```
``` json
HTTP 404 NOT FOUND
{
    "detail": "No Follow matches the given query."
}

```

# `PUT` `api/authors/{author_serial}/followers/{author_id}`
## Description - Local Only
Not used remotely. This endpoint is not meant for follow requests: See Inbox Instead

This endpoint is meant to modify the database such that the author pointed to by the ID is a follower of the local author referred to by `author_serial` (who is making the request).

If a user other than the local author pointed to by `author_serial` makes the request, then the server will respond 403 NOT AUTHORIZED. Otherwise it will respond 200 OKAY.
## Example
`https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/4/followers/https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2`
then put in the django UI

## Response Example:
``` json
For https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/4/followers/https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2 and then making a put request
HTTP 403 Forbidden
Allow: DELETE, OPTIONS, GET, PUT
Content-Type: application/json
Vary: Accept

``` 
# `DELETE` `api/authors/{author_serial}/followers/{author_id}`
## Description - Local Only
Not used Remotely.

This endpoint is for removing the follower referred to by `author_id` if they are a follower of the local author referred to by `author_serial`.

On deletion, the server will response 200 OK. If there is no follower relationship between the two authors, the server will respond 404 NOT FOUND. And if the requester is not authorized as the local author, then the server will respond 403.

## Example
`https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/4/followers/https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2`
then delete in the django UI

## Request/Response Fields
* request: author FQID, (string)
* response: none, just error code. 

## Example Output
``` json
DELETE /api/authors/4/followers/https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2
HTTP 403 Forbidden
Allow: DELETE, OPTIONS, GET, PUT
Content-Type: application/json
Vary: Accept
``` 

# `GET` `/api/authors/{author_serial}/posts/{post_serial}`

## Description
Purpose: Retrieve a specific post by an author.
   * When to use: To view detailed information about a particular post.
   * Why not use: If you need a list of posts, consider using `/api/authors/{author_id}/posts`.
Friends-only posts can only be viewed by friends.

## Examples
`http://host.com/api/3/posts/4`

`http://host.com/api/2/posts/1`

### Example with current deployment
`https://f24-honeydew-aeea8463c39c.herokuapp.com/api/2/posts/17`

## Request/Response Fields
* Request:
   * author_id (string): The ID of the author.
   * post_id (string): The ID of the post.

* Response:
   * type (string): "post"
   * id (string): Unique identifier for the post.
   * title (string): Title of the post.
   * content (string): The main content of the post.
   * published (string): Timestamp when the post was published.
   * author (object): Information about the author who made the post.

## Response Example:
```json
for: https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2/posts/1
HTTP 200 OK
Allow: DELETE, OPTIONS, GET, PUT
Content-Type: application/json
Vary: Accept

{
    "type": "post",
    "id": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2/posts/1",
    "title": "testpost1Ben",
    "description": "testpost1Ben",
    "contentType": "text/plain",
    "content": "testpost1Ben",
    "author": {
        "type": "author",
        "id": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2",
        "host": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/",
        "displayName": "Ben44",
        "github": null,
        "profileImage": "https://imgur.com/gallery/mare-foal-fhv3QDB#/t/art",
        "page": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/authors/2"
    },
    "published": "2024-11-24T22:25:31.705185Z",
    "visibility": "PUBLIC"
}
```
# `PUT` `/api/authors/{author_serial}/posts/{post_serial}`

## Description - Local Only
* Purpose: Update an existing post.
   * When to use: To modify the content, title, or metadata of a post.
   * The request must include all fields, as partial updates are not supported.

## Examples
`http://host.com/api/3/posts/4`

`http://host.com/api/2/posts/1`

### Example with current deployment
`https://f24-honeydew-aeea8463c39c.herokuapp.com/api/2/posts/17`

## Request/Response Fields
* Request:
   * Path Parameters:
      * author_id (string): The ID of the author.
      * post_id (string): The ID of the post.
   * JSON Fields:
      * title (string, required): Updated title.
      * content (string, required): Updated content.
      * published (string, optional): Timestamp when the post should be published.
      * ect. for all felids in the GET response above

* Response:
   * Status:
      * 200 OK if the post was successfully updated.
      * 401 Unauthorized if you do not have authority to edit the post

## Response Example:

```http
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept
```
```http
HTTP 401 Unauthorized
Allow: DELETE, OPTIONS, GET, PUT
Content-Type: application/json
Vary: Accept
```


# `DELETE` `/api/authors/{author_serial}/posts/{post_serial}`

## Description - Local Only
Purpose: Delete a specific post.
   * When to use: To change a post created by an author to deleted status.
   * Why not use: When you want to permanently delete a post (only the local admin may do this).

## Examples
`http://host.com/api/3/posts/4`

`http://host.com/api/2/posts/1`

### Example with current deployment
`https://f24-honeydew-aeea8463c39c.herokuapp.com/api/2/posts/17`

## Request/Response Fields
* Request:
   * Path Parameters:
      * author_id (string): The ID of the author.
      * post_id (string): The ID of the post.

* Response:
   * Status:
      * 204 No Content if the post was successfully deleted.

## Response Example:
```
204 No Content
```

# `GET` `/api/posts/{post_fqid}`
## Description
Purpose: Get a specific post that is not necessarily local to the node.
        * When to use: To access a post that is not local to this node
        * When not to use: When you are not a local author of this node
## Examples
`http://host.com/api/posts/http://example.com/api/authors/21/posts/1`

`http://host.com/api/posts/http%3A%2F%2Fexample-node-2%2Fauthors%2F43%2Fposts%2F43`

### Example with current deployment
`https://f24-honeydew-aeea8463c39c.herokuapp.com/api/posts/http://f24-honeydew-aeea8463c39c.herokuapp.com/api/authors/2/posts/2`

## Request/Response Fields
* Request:
    *post_id (string): the Fully Qualified ID of the post

* Response:
     * Status:
           * 200: You are an authorized local user and the post is found.
           * 404: The post's FQID does not match with the rest of our system
           * 403: You are not an authorized local user of the node

## Response Example:
```json
for: https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/posts/https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2/posts/1
HTTP 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Vary: Accept

{
    "type": "post",
    "id": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2/posts/1",
    "title": "testpost1Ben",
    "description": "testpost1Ben",
    "contentType": "text/plain",
    "content": "testpost1Ben",
    "author": {
        "type": "author",
        "id": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2",
        "host": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/",
        "displayName": "Ben44",
        "github": null,
        "profileImage": "https://imgur.com/gallery/mare-foal-fhv3QDB#/t/art",
        "page": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/authors/2"
    },
    "published": "2024-11-24T22:25:31.705185Z",
    "visibility": "PUBLIC"
}
```

# `GET` `/api/authors/{author_serial}/posts`
## Description
Purpose: Get the most recent posts by an Author
    * When to use: To get posts by an author
    * When not to use: When you only need a single specific Post.

## Examples
`http://host.com/api/authors2/posts`

`http://host.com/api/authors14/posts`

### Example with current deployment
`https://f24-honeydew-aeea8463c39c.herokuapp.com/api/4/posts`

## Request/Response Fields
* Request:
    * Path Parameters:
        * author_serial (string) : Serial identification number for author.
    * Query Parameters:
        * page (int) - Page number of posts being grabbed (based on size)
        * size (int) - Size of a specific page
* Response:
   * type (string): "posts"
   * page_number (int): Page number of returned page.
   * size (int): Number of posts per page.
   * count (int): Number of posts.
   * src (list): List of all post objects by the author.

## Response Example:
```json
for https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2/posts
HTTP 200 OK
Allow: OPTIONS, GET, POST
Content-Type: application/json
Vary: Accept

{
    "type": "posts",
    "page_number": 1,
    "size": 5,
    "count": 1,
    "src": [
        {
            "type": "post",
            "id": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2/posts/1",
            "title": "testpost1Ben",
            "description": "testpost1Ben",
            "contentType": "text/plain",
            "content": "testpost1Ben",
            "author": {
                "type": "author",
                "id": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/2",
                "host": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/",
                "displayName": "Ben44",
                "github": null,
                "profileImage": "https://imgur.com/gallery/mare-foal-fhv3QDB#/t/art",
                "page": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/authors/2"
            },
            "published": "2024-11-24T22:25:31.705185Z",
            "visibility": "PUBLIC"
        }
    ]
}

```

# `POST` `/api/authors/{author_serial}/posts`
## Description - Local Only
* Purpose: To create a post made by the author.
    * When to use: When the author wants to make a post as theirself.
    * When not to use: When editting a post (See `PUT` `/api/authors/{author_serial}/posts/{post_serial}`)

## Examples
`http://host.com/api/authors/2/posts`

`http://host.com/api/authors/14/posts`

### Example with current deployment
`https://f24-honeydew-aeea8463c39c.herokuapp.com/api/4/posts`

## Request/Response Fields
* Request:
    * author_serial (string) - Serial identification number for author.

* Response:
    * 200 - If the post is correct and the author is locally authenticated.
    * 401 - If the author cannot be authenticated, or the autheticated author is not the author matching `author_serial`
    * 400 - If the post is not compliant with our object

## Example Responses:
```json
POST /api/authors/2/posts
HTTP 401 Unauthorized
Allow: OPTIONS, GET, POST
Content-Type: application/json
Vary: Accept
```
