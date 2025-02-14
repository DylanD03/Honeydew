class InvalidMockDB:
  """
    Create Invalid mock data for testing. 
    This mock data is design to Fail! And test if our Inbox handles bad data properly
    EX: Return 400 if missing FQID, etc.
  """

  def __init__(self):
    self.follow_list = self.generateFollows()
    self.comment_list = self.generateComments()
    self.like_list = self.generateLikes()
    self.post_list = self.generatePosts()
  
  def generatePosts(self):

    return [
      {
        "type": "post",
        "title": "Hello ALL",
        "id": "",
        "description": ":DDD",
        "contentType": "text/plain",
        "content": "I like this app",
        "author": {
            "type": "author",
            "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51",
        },
        "comments": {
            "type": "comments",
            "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/authors/51/posts/145",
            "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/posts/145/comments",
            "page_number": 1,
            "size": 10,
            "count": 1,
            "src": [
                {
                  "type": "comment",
                  "author": {
                      "type": "author",
                      "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51",
                      "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/app/authors/https%253A%252F%252Ff24-fuchsia-605b02c3dd87.herokuapp.com%252Fapi%252Fauthors%252F51",
                      "host": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/",
                      "displayName": "dndu_fuschia",
                      "github": "https://github.com/DylanD03",
                      "profileImage": "https://i.pinimg.com/originals/7c/ee/6f/7cee6fa507169843e3430a90dd5377d4.jpg"
                  },
                  "comment": "ANother Great post",
                  "contentType": "text/plain",
                  "published": "2024-12-04T06:02:54.253231+00:00",
                  "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/commented/44",
                  "post": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/posts/145",
                  "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/authors/51/posts/145",
                  "likes": {
                      "type": "likes",
                      "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/commented/44/likes",
                      "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/authors/dndu_fuschia/comments/44/likes",
                      "page_number": 1,
                      "size": 10,
                      "count": 0,
                      "src": []
                    },
                    "url_id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/commented/44"
                }
            ]
        },
        "likes": {
            "type": "likes",
            "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/commented/145/likes",
            "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/authors/dndu_fuschia/comments/145/likes",
            "page_number": 1,
            "size": 10,
            "count": 0,
            "src": []
        },
        "published": "2024-12-04T05:55:02.695162+00:00",
        "visibility": "PUBLIC"
      },
        {
          "type": "post",
          "id": "",
          "title": "",
          "description": "",
          "contentType": "text/plain",
          "content": "### Markdown",
          "author": {
              "type": "author",
              "id": "",
              "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
              "displayName": "bstals",
              "github": "None",
              "profileImage": "https://i.imgur.com/DIiFe5O.png",
              "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/authors/1"
          },
          "published": "2024-11-24T23:35:09.272030Z",
          "visibility": "PUBLIC",
          "comments": {},
          "likes": {}
      },

    ]

  def generateLikes(self):
    return [
        {
            "type": "like",
            "id": "",
            "author": {
                "type": "author",
                "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1",
                "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
                "displayName": "bstals",
                "github": "",
                "profileImage": "https://i.imgur.com/DIiFe5O.png",
                "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/authors/1"
            },
            "object": "",
            "published": ""
        },
        {
            "type": "like",
            "author": {
                "type": "author",
                "id": "",
                "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/app/authors/https%253A%252F%252Ff24-fuchsia-605b02c3dd87.herokuapp.com%252Fapi%252Fauthors%252F51",
                "host": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/",
                "displayName": "dndu_fuschia",
                "github": "https://github.com/DylanD03",
                "profileImage": "https://i.pinimg.com/originals/7c/ee/6f/7cee6fa507169843e3430a90dd5377d4.jpg"
            },
            "published": "2024-12-04T05:55:06.353497+00:00",
            "id": "",
            "object": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/posts/145"
        },
        {
            "type": "like",
            "author": {
                "type": "author",
                "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51",
                "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/app/authors/https%253A%252F%252Ff24-fuchsia-605b02c3dd87.herokuapp.com%252Fapi%252Fauthors%252F51",
                "host": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/",
                "displayName": "dndu_fuschia",
                "github": "https://github.com/DylanD03",
                "profileImage": "https://i.pinimg.com/originals/7c/ee/6f/7cee6fa507169843e3430a90dd5377d4.jpg"
            },
            "published": "2024-12-04T05:55:06.353497+00:00",
            "id": "",
            "object": ""
        }
    ]

  def generateComments(self):
    return [
      {
        "type": "comment",
        "author": {
          "type": "author",
          "id": "",
          "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api//authors/https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/2",
          "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
          "displayName": "chartreuse-honeydew",
          "profileImage": "https://i.imgur.com/tEyA1Xc.jpeg"
        },
        "comment": "cool post",
        "contentType": "text/plain",
        "published": "2024-12-03T00:57:42.402Z",
        "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/2/commented/1",
        "post": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/82/posts/680",
        "likes": {
          "type": "likes",
          "page": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/82/posts/680",
          "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/2/commented/1/likes/",
        }
      },
      {
      "type": "comment",
      "author": {
        "type": "author",
        "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
        "page": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api//authors/https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
        "host": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/",
        "displayName": "honeydew-chartreuse",
        "profileImage": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/static/images/default_pfp_2.jpg"
      },
      "comment": "I like this post",
      "contentType": "text/plain",
      "published": "2024-12-04T02:36:38.594Z",
      "id": "",
    },

        
      
    ]

  def generateFollows(self):
    return [
      {
        "type": "follow",      
        "summary":"Greg wants to follow Lara",
        "actor":{
          "type": "author",
          "id": "",
          "host": "https://midnightblue-404-d2b955deb49d.herokuapp.com/api/",
          "displayName": "Midnight_dylan!1",
          "github": "",
          "profileImage": "",
          "page": "https://midnightblue-404-d2b955deb49d.herokuapp.com/author/https%3A%2F%2Fmidnightblue-404-d2b955deb49d.herokuapp.com%2Fapi%2Fauthors%2F1b09cc86-7f76-4e96-bdb7-68f6d51bf3de"
        },
        "object":{
            "type": "author",
            "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1",
            "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
            "displayName": "bstals",
            "github": "https://github.com/stalsb",
            "profileImage": "https://i.imgur.com/DIiFe5O.jpeg",
            "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/authors/1"
        }
      },
      {
      "type": "follow",      
      "summary":"weird summary...",
      "actor":{
        "type": "author",
        "id": "https://midnightblue-404-d2b955deb49d.herokuapp.com/author/https%3A%2F%2Fmidnightblue-404-d2b955deb49d.herokuapp.com",
        "host": "https://midnightblue-404-d2b955deb49d.herokuapp.com/api/",
        "displayName": "Midnight_dylan!1",
        "github": "",
        "profileImage": "",
        "page": "https://midnightblue-404-d2b955deb49d.herokuapp.com/author/https%3A%2F%2Fmidnightblue-404-d2b955deb49d.herokuapp.com%2Fapi%2Fauthors%2F1b09cc86-7f76-4e96-bdb7-68f6d51bf3de"
      },
      "object":{
          "type": "author",
          "id": "",
          "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
          "displayName": "bstals",
          "github": "https://github.com/stalsb",
          "profileImage": "https://i.imgur.com/DIiFe5O.jpeg",
          "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/authors/1"
      }
    }
    ]
