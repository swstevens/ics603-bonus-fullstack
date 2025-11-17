# Part 3: Multi-User Support Architecture

```mermaid
graph TB
    subgraph "Database Changes"
        UsersTable[users table<br/>- id PRIMARY KEY<br/>- first_name<br/>- email]
        ReflectionsTable[reflections table<br/>+ user_id FK → users.id]
        TopicsTable[topics table<br/>+ user_id FK → users.id]
        RefTopicsTable[reflection_topics<br/>unchanged]
    end

    subgraph "Backend Changes - models.py"
        UserModel[User model<br/>- id, first_name, email<br/>- reflections relationship<br/>- topics relationship]
        RefModel[Reflection model<br/>+ user_id FK<br/>+ user relationship]
        TopicModel[Topic model<br/>+ user_id FK<br/>+ user relationship]
    end

    subgraph "Backend Changes - create_db.py"
        SeedUsers[Insert 2 users:<br/>- John john@test.com<br/>- Jane jane@test.com]
    end

    subgraph "Backend Changes - api.py"
        GetUsersAPI[GET /api/users<br/>Returns all users]
        GetReflAPI[GET /api/reflections?user_id=X<br/>Filter by user_id]
        GetTopicsAPI[GET /api/topics?user_id=X<br/>Filter by user_id]
        CreateRefAPI[POST /api/reflections<br/>+ user_id in payload]
        ClassifyAPI[POST /api/reflections/classify<br/>+ user_id in payload<br/>Filter existing topics by user]
    end

    subgraph "Frontend Changes - main.py"
        UserDropdown[rx.select - User dropdown<br/>- Load users on mount<br/>- Store selected_user_id in state<br/>- Pass to child components]
    end

    subgraph "Frontend Changes - add_form.py"
        FormUserDD[rx.select - User dropdown<br/>- Select user for attribution<br/>- Pass user_id to classify & create]
        FormSubmit[Submit flow:<br/>1. Classify with user_id<br/>2. Create with user_id]
    end

    subgraph "Frontend Changes - reflections_list.py"
        FilterReflections[load_reflections:<br/>- GET /api/reflections?user_id=X<br/>- Use selected_user_id from main]
    end

    UsersTable -.->|FK| ReflectionsTable
    UsersTable -.->|FK| TopicsTable

    UserModel --> RefModel
    UserModel --> TopicModel

    SeedUsers --> UsersTable

    GetUsersAPI --> UsersTable
    GetReflAPI --> ReflectionsTable
    GetTopicsAPI --> TopicsTable
    CreateRefAPI --> ReflectionsTable
    ClassifyAPI --> TopicsTable

    UserDropdown --> FilterReflections
    FormUserDD --> FormSubmit
    FormSubmit --> CreateRefAPI
    FormSubmit --> ClassifyAPI

    style UsersTable fill:#e8f5e9
    style ReflectionsTable fill:#e8f5e9
    style TopicsTable fill:#e8f5e9
    style UserDropdown fill:#ffe1e1
    style FormUserDD fill:#ffe1e1
```

## Implementation Steps

### 1. Update models.py
```python
# Add User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    reflections = relationship("Reflection", back_populates="user")
    topics = relationship("Topic", back_populates="user")

# Update Topic model
class Topic(Base):
    # ... existing fields ...
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="topics")

# Update Reflection model
class Reflection(Base):
    # ... existing fields ...
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="reflections")
```

### 2. Update create_db.py
```python
# After creating tables, seed users
users_data = [
    {"first_name": "John", "email": "john@test.com"},
    {"first_name": "Jane", "email": "jane@test.com"}
]
for user_data in users_data:
    if not db.query(User).filter(User.email == user_data["email"]).first():
        db.add(User(**user_data))
db.commit()
```

### 3. Update api.py
```python
# Add GET users endpoint
@app.get("/api/users")
async def get_users():
    # Return all users

# Update GET reflections - add user_id filter
@app.get("/api/reflections")
async def get_all_reflections(user_id: int = None):
    # Filter by user_id if provided

# Update GET topics - add user_id filter
@app.get("/api/topics")
async def get_topics(user_id: int = None):
    # Filter by user_id if provided

# Update POST reflections - add user_id
class CreateReflectionInput(BaseModel):
    # ... existing fields ...
    user_id: int

# Update POST classify - add user_id
class ClassifyReflectionInput(BaseModel):
    # ... existing fields ...
    user_id: int
```

### 4. Update main.py
```python
# Add MainState with user selection
class MainState(rx.State):
    users: list = []
    selected_user_id: int = 1

    async def load_users(self):
        # GET /api/users

    def set_user(self, user_id: int):
        self.selected_user_id = user_id

# Add user dropdown to layout
rx.select(
    MainState.users,
    on_change=MainState.set_user
)
```

### 5. Update add_form.py
```python
# Add user_id field to state
class AddFormState(rx.State):
    # ... existing fields ...
    selected_user_id: int = 1

# Add user dropdown to form
# Pass user_id to classify and create API calls
```

### 6. Update reflections_list.py
```python
# Update load_reflections to accept user_id
async def load_reflections(self, user_id: int):
    # GET /api/reflections?user_id={user_id}
```

## Key Changes Summary
1. **Database**: Add users table, add user_id FK to reflections and topics
2. **API**: Add user filtering, user_id in create/classify payloads
3. **Frontend**: User dropdown in main and form, filter by selected user
