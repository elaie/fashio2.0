const $ = require( "jquery" );
var withQuery = require('with-query').default;

// Helpers for API Handlers
// JSON detection
const type = (object) => {
    var stringConstructor = "test".constructor;
    var arrayConstructor = [].constructor;
    var objectConstructor = ({}).constructor;

    if (object === null) {
        return "null";
    }
    if (object === undefined) {
        return "undefined";
    }
    if (object.constructor === stringConstructor) {
        return "String";
    }
    if (object.constructor === arrayConstructor) {
        return "Array";
    }
    if (object.constructor === objectConstructor) {
        return "Object";
    }
    return "unknown";
};

// get cookie function e.g. CSRF token
const getCookie = (name) => {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

//----------------------------------------------------------------
// Actual API Handlers

const getCurrentUserInfo = () => {
    return fetch("/api/current_user/").then(response => {
        if (response.status >= 400) {
            return { 
                'error': 'Retrieve current user: Something went wrong' 
            };
        }
        return response.json();
    });
};

const getUserInfoByUsername = (username, query={}) => {
    return fetch(withQuery(`/api/username/${username}/`, query)).then(response => {
        if (response.status >= 400) {
            return { 
                'error': 'Retrieve user by username: Something went wrong' 
            };
        }
        return response.json();
    });
};

const updateUserInfo = (userInfo) => {
    return fetch(`/api/current_user/`, {
        method: "PATCH",
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(userInfo)
    })
    .then(response => {
        if (response.status >= 400) {
            return { 
                'error': 'Update user by username: Something went wrong' 
            };
        }
        return {'message': 'User updated'};
    });
};

const getAllTweets = (query) => {
    return fetch(withQuery("/api/tweet/", query))
        .then(response => {
            if (response.status >= 400) {
                return { 
                    'error': 'Retrieve all tweets: Something went wrong' 
                };
            }
            let pages = 1;
            for (let header of response.headers.entries()) {
                if (header[0] === 'pages') {
                    pages = header[1];
                }
            }
            return {
                'tweets': response.json(),
                'pages': pages || 1,
            };
        });
};

const postTweet = (tweet) => {
    return fetch("/api/tweet/", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(tweet)
    })
    .then(response => {
        if (response.status >= 400) {
            return { 
                'error': 'Post tweet: Something went wrong' 
            };
        }
        return response.json();
    });
};

const likeTweet = (tweetID) => {
    return fetch("/api/tweet_like/", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            "tweet": tweetID
        })
    })
};

const getTweetLikes = (query) => {
    return fetch(withQuery('/api/tweet_like/', query))
        .then(response => {
            if (response.status >= 400) {
                return { 
                    'error': 'Get tweet likes: Cannot get tweet likes by current user and tweetID' 
                };
            }
            return response.json();
        });
};

const isTweetLiked = (tweetID) => {
    return getTweetLikes({ 'tweet': tweetID, 'current': true })
        .then(likes => {
            if (type(likes) === "Object" && likes.error) {
                return { 
                    'error': 'Is tweet liked: Something went wrong' 
                };
            }
            return likes.length > 0;
        });
};

const unlikeTweet = (tweetID) => {
    return getTweetLikes({ 'tweet': tweetID, 'current': true })
        .then(likes => {
            if (type(likes) === "Object" && likes.error) {
                return { 
                    'error': 'Unlike tweet: Something went wrong' 
                };
            }
            for (var i = 0; i < likes.length; i++) {
                return fetch(`/api/tweet_like/${likes[i].id}/`, {
                    method: "DELETE",
                    headers: {
                        'Accept': 'application/json',
                        "Content-Type": "application/json",
                        'X-CSRFToken': getCookie('csrftoken'),
                    }
                });
            }
        });
};

const deleteTweet = (tweetID) => {
    return fetch(`/api/tweet/${tweetID}/`, {
        method: "DELETE",
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => {
        if (response.status >= 400) {
            return { 
                'error': 'Delete tweet: Something went wrong' 
            };
        }
        return {'message': 'Tweet deleted'};
    });
};

const editTweet = (tweetID, tweet) => {
    return fetch(`/api/tweet/${tweetID}/`, {
        method: "PUT",
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(tweet)
    })
    .then(response => {
        if (response.status >= 400) {
            return { 
                'error': 'Edit tweet: Something went wrong' 
            };
        }
        return response.json();
    });
};


const followUser = (userID) => {
    return fetch("/api/follow/", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json",
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            "user": userID
        })
    })
};

const getFollowers = (query) => {
    return fetch(withQuery('/api/follow/', query))
        .then(response => {
            if (response.status >= 400) {
                return { 
                    'error': 'Get followers: Cannot get user followers by userID w/o current user as follower filter' 
                };
            }
            return response.json();
        });
};

const isUserFollowedByMe = (userID) => {
    return getFollowers({ 'user': userID, 'current': true })
        .then(follows => {
            if (type(follows) === "Object" && follows.error) {
                return { 
                    'error': 'Is user followed by me: Something went wrong' 
                };
            }
            return follows.length > 0;
        });
};

const unfollowUser = (userID) => {
    return getFollowers({ 'user': userID, 'current': true })
        .then(follows => {
            if (type(follows) === "Object" && follows.error) {
                return { 
                    'error': 'Unfollow: Something went wrong' 
                };
            }
            for (var i = 0; i < follows.length; i++) {
                return fetch(`/api/follow/${follows[i].id}/`, {
                    method: "DELETE",
                    headers: {
                        'Accept': 'application/json',
                        "Content-Type": "application/json",
                        'X-CSRFToken': getCookie('csrftoken'),
                    }
                });
            }
        });
};




export default { type, getCookie, 
                 getCurrentUserInfo, updateUserInfo, getUserInfoByUsername,
                 getAllTweets, postTweet, likeTweet, isTweetLiked, unlikeTweet, deleteTweet, editTweet,
                 isUserFollowedByMe, followUser, unfollowUser, };