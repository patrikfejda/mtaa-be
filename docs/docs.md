---
title: "Messenger app COMLY"
subtitle: "Assignment no. 1 -  Mobile technologies and applications"
author: [Patrik Fejda, Matej Pavlík]
date: "27.4.2023"
keywords: [Markdown, Example]
titlepage: true
titlepage-color: "423f3b"
titlepage-text-color: "FFFAFA"
titlepage-rule-color: "FFFAFA"
titlepage-rule-height: 2
link-citations: true
linkcolor: "423f3b"
---
\pagebreak

## Assignment Information

|                |                                                            |
| -------------- | ---------------------------------------------------------- |
| **Name**       | Messenger app COMLY                                        |
| **Task**       | Docs                                                       |
| **Team**       | Patrik Fejda, Matej Pavlík                                 |
| **University** | Slovak Technical University in Bratislava                  |
| **Faculty**    | Faculty of Informatics and Information Technologies        |
| **Subject**    | MTAA_B - Mobile technologies and applications              |
| **Year**       | 2022/2023 Summer semester                                  |
| **Exercising** | Ing. Marek Galinski, PhD.                                  |
| **Lecturer**   | prof. Ing. Ivan Kotuliak, PhD. , Ing. Marek Galinski, PhD. |
| **Group**      | Tuesday 11:00                                              |

\pagebreak

## Introduction

We are building a native mobile app for Android - a messaging app that will allow users to communicate with each other.

The app will allow the users to communicate in one-2-one chats and group chats and to share their current status with other users.

### Project objectives

The main objective of the project is to build a modern messaging app, that will fulfill the social needs of the nowadays users.

The app is reflecting the social need for being more "real" by sharing the current status and location with other users.
Status will allow users to share their current mood, activity or something new in a gentle way - with no feel of flaunting or bragging. 

One of other advantages of the app will be that no "friending" will be required - the users will be able to communicate with each other without any prior communication.

## Features

### One-2-One Chats

The app will allow users to communicate with each other in one-2-one chats.
They will be able to send message to every user in the app.
User will be able to see the list of all the users in the app and start a chat with any of them.
In additional, they can send photos taken by the in-app camera.

### Group Chats

Same as one-2-one chats, but with multiple users.
The users will be able to create a group chat with other users.
Every group chat will have a name, which will be set by the user who created the group and can be changed by any user in the group.

### Video calls

The app will allow users to make video calls to each other. 
Video calls will be possible both in one-2-one chats and in group chats.
The videocalls will have a slack's huddle-like style - the user will not get any bothering notifications about the call, but will be able to join the call at any time clicking the "Join call" button.

### User status

The app will allow users to set their status. The status will be visible to all the users in the app.

Status is meant to be a simple quote or a short message about their current mood or activity and their current location.
Sharing status without sharing the location will not be possible.

### User profile

User can set their display name and profile picture. The profile picture will be visible to all the users in the app.
The display name will be default to the username, but can be changed by the user.

## Technical specification

### Backend

The backend will contain the following services:

- postgresql database
- python API app
  
Services will be deployed on a single server using Docker.

Python API app will be built using FastAPI framework.
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
For connecting to the database, we will use SQLAlchemy ORM.
Sending messages will be done using websockets.
Storing binary files (images) will be done using filestorage.

#### BE Used libraries

- `datetime`: A library for working with dates and times.
- `enum`: A library for creating enumerated constants in Python.
- `faker`: A library for generating fake data such as names, addresses, and phone numbers.
- `fastapi`: A modern, fast web framework for building APIs.
- `filetype`: A library for detecting file types by their content.
- `humps`: A library for converting object keys between camelCase and snake_case.
- `json`: A library for encoding and decoding JSON data.
- `jose`: A library for encoding, decoding, and verifying JSON Web Tokens (JWTs).
- `os`: A library for interacting with the operating system.
- `pydantic`: A library for data validation and settings management based on Python type annotations.
- `pytest`: A library for writing and running tests in Python.
- `random`: A library for generating random numbers and values.
- `shutil`: A library for file operations, including copying and deleting files and directories.
- `signal`: A library for sending and receiving signals between processes.
- `sqlalchemy`: A library for working with SQL databases in Python.
- `string`: A library for working with strings and text.
- `typing`: A library for defining and using Python type hints.
- `unicodedata`: A library for working with Unicode characters and text.

### Deployment

The app (consisting of postgresql database and python API app) will be deployed on a single server using Docker.

Docker image is provided in the repo.

Docker will be use both for development and production environments,
which will provide consistency between environments and will allow for easy deployment.

