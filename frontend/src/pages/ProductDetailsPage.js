import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { deleteProduct, getProductDetails } from "../actions/productActions";
import Message from "../components/Message";
import {
  Spinner,
  Row,
  Col,
  Container,
  Card,
  Button,
  Modal,
} from "react-bootstrap";
import { Link } from "react-router-dom";
import {
  CREATE_PRODUCT_RESET,
  DELETE_PRODUCT_RESET,
  UPDATE_PRODUCT_RESET,
  CARD_CREATE_RESET,
} from "../constants";
import "./product-page.css";

const ProductDetailsPage = ({ history, match }) => {
  const dispatch = useDispatch();
  console.log("PRODUCT DETAIL PAGE");
  // modal state and functions
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  // product details reducer
  const productDetailsReducer = useSelector(
    (state) => state.productDetailsReducer
  );
  const { loading, error, product } = productDetailsReducer;

  // login reducer
  const userLoginReducer = useSelector((state) => state.userLoginReducer);
  const { userInfo } = userLoginReducer;

  // product details reducer
  const deleteProductReducer = useSelector(
    (state) => state.deleteProductReducer
  );
  const { success: productDeletionSuccess } = deleteProductReducer;

  useEffect(() => {
    dispatch(getProductDetails(match.params.id));
    dispatch({
      type: UPDATE_PRODUCT_RESET,
    });
    dispatch({
      type: CREATE_PRODUCT_RESET,
    });
    dispatch({
      type: CARD_CREATE_RESET,
    });
  }, [dispatch, match]);

  // product delete confirmation
  const confirmDelete = () => {
    dispatch(deleteProduct(match.params.id));
    handleClose();
  };

  // after product deletion
  if (productDeletionSuccess) {
    alert("Product successfully deleted.");
    history.push("/");
    dispatch({
      type: DELETE_PRODUCT_RESET,
    });
  }
  // Define some example data for the product
  const product2 = {
    name: "Example Product",
    bio: "This is a short description of the product.",
    price: 19.99,
    colors: ["red", "green", "blue"],
    sizes: ["S", "M", "L", "XL"],
    images: [
      "https://example.com/image1.jpg",
      "https://example.com/image2.jpg",
      "https://example.com/image3.jpg",
    ],
  };

  // Use state to keep track of which color and size is selected
  const [selectedColor, setSelectedColor] = useState(product2.colors[0]);
  const [selectedSize, setSelectedSize] = useState(product2.sizes[0]);

  // Event handler for when the buy now button is clicked

  return (
    <div className="product-page">
      <div className="product-info">
        <div className="container3">
          <img src={product.image} alt="Image 1" className="image" />
          <img src={product.image} alt="Image 2" className="image" />
          <img src={product.image} alt="Image 3" className="image" />
        </div>
      </div>

      <div className="product-description">{/* product description */}</div>
      <div className="product-info">
        <Link to={`/userProfile/${product.product_from}`}>
          <h2>{product.product_from}</h2>
        </Link>
        <h1>{product2.name}</h1>
        <p>{product2.bio}</p>
        <h2>{product.price}</h2>
        <div className="color-options">
          {product2.colors.map((color) => (
            <button
              key={color}
              className={selectedColor === color ? "selected" : ""}
              style={{ backgroundColor: color }}
              onClick={() => setSelectedColor(color)}
            />
          ))}
        </div>
        <div className="size-options">
          {product2.sizes.map((size) => (
            <button
              key={size}
              className={selectedSize === size ? "selected" : ""}
              onClick={() => setSelectedSize(size)}
            >
              {size}
            </button>
          ))}
        </div>
        {product.stock ? (
          <Link to={`${product.id}/checkout/`}>
            <button className="btn btn-primary">
              <span>Pay with Stripe</span>
            </button>
          </Link>
        ) : (
          <Message variant="danger">Out Of Stock!</Message>
        )}
        <div className="product-description">
          <h3>Description:</h3>
          <p>This is a longer description of the product.</p>
        </div>
      </div>
    </div>
  );
};

export default ProductDetailsPage;
