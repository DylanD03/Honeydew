class MockDB:
  """
    Create mock data for testing. This mock data includes Data from other Teams, 
    has empty fields to test coverage for a variety of possible post requests.
    Examples: 
        Comments/Likes missing in 'Post' objects, or being set as empty lists/dictionaries.
        'Comment' objects having likes within them
        Objects containing pagination or without pagination
        Data fields being empty ( set to "")
        And more

    Mock Data Includes Data from Teams: Fushia, Honeydew (us), Chatreuse, Midnight Blue, Gold.
    Indentation of the JSON is off cause every team does it differently and id rather not manually fix it everytime
  """

  def __init__(self):
    self.author_list = self.generateAuthors()
    self.follow_list = self.generateFollows()
    self.comment_list = self.generateComments()
    self.like_list = self.generateLikes()
    self.post_list = self.generatePosts()
  
  def generatePosts(self):

    return [
      {
        "type": "post",
        "title": "Hello ALL",
        "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/posts/145",
        "description": ":DDD",
        "contentType": "text/plain",
        "content": "I like this app",
        "author": {
            "type": "author",
            "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51",
            "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/app/authors/https%253A%252F%252Ff24-fuchsia-605b02c3dd87.herokuapp.com%252Fapi%252Fauthors%252F51",
            "host": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/",
            "displayName": "dndu_fuschia",
            "github": "https://github.com/DylanD03",
            "profileImage": "https://i.pinimg.com/originals/7c/ee/6f/7cee6fa507169843e3430a90dd5377d4.jpg"
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
          "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1/posts/1",
          "title": "",
          "description": "",
          "contentType": "text/plain",
          "content": "### Markdown",
          "author": {
              "type": "author",
              "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1",
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
      {
        "type": "post",
        "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1/posts/2",
        "title": "",
        "description": "",
        "contentType": "text/plain",
        "content": "new post for fuchsia",
        "author": {
            "type": "author",
            "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1",
            "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
            "displayName": "bstals",
            "github": "",
            "profileImage": "",
            "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/authors/1"
        },
        "published": "2024-11-24T23:57:38.318173Z",
        "visibility": "PUBLIC",
        "comments": [],
        "likes": []
      },
      {
        "type": "post",
        "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1/posts/3",
        "title": "Can Midnight Blue View this?",
        "description": "pls work",
        "contentType": "text/plain",
        "content": "Can you see?",
        "author": {
            "type": "author",
            "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1",
            "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
            "displayName": "bstals",
            "github": "https://github.com/stalsb",
            "profileImage": "https://i.imgur.com/DIiFe5O.jpeg",
            "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/authors/1"
        },
        "published": "2024-11-25T00:14:42.922382Z",
        "visibility": "PUBLIC"
      }
    ]

  def generateLikes(self):
    return [
        {
            "type": "like",
            "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1/liked/9",
            "author": {
                "type": "author",
                "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1",
                "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
                "displayName": "bstals",
                "github": "",
                "profileImage": "https://i.imgur.com/DIiFe5O.png",
                "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/authors/1"
            },
            "object": "https://whip-deploy-dcf2d63e2998.herokuapp.com/api/authors/dbbe80ec-437c-48d2-b4a2-af8f920a098b/posts/768",
            "published": ""
        },
        {
            "type": "like",
            "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1/liked/8",
            "author": {
                "type": "author",
                "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1",
                "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
                "displayName": "bstals",
                "github": "https://github.com/stalsb",
                "profileImage": "https://i.imgur.com/DIiFe5O.jpeg",
                "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/authors/1"
            },
            "object": "https://midnightblue-404-d2b955deb49d.herokuapp.com/api/authors/d8bb0aed-1133-4450-a4e2-76ac139c6e9c/posts/df1b89f2-06d4-4297-b320-451d2e546788",
            "published": "2024-11-26T00:51:45.485155Z"
        },
        {
            "type": "like",
            "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1/liked/7",
            "author": {
                "type": "author",
                "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1",
                "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
                "displayName": "bstals",
                "github": "https://github.com/stalsb",
                "profileImage": "https://i.imgur.com/DIiFe5O.jpeg",
                "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/authors/1"
            },
            "object": "https://c404-project-7bb630f157d0.herokuapp.com/api/authors/fbbffca4-794d-4004-9392-a1a204792558/posts/2224",
            "published": ""
        },
        {
          "type": "like",
          "author": {
            "type": "author",
            "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "page": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api//authors/https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "host": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/",
            "displayName": "honeydew-chartreuse",
            "github": "",
            "profileImage": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/static/images/default_pfp_2.jpg"
          },
          "published": "2024-12-04T02:36:29.797Z",
          "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/liked/300",
          "object": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/posts/695"
        },
        {
          "type": "like",
          "author": {
            "type": "author",
            "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "page": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api//authors/https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "host": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/",
            "displayName": "honeydew-chartreuse",
            "github": "",
            "profileImage": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/static/images/default_pfp_2.jpg"
          },
          "published": "2024-12-04T02:40:54.033Z",
          "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/liked/302",
          "object": "https://gold-d9aafb476531.herokuapp.com/api/authors/test/posts/139"
        },
        {
          "type": "like",
          "author": {
            "type": "author",
            "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "page": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api//authors/https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "host": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/",
            "displayName": "honeydew-chartreuse",
            "github": "",
            "profileImage": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/static/images/default_pfp_2.jpg"
          },
          "published": "2024-12-04T02:40:55.475Z",
          "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/liked/303",
          "object": "https://navajo-white-4845eeb9c06c.herokuapp.com/api/authors/mihawk/posts/5eed9632-c119-4b8f-856a-20c827672185"
        },
        {
          "type": "like",
          "author": {
            "type": "author",
            "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "page": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api//authors/https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "host": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/",
            "displayName": "honeydew-chartreuse",
            "github": "",
            "profileImage": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/static/images/default_pfp_2.jpg"
          },
          "published": "2024-12-04T02:41:32.826Z",
          "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/liked/304",
          "object": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/82/posts/681"
        },
        {
          "type": "like",
          "author": {
            "type": "author",
            "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "page": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api//authors/https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "host": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/",
            "displayName": "honeydew-chartreuse",
            "github": "",
            "profileImage": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/static/images/default_pfp_2.jpg"
          },
          "published": "2024-12-04T02:41:34.472Z",
          "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/liked/305",
          "object": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/82/posts/680"
        },
        {
          "type": "like",
          "author": {
            "type": "author",
            "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "page": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api//authors/https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "host": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/",
            "displayName": "honeydew-chartreuse",
            "github": "",
            "profileImage": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/static/images/default_pfp_2.jpg"
          },
          "published": "2024-12-04T02:41:41.925Z",
          "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/liked/306",
          "object": "https://gold-d9aafb476531.herokuapp.com/api/authors/test/posts/133"
        },
        {
          "type": "like",
          "author": {
            "type": "author",
            "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "page": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api//authors/https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71",
            "host": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/",
            "displayName": "honeydew-chartreuse",
            "github": "",
            "profileImage": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/static/images/default_pfp_2.jpg"
          },
          "published": "2024-12-04T02:42:00.600Z",
          "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/liked/307",
          "object": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/9/posts/19"
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
            "published": "2024-12-04T05:55:11.477620+00:00",
            "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/liked/60",
            "object": "https://navajo-white-4845eeb9c06c.herokuapp.com/api/authors/mihawk/posts/5eed9632-c119-4b8f-856a-20c827672185"
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
            "published": "2024-12-04T05:55:10.501300+00:00",
            "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/liked/59",
            "object": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/65/posts/141"
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
            "published": "2024-12-04T05:55:09.658170+00:00",
            "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/liked/58",
            "object": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/9/posts/21"
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
            "published": "2024-12-04T05:55:08.471020+00:00",
            "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/liked/57",
            "object": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/9/posts/23"
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
            "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/liked/56",
            "object": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/posts/145"
        }
    ]

  def generateComments(self):
    return [
      {
          "type": "comment",
          "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1/commented/7",
          "author": {
              "type": "author",
              "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1",
              "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
              "displayName": "bstals",
              "github": "https://github.com/stalsb",
              "profileImage": "https://i.imgur.com/DIiFe5O.jpeg",
              "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/authors/1"
          },
          "comment": "Yay work pls",
          "contentType": "text/plain",
          "published": "2024-11-26T00:36:39.142365Z",
          "post": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/68/posts/105"
      },
      {
        "type": "comment",
        "author": {
          "type": "author",
          "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/2",
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
          "page_number": 1,
          "size": 50,
          "count": 0,
          "src": []
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
      "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/commented/244",
      "post": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/posts/695",
      "likes": {
        "type": "likes",
        "page": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/posts/695",
        "id": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/commented/244/likes/",
        "page_number": 1,
        "size": 50,
        "count": 0,
        "src": []
      }
    },
    {
      "type": "comment",
      "author": {
        "type": "author",
        "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/13",
        "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api//authors/https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/13",
        "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
        "displayName": "demo_practice",
        "profileImage": "https://i.imgur.com/tEyA1Xc.jpeg"
      },
      "comment": "### Me too",
      "contentType": "text/markdown",
      "published": "2024-12-04T02:36:58.462Z",
      "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/13/commented/1",
      "post": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/posts/695",
      "likes": {
        "type": "likes",
        "page": "https://f24-project-chartreuse-b4b2bcc83d87.herokuapp.com/chartreuse/api/authors/71/posts/695",
        "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/13/commented/1/likes/",
      }
    },
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
    "comment": "Another one",
    "contentType": "text/plain",
    "published": "2024-12-04T06:03:08.499133+00:00",
    "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/commented/46",
    "post": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/9/posts/21",
    "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/authors/59/posts/142",
    "likes": {
        "type": "likes",
        "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/commented/46/likes",
        "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/authors/dndu_fuschia/comments/46/likes",
        "page_number": 1,
        "size": 10,
        "count": 0,
        "src": []
    },
    "url_id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/commented/46"
},
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
    "comment": "Cool Beans",
    "contentType": "text/plain",
    "published": "2024-12-04T06:03:02.337613+00:00",
    "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/commented/45",
    "post": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/9/posts/21",
    "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/authors/59/posts/142",
    "likes": {
        "type": "likes",
        "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/commented/45/likes",
        "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/authors/dndu_fuschia/comments/45/likes",
        "page_number": 1,
        "size": 10,
        "count": 0,
        "src": []
    },
    "url_id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/commented/45"
},
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
},
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
    "comment": "WOW great post",
    "contentType": "text/plain",
    "published": "2024-12-04T06:02:46.649594+00:00",
    "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/commented/43",
    "post": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/posts/146",
    "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/authors/51/posts/146",
    "likes": {
        "type": "likes",
        "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/commented/43/likes",
        "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/authors/dndu_fuschia/comments/43/likes",
        "page_number": 1,
        "size": 10,
        "count": 0,
        "src": []
    },
    "url_id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/51/commented/43"
}
        
      
    ]

  def generateFollows(self):
    return [
      {
        "type": "follow",      
        "summary":"Greg wants to follow Lara",
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
          "id": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/authors/1",
          "host": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/api/",
          "displayName": "bstals",
          "github": "https://github.com/stalsb",
          "profileImage": "https://i.imgur.com/DIiFe5O.jpeg",
          "page": "https://f24-project-honeydew-bstals-76c059d88b9b.herokuapp.com/authors/1"
      }
    }
    ]

  def generateAuthors(self):
    return [
      {
        "id": "https://c404-project-7bb630f157d0.herokuapp.com/api/authors/fbbffca4-794d-4004-9392-a1a204792558",
        "type": "author",
        "host": "https://c404-project-7bb630f157d0.herokuapp.com/api/",
        "displayName": "",
        "github": "",
        "profileImage": "",
        "page": "https://c404-project-7bb630f157d0.herokuapp.com/authors/fbbffca4-794d-4004-9392-a1a204792558"
      },
      {
        "type": "author",
        "id": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/authors/9",
        "host": "https://honeydew-schopra1-705a2edd3662.herokuapp.com/api/",
        "displayName": "s",
        "github": "",
        "profileImage": "https://gratisography.com/wp-content/uploads/2024/10/gratisography-cool-cat-800x525.jpg",
        "page": ""
      },
      {
        "type": "author",
        "id": "",
        "host": "https://midnightblue-404-d2b955deb49d.herokuapp.com/api/",
        "displayName": "Midnight_dylan!1",
        "github": "",
        "profileImage": "",
        "page": "https://midnightblue-404-d2b955deb49d.herokuapp.com/author/https%3A%2F%2Fmidnightblue-404-d2b955deb49d.herokuapp.com%2Fapi%2Fauthors%2F1b09cc86-7f76-4e96-bdb7-68f6d51bf3de"
      },
      {
        "type": "author",
        "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/18",
        "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/app/authors/https%253A%252F%252Ff24-fuchsia-605b02c3dd87.herokuapp.com%252Fapi%252Fauthors%252F18",
        "host": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/",
        "displayName": "Mom",
        "github": "",
        "profileImage": "https://www.wikihow.com/images/thumb/2/21/Karen-Haircut-Step-4.jpg/v4-728px-Karen-Haircut-Step-4.jpg.webp"
      },
      {
        "type": "author",
        "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/22",
        "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/app/authors/https%253A%252F%252Ff24-fuchsia-605b02c3dd87.herokuapp.com%252Fapi%252Fauthors%252F22",
        "host": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/",
        "displayName": "pyhntest",
        "github": "",
        "profileImage": "https://static-ca.gamestop.ca/images/products/786273/3max.jpg"
      },
      {
        "type": "author",
        "id": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/authors/25",
        "page": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/app/authors/https%253A%252F%252Ff24-fuchsia-605b02c3dd87.herokuapp.com%252Fapi%252Fauthors%252F25",
        "host": "https://f24-fuchsia-605b02c3dd87.herokuapp.com/api/",
        "displayName": "Garlyk",
        "github": "",
        "profileImage": "https://i.redd.it/some-of-my-favourite-medieval-cat-paintings-v0-rmpc1ru4uolb1.jpg?width=1024&format=pjpg&auto=webp&s=9421bdb6cca16c0f601e3ea14f02cd309975e506"
      },
    ]

    