Local development environment will be deployed using docker-compose.
The production environment will be deployed on a cloud server.

### Frontend

The app will be build for Android using React Native.

The frontend will be using the following tech stack:

- React Native
- TypeScript
- NativeBase for UI components
- Redux for state management
- Immer for handling immutable data (via Redux Toolkit)
- React Navigation for navigating between screens

#### FE Used libraries

- `date-fns`: A JavaScript date utility library with a focus on providing functions to format, parse, and manipulate dates.
  - `formatRelative`: A function that formats a date as a string representing the time difference relative to the current date. For example, "2 days ago" or "in 3 hours".
  - `parseJSON`: A function that parses a string representation of a date in ISO format and returns a Date object.
- `date-fns/locale`: A module that provides localized strings for date-fns.
  - `enUS`: An object containing English (United States) localized strings for use with date-fns.
- `immer`: A library that allows you to work with immutable data in a more convenient way by using a draft state that you can modify as if it were mutable.
  - `produce`: A function that takes an initial state and a modifier function, and returns a new state that is the result of applying the modifier function to the initial state.
- `native-base`: A UI library for React Native that provides pre-built, customizable components.
  - `Avatar`: A component for displaying user avatars.
  - `Box`: A component for creating layout boxes with customizable styles.
  - `Button`: A component for creating buttons with customizable styles.
  - `FormControl`: A component for creating form controls with customizable styles.
  - `Input`: A component for creating text input fields with customizable styles.
  - `Text`: A component for displaying text with customizable styles.
  - `VStack`: A component for creating vertically stacked layout boxes with customizable styles.
  - `HStack`: A component for creating horizontally stacked layout boxes with customizable styles.
  - `View`: A component for creating layout views with customizable styles.
  - `NativeBaseProvider`: A component that provides a theme to all NativeBase components.
  - `extendTheme`: A function that allows you to extend the default NativeBase theme with your own customizations.
  - `Center`: A component for centering child elements within a layout.
  - `Icon`: A component for displaying icons from various icon sets with customizable styles.
  - `IconButton`: A component for creating clickable icons with customizable styles.
  - `StatusBar`: A component for customizing the status bar on Android and iOS devices.
  - `useToken`: A hook that allows you to access theme tokens from the NativeBase theme.
  - `Toast`: A component for displaying toast messages with customizable styles.
  - `IAlertProps`: A type definition for props that can be passed to the Alert component.
- `react`: a JavaScript library for building user interfaces.
  - `React`: the main package for building UI components using React.
  - `useState`: a hook that allows functional components to have stateful logic.
- `react-native`: a framework for building mobile applications using React.
  - `AppRegistry`: a module that registers the root component of the application.
  - `Alert`: a module that displays an alert dialog.
  - `View`: a component used for grouping and positioning other components.
  - `Text`: a component used for displaying text.
  - `Modal`: a component used for displaying content over other content.
  - `Pressable`: a component used for handling user touch events.
  - `ScrollView`: a component used for scrolling content that is too large to fit on the screen.
- `react-native-fs`: a module that provides access to the file system on a device.
  - `RNFS`: the main module for interacting with the file system.
- `react-native-geo-location-service`: a module that provides access to the device's location.
  - `Geolocation`: the main module for interacting with the location service.
- `react-native-image-picker`: a module that allows users to select or capture images from their device's camera or gallery.
  - `launchCamera`: a function that launches the device's camera to take a new photo.
  - `launchImageLibrary`: a function that launches the device's gallery to select an existing photo.
- `react-native-permissions`: a module that provides access to the device's permissions.
  - `check`: a function that checks if a specific permission is granted.
  - `PERMISSIONS`: an object that contains the names of various permissions.
  - `request`: a function that requests a specific permission.
  - `RESULTS`: an object that contains the possible results of a permission request.
  - `openSettings`: a function that opens the device's settings app to the permissions page.
- `react-native-vector-icons/MaterialIcons`: a module that provides access to the Material Icons font.
  - `MaterialIcons`: a component that renders an icon from the Material Icons font.
- `react-navigation/bottom-tabs`
  - `BottomTabHeaderProps`: Props for the header component of a bottom tab navigator.
  - `BottomTabBarProps`: Props for the bottom tab bar component of a bottom tab navigator.
  - `createBottomTabNavigator`: Function to create a bottom tab navigator.
  - `bottomTabScreenOptions`: Options for a screen in a bottom tab navigator.
