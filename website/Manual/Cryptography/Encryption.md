
It's a process of making readable data unreadable.

Encryption converts [[Plaintext]] into [[Ciphertext]]

## Encryption process

```mermaid
flowchart LR
    subgraph "Sender Side"
        A[Plaintext Message] -->|1. Prepare Message| B(Original Data)
        B --> C{Encryption Algorithm}
        K1[Encryption Key] -->|2. Apply Key| C
        C -->|3. Generate| D[Encrypted Data/Ciphertext]
        D -->|4. Transmit| T([Transmission Channel])
    end

    subgraph "Receiver Side"
        T -->|5. Receive| E[Encrypted Data/Ciphertext]
        E --> F{Decryption Algorithm}
        K2[Decryption Key] -->|6. Apply Key| F
        F -->|7. Decrypt| G[Recovered Plaintext]
    end

    subgraph "Key Management"
        KG[Key Generation] --> K1
        KG --> K2

        style KG fill:#f9f,stroke:#333,stroke-width:2px
    end

    class A,B,G plainData
    class D,E encrypted
    class C,F process
    class K1,K2 key
```

---

#Cybersecurity #TerminologyDefinitions #ConceptExplanation #Beginner
