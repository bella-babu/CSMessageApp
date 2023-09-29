# CSMessageApp

A web-based customer service messaging application to streamline and manage customer inquiries.

## Overview

CSMessageApp provides a platform for customers to send messages or inquiries. Agents can log in to the portal, view these messages, and reply to them. The application ensures streamlined communication and efficient handling of customer inquiries.

## Features

- **Customer Portal**: Customers can send their inquiries or messages.
- **Agent Portal**: Agents can view customer messages and respond. Multiple agents can log in simultaneously.
- **Bootstrap Integration**: Provides a clean and responsive design.
- **Database**: Stores customer messages and agent replies.
- **User Authentication** (upcoming): Ensures that only authorized agents can access the portal.

## Setup & Installation

1. **Clone the repository**:
   git clone https://github.com/bella-babu/CSMessageApp.git

2. **Navigate to the directory**:
   cd CSMessageApp

3. **Install required Python packages**:
   pip install -r requirements.txt

4. **Run the application**:
   python app.py

5. Open a web browser and navigate to `http://localhost:5000` to access the application.

## Usage

1. **Customer Portal**: Navigate to the main page (`http://localhost:5000`). Customers can enter their message and click "Send".
2. **Agent Portal**: Navigate to the agent portal (`http://localhost:5000/agent_portal`). Agents can view customer messages and reply to them.

## Future Enhancements

- Integrate user registration and password reset functionality for agents.
- Implement real-time message updates using WebSockets.
- Add search and filtering options for agents to manage messages more efficiently.
- Incorporate a more advanced authentication mechanism.

## Contribution

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
