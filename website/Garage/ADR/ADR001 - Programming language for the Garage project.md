| Status       | Implemented                                                            |
| :----------- | :--------------------------------------------------------------------- |
| **Decision** | Python selected as primary programming language for the Garage project |

## Context

Which programming language should be used for the Garage project? The project will include machine learning, DevOps components, and needs to align with my personal development goals while balancing complexity and productivity.

## References

- [The Zen of Python](https://www.python.org/dev/peps/pep-0020/)
- [.Nett vs. Python](https://www.reddit.com/r/dotnet/comments/1i3jnqf/net_vs_python/)
- [Fluent Assertions becomes paid software](https://www.reddit.com/r/dotnet/comments/1i17jm0/fluentassertions_becomes_paid_software_for/?rdt=46633)
- [From Free to Fee: .NET Tools That Transitioned to Paid Models](https://www.perplexity.ai/search/i-am-looking-for-other-cased-i-_NfMzynCTDqnr7Q5G9ksAA#0)
- [What are the most popular programming languages in 2025 and what will be in 2030](https://www.perplexity.ai/search/what-are-the-most-popular-prog-JyEITelbSviGWtp9nJ9iWg?0=d#0)

## Requirements

| #     | Requirement                              | Importance | Notes                                                    |
| :---- | :--------------------------------------- | :--------- | :------------------------------------------------------- |
| **1** | Support for machine learning development | MUST       | Need robust ML libraries and ecosystem                   |
| **2** | DevOps compatibility                     | MUST       | Should work well with automation, infrastructure as code |
| **3** | Ease of learning/productivity            | SHOULD     | Balance between learning curve and productivity          |
| **4** | Community support and resources          | SHOULD     | Active community, documentation, tutorials               |
| **5** | Previous experience leverage             | SHOULD     | Ability to build on existing knowledge                   |
| **6** | Alignment with project philosophy        | SHOULD     | Match with "Zen of the Garage" principles                |

## Considered options

|                                       | JavaScript                                                                                                      | C#                                                                                         | Python                                                                                                                        |
| :------------------------------------ | :-------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| **High-level design**                 | Web-focused language with Node.js for backend                                                                   | Strongly-typed OOP language with .NET ecosystem                                            | General-purpose language with extensive libraries                                                                             |
| **Support for ML development**        | Limited native ML capabilities. Libraries like TensorFlow.js exist but are less mature than Python alternatives | ML.NET exists but has less community adoption and fewer resources than Python ML ecosystem | Excellent ML support with libraries like TensorFlow, PyTorch, scikit-learn, pandas, etc. De facto standard for ML development |
| **DevOps compatibility**              | Good for web automation, less common for other DevOps tasks                                                     | I didn't heard about using .Net by DevOps                                                  | Excellent for DevOps with libraries like Ansible, Fabric, widely used in infrastructure automation                            |
| **Ease of learning/productivity**     | Already proficient, high productivity                                                                           | 5 months experience, more complex syntax and concepts                                      | Gentle learning curve, readable syntax, rapid development                                                                     |
| **Community support**                 | Very large community, abundant resources                                                                        | Strong community, primarily Microsoft-focused                                              | Massive community across academic, industry and open source                                                                   |
| **Previous experience leverage**      | High (proficient)                                                                                               | Medium (5 months experience)                                                               | Low (presumably less experience)                                                                                              |
| **Alignment with project philosophy** | Partially aligns with independence, but ecosystem can be fragmented                                             | Less aligned - corporate backing, complexity over simplicity                               | Strongly aligned - "Zen of Python" philosophy matches "Zen of the Garage"                                                     |
| **High-level estimation**             | Medium effort - building on existing knowledge                                                                  | High effort - still learning the ecosystem                                                 | Medium-high effort - learning curve but simpler syntax                                                                        |
| **Cost analysis**                     | Free and open source                                                                                            | Some tools may require licenses, though core is free                                       | Free and open source                                                                                                          |

## Decision

In the **context of the Garage** project with **machine learning and DevOps components**,

facing **the need to select a programming language that balances ML capabilities, DevOps integration, and personal learning goals**,

I decided for **Python** and neglected JavaScript and C#,

to achieve **better support for machine learning, simpler DevOps integration**

accepting that I'll **need to invest time in learning a new language** despite having more experience with JavaScript and recent work with C#.

## Consequences

1. **More accessible:**
   - Machine learning development becomes significantly more accessible with Python's mature ecosystem
   - DevOps tasks will be streamlined with Python's widespread support in that domain
   - The philosophy of Python aligns well with the "Zen of the Garage" principles

2. **More complicated:**
   - Need to learn a new language and ecosystem
   - Need to build up Python proficiency comparable to existing JavaScript knowledge
   - Potentially slower initial development due to learning curve

3. **Positive consequences:**
   - Learning Python adds a valuable skill applicable across many domains
   - Better positioned for machine learning projects
   - Simpler syntax may lead to more maintainable code
   - Strong community support for both ML and DevOps
   - Python is the most popular programming in the world, so I can reach more people with my articles and projects than with C#

4. **Negative consequences:**
   - Not leveraging deeper JavaScript knowledge
   - Potential context switching costs between different programming languages
   - At work I use C# and in the garage Python, which can be overwhelming for me in the short term
   - Some initial productivity loss during learning phase
