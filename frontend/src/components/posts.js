import { Card } from 'react-bootstrap'
import { Link } from 'react-router-dom'

import React from 'react'

function Post({ post }) {
    console.log("INSIDE POST.JS")
    console.log(post.id)
    return (
        <div>
            <Card className="mb-4 rounded">

                <Card.Body>
                <Link to={`/post/${post.id}`}>
                    <Card.Img variant="top" src={post.post_image} height="162" />
                </Link>
                    <Link to={`/post/${post.id}`}>
                        <Card.Title as="div">
                            <strong>{post.post_name}</strong>
                        </Card.Title>
                    </Link>
                </Card.Body>
            </Card>
        </div>
    )
}

export default Post
