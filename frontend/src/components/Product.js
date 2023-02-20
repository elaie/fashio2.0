import { Card } from "react-bootstrap";
import { Link } from "react-router-dom";

import React from "react";
import "../pages/product-page.css";
function Product({ product }) {
  return (
    <div>
      <div className="product-card">
    
          <Link to={`/product/${product.id}`}>
            <img className="product-image" src={product.image} />
          </Link>
          <Link to={`/product/${product.id}`}>
            <p className="product-price">{product.name}</p>
          </Link>
          <Card.Text as="h3">₹ {product.price}</Card.Text>
       
      </div>
    </div>
  );
}

export default Product;
