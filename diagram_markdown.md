
## Complex Real-world Mermaid Chart Examples

### 1. Flowchart – Order Fulfillment System
```mermaid
flowchart LR
  subgraph Order Intake
    A[Customer places order] --> B{Payment valid?}
  end
  B -- Yes --> C[Reserve inventory]
  C --> D{Inventory ≥0?}
  D -- Yes --> E[Send confirmation]
  D -- No --> F[Notify out-of-stock]
  B -- No --> G[Reject payment]
  E --> H[Ship order]
  H --> I[Update tracking]
  classDef warning fill:#f96;
  class F,G warning
```

### 2. Sequence Diagram – API Authentication & Data Fetch
```mermaid
sequenceDiagram
  participant U as User
  participant A as Auth Service
  participant API as Main API
  participant DB as Database

  U->>A: /login
  A-->>U: JWT token
  U->>API: GET /data [token]
  API->>A: Validate token
  A-->>API: Token OK
  API->>DB: SELECT * FROM records WHERE user_id
  DB-->>API: return rows
  API-->>U: 200 OK [JSON]
```

### 3. Class Diagram – E‑commerce Domain
```mermaid
classDiagram
  class User {
    +int id
    +String email
    +placeOrder()
  }
  class Order {
    +int orderId
    +Date created
    +addItem()
  }
  class Product {
    +int productId
    +String name
    +double price
  }
  User "1" o-- "*" Order : places
  Order "*" -- "*" Product : includes
  class ShoppingCart {
    +Map<Product, int> items
    +checkout()
  }
  User "1" *-- "1" ShoppingCart
```

### 4. Entity‑Relationship Diagram – SaaS Schema
```mermaid
erDiagram
  USER }|..|{ ACCOUNT : owns
  ACCOUNT ||--o{ PROJECT : contains
  PROJECT ||--|{ TASK : includes
  TASK }o--|| COMMENT : "has comments"
  PROJECT }|--|{ TEAM : managed_by
  TEAM ||--o{ USER : includes
```

### 5. Gantt Chart – Sprint Planning
```mermaid
gantt
  title Sprint 42 (July 2025)
  dateFormat YYYY-MM-DD
  section Planning
    Requirements Review :done, a1, 2025-07-01, 2d
    Sprint Kick-Off      :crit, a2, after a1, 1d
  section Development
    Backend APIs         :active, a3, 2025-07-04, 5d
    Frontend UI          :active, a4, after a3, 7d
  section QA
    Testing              :after a4, 4d
    Bug Fixes            :after testing, 3d
  section Deployment
    Staging Rollout      :milestone, 2025-07-20
    Production Release   :crit, b1, after Staging Rollout, 1d
```

### 6. Mindmap – Product Ideation
```mermaid
mindmap
  root((Product Launch))
    Strategy
      Market Research
        Competitor Analysis
        Customer Interviews
      Positioning
    Features
      Core
        Authentication
        Dashboard
      Advanced
        AI Insights
        Mobile Sync
    Risks
      Technical
      Market
      Regulatory
```

### 7. State Diagram – Order Lifecycle
```mermaid
stateDiagram-v2
  [*] --> Pending
  Pending --> Confirmed : payment_received
  Confirmed --> Packed
  Packed --> Shipped
  Shipped --> Delivered
  Confirmed --> Cancelled : payment_failed
  Pending --> Cancelled : user_cancel
  Cancelled --> [*]
  Delivered --> [*]
```

### 8. User Journey – Mobile App Onboarding
```mermaid
journey
  title Onboarding Flow
  section Install
    View Welcome Screen: 5: Me
    Allow Permissions: 4: Me
  section Setup
    Create Account: 3: Me
    Set Preferences: 2: Me
  section First Use
    Tutorial Walkthrough: 3: Me
    Perform First Task: 2: Me
```

