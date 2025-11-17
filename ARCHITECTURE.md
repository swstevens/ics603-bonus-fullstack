# Frontend Architecture

```mermaid
graph TB
    subgraph "Frontend Architecture"
        Main[main.py<br/>- Title<br/>- Navigation Links<br/>- User Dropdown]

        subgraph "Components Folder"
            AddForm[add_form.py<br/>- User dropdown<br/>- Title input<br/>- Text input<br/>- Timestamp<br/>- Submit button]
            ReflectionsList[reflections_list.py<br/>- Fetch all reflections<br/>- Display table<br/>- Click to view single]
            SingleReflection[single_reflection.py<br/>- Display one reflection<br/>- Show title, text, timestamp<br/>- Show topics]
        end
    end

    subgraph "API Endpoints"
        ClassifyAPI[POST /api/reflections/classify]
        CreateAPI[POST /api/reflections]
        GetAllAPI[GET /api/reflections]
        GetOneAPI[GET /api/reflections/:id]
        GetTopicsAPI[GET /api/topics]
        GetUserReflectionsAPI[GET /api/reflections?user_id=X]
    end

    subgraph "Database - Part 3"
        Users[(users table<br/>- id<br/>- first_name<br/>- email)]
        Reflections[(reflections table<br/>- id<br/>- title<br/>- text<br/>- timestamp<br/>- user_id FK)]
        Topics[(topics table<br/>- id<br/>- name<br/>- user_id FK)]
        RefTopics[(reflection_topics<br/>- reflection_id<br/>- topic_id)]
    end

    Main -->|Route: /| AddForm
    Main -->|Route: /reflections| ReflectionsList
    ReflectionsList -->|Click reflection| SingleReflection

    AddForm -->|1. Classify| ClassifyAPI
    AddForm -->|2. Create| CreateAPI
    AddForm -.->|Navigate after submit| ReflectionsList

    ReflectionsList -->|Fetch| GetAllAPI
    ReflectionsList -->|Filter by user_id| GetUserReflectionsAPI
    SingleReflection -->|Fetch| GetOneAPI

    CreateAPI --> Reflections
    CreateAPI --> RefTopics
    GetAllAPI --> Reflections
    GetOneAPI --> Reflections
    ClassifyAPI --> GetTopicsAPI --> Topics
    GetUserReflectionsAPI --> Reflections

    Reflections -->|FK| Users
    Topics -->|FK| Users
    Reflections -.->|M:N| RefTopics
    Topics -.->|M:N| RefTopics

    style Main fill:#e1f5ff
    style AddForm fill:#fff4e1
    style ReflectionsList fill:#fff4e1
    style SingleReflection fill:#fff4e1
    style Users fill:#e8f5e9
    style Reflections fill:#e8f5e9
    style Topics fill:#e8f5e9
    style RefTopics fill:#e8f5e9
```

## Architecture Summary

### Part 2 (Frontend - Initial)
- **main.py**: Container with title, navigation links
- **components/add_form.py**: Form component (calls classify → create → navigate)
- **components/reflections_list.py**: Table view (calls get all, clickable rows)
- **components/single_reflection.py**: Detail view (calls get by id)

### Part 3 (Multi-User Extension)
- **Database**: Add `users` table, add `user_id` FK to `reflections` and `topics`
- **API**: Add user filtering to GET endpoints
- **Frontend**: User dropdown in main.py (filters all views), user dropdown in add_form.py (attribution)

## Flow
1. User selects user → filters all views
2. User fills form → classifies topics → creates reflection → navigates to list
3. User views list → clicks item → views single reflection
