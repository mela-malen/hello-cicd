---
layout: default
title: Visitor Journey
nav_order: 10
has_children: false
---

<div class="neon-header-retro">
  <h1 class="neon-heading-retro">VISITOR JOURNEY</h1>
  <p class="neon-subtitle-retro">Experience the Neon Highway</p>
</div>

## Complete Visitor Journey

```mermaid
flowchart TB
    subgraph Entry["ENTRY POINTS"]
        Search["Search Engine"]
        Direct["Direct Link"]
        Social["Social Media"]
        Referral["Word of Mouth"]
    end

    subgraph Discovery["DISCOVERY"]
        Home["Home Page - First Impression"]
        CTA["Click CTA"]
    end

    subgraph Interest["INTEREST"]
        Features["View Features"]
        Newsletters["Explore Newsletters"]
        Benefits["View Benefits"]
    end

    subgraph Action["ACTION"]
        Form["Subscribe Form"]
        Select["Select Topics"]
        Confirm["Confirm Email"]
    end

    subgraph Retention["RETENTION"]
        Welcome["Welcome Email"]
        Content["Receive Content"]
        Engage["Interact"]
    end

    subgraph Advocacy["ADVOCACY"]
        Share["Share with Friends"]
        Feedback["Leave Review"]
        Return["Return Visitor"]
    end

    Entry --> Discovery
    Discovery --> Interest
    Interest --> Action
    Action --> Retention
    Retention --> Advocacy
    Advocacy -->|Loop| Entry

    classDef entry fill:#ff00ff,stroke:#fff,stroke-width:3px,color:#fff
    classDef discover fill:#00ffff,stroke:#fff,stroke-width:3px,color:#000
    classDef interest fill:#ffff00,stroke:#fff,stroke-width:3px,color:#000
    classDef action fill:#ff6600,stroke:#fff,stroke-width:3px,color:#fff
    classDef retention fill:#00ff00,stroke:#fff,stroke-width:3px,color:#000
    classDef advocacy fill:#ff0066,stroke:#fff,stroke-width:3px,color:#fff

    class Entry,Search,Direct,Social,Referral entry
    class Discovery,Home,CTA discover
    class Interest,Features,Newsletters,Benefits interest
    class Action,Form,Select,Confirm action
    class Retention,Welcome,Content,Engage retention
    class Advocacy,Share,Feedback,Return advocacy
```

---

## User Touchpoints Sequence

```mermaid
sequenceDiagram
    participant V as Visitor
    participant W as Website
    participant E as Email
    participant DB as Database

    V->>W: Arrives on Home
    W->>V: Neon Welcome
    V->>W: Explores Content

    par Subscribe Flow
        V->>W: Clicks Subscribe
        W->>V: Newsletter Selection
        V->>W: Chooses Topics
        V->>W: Enters Email
        W->>DB: Save Subscriber
        DB-->>W: Saved
        W->>V: Success Message
    and Email Flow
        E->>V: Welcome Email
        V->>E: Opens Email
        E->>V: Clicks Link
        V->>W: Returns to Site
    end

    V->>W: Engages with Content
    W->>DB: Track Engagement
    V->>W: Shares with Friends
```

---

## Journey Map - 5 Stages

