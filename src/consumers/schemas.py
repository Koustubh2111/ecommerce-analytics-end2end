schema = {

    'add-to-cart-events' : """
                        {
                        "$schema": "http://json-schema.org/draft-07/schema#",
                        "title": "AddToCart",
                        "description": "Schema for add-to-cart events",
                        "type": "object",
                        "properties": {
                            "userId": {
                            "type": "integer"
                            },
                            "productId": {
                            "type": "integer"
                            },
                            "timestamp": {
                            "type": "string",
                            "format": "date-time"
                            },
                            "quantity": {
                            "type": "integer"
                            }
                        },
                        "required": ["userId", "productId", "timestamp", "quantity"] 
                        }
                        """, \
                        
    'abandon-cart' : """
                    {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "title": "AbandonedCart",
                    "description": "Schema for abandoned cart events",
                    "type": "object",
                    "properties": {
                        "userId": {
                        "type": "integer"
                        },
                        "productId": {
                        "type": "integer"
                        },
                        "timestamp": {
                        "type": "string",
                        "format": "date-time"
                        }
                    },
                    "required": ["userId", "productId", "timestamp"]
                    }
                    """, \
                    
    'purchase-events' : """
                    {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "title": "Purchase",
                    "description": "Schema for purchase events",
                    "type": "object",
                    "properties": {
                        "userId": {
                        "type": "integer"
                        },
                        "orderId": {
                        "type": "integer"
                        },
                        "productId": {
                        "type": "integer"
                        },
                        "timestamp": {
                        "type": "string",
                        "format": "date-time"
                        },
                        "quantity": {
                        "type": "integer"
                        },
                        "price": {
                        "type": "number"
                        }
                    },
                    "required": ["userId", "orderId", "productId", "timestamp", "quantity", "price"]
                    }
                    """, \
    'transactions' : """
                    {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "title": "AddToCart",
                    "description": "Schema for add-to-cart events",
                    "type": "object",
                    "properties": {
                        "userId": {
                        "type": "integer"
                        },
                        "productId": {
                        "type": "integer"
                        },
                        "timestamp": {
                        "type": "string",
                        "format": "date-time"
                        },
                        "quantity": {
                        "type": "integer"
                        }
                    },
                    "required": ["userId", "productId", "timestamp", "quantity"] 
                    }
                    """
}

