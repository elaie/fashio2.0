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
import "./productUserpage.css";

function ProductsUserListPage(props) {
  const myString = props.match.params.str;

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

  return (
    <div>
      {error && <Message variant="danger">{error}</Message>}
      {loading && (
        <span style={{ display: "flex" }}>
          <h5>Getting Products</h5>
          <span className="ml-2">
            <Spinner animation="border" />
          </span>
        </span>
      )}
      <div>
        <Row>
          {products.filter((item) => item.product_from == myString).length === 0
            ? showNothingMessage()
            : products
                .filter((item) => item.product_from == myString)
                .map((product, idx) => (
                  <Col key={product.id} sm={12} md={6} lg={4} xl={3}>
                    <div className="mx-2">
                      <Product product={product} />
                    </div>
                  </Col>
                ))}
        </Row>
      </div>
    </div>
  );
}

export default ProductsUserListPage;