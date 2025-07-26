
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
C4Context
  title System Context diagram for Internet Banking System
  Enterprise_Boundary(b0, "BankBoundary0") {
    Person(customerA, "Banking Customer A", "A customer of the bank, with personal bank accounts.")
    Person(customerB, "Banking Customer B")
    Person_Ext(customerC, "Banking Customer C", "desc")

    Person(customerD, "Banking Customer D", "A customer of the bank, <br/> with personal bank accounts.")

    System(SystemAA, "Internet Banking System", "Allows customers to view information about their bank accounts, and make payments.")

    Enterprise_Boundary(b1, "BankBoundary") {

      SystemDb_Ext(SystemE, "Mainframe Banking System", "Stores all of the core banking information about customers, accounts, transactions, etc.")

      System_Boundary(b2, "BankBoundary2") {
        System(SystemA, "Banking System A")
        System(SystemB, "Banking System B", "A system of the bank, with personal bank accounts. next line.")
      }

      System_Ext(SystemC, "E-mail system", "The internal Microsoft Exchange e-mail system.")
      SystemDb(SystemD, "Banking System D Database", "A system of the bank, with personal bank accounts.")

      Boundary(b3, "BankBoundary3", "boundary") {
        SystemQueue(SystemF, "Banking System F Queue", "A system of the bank.")
        SystemQueue_Ext(SystemG, "Banking System G Queue", "A system of the bank, with personal bank accounts.")
      }
    }
  }

  BiRel(customerA, SystemAA, "Uses")
  BiRel(SystemAA, SystemE, "Uses")
  Rel(SystemAA, SystemC, "Sends e-mails", "SMTP")
  Rel(SystemC, customerA, "Sends e-mails to")

  UpdateElementStyle(customerA, $fontColor="red", $bgColor="grey", $borderColor="red")
  UpdateRelStyle(customerA, SystemAA, $textColor="blue", $lineColor="blue", $offsetX="5")
  UpdateRelStyle(SystemAA, SystemE, $textColor="blue", $lineColor="blue", $offsetY="-10")
  UpdateRelStyle(SystemAA, SystemC, $textColor="blue", $lineColor="blue", $offsetY="-40", $offsetX="-50")
  UpdateRelStyle(SystemC, customerA, $textColor="red", $lineColor="red", $offsetX="-50", $offsetY="20")

  UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
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
quadrantChart
    title Reach and engagement of campaigns
    x-axis Low Reach --> High Reach
    y-axis Low Engagement --> High Engagement
    quadrant-1 We should expand
    quadrant-2 Need to promote
    quadrant-3 Re-evaluate
    quadrant-4 May be improved
    Campaign A: [0.3, 0.6]
    Campaign B: [0.45, 0.23]
    Campaign C: [0.57, 0.69]
    Campaign D: [0.78, 0.34]
    Campaign E: [0.40, 0.34]
    Campaign F: [0.35, 0.78]
```

### 15. Sankey Diagram – User Onboarding Funnel
```mermaid
---
config:
  sankey:
    showValues: false
---
sankey-beta

