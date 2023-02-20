import {
    POST_LIST_REQUEST,
    POST_LIST_SUCCESS,
    POST_LIST_FAIL,

    POST_DETAILS_REQUEST,
    POST_DETAILS_SUCCESS,
    POST_DETAILS_FAIL,

    CREATE_POST_REQUEST,
    CREATE_POST_SUCCESS,
    CREATE_POST_FAIL,
    CREATE_POST_RESET,

    DELETE_POST_REQUEST,
    DELETE_POST_SUCCESS,
    DELETE_POST_FAIL,
    DELETE_POST_RESET,

    UPDATE_POST_REQUEST,
    UPDATE_POST_SUCCESS,
    UPDATE_POST_FAIL,
    UPDATE_POST_RESET,
} from '../constants/index'



// posts list
export const postListReducer = (state = { posts: [] }, action) => {
    switch (action.type) {
        case POST_LIST_REQUEST:
            return {
                ...state,
                loading: true,
                posts: [],   // always pass the object during the request
                error: ""
            }
        case POST_LIST_SUCCESS:
            return {
                ...state,
                loading: false,
                posts: action.payload,
                error: ""
            }
        case POST_LIST_FAIL:
            return {
                ...state,
                loading: false,
                error: action.payload
            }
        default:
            return state
    }
}


// posts details
export const postDetailsReducer = (state = { posts: {} }, action) => {
    switch (action.type) {
        case POST_DETAILS_REQUEST:
            return {
                ...state,
                loading: true,
                posts: {},        // always pass the object during the request
                error: ""
            }
        case POST_DETAILS_SUCCESS:
            return {
                ...state,
                loading: false,
                posts: action.payload,
                error: ""
            }
        case POST_DETAILS_FAIL:
            return {
                ...state,
                loading: false,
                error: action.payload
            }
        default:
            return state
    }
}

// create posts reducer
export const createPostReducer = (state = { posts: {} }, action) => {
    switch (action.type) {
        case CREATE_POST_REQUEST:
            return {
                ...state,
                loading: true,
                posts: {},
                success: false,
                error: ""
            }
        case CREATE_POST_SUCCESS:
            return {
                ...state,
                loading: false,
                success: true,
                posts: action.payload,
                error: ""
            }
        case CREATE_POST_FAIL:
            return {
                ...state,
                loading: false,
                success: false,
                posts: {},
                error: action.payload
            }
        case CREATE_POST_RESET:
            return {
                ...state,
                loading: false,
                success: false,
                posts: {},
                error: ""
            }
        default:
            return state
    }
}

// update posts reducer
export const updatePostReducer = (state = { posts: {} }, action) => {
    switch (action.type) {
        case UPDATE_POST_REQUEST:
            return {
                ...state,
                loading: true,
                posts: {},
                success: false,
                error: ""
            }
        case UPDATE_POST_SUCCESS:
            return {
                ...state,
                loading: false,
                success: true,
                posts: action.payload,
                error: ""
            }
        case UPDATE_POST_FAIL:
            return {
                ...state,
                loading: false,
                success: false,
                posts: {},
                error: action.payload
            }
        case UPDATE_POST_RESET:
            return {
                ...state,
                loading: false,
                success: false,
                posts: {},
                error: ""
            }
        default:
            return state
    }
}


// delete posts reducer
export const deletePostReducer = (state = {}, action) => {
    switch (action.type) {
        case DELETE_POST_REQUEST:
            return {
                ...state,
                loading: true,
                success: false,
                error: ""
            }
        case DELETE_POST_SUCCESS:
            return {
                ...state,
                loading: false,
                success: true,
                error: ""
            }
        case DELETE_POST_FAIL:
            return {
                ...state,
                loading: false,
                success: false,
                error: action.payload
            }
        case DELETE_POST_RESET:
            return {
                ...state,
                loading: false,
                success: false,
                error: ""
            }
        default:
            return state
    }
}


