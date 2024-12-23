# **MyNewProject**

**MyNewProject** is a Django-based application for creating and managing chatbots. The system integrates text embeddings, document processing, and personalized chatbot personalities to provide users with an interactive chatbot experience.

---

## **Features**

### **Core Functionalities**
1. **User Management:**
   - User registration with email and strong password validation.
   - Login with username and password.
   - Profile management with an API key generation system.

2. **Chatbot Management:**
   - Multi-step chatbot creation process:
     1. Define chatbot details (name and description).
     2. Customize personality (tone and behavior).
     3. Upload documents for knowledge embedding.
   - Dashboard to view and manage user-created chatbots.

3. **Document Processing and Embeddings:**
   - Process uploaded documents into manageable chunks.
   - Generate and store embeddings for document chunks using `SentenceTransformer`.

4. **Response Generation:**
   - Generate chatbot responses using OpenAI's GPT-2.

---

## **Getting Started**

### **Prerequisites**
- Python 3.8 or later
- Virtual environment (recommended)
- Required libraries (see `requirements.txt`)

### **Installation**
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/mynewproject.git
   cd mynewproject
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start the Server:**
   ```bash
   python manage.py runserver
   ```

---

## **Usage**

### **1. User Registration and Login**
- Access the **registration** page at `/register/` to create a new account.
- Log in to the system using `/login/`.

### **2. Chatbot Creation Process**
- Step 1: Define chatbot details at `/create_chatbot/step1/`.
- Step 2: Customize personality and behavior at `/create_chatbot/step2/<chatbot_id>/`.
- Step 3: Upload relevant documents at `/create_chatbot/step3/<chatbot_id>/`.

### **3. Dashboard**
- View your created chatbots and statistics at `/dashboard/`.

---

## **Project Structure**

```plaintext
mynewproject/
│
├── myapp/
│   ├── chroma_utils.py       # Handles embeddings storage and query.
│   ├── document_utils.py     # Processes documents and generates embeddings.
│   ├── forms.py              # User forms (registration, chatbot forms, etc.).
│   ├── models.py             # Database models (Chatbot, Document, UserProfile).
│   ├── views.py              # Django views for chatbot creation and user management.
│   ├── templates/            # HTML templates for registration, login, etc.
│   └── static/               # Static files (CSS, JS).
│
├── mynewproject/
│   ├── settings.py           # Django project settings.
│   ├── urls.py               # URL routing for the project.
│   └── wsgi.py               # WSGI configuration.
│
├── requirements.txt          # List of project dependencies.
└── README.md                 # Project documentation (you are here).
```

---

## **Key Components**

### **Chroma Utils**
- **Purpose:** Store and query embeddings using `chromadb`.
- Functions:
  - `store_embeddings(chatbot_id, embeddings)`: Stores document embeddings in ChromaDB.
  - `fetch_relevant_chunks(chatbot_id, query)`: Retrieves relevant document chunks for a given query.

### **Document Utils**
- **Purpose:** Process uploaded documents and generate embeddings.
- Functions:
  - `process_document(file_path)`: Reads a document, splits it into chunks, and encodes them into embeddings.

### **Models**
- **Chatbot:** Stores chatbot metadata (name, description, personality).
- **Document:** Tracks uploaded files linked to chatbots.
- **DocumentChunk:** Stores processed document chunks.

---

## **Dependencies**
The project relies on the following key libraries:
- **Django**: Web framework for rapid development.
- **Transformers**: GPT-2 for text generation.
- **Sentence-Transformers**: For embedding generation.
- **ChromaDB**: Vector database for efficient query of document embeddings.

For the full list, see `requirements.txt`.

---

## **Future Enhancements**
- Implement chatbot API for external access.
- Add real-time chat interface.
- Enhance security with email verification during registration.
- Extend support for additional file types (e.g., PDF).
