import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getProductsList } from '../actions/productActions';
import Message from '../components/Message';
import { Spinner, Row, Col } from 'react-bootstrap';
import Product from '../components/Product';
import { useHistory } from "react-router-dom";
import { CREATE_PRODUCT_RESET } from '../constants';
import { Form, Button } from "react-bootstrap";
import { createProduct } from "../actions/productActions";
import { checkTokenValidation, logout } from "../actions/userActions";
import stockImg from "./img-not-found.jpg";


function ProductsListPage() {

    let history = useHistory()
    let searchTerm = history.location.search
    const dispatch = useDispatch()

    // products list reducer
    const productsListReducer = useSelector(state => state.productsListReducer)
    const { loading, error, products } = productsListReducer



    const [product_from, setProduct_from] = useState("");
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [price, setPrice] = useState("100");
    const [stock, setStock] = useState(false);
    const [image, setImage] = useState(null);
    const [image2, setImage2] = useState(stockImg);
    const [image3, setImage3] = useState(stockImg);
  
    // login reducer
    const userLoginReducer = useSelector((state) => state.userLoginReducer);
    const { userInfo } = userLoginReducer;
  
    // create product reducer
    const createProductReducer = useSelector(
      (state) => state.createProductReducer
    );
    const {
      product,
      success: productCreationSuccess,
      error: productCreationError,
    } = createProductReducer;
  
    console.log(products)
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
  
    const onSubmit = (e) => {
      e.preventDefault();
  
      let form_data = new FormData();
      form_data.append("product_from", product_from);
      form_data.append("name", name);
      form_data.append("description", description);
      form_data.append("price", price);
      form_data.append("stock", stock);
      form_data.append("image", image);
      form_data.append("image2", image2);
      form_data.append("image3", image3);
  
      dispatch(createProduct(form_data));
    };
  
    if (productCreationSuccess) {
      alert("Product successfully created.");
      history.push(`/product/${product.id}/`);
      dispatch({
        type: CREATE_PRODUCT_RESET,
      });
    }
  
    if (userInfo && tokenError === "Request failed with status code 401") {
      alert("Session expired, please login again.");
      dispatch(logout());
      history.push("/login");
      window.location.reload();
    }
    

    useEffect(() => {
        dispatch(getProductsList())
        dispatch({
            type: CREATE_PRODUCT_RESET
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
                
            <Form onSubmit={onSubmit}>
        <Form.Group controlId="name">
          <Form.Label>
            <b>Product Name</b>
          </Form.Label>
          <Form.Control
            required
            autoFocus={true}
            type="text"
            value={name}
            placeholder="product name"
            onChange={(e) => {
              setName(e.target.value);
              setProduct_from(userInfo.username);
            }}
          ></Form.Control>
        </Form.Group>

        <Form.Group controlId="description">
          <Form.Label>
            <b>Product Description</b>
          </Form.Label>
          <Form.Control
            required
            type="text"
            value={description}
            placeholder="product description"
            onChange={(e) => setDescription(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Form.Group controlId="price">
          <Form.Label>
            <b>Price</b>
          </Form.Label>
          <Form.Control
            required
            type="text"
            pattern="[0-9]+(\.[0-9]{1,2})?%?"
            value={price}
            placeholder="199.99"
            step="0.01"
            maxLength="8"
            onChange={(e) => setPrice(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <span style={{ display: "flex" }}>
          <label>In Stock</label>
          <input
            type="checkbox"
            value={stock}
            className="ml-2 mt-2"
            onChange={() => setStock(!stock)}
          />
        </span>

        <Form.Group controlId="image">
          <Form.Label>
            <b>Product Image</b>
          </Form.Label>
          <Form.Control
            required
            type="file"
            onChange={(e) => {
              setImage(e.target.files[0]);
            }}
          ></Form.Control>
        </Form.Group>
        <Form.Group controlId="image2">
          <Form.Label>
            <b>Product Image</b>
          </Form.Label>
          <Form.Control
            required
            type="file"
            onChange={(e) => setImage2(e.target.files[0])}
          ></Form.Control>
        </Form.Group>
        <Form.Group controlId="image3">
          <Form.Label>
            <b>Product Image</b>
          </Form.Label>
          <Form.Control
            required
            type="file"
            onChange={(e) => setImage3(e.target.files[0])}
          ></Form.Control>
        </Form.Group>
        <Button
          type="submit"
          variant="success"
          className="btn-sm button-focus-css"
        >
          Save Product
        </Button>
        <Button
          type="submit"
          variant="primary"
          className="btn-sm ml-2 button-focus-css"
          onClick={() => {
            history.push("/");
          }}
        >
          Cancel
        </Button>
      </Form>
            
                <Row>

                    {/* If length of the filter result is equal to 0 then show 'nothing found' message
                        with help of showNothingMessage function else show the filtered result on the
                        webpage and then run the map function */}
                    
                    {(products.filter((item) =>
                        item.product_from == userInfo.username
                    )).length === 0 ? showNothingMessage() : 
                    
                    (products.filter((item) =>
                    item.product_from == userInfo.username
                    )).map((product, idx) => (
                        <Col key={product.id} sm={12} md={6} lg={4} xl={3}>
                            <div className="mx-2"> 
                                <Product product={product} />
                            </div>
                        </Col>
                    )
                    )}
                </Row>
            </div>
        </div>
    )
}

export default ProductsListPage