- `react-navigation/native`
  - `DarkTheme`: Predefined dark theme for a navigation container.
  - `NavigationContainer`: Component that manages the navigation tree and handles the navigation state.
  - `useFocusEffect`: Hook that runs an effect when a screen gains or loses focus.
  - `CompositeScreenProps`: Type for the props of a screen in a navigation container.
- `react-navigation/native-stack`
  - `NativeStackHeaderProps`: Props for the header component of a native stack navigator.
  - `createNativeStackNavigator`: Function to create a native stack navigator.
  - `NativeStackScreenProps`: Type for the props of a screen in a native stack navigator.
- `react-redux`
  - `Provider`: Component that provides the Redux store to the component tree.
  - `TypedUseSelectorHook`: Hook that provides typed access to the Redux store's state.
  - `useDispatch`: Hook that returns the dispatch function from the Redux store.
  - `useSelector`: Hook that returns a value from the Redux store's state.
- `react-test-renderer`
  - `renderer`: Object with methods for rendering React components for testing purposes.
- `reduxjs/toolkit`
  - `createSlice`: Function to create a slice of the Redux store's state and associated reducers and actions.
  - `isAnyOf`: Function to create a matcher that returns true if any of the given action types match the action.
  - `configureStore`: Function to create a Redux store with preconfigured settings and middleware.
  - `Middleware`: Interface for a Redux middleware.
  - `isRejectedWithValue`: Function to create a matcher that returns true if an action is a rejected promise with a specific value.
  - `Action`: Interface for a Redux action.
  - `ThunkAction`: Type for a Redux thunk action.
- `reduxjs/toolkit/query/react`
  - `createApi`: Function to create an API object with preconfigured endpoints for making network requests.
  - `fetchBaseQuery`: Function to create a base fetch function for use with an API object.

### System APIs

The app will allow users to use the camera for taking photos and videos and for making video calls.
Also, the app will use the location services for sharing their location in status.

For that purpose, the app will use the following system APIs:

- Camera and gallery
- GPS location

## Users

App will have only type of users - regular users.
A regular user will be able to self-register in the app and use the app to communicate with other users.

In the app, no need for administrators will be required.

## UAT Tests

### Test 1: Send message to new user

**Description:** User sends a message to a user, with whom he has not had any previous communication.

**Preconditions:** User is logged in, user has a stable internet connection.

**Postconditions:** Message is sent to the user, user receives the message.

**Steps:**

1. User clicks on the "New message" button in the conversation list menu.
2. System displays a list of all users.
3. User selects a user, with whom he wants to communicate.
4. System shows a chat screen with selected user.
5. User types a message and clicks on the "Send" button.
6. System sends the message to the user.

### Test 1.1: Send message to old user (Alternative flow)

**Description:** User sends a message to a user, with whom he has had previous communication.

**Preconditions:** User is logged in, user has a stable internet connection.

**Postconditions:** Message is sent to the user, user receives the message.

**Steps:**

1. User selects a conversation with user, with whom he wants to communicate.
2. Continue with step 4 from Test 1.

### Test 2: Create group

**Description:** User creates a chat group with other users.

**Preconditions:** User is logged in, user has a stable internet connection.

**Postconditions:** Group is created, selected users are added to the group.

**Steps:**

1. User clicks on the "New message" button in the conversation list menu.
2. System displays a list of all users.
3. User clicks on the "Create group" button.
4. System displays a list of all users with checkboxes, input group name field and a "Create" button.
5. User sets the group name and selects users, with whom he wants to create a group and clicks on the "Create" button.
6. System creates a group, adds selected users to the group and displays the group chat.

### Test 3: Send message to group

**Description:** User sends a message to a group.

**Preconditions:** User is logged in, user has a stable internet connection, user is in a group (see Test 2).

**Postconditions:** Message is sent to the group, all users in the group receive the message.

**Steps:**

1. User selects a group conversation.
2. System shows a chat screen with selected group.
3. User types a message and clicks on the "Send" button.
4. Message is sent to the group.

### Test 4: Set status

**Description:** User sets their status.

**Preconditions:** User is logged in, user has a stable internet connection and GPS is enabled.

**Postconditions:** User's status is set with GPS information.

**Steps:**

1. User clicks on the "Status" button in the conversation list menu.
2. System displays a status screen with a text input field and a "Set" button.
3. User types a status and clicks on the "Set" button.
4. System fetched the GPS info from the device and sets the status with GPS info.

### Test 5: Send photo

**Description:** User sends a photo to another user.

**Preconditions:** User is logged in, user has a stable internet connection, app has working access to camera.

**Postconditions:** Photo is sent to the user.

**Steps:**

