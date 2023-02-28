# MTAA APP DOCS

Figma project can be found [here](https://www.figma.com/file/ROXp0vs8txJrxb912lWvNa/MTAA-APP?node-id=0%3A1&t=vOF8JKwrQrwcdOob-0)


## Introduction

We are building a native mobile app for Android - a messaging app that will allow users to communicate with each other.The app will allow the users to communicate in one-2-one chats and group chats.

## Features

### Video calls

The app will allow users to make video calls to each other. 

### User status

The app will allow users to set their status. The status will be visible to all the users in the app.

Status is meant to be a simple quote or a short message about their current mood or activity.

### User profile

User can set their display name and profile picture. The profile picture will be visible to all the users in the app.

## Data model

```mermaid
classDiagram
    class User {
        Int id
        String email
        String username
        String password
        Strind display_name
        String profile_photo_url
        Timestamp created_at
        login()
        register()
        set()
    }
    class Status {
        Int id
        User user_id
        String status
        Float longitude
        Float latitude
        Timestamp created_at
        create()
        delete()
    }
    class Conversation {
        Int id
        Boolean is_group
        String name
        List<User> users
        Timestamp created_at
        create()
        delete()
    }
    class Message {
        Int id
        User user_id
        Conversation conversation_id
        String message
        Timestamp created_at
        create()
    }

    User "1" -- "0*" Status
    Conversation "0*" -- "0*" User
    User "1" -- "0*" Message
    Conversation "1" -- "0*" Message
```

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

#### Test 1.1: Send message to old user (Alternative flow)

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

### Test 4: Add user to group

**Description:** User adds a user to an existing group.
**Preconditions:** User is logged in, user has a stable internet connection, user is in a group (see Test 2).
**Postconditions:** User is added to the group.
**Steps:**
1. User selects a group conversation.
2. System shows a chat screen with selected group.
3. User clicks on the header of the group.
4. System displays a conversation settings screen.
5. User clicks on the "Add user" button.
6. System displays a list of users (that are not in the group already) with checkboxes and a "Add" button.
7. User selects users, whom he wants to add to the group and clicks on the "Add" button.
8. System adds selected users to the group and shows the group chat screen.

#### Test 4.1: Delete user from group (Alternative flow)

**Description:** User deletes a user from an existing group.
**Preconditions:** User is logged in, user has a stable internet connection, users (the deletor and the deletee) are in a group (see Test 2).
**Postconditions:** User is deleted from the group.
**Steps:**
1. Follow steps 1-4 from Test 4.
2. User clicks on the "Delete user" button.
3. System displays a list of users (that are in the group) with checkboxes and a "Delete" button.
4. User selects users, whom he wants to delete from the group and clicks on the "Delete" button.
5. System deletes selected users from the group and shows the group chat screen.

### Test 5: Set status

**Description:** User sets their status.
**Preconditions:** User is logged in, user has a stable internet connection and GPS is enabled.
**Postconditions:** User's status is set with GPS information.
**Steps:**
1. User clicks on the "Status" button in the conversation list menu.
2. System displays a status screen with a text input field and a "Set" button.
3. User types a status and clicks on the "Set" button.
4. System fetched the GPS info from the device and sets the status with GPS info.

### Test 6: Send photo

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

### Test 7: Set profile photo

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

#### Test 7.1: Change display name (Alternative flow)

**Description:** User changes their display name.
**Preconditions:** User is logged in, user has a stable internet connection.
**Postconditions:** User's display name is changed.
**Steps:**
1. Follow steps 1-2 from Test 7.
2. User types a new display name and clicks on the "Set" button.
3. System changes the display name.

### Test 8: Send message with no internet connection

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

### Test 9: Save draft message

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

### Test 10: Weak password

**Description:** User tries to register with a weak password.
**Preconditions:** User is not logged in, user has a stable internet connection.
**Postconditions:** User is not registered.
**Steps:**
1. User clicks on the "Register" button in the login screen.
2. System displays a registration screen with a form and a "Register" button.
3. User types valid email, display name and a weak password, clicks on the "Register" button.
4. System displays an error message.  

#### Test 10.1: Email alredy exists (Alternative flow)

**Description:** User tries to register with an email that already exists.
**Preconditions:** User is not logged in, user has a stable internet connection.
**Postconditions:** User is not registered.
**Steps:**
1. Follow steps 1-2 from Test 10.
2. User types valid email of user that already exists, display name and a strong password, clicks on the "Register" button.
3. System displays an error message.

### Test 11: Not appropriate language in status

**Description:** User tries to set a status with not appropriate language.
**Preconditions:** User is logged in, user has a stable internet connection and GPS is enabled.
**Postconditions:** User's status is not set.
**Steps:**
1. User clicks on the "Status" button in the conversation list menu.
2. System displays a status screen with a text input field and a "Set" button.
3. User types a status with not appropriate language and clicks on the "Set" button.
4. System displays an error message.

### Test 12: GPS not available

**Description:** User tries to set a status with GPS not available.
**Preconditions:** User is logged in, user has a stable internet connection and GPS is not available.
**Postconditions:** User's status is not set.
**Steps:**
1. User clicks on the "Status" button in the conversation list menu.
2. System displays a status screen with a text input field and a "Set" button.
3. User types a status and clicks on the "Set" button.
4. System displays an error message.