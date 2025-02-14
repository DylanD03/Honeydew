
/*
                          HELPER FUNCTIONS
      Below are helper functions to fetch from our API Endpoints. 

      USED IN STREAM.HTML AND POST_VIEW.HTML TEMPLATES
*/

async function like_post(userFQID, authorFQID, postFQID, interactionCount) {
  /* 
    Creates a Like object when the user (userSerial) Like's the post (postSerial) 
  
    The Post body requires three fields:
    (String) user_fqid:  The FQID of the user interacting with the post
    (String) author_fqid: The FQID of the post's Author
    (String) post_fqid: The FQID of the post itself
  */
  console.log("Creating Like: ", "User Liking: ", userFQID, "Post: ", postFQID)
  await fetch(`/api/authors/handle_like_post`, {
    method: 'POST',
    headers: {
      "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      type: 'like',
      user_fqid: userFQID, // User liking the post
      author_fqid: authorFQID,
      post_fqid: postFQID, 
    }),
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error creating Like! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Like created successfully:', data);
      // Update the like count in the UI
      interactionCount.textContent = parseInt(interactionCount.textContent) + 1
    })
    
}


async function display_likes(authorFQID, postFQID, interactionCount) {
  /* 
    Gets the number of likes from other authors, 
    on authorSerial's post, then updates the likes Count (interactionCount) accordingly
    in the UI.

    The Post body requires three fields:
    (String) author_fqid: The FQID of the post's Author
    (String) post_fqid: The FQID of the post itself
  */
  console.log("in display likes")
  const response = await fetch(`/api/authors/all_likes`,
      {
        method: 'POST',
        headers: {
          "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          type: 'like',
          author_fqid: authorFQID,
          post_fqid: postFQID, 
      }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error getting Post Likes! Status: ${response.status}`);
      }
      return response.json(); // Parse the JSON from the response
    })
    .then(data => {
      interactionCount.textContent = (data.count || 0); // Set Like values
      return data
    })
}


async function check_user_liked_post(userFQID, authorFQID, postFQID) {
  /* 
    Checks to see if the current user has already liked a specific post,
    Using our backend API

    The Post body requires three fields:
    (String) user_fqid:  The FQID of the user interacting with the post
    (String) author_fqid: The FQID of the post's Author
    (String) post_fqid: The FQID of the post itself
  */

  return fetch(`/api/user/has_liked`, {
      method: 'POST',
      headers: {
        "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_fqid: userFQID,
        author_fqid: authorFQID,
        post_fqid: postFQID, 
      }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error checking like status! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      return data.is_liked
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

async function delete_like(userFQID, authorFQID, postFQID, interactionCount) {
  /*
    This function calls our API endpoint to delete a like from the database
    
    The Post body requires three fields:
    (String) user_fqid:  The FQID of the user interacting with the post
    (String) author_fqid: The FQID of the post's Author
    (String) post_fqid: The FQID of the post itself

  */
  console.log("Deleting Like: ", "User: ", userFQID, "Post: ", postFQID);
  await fetch(`/api/user/unlike_post`, {
    method: 'DELETE',
    headers: {
      "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_fqid: userFQID, // user unliking the post
      author_fqid: authorFQID,
      post_fqid: postFQID, 
    }),
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error deleting Like! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Like deleted successfully:', data);
      interactionCount.textContent = parseInt(interactionCount.textContent) - 1
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

async function fetch_activity(user_serial, user_github) {
  /* 
    This method pulls recent GitHub activity for a particular user,
    and automatically converts them into Post objects
    Credits: https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28#list-public-events-for-a-user 
  */
  /* Get Current user's Github Info */
  console.log("*** in fetch_activity ***")
  const userSerial = user_serial
  const userGithubURL = user_github                                                       // For example: https://github.com/DylanD03
  const userGithubID = userGithubURL.split('/')[userGithubURL.split('/').length - 1]      // Parses the above URL to DylanD03

  if (!userGithubID) {
    console.log("User has not input their github url into their profile page")
    return
  }
  /* Fetch User's Public Activity from Github*/
  const url = `https://api.github.com/users/${userGithubID}/events/public?per_page=10`;
  console.log("url: ", url)
  return await fetch(url, {
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": "Bearer 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",
      "X-GitHub-Api-Version": "2022-11-28"
    }
  }).then(response => {
    if (!response.ok) {
      throw new Error(`Error Fetching Github Activity! Status: ${response.status}`);
    }
    return response.json();
  }).then(data => {
    console.log("Fetching Github Activity Successful!")
    /* Create posts of each new activity */
    create_activity_posts(userSerial, data)
  })
    .catch(error => {
      console.error('Error:', error);
    });
}

async function create_activity_posts(userSerial, activityJSON) {
  /* 
    Given a list of activities, this will call our backend API
    to generate a Post object for each activity

    The expected data schema for activityJSON can be found here:
    https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28#list-public-events-for-a-user 
  */
  console.log("*** in create_activity_posts ***")
  const url = `/api/authors/${userSerial}/github_posts`;
  console.log("url", url)

  for (const activity of activityJSON) {
    // Send only relavent data to create a Post object
    const activityPost = {
      
      title: `${activity.actor.login || "Anonymous"}'s ${activity.type}`,  // For example: "DylanD03's PULLRequestEvent"
      description: "Automatic Github Activity Post",
      content_type: "text/markdown",
      content: generateMarkdownContent(activity),  // Generate markdown from activity
      visibility: "PUBLIC",
      github_activity_id: `${activity.id}`,  // Unique Identifier for Github Events
    };
    console.log(" ** activity post **")
    console.log(activityPost)
    // Send the data to our backend API to create a Post object
    await fetch(url, {
      method: 'POST',
      headers: {
        "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(activityPost)
    })
  }
}

function generateMarkdownContent(activity) {
  /*
    Creates a string in Markdown format to present Github activity
    details more cleanly

    The expected data schema for activity can be found here:
    https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28#list-public-events-for-a-user 
  */
  /* Create our activity Header */
  let content = `### Activity Type: ${activity.type}\n`;
  content += `---\n`
  /* Create hyperlinks in Markdown for the Repository and User */
  content += `**In Repository:** [${activity.repo.name}](https://github.com/${activity.repo.name})\n`;
  content += `**Github User:** [${activity.actor.login}](https://github.com/${activity.actor.login})\n`;
  content += `---\n`
  /* 
    Specific content formatting based on Activity Type
    credit: https://www.markdownguide.org/basic-syntax/
  */
  if (activity.type === 'PushEvent') {
    // Map each commit to it's description, and hyperlink to that commit
    // credit: chatgpt for this commit mapping 
    commits = activity.payload.commits.map(commit => `1. [${commit.message}](${commit.url})`) // 1. before every element will still generate an ordered list. https://www.markdownguide.org/basic-syntax/#ordered-lists
    content += `**Commits:** ${commits.join('\n')}\n`;
  } else if (activity.type === 'PullRequestEvent') {
    const pr = activity.payload.pull_request;
    // Generate link to pull request
    content += `**Pull Request:** [${pr.title}](${pr.html_url})`
  } else {
    // For all other activities, just display the entire payload
    content += `**${activity.type}**: ${JSON.stringify(activity.payload)}\n`
  }

  return content;
}

function slugify(url) {
  /* 
    Remove non-alphanumeric characters from post FQID, so each post (HTML) componenet 
    Can be assigned a uniquely identifiable ID. 
      For Example: id="likeButton${postid}
    This addresses an issue where HTML does not allow special characters like '.', or '/'
    in a tag's ID.
    Credit: https://dev.to/bybydev/how-to-slugify-a-string-in-javascript-4o9n 
  */
  return url
    .replace(/[:.]/g, '') // Remove ':' and '.' 
    .replace(/[^a-zA-Z0-9-_:.]/g, '') // Remove more invalid characters 
    .replace(/^-+|-+$/g, '') // Trim leading and trailing hyphens
    .toLowerCase();
}

console.log('display_comments function is loaded:', typeof display_comments);