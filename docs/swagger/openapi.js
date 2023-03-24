// read swagger/swagger.json to dictionary
var spec = {
    "swagger": "2.0",
    "info": {
        "version": "1.0.1",
        "title": "COM.LY API"
    },
    "basePath": "/v1",
    "schemes": [
        "https"
    ],
    "definitions": {
        "User": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "example": 1
                },
                "email": {
                    "type": "string",
                    "example": "user@example.com"
                },
                "username": {
                    "type": "string",
                    "example": "johndoe"
                },
                "displayName": {
                    "type": "string",
                    "example": "John Doe"
                },
                "profilePhotoUrl": {
                    "type": "string",
                    "example": "https://example.com/profile.jpg"
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time",
                    "example": "2023-03-10T12:34:56.789Z"
                }
            }
        },
        "Status": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "example": 1
                },
                "user": {
                    "$ref": "#/definitions/User"
                },
                "status": {
                    "type": "string",
                    "example": "Hello, World!"
                },
                "longitude": {
                    "type": "number",
                    "format": "float",
                    "example": 43.6532
                },
                "latitude": {
                    "type": "number",
                    "format": "float",
                    "example": -79.3832
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time",
                    "example": "2023-03-10T12:34:56.789Z"
                }
            }
        },
        "Conversation": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "example": 1
                },
                "is_group": {
                    "type": "boolean",
                    "example": true
                },
                "name": {
                    "type": "string",
                    "example": "My Group Chat"
                },
                "users": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/User"
                    }
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time",
                    "example": "2023-03-10T12:34:56.789Z"
                }
            }
        },
        "Message": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "example": 1
                },
                "user": {
                    "$ref": "#/definitions/User"
                },
                "conversation_id": {
                    "type": "integer",
                    "example": 123
                },
                "message": {
                    "type": "string",
                    "example": "Hello, World!"
                },
                "photo_url": {
                    "type": "string",
                    "example": "https://example.com/photo.jpg"
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time",
                    "example": "2023-03-10T12:34:56.789Z"
                }
            }
        }
    },
    "consumes": [
        "application/json"
    ],
    "produces": [
        "application/json"
    ],
    "paths": {
        "/user/login": {
            "post": {
                "summary": "Login user",
                "tags": [
                    "User"
                ],
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [{
                    "in": "body",
                    "name": "credentials",
                    "description": "User's login credentials",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string"
                            },
                            "password": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "username",
                            "password"
                        ]
                    }
                }],
                "responses": {
                    "200": {
                        "description": "Successful login",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "access_token": {
                                    "type": "string"
                                },
                                "user": {
                                    "$ref": "#/definitions/User"
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Invalid credentials"
                    }
                }
            }
        },
        "/user/register": {
            "post": {
                "summary": "Register user",
                "tags": [
                    "User"
                ],
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [{
                    "in": "body",
                    "name": "user",
                    "description": "User's registration details",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string"
                            },
                            "password": {
                                "type": "string"
                            },
                            "email": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "username",
                            "password",
                            "email"
                        ]
                    }
                }],
                "responses": {
                    "200": {
                        "description": "Successful registration",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "access_token": {
                                    "type": "string"
                                },
                                "user": {
                                    "$ref": "#/definitions/User"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid registration data"
                    }
                }
            }
        },
        "/user": {
            "get": {
                "summary": "Get user",
                "tags": [
                    "User"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [{
                    "in": "header",
                    "name": "Authorization",
                    "description": "JWT Access token",
                    "type": "string",
                    "required": true
                }],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "schema": {
                            "$ref": "#/definitions/User"
                        }
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            },
            "put": {
                "summary": "Update user",
                "tags": [
                    "User"
                ],
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [{
                        "in": "header",
                        "name": "Authorization",
                        "description": "JWT Access token",
                        "type": "string",
                        "required": true
                    },
                    {
                        "in": "body",
                        "name": "user",
                        "description": "User's updated details",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "displayName": {
                                    "type": "string"
                                },
                                "profilePhotoUrl": {
                                    "type": "string"
                                }
                            }
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation"
                    },
                    "400": {
                        "description": "Invalid user data"
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            }
        },
        "/user/all": {
            "get": {
                "summary": "Get all users",
                "tags": [
                    "User"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [{
                    "in": "header",
                    "name": "Authorization",
                    "description": "JWT Access token",
                    "type": "string",
                    "required": true
                }],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/User"
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            }
        },
        "/status": {
            "post": {
                "summary": "Create status",
                "tags": [
                    "Status"
                ],
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [{
                        "in": "header",
                        "name": "Authorization",
                        "description": "JWT Access token",
                        "type": "string",
                        "required": true
                    },
                    {
                        "in": "body",
                        "name": "status",
                        "description": "Status to be created",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "status": {
                                    "type": "string"
                                },
                                "user": {
                                    "type": "integer"
                                },
                                "latitude": {
                                    "type": "number"
                                },
                                "longitude": {
                                    "type": "number"
                                }
                            },
                            "required": [
                                "status",
                                "user",
                                "latitude",
                                "longitude"
                            ]
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation"
                    },
                    "400": {
                        "description": "Invalid status data"
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            },
            "get": {
                "summary": "Get status",
                "tags": [
                    "Status"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [{
                        "in": "header",
                        "name": "Authorization",
                        "description": "JWT Access token",
                        "type": "string",
                        "required": true
                    },
                    {
                        "in": "query",
                        "name": "id",
                        "description": "Status ID",
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "schema": {
                            "$ref": "#/definitions/Status"
                        }
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            },
            "delete": {
                "summary": "Delete status",
                "tags": [
                    "Status"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [{
                        "in": "header",
                        "name": "Authorization",
                        "description": "JWT Access token",
                        "type": "string",
                        "required": true
                    },
                    {
                        "in": "query",
                        "name": "id",
                        "description": "Status ID",
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation"
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            }
        },
        "/status/all": {
            "get": {
                "summary": "Get all statuses",
                "tags": [
                    "Status"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [{
                    "in": "header",
                    "name": "Authorization",
                    "description": "JWT Access token",
                    "type": "string",
                    "required": true
                }],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/Status"
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            }
        },
        "/conversation": {
            "post": {
                "summary": "Create conversation",
                "tags": [
                    "Conversation"
                ],
                "consumes": [
                    "application/json"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [{
                        "in": "header",
                        "name": "Authorization",
                        "description": "JWT Access token",
                        "type": "string",
                        "required": true
                    },
                    {
                        "in": "body",
                        "name": "conversation",
                        "description": "Conversation to be created",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string"
                                },
                                "users": {
                                    "type": "array",
                                    "items": {
                                        "type": "integer"
                                    }
                                },
                                "is_group": {
                                    "type": "boolean"
                                }
                            },
                            "required": [
                                "name",
                                "users",
                                "is_group"
                            ]
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation"
                    },
                    "400": {
                        "description": "Invalid conversation data"
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            },
            "get": {
                "summary": "Get conversation",
                "tags": [
                    "Conversation"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [{
                        "in": "header",
                        "name": "Authorization",
                        "description": "JWT Access token",
                        "type": "string",
                        "required": true
                    },
                    {
                        "in": "query",
                        "name": "id",
                        "description": "Conversation ID",
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "schema": {
                            "$ref": "#/definitions/Conversation"
                        }
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            }
        },
        "/conversation/all": {
            "get": {
                "summary": "Get all conversations related to user",
                "tags": [
                    "Conversation"
                ],
                "produces": [
                    "application/json"
                ],
                "parameters": [{
                    "in": "header",
                    "name": "Authorization",
                    "description": "JWT Access token",
                    "type": "string",
                    "required": true
                }],
                "responses": {
                    "200": {
                        "description": "Successful operation",
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/Conversation"
                            }
                        }
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                }
            }
        },
        "/message": {
            "post": {
                "summary": "Create a new message",
                "tags": [
                    "Message"
                ],
                "description": "Use this endpoint to create a new message in a conversation",
                "parameters": [{
                    "in": "header",
                    "name": "Authorization",
                    "description": "JWT Access token",
                    "type": "string",
                    "required": true
                }, {
                    "in": "body",
                    "name": "message",
                    "description": "Message object",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "ID of the user sending the message",
                                "example": "123"
                            },
                            "conversation_id": {
                                "type": "string",
                                "description": "ID of the conversation the message is being sent to",
                                "example": "456"
                            },
                            "text": {
                                "type": "string",
                                "description": "Text content of the message",
                                "example": "Hello world"
                            },
                            "photo_url": {
                                "type": "string",
                                "description": "Text content of the message",
                                "example": "https://example.com/photo.jpg"
                            }
                        },
                        "required": [
                            "user",
                            "conversation",
                            "text"
                        ]
                    }
                }],
                "responses": {
                    "200": {
                        "description": "Message created successfully"
                    },
                    "400": {
                        "description": "Invalid input"
                    },
                    "401": {
                        "description": "Unauthorized request"
                    }
                }
            },
            "get": {
                "summary": "Get message",
                "tags": [
                    "Message"
                ],
                "description": "Use this endpoint to retrieve a specific message",
                "parameters": [{
                    "in": "header",
                    "name": "Authorization",
                    "description": "JWT Access token",
                    "type": "string",
                    "required": true
                }, {
                    "in": "query",
                    "name": "message_id",
                    "type": "string",
                    "required": true,
                    "description": "ID of the message to retrieve"
                }],
                "responses": {
                    "200": {
                        "description": "Message retrieved successfully",
                        "schema": {
                            "$ref": "#/definitions/Message"
                        }
                    },
                    "400": {
                        "description": "Invalid input"
                    },
                    "401": {
                        "description": "Unauthorized request"
                    }
                }
            }
        },
        "/message/conversation/all": {
            "get": {
                "summary": "Get all messages in a conversation",
                "tags": [
                    "Message"
                ],
                "description": "Use this endpoint to retrieve all messages in a conversation",
                "parameters": [{
                    "in": "header",
                    "name": "Authorization",
                    "description": "JWT Access token",
                    "type": "string",
                    "required": true
                }, {
                    "in": "query",
                    "name": "conversation_id",
                    "type": "string",
                    "required": true,
                    "description": "ID of the conversation to retrieve messages from"
                }],
                "responses": {
                    "200": {
                        "description": "Messages retrieved successfully",
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/Message"
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input"
                    },
                    "401": {
                        "description": "Unauthorized request"
                    }
                }
            }
        }
    }
}