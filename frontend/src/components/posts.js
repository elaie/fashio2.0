import { Card } from 'react-bootstrap'
import { Link } from 'react-router-dom'

import React from 'react'

function Post({ post }) {
    return (
        <div>
            <Card className="mb-4 rounded">

                <Card.Body>
                <Link to={`/posts/${post.id}`}>
                    <Card.Img variant="top" src={post.image} height="162" />
                </Link>
                    <Link to={`/posts/${post.id}`}>
                        <Card.Title as="div">
                            <strong>{post.name}</strong>
                        </Card.Title>
                    </Link>

                    <Card.Text as="h3">
                        ₹ {post.price}
                    </Card.Text>
                </Card.Body>
            </Card>
        </div>
    )
}

export default Post
