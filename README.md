# Notely

Notely is an intuitive note-taking application that allows users to easily create, manage, and organize their notes.

---

## 🚀 Features

- **Create Notes**: Create new notes.
- **Update Notes**: Modify existing notes with updated content.
- **Delete Notes**: Remove notes you no longer need.
- **Organize Notes**: Organize and categorize notes by moving them between folders.
- **MongoDB Integration**: Notes are stored in a MongoDB database, using the Motor async driver.
- **FastAPI Backend**: Backend powered by FastAPI, optimized for asynchronous requests.
- **Modern Frontend**: Built with TypeScript and Vite.
- **Firebase Authentication**: Login with Firebase Authentication, supporting Google, GitHub, and other providers.

---

## 🛠️ Tech Stack

| **Category**       | **Technology**         |
|--------------------|------------------------|
| **Backend**        | FastAPI                |
| **Frontend**       | TypeScript, Vite       |
| **Database**       | MongoDB                |
| **Authentication** | Firebase Authentication|
| **Testing**        | Jest (Frontend), Pytest (Backend) |

---

## ⚙️ Setup

### **Prerequisites**

Ensure the following dependencies are installed:

- **Python** (>= 3.10)
- **Node.js** (>= 22)
- **uv** (for managing Python dependencies) → [Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
- **yarn** (for frontend dependencies) → [Installation Guide](https://formulae.brew.sh/formula/yarn)
- **docker & docker-compose** 

---

## 🔑 Firebase Authentication Setup (GitHub as Provider)

### **How It Works**

1. User clicks **"Sign in with GitHub"** in the app.
2. The app redirects the user to **GitHub’s OAuth login page**.
3. User authorizes the app to access their GitHub profile.
4. GitHub sends an **OAuth access token** to Firebase.
5. Firebase verifies the token and creates the user in Firebase Authentication.
6. The user is logged in, and Firebase returns an authentication token.
7. The frontend uses this token to authenticate requests with the backend.
8. Firebase automatically refreshes the token every hour, maintaining the user session without requiring re-login or refresh token requests to the backend.

### **📌 Setting Up GitHub Authentication in Firebase**

#### **1️⃣ Enable GitHub in Firebase**

1. Go to [Firebase Console](https://console.firebase.google.com/).
2. Select your project (or create one if needed) and navigate to **Authentication** → **Sign-in method**.
3. Enable **GitHub** as a sign-in provider.
4. Firebase will request a **Client ID** and **Client Secret** (obtain these from GitHub).

#### **2️⃣ Set Up a GitHub OAuth App**

1. Go to [GitHub Developer Settings](https://github.com/settings/developers).
2. Click **"New OAuth App"**.
3. Fill in the required details:
   - **Application Name**: Your app's name.
   - **Homepage URL**: Your app’s URL (or `http://localhost:3000` for local development).
   - **Authorization Callback URL**: Obtain this from Firebase (`https://your-project.firebaseapp.com/__/auth/handler`).
4. Click **"Register application"**.
5. Copy the **Client ID** and **Client Secret** and paste them into the Firebase Authentication settings.

---

## ⚡ Asynchronous Backend with FastAPI and Motor

FastAPI is optimized for asynchronous programming, allowing multiple requests to be processed concurrently without blocking. 
Additionally, we use **Motor**, an async MongoDB driver, to perform non-blocking database operations. 

---

## 🔧 Backend Setup

### **1️⃣ Install Dependencies**
Navigate to the **backend** directory and run:
```sh
uv sync --group prod --group test --group lint
```

### **2️⃣ Start MongoDB with a Replica Set**
A **MongoDB replica set** is required for atomic transactions. Run the following command to start a MongoDB container with a replica set:
```sh
docker run -d -p 27017:27017 --name mongo -v mongo_data:/data/db mongo:5 mongod --replSet myReplicaSet
```
Initialize the replica set:
```sh
docker exec -it mongo mongosh
use development
rs.initiate()
```

### **3️⃣ Configure Environment Variables**
Create a `.env` file inside the backend directory and copy values from `.env.example`.

📍 **Where to Find Firebase Env Var Values**

1️⃣ Go to [Firebase Console](https://console.firebase.google.com/)

2️⃣ Select your project

3️⃣ Navigate to **Project Settings** (⚙️) → **Service Accounts**

4️⃣ Click **"Generate new private key"**

5️⃣ Download the `.json` file (contains necessary values)

### **4️⃣ Run the Backend Server**

Navigate to the root directory and run:

```sh
make run_be
```

---

## 🎨 Frontend Setup

### **1️⃣ Install Dependencies**
Navigate to the **frontend** directory and run:
```sh
yarn install
```

### **2️⃣ Configure Environment Variables**
Create a `.env` file inside the frontend directory and copy values from `.env.example`.

📍 **Steps to Find Firebase Configuration Values**

1️⃣ Go to [Firebase Console](https://console.firebase.google.com/)

2️⃣ Select your project

3️⃣ Navigate to **Project Settings** (⚙️)

4️⃣ Scroll down to the **"Your apps"** section

5️⃣ Click on your **Web App** (or create one if needed)

6️⃣ Copy values from the Firebase SDK snippet

### **3️⃣ Run the Frontend**

Navigate to the root directory and run:

```sh
make run_fe
```

---

## 🐋 Alternative: Docker Setup

Run the following to start the backend and frontend containers:

```sh
docker-compose -f docker-compose.dev.yml up backend frontend
```

### **Start MongoDB with a Replica Set**
A **MongoDB replica set** is required for atomic transactions. Run the following command to start a MongoDB container with a replica set in the same network as the backend and frontend containers:
```sh
docker run -d -p 27017:27017 --network notely_default --name mongo -v mongo_data:/data/db mongo:5 mongod --replSet myReplicaSet --bind_ip localhost,mongo
```
Initialize the replica set:
```sh
docker exec -it mongo mongosh
use development
rs.initiate()
```


Now, open **[http://localhost:3000/](http://localhost:3000/)** and start using Notely! 🎉


## 🧪 Running Tests

### **Backend Tests**
The backend uses **Pytest** for testing. To run the tests, navigate to the root directory and execute:
```sh
make test_be
```
📌 **Troubleshooting**
If you encounter issues with Python recognizing modules, try setting the `PYTHONPATH`:
```sh
export PYTHONPATH=$(pwd):$PYTHONPATH
```

### **Frontend Tests**
The frontend is tested using **Jest**. To run the tests, navigate to the root directory and run:
```sh
make test_fe
```