```mermaid
flowchart LR
    subgraph Stage1["STAGE 1: AWARENESS"]
        A1["Discover via Search"]
        A2["See Ad/Post"]
        A3["Social Share"]
    end

    subgraph Stage2["STAGE 2: CONSIDERATION"]
        B1["Visit Home"]
        B2["Read Content"]
        B3["Evaluate Options"]
    end

    subgraph Stage3["STAGE 3: CONVERSION"]
        C1["Fill Form"]
        C2["Confirm Email"]
        C3["Subscribe"]
    end

    subgraph Stage4["STAGE 4: RETENTION"]
        D1["Get Newsletter"]
        D2["Learn and Grow"]
        D3["Build Habit"]
    end

    subgraph Stage5["STAGE 5: ADVOCACY"]
        E1["Share Experience"]
        E2["Write Review"]
        E3["Refer Friends"]
    end

    A1 --> B1
    A2 --> B1
    A3 --> B1
    B1 --> B2
    B2 --> B3
    B3 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> D1
    D1 --> D2
    D2 --> D3
    D3 --> E1
    E1 --> E2
    E2 --> E3

    classDef stage1 fill:#ff00ff,stroke:#fff,stroke-width:4px,color:#fff
    classDef stage2 fill:#00ffff,stroke:#fff,stroke-width:4px,color:#000
    classDef stage3 fill:#ffff00,stroke:#fff,stroke-width:4px,color:#000
    classDef stage4 fill:#00ff00,stroke:#fff,stroke-width:4px,color:#000
    classDef stage5 fill:#ff0066,stroke:#fff,stroke-width:4px,color:#fff

    class Stage1,A1,A2,A3 stage1
    class Stage2,B1,B2,B3 stage2
    class Stage3,C1,C2,C3 stage3
    class Stage4,D1,D2,D3 stage4
    class Stage5,E1,E2,E3 stage5
```

---

## Conversion Funnel

```mermaid
flowchart TD
    Start([ENTER FUNNEL]) --> A["100% Visitors - Home Page"]

    A -->|Convert| B["60% Engaged - Viewed Content"]
    B -->|Convert| C["35% Interested - Explored Newsletters"]
    C -->|Convert| D["20% Action - Started Form"]
    D -->|Convert| E["15% Subscribed"]
    E -->|Convert| F["12% Active - Regular Readers"]

    A -->|Bounce| AB["40% Bounced"]
    B -->|Drop| BC["25% Dropped"]
    C -->|Drop| CD["15% Dropped"]
    D -->|Drop| DE["5% Dropped"]
    E -->|Drop| EF["3% Unsubscribed"]

    classDef funnel fill:#1a1a2e,stroke:#ff00ff,stroke-width:3px,color:#fff
    classDef step fill:#0d1b2a,stroke:#00ffff,stroke-width:2px,color:#fff
    classDef drop fill:#2d2d44,stroke:#ff0000,stroke-width:2px,color:#ff6666
    classDef startend fill:#5c2d91,stroke:#ffff00,stroke-width:4px,color:#fff

    class Start,A,B,C,D,E,F funnel
    class AB,BC,CD,DE,EF drop
```

---

## Conversion Triggers

```mermaid
flowchart TB
    subgraph Triggers["CONVERSION TRIGGERS"]
        T1["Visually Stunning Design"]
        T2["Clear Value Proposition"]
        T3["Curated Newsletter Topics"]
        T4["Trust Signals"]
        T5["Exclusive Content"]
        T6["Social Proof"]
        T7["Clear CTA"]
        T8["Mobile Optimized"]
    end

    subgraph Result["RESULT"]
        R["Higher Conversion Rates"]
    end

    T1 --> R
    T2 --> R
    T3 --> R
    T4 --> R
    T5 --> R
    T6 --> R
    T7 --> R
    T8 --> R

    classDef trigger fill:#1a1a2e,stroke:#ffff00,stroke-width:2px,color:#fff
    classDef result fill:#0f3460,stroke:#00ff00,stroke-width:3px,color:#fff

    class Triggers,T1,T2,T3,T4,T5,T6,T7,T8 trigger
    class Result,R result
```

---

## Newsletter Selection Journey

