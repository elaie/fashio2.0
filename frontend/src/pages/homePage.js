import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getProductsList } from "../actions/productActions";
import Message from "../components/Message";
import { Spinner, Row, Col } from "react-bootstrap";
import Product from "../components/Product";
import { useHistory } from "react-router-dom";
import { CREATE_PRODUCT_RESET } from "../constants";
import { Form, Button } from "react-bootstrap";
import { createProduct } from "../actions/productActions";
import { checkTokenValidation, logout } from "../actions/userActions";
import stockImg from "./img-not-found.jpg";
import axios from 'axios';
import "./home-page.css"; // import CSS styles

function HomePage() {
  const [posts, setPosts] = useState([]);
  function postData(variableString) {
    console.log("DATA INSIDE POSTDATA")
    console.log(variableString)
    axios.post('/api/your-endpoint/', { data: variableString })
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
      });
  }
  useEffect(()=> {
    postData(userInfo.username);
  })
  useEffect(() => {
      axios.get('/api/posts/').then(response => {
          setPosts(response.data);
      });
  }, []);
  const [page, setPage] = useState(1);

  let history = useHistory();
  let searchTerm = history.location.search;
  const dispatch = useDispatch();

  // products list reducer
  const productsListReducer = useSelector((state) => state.productsListReducer);
  const { loading, error, products } = productsListReducer;

  // login reducer
  const userLoginReducer = useSelector((state) => state.userLoginReducer);
  const { userInfo } = userLoginReducer;

  useEffect(() => {
    if (!userInfo) {
      history.push("/login");
    }
    dispatch(checkTokenValidation());
  }, [dispatch, userInfo, history]);

  useEffect(() => {
    dispatch(getProductsList());
    dispatch({
      type: CREATE_PRODUCT_RESET,
    });
    //dispatch(checkTokenValidation())
  }, [dispatch]);

  const showNothingMessage = () => {
    return (
      <div>
        {!loading ? <Message variant="info">Nothing to show</Message> : ""}
      </div>
    );
  };
  // function to handle infinite scrolling
  const handleScroll = () => {
    if (
      window.innerHeight + document.documentElement.scrollTop ===
      document.documentElement.offsetHeight
    ) {
      setPage(page + 1);
    }
  };

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);


  
  const handleLike = (id) => {
    console.log("USERINFO")
    console.log(userInfo.username)
    const config = {
      headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${userInfo.token}`
      }
  }
    axios.patch(`/api/posts/${id}/like/`).then(response => {
        setPosts(posts.map(post => post.id === id ? response.data : post));
    });
};

const handleUnlike = (id) => {
    axios.patch(`/api/posts/${id}/unlike/`).then(response => {
        setPosts(posts.map(post => post.id === id ? response.data : post));
    });
};

const isLiked = (id) => {
    const post = posts.find(post => post.id === id);
    return post && post.users.indexOf(userInfo.username) !== -1 ;
};

  return (
    <div>
      {products.filter((item) => item.product_from).length === 0 ? (
        showNothingMessage()
      ) : (
        <div className="card-container">
          {products
            .filter((item) => item.product_from)
            .map((product, idx) => (
             <div>
                <div className="card-header">
                  <img src={product.image} alt={product.name} />
                  <div className="card-header-info">
                    <h3>{product.name}</h3>
                  </div>
                
                </div>
                  <div className="card-body">
                  <img src={product.image} alt={product.name} />
                  <div className="card-body-info">
                    <div className="card-icons">
                      <div className="icon">
                        <i className="far fa-heart"></i>
                        <button onClick={() => isLiked(product.id) ? handleUnlike(product.id) : handleLike(product.id)}>
                        {isLiked(product.id) ? `Unlike (${product.likes})` : `Like (${product.likes})`}
                    </button>
                        <span>12</span>
                      </div>
                      <div className="icon">
                        <i className="far fa-comment"></i>
                        <span>4</span>
                      </div>
                      <div className="icon">
                        <i className="fas fa-share"></i>
                      </div>
                      <div className="icon">
                        <i className="fas fa-shopping-cart"></i>
                      </div>
                    </div>
                  </div>
                </div>
                </div>
            ))}
        </div>
      )}
     
    </div>
  );
}

export default HomePage;