### 9. Requirement Diagram – Compliance App
```mermaid
flowchart LR
  R1["Users must authenticate via MFA"]
  R2["System shall encrypt data at rest"]
  R2 --> R1
```

### 10. Git Graph – Release Workflow
```mermaid
gitGraph
  commit id:"init" tag:"v1.0"
  branch develop
  commit id:"feat/api"
  commit id:"feat/ui"
  checkout main
  merge develop tag:"v1.1"
  branch hotfix
    commit id:"fix/security"
  checkout main
  merge hotfix tag:"v1.1.1"
```

### 11. C4 Context Diagram – Microservices
```mermaid
flowchart LR
  admin["Admin User"] --> web["Web Frontend"]
  web --> api["API Gateway"]
  api --> db["User DB"]
```

### 12. Timeline – Product Roadmap
```mermaid
timeline
  title 2025 Roadmap
  2025-01-15 : Feature A launch
  2025-03-01 : Beta testing Feature B
  section Q3
    2025-07-01 : Launch mobile app
    2025-09-15 : User milestone 50k
```

### 13. Pie Chart – Market Share
```mermaid
pie
  title Q2 2025 Market Share
  "Brand X": 40
  "Brand Y": 25
  "Brand Z": 15
  "Others": 20
```

### 14. Quadrant Chart – Risk Matrix
```mermaid
flowchart LR
  A["Low,Low\nInformational"]
  B["High,Low\nOpportunity"]
  C["Low,High\nWatchlist"]
  D["High,High\nCritical"]
```

### 15. Sankey Diagram – User Onboarding Funnel
```mermaid
flowchart TD
  Onboarding["Landing Page 10000"] --> SignUp["Sign-Ups 3000"]
  SignUp --> Verify["Verification 2500"]
  Verify --> FirstUse["First Use 2000"]
  FirstUse --> Retained["Retained 1200"]
```

### 16. XY (Scatter) – Sales vs. Marketing Spend
```mermaid
flowchart LR
  A((50,10)) --> B((80,20)) --> C((120,25)) --> D((150,30)) --> E((200,45))
```

### 17. Block Diagram – System Architecture
```mermaid
flowchart TB
  subgraph Backend
    B1[(API Server)]
    B2[(Auth Service)]
    B3[(Database)]
    B1 --> B2
    B2 --> B3
  end
  subgraph Frontend
    F1[(Web App)]
    F1 --> B1
  end
```

### 18. Packet Diagram – Network Frame
```mermaid
flowchart TD
  Ethernet[[Ethernet Frame]]
  MAC["MAC: 00:11:22:33:44:55"]
  IP["IP: 192.168.0.1"]
  Payload["Payload: TCP segment"]
  Ethernet --> MAC
  Ethernet --> IP
  Ethernet --> Payload
```

### 19. Kanban Board – Release Tracker
```mermaid
kanban
  title Sprint Board
  backlog, ready, in-progress, qa, done
  backlog : Define API endpoints
  ready : Write unit tests
  in-progress : Build CI pipeline
  qa : Security review
  done : Deploy v2.0
```

### 20. Architecture Diagram – Service Mesh
```mermaid
flowchart TD
  subgraph Cloud
    api_gw[API Gateway]
    svc1[Order Service]
    svc2[Inventory Service]
    mesh[Service Mesh]
  end
  api_gw --> mesh
  mesh --> svc1
  mesh --> svc2
```

### 21. Radar Chart – Team Skills
```mermaid
flowchart TD
  TeamA --> Backend["Backend: 4"]
  TeamA --> Frontend["Frontend: 3"]
  TeamA --> DB["DB: 5"]
  TeamA --> DevOps["DevOps: 4"]
  TeamA --> UX["UX: 2"]
```

### 22. Treemap – Revenue by Region
```mermaid
pie
  title Revenue 2025
  "North America": 500000
  "Europe": 300000
  "Asia": 200000
  "Other": 50000
```