```mermaid
flowchart TD
    Start([Visitor on Subscribe Page]) --> Survey["Display Newsletter Cards"]

    subgraph Selection["NEWSLETTER SELECTION"]
        Card1["Kost and Nutrition"]
        Card2["Mindset"]
        Card3["Knowledge and Research"]
        Card4["Weekly Workouts"]
        Card5["AI Training with Jaine"]
    end

    Card1 --> Toggle1["Toggle On/Off"]
    Card2 --> Toggle2["Toggle On/Off"]
    Card3 --> Toggle3["Toggle On/Off"]
    Card4 --> Toggle4["Toggle On/Off"]
    Card5 --> Toggle5["Toggle On/Off"]

    Toggle1 --> Validate["Validate Selection"]
    Toggle2 --> Validate
    Toggle3 --> Validate
    Toggle4 --> Validate
    Toggle5 --> Validate

    Validate -->|None| Warning["Select at least 1"]
    Warning --> Survey

    Validate -->|1+| EmailForm["Enter Email"]
    EmailForm --> Submit["Submit Subscription"]
    Submit --> Success([Welcome Aboard])

    classDef startend fill:#5c2d91,stroke:#ffff00,stroke-width:4px,color:#fff
    classDef card fill:#1a1a2e,stroke:#ff00ff,stroke-width:3px,color:#fff
    classDef action fill:#0f3460,stroke:#00ffff,stroke-width:2px,color:#fff

    class Start,Success startend
    class Selection,Card1,Card2,Card3,Card4,Card5 card
    class Survey,Toggle1,Toggle2,Toggle3,Toggle4,Toggle5,Validate,EmailForm,Submit,Warning action
```

---

## Exit Points and Recovery

```mermaid
flowchart TD
    subgraph Exit["EXIT DETECTED"]
        E1["Close Browser"]
        E2["Form Abandonment"]
        E3["Unsubscribed"]
        E4["Bounce from Email"]
    end

    subgraph Recovery["RECOVERY ACTIONS"]
        R1["Exit Intent Popup"]
        R2["Auto-Save Form"]
        R3["Win-Back Campaign"]
        R4["Re-Engagement Sequence"]
    end

    subgraph Success["RECOVERY"]
        S1["Returns to Site"]
        S2["Completes Form"]
        S3["Re-subscribes"]
    end

    Exit --> Recovery
    Recovery --> Success

    classDef exit fill:#2d2d44,stroke:#ff0000,stroke-width:2px,color:#ff6666
    classDef recovery fill:#1a1a2e,stroke:#ffff00,stroke-width:2px,color:#fff
    classDef success fill:#0d1b2a,stroke:#00ff00,stroke-width:2px,color:#fff

    class Exit,E1,E2,E3,E4 exit
    class Recovery,R1,R2,R3,R4 recovery
    class Success,S1,S2,S3 success
```

---

## Success Metrics KPIs

```mermaid
graph LR
    subgraph KPIs["KEY PERFORMANCE INDICATORS"]
        K1["Monthly Visitors - 10,000+"]
        K2["Signup Rate - 5%+"]
        K3["Email Open Rate - 25%+"]
        K4["Monthly Active - 40%"]
        K5["Referral Rate - 10%"]
        K6["NPS Score - 50+"]
    end

    K1 --> K2
    K2 --> K3
    K3 --> K4
    K4 --> K5
    K5 --> K6

    classDef kpi fill:#1a1a2e,stroke:#00ff00,stroke-width:3px,color:#fff

    class KPIs,K1,K2,K3,K4,K5,K6 kpi
```

---

[Back to Overview](architecture/overview.md) | [Next: API Reference](architecture/api.md)

<style>
.neon-header-retro {
  background: linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
  padding: 3rem 0;
  border-radius: 12px;
  margin-bottom: 2rem;
  border: 3px solid #ff00ff;
  box-shadow: 0 0 20px #ff00ff, 0 0 40px #ff00ff inset;
  text-align: center;
}

.neon-heading-retro {
  font-family: 'Courier New', monospace;
  font-size: 3rem;
  font-weight: bold;
  color: #fff;
  text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 40px #ff00ff, 0 0 80px #ff00ff;
  margin: 0;
  letter-spacing: 4px;
}

.neon-subtitle-retro {
  font-family: 'Courier New', monospace;
  font-size: 1.3rem;
  color: #00ffff;
  text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff;
  margin-top: 1rem;
  letter-spacing: 2px;
}

.mermaid {
  background: #0a0a0a;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
}
</style>
