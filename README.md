# [HarvestHub - MERN, Flask, Machine Learning]

> HarvestHub is a comprehensive agricultural project aimed at revolutionizing farming practices by leveraging technology and data-driven insights. It consists of several components, including a React web application, a server-side MERN Stack backend, and an ensembled machine learning model for precise recommendations for crops based on soil parameters.

## Features
- **Crop Recommendation**: Utilizes machine learning algorithms to provide personalized crop recommendations based on soil and environmental data.
- **RestAPIs**: Single API calls for the web app.
- **Secure**: The application is secured with Bcrypt and JWT libraries.
- **Community Forum**: Facilitates knowledge sharing and collaboration among farmers through a dedicated forum.
- **User Authentication**: Users can sign up, log in, and log out securely.

## Technologies Used

- **MongoDB**: NoSQL database used for storing user data, posts, and other information.
- **Express.js**: Web application framework for building APIs and handling HTTP requests.
- **React.js**: Frontend library for building user interfaces.
- **Node.js**: JavaScript runtime environment used for server-side logic.
- **Mongoose**: MongoDB object modeling tool for Node.js.
- **JWT (JSON Web Tokens)**: Used for user authentication and authorization.
- **Bcrypt**: Used for encrypting user passwords.
- **Flask**: Micro web framework written in Python used to load and run the ML model and interact with it.

## Project Structure
The project is organized into the following folders:

- **Server**: Houses the backend server implementation using the MERN stack (MongoDB, Express.js, React.js, Node.js).
- **Client**: Contains the code for the web application frontend, developed using React.js.
- **ML**: Includes the machine learning module responsible for crop recommendation, implemented using Python.

<h3>How to run</h3>
To run HarvestHub on your local machine, follow these steps:

1. Clone the Repository
   ```bash
   git clone https://github.com/prasooncodes/harvesthub.git
   cd harvesthub
   ```

2. Install Dependencies
- **Server**
   ```bash
   cd server
   npm install
   ```

- **Client**
   ```bash
   cd client
   npm install
   ```

- **ML**
   ```bash
   pip install numpy
   pip install pandas
   pip install sklearn
   pip install requests
   pip install pickle
   ```

4. Set Up MongoDB
Ensure you have MongoDB installed and running on your system. Update the MongoDB connection string in the server code if necessary.

5. Start the Servers
- **Server**
  ```bash
  cd server
  npm start
  ```
  
- **Client**
   ```bash
  cd client
  npm run dev
   ```

- **ML**
   ```bash
   cd ml
   python app.py
   ```

6. Access the Application
Web App: Open your web browser and go to http://localhost:3000.

