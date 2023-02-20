import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getPostList } from '../actions/postActions';
import Message from '../components/Message';
import { Spinner, Row, Col } from 'react-bootstrap';
import Post from '../components/posts';
import { useHistory } from "react-router-dom";
import { CREATE_POST_RESET } from '../constants';
import { checkTokenValidation, logout } from "../actions/userActions";


function ProductsUserListPage() {

    let history = useHistory()
    let searchTerm = history.location.search
    const dispatch = useDispatch()

    // products list reducer
    const postListReducer = useSelector(state => state.postListReducer)
    const { loading, error, posts } = postListReducer

  
    // login reducer
    const userLoginReducer = useSelector((state) => state.userLoginReducer);
    const { userInfo } = userLoginReducer;
  
    // create product reducer
    const createProductReducer = useSelector(
      (state) => state.createProductReducer
    );
  
    // check token validation reducer
    const checkTokenValidationReducer = useSelector(
      (state) => state.checkTokenValidationReducer
    );
    const { error: tokenError } = checkTokenValidationReducer;
  
    useEffect(() => {
      if (!userInfo) {
        history.push("/login");
      }
      dispatch(checkTokenValidation());
    }, [dispatch, userInfo, history]);
  
   
  
    if (userInfo && tokenError === "Request failed with status code 401") {
      alert("Session expired, please login again.");
      dispatch(logout());
      history.push("/login");
      window.location.reload();
    }
    

    useEffect(() => {
        dispatch(getPostList())
        dispatch({
            type: CREATE_POST_RESET
        })
        //dispatch(checkTokenValidation())
    }, [dispatch])

    const showNothingMessage = () => {
        return (
            <div>
                {!loading ? <Message variant='info'>Nothing to show</Message> : ""}                
            </div>
        )
    }

   

    return (
        <div>
            {error && <Message variant='danger'>{error}</Message>}
            {loading && <span style={{ display: "flex" }}>
                <h5>Getting Products</h5>
                <span className="ml-2">
                    <Spinner animation="border" />
                </span>
            </span>}
            <div>         
                <Row>

                    {/* If length of the filter result is equal to 0 then show 'nothing found' message
                        with help of showNothingMessage function else show the filtered result on the
                        webpage and then run the map function */}
                    
                    {(posts.filter((item) =>
                        item.product_from == userInfo.username
                    )).length === 0 ? showNothingMessage() : 
                    
                    (posts.filter((item) =>
                    item.post_name == userInfo.username
                    )).map((post) => (
                        <Col key={post.id} sm={12} md={6} lg={4} xl={3}>
                            <div className="mx-2"> 
                                <Post post={post} />
                            </div>
                        </Col>
                    )
                    )}
                </Row>
            </div>
        </div>
    )
}

export default ProductsUserListPage