1. User selects a conversation with user, with whom he wants to communicate.
2. System shows a chat screen with selected user.
3. User clicks on the "Photo" button.
4. Sytem opens the camera interface.
5. User takes a photo and clicks on the "Send" button.
6. System sends the photo to the user.

### Test 6: Set profile photo

**Description:** User sets their profile photo.

**Preconditions:** User is logged in, user has a stable internet connection and app has working access to gallery.

**Postconditions:** User's profile photo and display name are set.

**Steps:**

1. User clicks on the "Settings" button in the conversation list menu.
2. System displays a settings screen with a "Change photo" button, a "Change display name" box.
3. User clicks on the "Change photo" button.
4. System opens the gallery interface.
5. User selects a photo and clicks on the "Set" button.
6. Profile photo is set.

### Test 6.1: Change display name (Alternative flow)

**Description:** User changes their display name.

**Preconditions:** User is logged in, user has a stable internet connection.

**Postconditions:** User's display name is changed.

**Steps:**

1. Follow steps 1-2 from Test 7.
2. User types a new display name and clicks on the "Set" button.
3. System changes the display name.

### Test 7: Send message with no internet connection

**Description:** User sends a message to another user with no internet connection.

**Preconditions:** User is logged in, user has no internet connection.

**Postconditions:** Message is saved as an unsent message (will sent when the internet connection is restored).

**Steps:**

1. User selects a conversation with user, with whom he wants to communicate.
2. System shows a chat screen with selected user.
3. User types a message and clicks on the "Send" button.
4. Message is saved as an unsent message.
5. User enables access to the internet.
6. System connectes to the server.
7. User clicks on the unsent message.
8. Message is sent to the user.

### Test 8: Save draft message

**Description:** User saves a draft message.

**Preconditions:** User is logged in, user has a stable internet connection.

**Postconditions:** Message is saved as a draft message.

**Steps:**

1. User selects a conversation with user, with whom he wants to communicate.
2. System shows a chat screen with selected user.
3. User types a message and clicks on the "Back" button.
4. System shows list of conversations screen.
5. User open the previous conversation.
6. System shows a chat screen with selected user and the draft message.
7. User click on the "Send" button.
8. Message is sent to the user.

### Test 9: Weak password

**Description:** User tries to register with a weak password.

**Preconditions:** User is not logged in, user has a stable internet connection.

**Postconditions:** User is not registered.

**Steps:**

1. User clicks on the "Register" button in the login screen.
2. System displays a registration screen with a form and a "Register" button.
3. User types valid email, display name and a weak password, clicks on the "Register" button.
4. System displays an error message.  

### Test 9.1: Email already exists (Alternative flow)

**Description:** User tries to register with an email that already exists.

**Preconditions:** User is not logged in, user has a stable internet connection.

**Postconditions:** User is not registered.

**Steps:**

1. Follow steps 1-2 from Test 10.
2. User types valid email of user that already exists, display name and a strong password, clicks on the "Register" button.
3. System displays an error message.

### Test 10: Not appropriate language in status

**Description:** User tries to set a status with not appropriate language.

**Preconditions:** User is logged in, user has a stable internet connection and GPS is enabled.

**Postconditions:** User's status is not set.

**Steps:**

1. User clicks on the "Status" button in the conversation list menu.
2. System displays a status screen with a text input field and a "Set" button.
3. User types a status with not appropriate language and clicks on the "Set" button.
4. System displays an error message.

### Test 11: GPS not available

**Description:** User tries to set a status with GPS not available.

**Preconditions:** User is logged in, user has a stable internet connection and GPS is not available.

**Postconditions:** User's status is not set.

**Steps:**

1. User clicks on the "Status" button in the conversation list menu.
2. System displays a status screen with a text input field and a "Set" button.
3. User types a status and clicks on the "Set" button.
4. System displays an error message.

## API endpoints

