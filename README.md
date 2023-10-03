# CSMessageApp

A web-based customer service messaging application to streamline and manage customer inquiries.

## Overview

CSMessageApp provides a platform for customers to send messages or inquiries. Agents can log in to the portal, view these messages, and reply to them. The application ensures streamlined communication and efficient handling of customer inquiries.

## Features

- **Customer Portal**:

  - Customers can send messages to agents.
  - Customers can search by their ID to see replies.

- **Agent Portal**:

  - Agents can login to view customer messages.
  - Agents can reply to customer messages.
  - Display of unread messages with distinct visual indication.
  - Messages are evenly distributed among agents to ensure efficient handling.
  - Agent registration feature.
  - Multiple agents can log in simultaneously and work in parallel without overlapping.

- **Database**:

  - SQLite based database for easy setup and portability.
  - Stores customer messages and agent replies.
  - Maintains agent registration, login credentials and message assignments.

- **Security**:
  - Agent passwords are securely hashed using bcrypt.
  - Sessions are maintained for logged-in agents to enhance security.
- **Bootstrap Integration**:
  - Provides a clean and responsive design for both customer and agent portals.

## Getting Started

### Prerequisites

- Python
- Flask
- SQLite
- bcrypt

### Setup & Installation

1. Clone the repository:
   git clone https://github.com/bella-babu/CSMessageApp.git

2. Navigate to the project directory:
   cd CSMessageApp

3. Install the required Python packages:
   pip install -r requirements.txt

4. Set up the database:
   python db_setup.py

5. Run the application:
   python app.py

6. The application should now be running at `http://127.0.0.1:5000/`.

## Usage

1. As a customer, navigate to the homepage to send a message or search for a reply using your ID.
2. As an agent, navigate to `/agentlogin` to access the agent portal. If it's your first time, register an account and then log in.
3. Agents can view assigned messages and reply to them directly from the agent portal.

## Future Enhancements

- Integrate user registration and password reset functionality for agents.
- Implement real-time message updates using WebSockets.
- Add search and filtering options for agents to manage messages more efficiently.
- Incorporate a more advanced authentication mechanism, possibly using OAuth or JWT.
- Add analytics to provide insights into agent performance and customer message trends.

## Demo

- Link: [Demo Link (Yet to be provided)]
