# Frontend Architecture - Detailed Implementation

```mermaid
graph TB
    subgraph "File Structure"
        MainPy[front-end/main.py]
        CompDir[front-end/components/]
        AddFormPy[components/add_form.py]
        ReflListPy[components/reflections_list.py]
        SingleRefPy[components/single_reflection.py]
    end

    subgraph "main.py Components"
        Title[rx.heading - 'Reflection Manager']
        NavTabs[rx.tabs - Navigation]
        Tab1[Tab: 'Add Reflection']
        Tab2[Tab: 'View Reflections']
        UserDD[User Dropdown - Part 3]
    end

    subgraph "add_form.py State & UI"
        AFState[AddFormState<br/>- title: str<br/>- text: str<br/>- timestamp: str<br/>- classified_topics: list]
        AFHandlers[Handlers<br/>- set_title<br/>- set_text<br/>- submit_reflection]
        AFSubmit[Submit Flow<br/>1. Call classify API<br/>2. Get topics<br/>3. Call create API<br/>4. Navigate to /reflections]
        AFUI[UI Elements<br/>- rx.input title<br/>- rx.text_area text<br/>- rx.button Submit]
    end

    subgraph "reflections_list.py State & UI"
        RLState[ReflectionsState<br/>- reflections: list<br/>- selected_id: int]
        RLHandlers[Handlers<br/>- load_reflections<br/>- select_reflection]
        RLUI[UI Elements<br/>- rx.table<br/>- rx.table.row clickable<br/>- Show: id, title, timestamp]
        RLNav[On Click<br/>Navigate to single view]
    end

    subgraph "single_reflection.py State & UI"
        SRState[SingleReflectionState<br/>- reflection: dict<br/>- reflection_id: int]
        SRHandlers[Handlers<br/>- load_reflection_by_id]
        SRUI[UI Elements<br/>- rx.heading title<br/>- rx.text text<br/>- rx.text timestamp<br/>- rx.badge topics]
    end

    subgraph "API Calls"
        ClassifyAPI[POST /api/reflections/classify<br/>Input: title, text, timestamp<br/>Output: topics list]
        CreateAPI[POST /api/reflections<br/>Input: title, text, timestamp, topics<br/>Output: reflection_id]
        GetAllAPI[GET /api/reflections<br/>Output: list of reflections]
        GetOneAPI[GET /api/reflections/:id<br/>Output: single reflection]
    end

    MainPy --> Title
    MainPy --> NavTabs
    NavTabs --> Tab1
    NavTabs --> Tab2

    Tab1 -.->|imports| AddFormPy
    Tab2 -.->|imports| ReflListPy

    AddFormPy --> AFState
    AddFormPy --> AFHandlers
    AddFormPy --> AFUI
    AFHandlers --> AFSubmit

    ReflListPy --> RLState
    ReflListPy --> RLHandlers
    ReflListPy --> RLUI
    RLUI --> RLNav

    RLNav -.->|imports| SingleRefPy
    SingleRefPy --> SRState
    SingleRefPy --> SRHandlers
    SingleRefPy --> SRUI

    AFSubmit -->|1. Classify| ClassifyAPI
    AFSubmit -->|2. Create| CreateAPI
    AFSubmit -.->|3. Navigate| Tab2

    RLHandlers -->|Fetch all| GetAllAPI
    SRHandlers -->|Fetch one| GetOneAPI

    style MainPy fill:#e1f5ff
    style AddFormPy fill:#fff4e1
    style ReflListPy fill:#fff4e1
    style SingleRefPy fill:#fff4e1
    style AFSubmit fill:#ffe1e1
    style ClassifyAPI fill:#e8f5e9
    style CreateAPI fill:#e8f5e9
    style GetAllAPI fill:#e8f5e9
    style GetOneAPI fill:#e8f5e9
```

## Implementation Plan

### 1. main.py
```python
# Structure:
- Import reflex
- Import components (add_form, reflections_list, single_reflection)
- Create index page with:
  * Title
  * rx.tabs with 2 tabs:
    - Tab 1: add_form component
    - Tab 2: reflections_list component
- Create app and compile
```

### 2. components/add_form.py
```python
# State:
class AddFormState(rx.State):
    title: str = ""
    text: str = ""

    async def submit_reflection(self):
        # 1. POST to /api/reflections/classify
        # 2. Get topics from response
        # 3. POST to /api/reflections with title, text, timestamp, topics
        # 4. rx.redirect("/reflections")

# Component:
def add_form():
    return rx.form with:
        - rx.input(on_change=State.set_title)
        - rx.text_area(on_change=State.set_text)
        - rx.button(on_click=State.submit_reflection)
```

### 3. components/reflections_list.py
```python
# State:
class ReflectionsState(rx.State):
    reflections: list = []

    def load_reflections(self):
        # GET /api/reflections
        # Set self.reflections

    def select_reflection(self, id):
        # rx.redirect(f"/reflections/{id}")

# Component:
def reflections_list():
    return rx.table with:
        - rx.table.header
        - rx.foreach(State.reflections, lambda r:
            rx.table.row(
                on_click=lambda: State.select_reflection(r.id)
            ))
```

### 4. components/single_reflection.py
```python
# State:
class SingleReflectionState(rx.State):
    reflection: dict = {}

    def load_reflection(self, id: int):
        # GET /api/reflections/{id}
        # Set self.reflection

# Component:
def single_reflection():
    return rx.vstack with:
        - rx.heading(State.reflection.title)
        - rx.text(State.reflection.text)
        - rx.text(State.reflection.timestamp)
        - rx.hstack(topics as badges)
```

## Part 3 Additions (Multi-User)
- Add user dropdown to main.py
- Add user_id to AddFormState and API calls
- Filter reflections by user_id in ReflectionsState