See [swagger](https://patrikfejda.github.io/mtaa-be/).

## Data model

```mermaid
classDiagram
    class User {
        Int id
        String email
        String username
        String password
        Strind displayName
        String profilePhotoUrl
        String jwt
        Timestamp createdAt
        login()
        register()
        set()
        get()
        getAll()
    }
    class Status {
        Int id
        User userId
        String status
        Float longitude
        Float latitude
        Timestamp createdAt
        create()
        get()
        getAll()
        delete()
    }
    class Conversation {
        Int id
        Boolean isGroup
        String name
        List<User> users
        Timestamp createdAt
        create()
        get()
        getAll()
        getAllMessagesInConversation()
    }
    class Message {
        Int id
        User userId
        Conversation conversationId
        String message
        String photoUrl
        Timestamp createdAt
        create()
        get()
    }

    User "1" -- "0*" Status
    Conversation "0*" -- "0*" User
    User "1" -- "0*" Message
    Conversation "1" -- "0*" Message
```

[![class diagram](https://mermaid.ink/img/pako:eNq1VNuK2zAQ_RWhp7Zkg5ykvlEK210KC81T2pdiMIM161VXlowkd5uG_HtlO8VObEJLqV48OnORztF4DrTQHGlKCwnW3gsoDVSZIn51CPli0ZBDj7TrQTki-LDfOSNUSbACISdo45MVVDhx1L70izaXdTjhwtYS9vl8ltGPQmJeP2mn88ZMD_z24gbss6jQOqhqUhgEhzyHkVfqUqhXrwfAYCmsQzPGLLrxtpxsb6X8jRzHsu0cuMZeE64TthUon5HTdukD_FFqcP7KqhSu4ThxgLvAr3PvsT9m1i6OEoeUM653Wn1HY_0dtLrG-IPWEkERYfPS6KaesD5_9E_-Nd61Kr3vZLL_kVyPbNFaKNE-qDGjWcqn0L9_3zOtitFmrguq_pTpfzDt_3-QxBPrje7GGQ0ySm5uvMHeeGs36sSzy5_8Q2SbfqXQdkzmotJsJF3QCo2fK9yPp07ojLon9C1CU29yMM8ZzdTRx0Hj9G6vCpo60-CCNjX3fE_TjKaPIK1Ha1A0PdAfNA2i9ZJtklUcvU3CdcTC1YLuPcw2y2gdrFcsjlcJS-LouKA_tfYl2DJi0SZmIUs2QZiEQdTV-9o5-0ORC6fN9jRO28_xFz4hkkk?type=png)](https://mermaid.live/edit#pako:eNq1VNuK2zAQ_RWhp7Zkg5ykvlEK210KC81T2pdiMIM161VXlowkd5uG_HtlO8VObEJLqV48OnORztF4DrTQHGlKCwnW3gsoDVSZIn51CPli0ZBDj7TrQTki-LDfOSNUSbACISdo45MVVDhx1L70izaXdTjhwtYS9vl8ltGPQmJeP2mn88ZMD_z24gbss6jQOqhqUhgEhzyHkVfqUqhXrwfAYCmsQzPGLLrxtpxsb6X8jRzHsu0cuMZeE64TthUon5HTdukD_FFqcP7KqhSu4ThxgLvAr3PvsT9m1i6OEoeUM653Wn1HY_0dtLrG-IPWEkERYfPS6KaesD5_9E_-Nd61Kr3vZLL_kVyPbNFaKNE-qDGjWcqn0L9_3zOtitFmrguq_pTpfzDt_3-QxBPrje7GGQ0ySm5uvMHeeGs36sSzy5_8Q2SbfqXQdkzmotJsJF3QCo2fK9yPp07ojLon9C1CU29yMM8ZzdTRx0Hj9G6vCpo60-CCNjX3fE_TjKaPIK1Ha1A0PdAfNA2i9ZJtklUcvU3CdcTC1YLuPcw2y2gdrFcsjlcJS-LouKA_tfYl2DJi0SZmIUs2QZiEQdTV-9o5-0ORC6fN9jRO28_xFz4hkkk)

## Changes from the design

### Minor

- `login` and `register` dont have `/user/` prefix but `v2/auth` instead
- using endpoint `v2/auth/check` instead of GET my data (`/user`)
- PUT `/user` path changed to PUT `users/me`
- Status - renamed attribute `status` to `text`

### Medium

- change paths from singular to plural (e.g. `/user` -> `/users`)
- GET `/status` is not implemented, only GET `/statuses` (Getting all statuses)
- DELETE `/status/{id}` - parameter `id` is in URL instead of body

### Major

- videocall is not implemented
  
## Wireframes

Figma project can be found [here](https://www.figma.com/proto/ROXp0vs8txJrxb912lWvNa/MTAA-APP?node-id=0%3A1)

### Login

![Login](./img/Log_In.png)

### Register

![Register](./img/Register.png)

### Message

![Message](./img/Message.png)

### New chat modal

![New chat modal](./img/New_chat_modal.png)

### Settings

![Settings](./img/Settings.png)

### Start a group chat modal

![Start a group chat modal](./img/Start_a_group_chat_modal.png)

### Status detail modal

![Status detail modal](./img/Status_detail_modal.png)

### Status

![Status](./img/Status.png)

### Video call

![Video call](./img/Video_call.png)