Agricultural 'waste',Bio-conversion,124.729
Bio-conversion,Liquid,0.597
Bio-conversion,Losses,26.862
Bio-conversion,Solid,280.322
Bio-conversion,Gas,81.144
Biofuel imports,Liquid,35
Biomass imports,Solid,35
Coal imports,Coal,11.606
Coal reserves,Coal,63.965
Coal,Solid,75.571
District heating,Industry,10.639
District heating,Heating and cooling - commercial,22.505
District heating,Heating and cooling - homes,46.184
Electricity grid,Over generation / exports,104.453
Electricity grid,Heating and cooling - homes,113.726
Electricity grid,H2 conversion,27.14
Electricity grid,Industry,342.165
Electricity grid,Road transport,37.797
Electricity grid,Agriculture,4.412
Electricity grid,Heating and cooling - commercial,40.858
Electricity grid,Losses,56.691
Electricity grid,Rail transport,7.863
Electricity grid,Lighting & appliances - commercial,90.008
Electricity grid,Lighting & appliances - homes,93.494
Gas imports,Ngas,40.719
Gas reserves,Ngas,82.233
Gas,Heating and cooling - commercial,0.129
Gas,Losses,1.401
Gas,Thermal generation,151.891
Gas,Agriculture,2.096
Gas,Industry,48.58
Geothermal,Electricity grid,7.013
H2 conversion,H2,20.897
H2 conversion,Losses,6.242
H2,Road transport,20.897
Hydro,Electricity grid,6.995
Liquid,Industry,121.066
Liquid,International shipping,128.69
Liquid,Road transport,135.835
Liquid,Domestic aviation,14.458
Liquid,International aviation,206.267
Liquid,Agriculture,3.64
Liquid,National navigation,33.218
Liquid,Rail transport,4.413
Marine algae,Bio-conversion,4.375
Ngas,Gas,122.952
Nuclear,Thermal generation,839.978
Oil imports,Oil,504.287
Oil reserves,Oil,107.703
Oil,Liquid,611.99
Other waste,Solid,56.587
Other waste,Bio-conversion,77.81
Pumped heat,Heating and cooling - homes,193.026
Pumped heat,Heating and cooling - commercial,70.672
Solar PV,Electricity grid,59.901
Solar Thermal,Heating and cooling - homes,19.263
Solar,Solar Thermal,19.263
Solar,Solar PV,59.901
Solid,Agriculture,0.882
Solid,Thermal generation,400.12
Solid,Industry,46.477
Thermal generation,Electricity grid,525.531
Thermal generation,Losses,787.129
Thermal generation,District heating,79.329
Tidal,Electricity grid,9.452
UK land based bioenergy,Bio-conversion,182.01
Wave,Electricity grid,19.013
Wind,Electricity grid,289.366
```

### 16. XY (Scatter) – Sales vs. Marketing Spend
```mermaid
---
config:
    xyChart:
        width: 900
        height: 600
        showDataLabel: true
    themeVariables:
        xyChart:
            titleColor: "#ff0000"
---
xychart-beta
    title "Sales Revenue"
    x-axis [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
    y-axis "Revenue (in $)" 4000 --> 11000
    bar [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
    line [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
```

### 17. Block Diagram – System Architecture
```mermaid
block-beta
columns 1
  db(("DB"))
  blockArrowId6<["&nbsp;&nbsp;&nbsp;"]>(down)
  block:ID
    A
    B["A wide one in the middle"]
    C
  end
  space
  D
  ID --> D
  C --> D
  style B fill:#969,stroke:#333,stroke-width:4px
```

### 18. Packet Diagram – Network Frame
```mermaid
---
title: "TCP Packet"
---
packet
0-15: "Source Port"
16-31: "Destination Port"
32-63: "Sequence Number"
64-95: "Acknowledgment Number"
96-99: "Data Offset"
100-105: "Reserved"
106: "URG"
107: "ACK"
108: "PSH"
109: "RST"
110: "SYN"
111: "FIN"
112-127: "Window"
128-143: "Checksum"
144-159: "Urgent Pointer"
160-191: "(Options and Padding)"
192-255: "Data (variable length)"
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
---
title: "Grades"
---
radar-beta
  axis m["Math"], s["Science"], e["English"]
  axis h["History"], g["Geography"], a["Art"]
  curve a["Alice"]{85, 90, 80, 70, 75, 90}
  curve b["Bob"]{70, 75, 85, 80, 90, 85}

  max 100
  min 0
```

### 22. Treemap – Revenue by Region
```mermaid
---
config:
    theme: 'forest'
---
treemap-beta
"Category A"
    "Item A1": 10
    "Item A2": 20
"Category B"
    "Item B1": 15
    "Item B2": 25
```
