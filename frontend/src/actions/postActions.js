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

    DELETE_POST_REQUEST,
    DELETE_POST_SUCCESS,
    DELETE_POST_FAIL,

    UPDATE_POST_REQUEST,
    UPDATE_POST_SUCCESS,
    UPDATE_POST_FAIL,
} from '../constants/index'

import axios from 'axios'

// posts list
export const getPostList = () => async (dispatch) => {
    try {
        dispatch({
            type: POST_LIST_REQUEST
        })

        // call api
        const { data } = await axios.get("/api/posts/")

        dispatch({
            type: POST_LIST_SUCCESS,
            payload: data
        })
    } catch (error) {
        dispatch({
            type: POST_LIST_FAIL,
            payload: error.message
        })
    }
}


// posts details
export const getPostDetails = (id) => async (dispatch) => {
    try {
        dispatch({
            type: POST_DETAILS_REQUEST
        })

        // call api
        const { data } = await axios.get(`/api/posts/${id}/`)

        dispatch({
            type: POST_DETAILS_SUCCESS,
            payload: data
        })
    } catch (error) {
        dispatch({
            type: POST_DETAILS_FAIL,
            payload: error.message
        })
    }
}


// create posts
export const createPost = (posts) => async (dispatch, getState) => {

    try {
        dispatch({
            type: CREATE_POST_REQUEST
        })

        // login reducer
        const {
            userLoginReducer: { userInfo },
        } = getState()

        const config = {
            headers: {
                "Content-Type": "multipart/form-data",
                Authorization: `Bearer ${userInfo.token}`
            }
        }

        // api call
        const { data } = await axios.post(
            "/api/posts-create/",
            posts,
            config
        )

        dispatch({
            type: CREATE_POST_SUCCESS,
            payload: data
        })
    } catch (error) {
        dispatch({
            type: CREATE_POST_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail : error.message
        })
    }
}

// delete posts
export const deletePost = (id) => async (dispatch, getState) => {
    try {
        dispatch({
            type: DELETE_POST_REQUEST
        })

        // login reducer
        const {
            userLoginReducer: { userInfo },
        } = getState()

        const config = {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${userInfo.token}`
            }
        }

        // api call
        const { data } = await axios.delete(
            `/api/posts-delete/${id}/`,
            config
        )

        dispatch({
            type: DELETE_POST_SUCCESS,
            payload: data
        })

    } catch (error) {
        dispatch({
            type: DELETE_POST_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail : error.message
        })
    }
}

// update posts
export const updatePost = (id, posts) => async (dispatch, getState) => {

    try {
        dispatch({
            type: UPDATE_POST_REQUEST
        })

        // login reducer
        const {
            userLoginReducer: { userInfo },
        } = getState()

        const config = {
            headers: {
                "Content-Type": "multipart/form-data",
                Authorization: `Bearer ${userInfo.token}`
            }
        }

        // api call
        const { data } = await axios.put(
            `/api/posts-update/${id}/`,
            posts,
            config
        )

        dispatch({
            type: UPDATE_POST_SUCCESS,
            payload: data
        })

    } catch (error) {
        dispatch({
            type: UPDATE_POST_FAIL,
            payload: error.response && error.response.data.detail ? error.response.data.detail : error.message
        })
    }
}

