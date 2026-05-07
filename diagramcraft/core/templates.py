"""Built-in diagram templates."""

from typing import Optional

TEMPLATES: dict[str, dict[str, str]] = {
    "flowchart": {
        "name": "Flowchart",
        "description": "Basic flowchart with decision logic",
        "code": """graph TD
    A[Start] --> B{Decision?}
    B -->|Yes| C[Action A]
    B -->|No| D[Action B]
    C --> E[End]
    D --> E
""",
    },
    "flowchart-lr": {
        "name": "Flowchart (Left-to-Right)",
        "description": "Horizontal flowchart layout",
        "code": """graph LR
    A[Start] --> B{Decision?}
    B -->|Yes| C[Action A]
    B -->|No| D[Action B]
    C --> E[End]
    D --> E
""",
    },
    "architecture": {
        "name": "System Architecture",
        "description": "Multi-layer system architecture diagram",
        "code": """graph TD
    subgraph Client
        Browser[Web Browser]
        Mobile[Mobile App]
    end

    subgraph Gateway
        LB[Load Balancer]
        API[API Gateway]
    end

    subgraph Services
        Auth[Auth Service]
        User[User Service]
        Order[Order Service]
    end

    subgraph Data
        DB[(Database)]
        Cache[(Redis Cache)]
        MQ[Message Queue]
    end

    Browser --> LB
    Mobile --> LB
    LB --> API
    API --> Auth
    API --> User
    API --> Order
    Auth --> DB
    User --> DB
    Order --> DB
    Auth --> Cache
    Order --> MQ
""",
    },
    "sequence": {
        "name": "Sequence Diagram",
        "description": "Interaction sequence between components",
        "code": """sequenceDiagram
    participant Client
    participant API
    participant Auth
    participant DB

    Client->>API: Request
    API->>Auth: Validate Token
    Auth->>DB: Check Session
    DB-->>Auth: Session Valid
    Auth-->>API: Authorized
    API->>DB: Query Data
    DB-->>API: Result
    API-->>Client: Response
""",
    },
    "orgchart": {
        "name": "Organization Chart",
        "description": "Organizational hierarchy",
        "code": """graph TD
    CEO[CEO] --> CTO[CTO]
    CEO --> CFO[CFO]
    CEO --> COO[COO]

    CTO --> Dev[Development Team]
    CTO --> QA[QA Team]
    CTO --> Infra[Infrastructure Team]

    CFO --> Finance[Finance]
    CFO --> Accounting[Accounting]

    COO --> Ops[Operations]
    COO --> HR[Human Resources]
""",
    },
    "class": {
        "name": "Class Diagram",
        "description": "UML class diagram",
        "code": """classDiagram
    class Animal {
        +String name
        +int age
        +makeSound() void
    }

    class Dog {
        +String breed
        +fetch() void
    }

    class Cat {
        +String color
        +purr() void
    }

    Animal <|-- Dog
    Animal <|-- Cat
""",
    },
    "gantt": {
        "name": "Gantt Chart",
        "description": "Project timeline chart",
        "code": """gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1
    Requirements    :done, req, 2024-01-01, 30d
    Design          :done, design, after req, 20d
    section Phase 2
    Development     :active, dev, after design, 60d
    Testing         :test, after dev, 20d
    section Phase 3
    Deployment      :deploy, after test, 10d
    Monitoring      :monitor, after deploy, 14d
""",
    },
    "er": {
        "name": "ER Diagram",
        "description": "Entity-Relationship diagram",
        "code": """erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : "is in"
    USER {
        int id PK
        string name
        string email
    }
    ORDER {
        int id PK
        int user_id FK
        date created_at
        string status
    }
    PRODUCT {
        int id PK
        string name
        float price
    }
    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
    }
""",
    },
    "state": {
        "name": "State Diagram",
        "description": "State machine diagram",
        "code": """stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: Start
    Processing --> Success: Complete
    Processing --> Failed: Error
    Failed --> Processing: Retry
    Success --> [*]
    Failed --> [*]
""",
    },
    "pie": {
        "name": "Pie Chart",
        "description": "Pie chart for data visualization",
        "code": """pie title Resource Distribution
    "Development" : 40
    "Operations" : 25
    "Marketing" : 20
    "Admin" : 15
""",
    },
    "mindmap": {
        "name": "Mind Map",
        "description": "Hierarchical mind map",
        "code": """mindmap
    root((Project))
        Frontend
            React
            TypeScript
            CSS
        Backend
            Python
            FastAPI
            PostgreSQL
        DevOps
            Docker
            CI/CD
            AWS
""",
    },
}


def list_templates() -> list[dict[str, str]]:
    """List all available templates.

    Returns:
        List of dicts with 'id', 'name', 'description' keys.
    """
    return [
        {"id": tid, "name": t["name"], "description": t["description"]}
        for tid, t in TEMPLATES.items()
    ]


def get_template(template_id: str) -> Optional[str]:
    """Get template code by ID.

    Args:
        template_id: Template identifier (e.g. 'flowchart', 'architecture')

    Returns:
        Template code string, or None if not found.
    """
    entry = TEMPLATES.get(template_id)
    return entry["code"] if entry else None


def get_template_info(template_id: str) -> Optional[dict[str, str]]:
    """Get full template info by ID."""
    return TEMPLATES.get(template_id)
