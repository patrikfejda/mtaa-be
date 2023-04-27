// read swagger/swagger.json to dictionary
var spec = {
    "openapi": "3.0.2",
    "info": {
        "title": "mtaa",
        "version": "0.1.0"
    },
    "paths": {
        "/v2/auth/login": {
            "post": {
                "tags": [
                    "auth"
                ],
                "summary": "Auth Login",
                "operationId": "auth_login_v2_auth_login_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/AuthLogin"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/AuthResponse"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/v2/auth/register": {
            "post": {
                "tags": [
                    "auth"
                ],
                "summary": "Auth Register",
                "operationId": "auth_register_v2_auth_register_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/UserCreate"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/AuthResponse"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/v2/auth/check": {
            "get": {
                "tags": [
                    "auth"
                ],
                "summary": "Auth Check",
                "operationId": "auth_check_v2_auth_check_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/User"
                                }
                            }
                        }
                    }
                },
                "security": [{
                    "OAuth2PasswordBearer": [

                    ]
                }]
            }
        },
        "/v2/users/": {
            "get": {
                "tags": [
                    "users"
                ],
                "summary": "Get All Users",
                "operationId": "get_all_users_v2_users__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Get All Users V2 Users  Get",
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/User"
                                    }
                                }
                            }
                        }
                    }
                },
                "security": [{
                    "OAuth2PasswordBearer": [

                    ]
                }]
            }
        },
        "/v2/users/me": {
            "put": {
                "tags": [
                    "users"
                ],
                "summary": "Update User Me",
                "operationId": "update_user_me_v2_users_me_put",
                "requestBody": {
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_update_user_me_v2_users_me_put"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/User"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                },
                "security": [{
                    "OAuth2PasswordBearer": [

                    ]
                }]
            }
        },
        "/v2/statuses/": {
            "get": {
                "tags": [
                    "statuses"
                ],
                "summary": "Get All Statuses",
                "operationId": "get_all_statuses_v2_statuses__get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Get All Statuses V2 Statuses  Get",
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/Status"
                                    }
                                }
                            }
                        }
                    }
                },
                "security": [{
                    "OAuth2PasswordBearer": [

                    ]
                }]
            },
            "post": {
                "tags": [
                    "statuses"
                ],
                "summary": "Create Status",
                "operationId": "create_status_v2_statuses__post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/StatusCreate"
                            }
                        }
                    },
                    "required": true
                },
                "responses": {
                    "201": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Status"
                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/v2/statuses/{status_id}": {
            "delete": {
                "tags": [
                    "statuses"
                ],
                "summary": "Delete Status",
                "operationId": "delete_status_v2_statuses__status_id__delete",
                "parameters": [{
                    "required": true,
                    "schema": {
                        "title": "Status Id",
                        "type": "integer"
                    },
                    "name": "status_id",
                    "in": "path"
                }],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {

                                }
                            }
                        }
                    },
                    "422": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        }
                    }
                },
                "security": [{
                    "OAuth2PasswordBearer": [

                    ]
                }]
            }
        },
        "/v2/health": {
            "get": {
                "summary": "Health",
                "operationId": "health_v2_health_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {

                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "AuthLogin": {
                "title": "AuthLogin",
                "required": [
                    "username",
                    "password"
                ],
                "type": "object",
                "properties": {
                    "username": {
                        "title": "Username",
                        "type": "string"
                    },
                    "password": {
                        "title": "Password",
                        "type": "string"
                    }
                }
            },
            "AuthResponse": {
                "title": "AuthResponse",
                "required": [
                    "accessToken",
                    "user"
                ],
                "type": "object",
                "properties": {
                    "accessToken": {
                        "title": "Accesstoken",
                        "type": "string"
                    },
                    "user": {
                        "$ref": "#/components/schemas/User"
                    }
                }
            },
            "Body_update_user_me_v2_users_me_put": {
                "title": "Body_update_user_me_v2_users_me_put",
                "type": "object",
                "properties": {
                    "displayName": {
                        "title": "Displayname",
                        "type": "string"
                    },
                    "profilePhoto": {
                        "title": "Profilephoto",
                        "type": "string",
                        "format": "binary"
                    }
                }
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {
                            "$ref": "#/components/schemas/ValidationError"
                        }
                    }
                }
            },
            "Status": {
                "title": "Status",
                "required": [
                    "id",
                    "latitude",
                    "longitude",
                    "text",
                    "createdAt",
                    "author"
                ],
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Id",
                        "type": "integer"
                    },
                    "latitude": {
                        "title": "Latitude",
                        "type": "string"
                    },
                    "longitude": {
                        "title": "Longitude",
                        "type": "string"
                    },
                    "text": {
                        "title": "Text",
                        "type": "string"
                    },
                    "createdAt": {
                        "title": "Createdat",
                        "type": "string",
                        "format": "date-time"
                    },
                    "author": {
                        "$ref": "#/components/schemas/User"
                    }
                }
            },
            "StatusCreate": {
                "title": "StatusCreate",
                "required": [
                    "latitude",
                    "longitude",
                    "text"
                ],
                "type": "object",
                "properties": {
                    "latitude": {
                        "title": "Latitude",
                        "type": "string"
                    },
                    "longitude": {
                        "title": "Longitude",
                        "type": "string"
                    },
                    "text": {
                        "title": "Text",
                        "type": "string"
                    }
                }
            },
            "User": {
                "title": "User",
                "required": [
                    "id",
                    "email",
                    "username"
                ],
                "type": "object",
                "properties": {
                    "id": {
                        "title": "Id",
                        "type": "integer"
                    },
                    "email": {
                        "title": "Email",
                        "type": "string"
                    },
                    "username": {
                        "title": "Username",
                        "type": "string"
                    },
                    "displayName": {
                        "title": "Displayname",
                        "type": "string"
                    },
                    "profilePhotoUrl": {
                        "title": "Profilephotourl",
                        "type": "string"
                    }
                }
            },
            "UserCreate": {
                "title": "UserCreate",
                "required": [
                    "email",
                    "username",
                    "password"
                ],
                "type": "object",
                "properties": {
                    "email": {
                        "title": "Email",
                        "type": "string",
                        "format": "email"
                    },
                    "username": {
                        "title": "Username",
                        "minLength": 3,
                        "type": "string"
                    },
                    "password": {
                        "title": "Password",
                        "minLength": 8,
                        "type": "string"
                    }
                }
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": [
                    "loc",
                    "msg",
                    "type"
                ],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {
                            "anyOf": [{
                                    "type": "string"
                                },
                                {
                                    "type": "integer"
                                }
                            ]
                        }
                    },
                    "msg": {
                        "title": "Message",
                        "type": "string"
                    },
                    "type": {
                        "title": "Error Type",
                        "type": "string"
                    }
                }
            }
        },
        "securitySchemes": {
            "OAuth2PasswordBearer": {
                "type": "oauth2",
                "flows": {
                    "password": {
                        "scopes": {

                        },
                        "tokenUrl": "v2/auth/login"
                    }
                }
            }
        }
    }
}