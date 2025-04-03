
A type of substitution cipher.

It shifts a letter in a [[Plaintext]] by a fixed number of position in the alphabet to produce the [[Ciphertext]]

```mermaid
flowchart LR
    subgraph "Key Concept"
        key[Shift Key: 3]
    end

    subgraph "Cipher Process"
        A[Original Plaintext: HELLO] -->|Step 1: Apply Shift Key| B{Substitution Process}
        key -->|Define Rotation| B
        B -->|Step 2: Shift Each Letter| C[Resulting Ciphertext: KHOOR]
    end

    subgraph "Letter-by-Letter Mapping"
        original["Original: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"]
        shifted["Shifted: D E F G H I J K L M N O P Q R S T U V W X Y Z A B C"]

        H["H → K"]
        E["E → H"]
        L1["L → O"]
        L2["L → O"]
        O["O → R"]
    end

    subgraph "Security Analysis"
        insecure["Weaknesses:"]-->freq["Vulnerable to Frequency Analysis"]
        insecure-->brute["Only 25 Possible Keys (Brute Force)"]
        insecure-->pattern["Pattern Preservation"]
    end

    class A plaintext
    class C ciphertext
    class B process
    class key key
    class original plaintext
    class shifted ciphertext

```

#Cybersecurity #ProgrammingFundamentals  #TerminologyDefinitions  #ConceptExplanation  #Beginner
