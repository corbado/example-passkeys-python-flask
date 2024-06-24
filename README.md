# Flask Passkey Example App

## Project Overview

This project implements a web application with a login system using Corbado' passkey-first authentication service
integrated with a Flask backend. The application consists of two main pages: a login page and a home page. Once users
log in successfully via the Corbado service on the login page, they are redirected to the home page where they can log
out and view protected content.

Please see the [full blog post](https://www.corbado.com/blog/passkeys-python-flask) to understand the detailed steps needed to integrate passkeys into Flask apps.

## Tools and Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python, used to build the backend of the application.
- **Corbado Python SDK**: A comprehensive Python SDK for interacting with Corbado services.
- **Python-dotenv**: A Python package to read key-value pairs from a `.env` file and set them as environment variables.
- **HTML & CSS**: Used to structure and style the frontend of the application.

## Features

- **Passkey-first Authentication**: Utilizes Corbado's authentication service for secure user login.
- **Session management**: Uses Corbado's session management to display content based on the user's authentication status.

## How to Use

### Step 1: Clone the Repository

Clone this repository to your local machine by running:

```sh
git clone https://github.com/corbado/example-passkeys-python-flask

```

### Step 2: Create .env File

To configure the credentials, you will need to create a .env file with your project ID and API secret from Corbado:
To get your project ID and API secret visit your [Corbado developer panel](https://app.corbado.com/).

Please refer to the [Corbado docs](https://docs.corbado.com/overview/welcome) for more details on obtaining the
necessary credentials and integrating Corbado authentication in your application.

```sh
PROJECT_ID=<your-project-id>
API_SECRET=<your-api-secret>

```

### Step 3: Run the Project

Use the following command to run the project in a docker container:

```sh
docker compose up
```
