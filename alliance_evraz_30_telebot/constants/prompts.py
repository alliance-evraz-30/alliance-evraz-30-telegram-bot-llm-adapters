def about_architecture():
    return (
        "The project is implemented in Python and adheres to the principles of hexagonal architecture"
        " (Ports and Adapters). This approach emphasizes the separation of concerns, organizing "
        "the system into distinct, interdependent layers. The layers and their responsibilities "
        "are as follows: "
        "Configuration Layer: Handles project setup, initialization, and environment-specific "
        "settings (e.g., settings.py, config.py). "
        "Presentation Layer: Manages interaction with users or external systems via APIs, web "
        "interfaces, or CLI utilities. It validates inputs and formats outputs. Includes controllers, "
        "serializers, and routing files. "
        "Application Layer: Coordinates use cases and workflows, connecting the Presentation and "
        "Domain layers. It executes business processes, enforces validation, and interacts with "
        "external systems via defined interfaces (e.g., services.py, orchestrators). "
        "Domain Layer: The core business logic, including entities, rules, and domain services. "
        "This layer is independent of frameworks or external systems and contains models, value "
        "objects, and domain-specific operations (e.g., product.py, order_validation.py). "
        "Infrastructure Layer: Manages technical concerns such as databases, external APIs, "
        "logging, and caching. It provides secondary adapters and implements interfaces defined "
        "in the Application Layer (e.g., repositories.py, api_clients.py). "
        "This modular structure supports dependency inversion, ensuring that the core business "
        "logic is decoupled from external systems. It promotes testability, scalability, and "
        "flexibility, enabling independent development and modification of each layer.")


def find_problems():
    return (
        "Analyze the Python project I provide, which follows Hexagonal Architecture principles. "
        "Your task is to identify common and severe architectural issues. Specifically, "
        "look for the following errors:\n\n"
        "1. **Encapsulation Violation in Core**: The core should be independent of external "
        "technologies, but look for instances where external dependencies (e.g., database "
        "queries or framework-specific code) are directly integrated into the core business logic.\n"
        "   - Example: Direct SQL queries inside core services or models instead of interacting "
        "with abstractions via ports and adapters.\n"
        "   - Solution: Ensure that core services interact with adapters through interfaces, "
        "not directly.\n\n"
        "2. **Overcomplicated Adapters**: Adapters should be focused on communication with external "
        "systems. Check if any adapters contain excessive business logic, violating the"
        " 'Single Responsibility Principle'.\n"
        "   - Example: Complex data processing inside adapters.\n"
        "   - Solution: Keep adapters as simple as possible, leaving business logic in the core.\n\n"
        "3. **Neglecting Testability**: Check if the code structure hinders unit testing, "
        "especially by hardcoding dependencies inside core services.\n"
        "   - Example: Specific class dependencies inside services, preventing easy mocking for testing.\n"
        "   - Solution: Ensure that all dependencies are injected through "
        "constructors or interfaces to facilitate mocking for tests.\n\n"
        "4. **Violation of Layer Independence**: One of the key principles"
        " is the independence of layers. Check if business logic depends on"
        " frameworks (e.g., Flask or Django), making the core logic tightly coupled to the infrastructure.\n"
        "   - Example: Core logic directly depending on a framework like Flask.\n"
        "   - Solution: Ensure that frameworks and libraries are only used in adapters,"
        " keeping them separate from the core.\n\n"
        "5. **Lack of Clear Separation Between Ports and Adapters**: Ensure that "
        "interfaces (ports) are clearly separated from their implementations (adapters). "
        "This prevents difficulties when changing technologies.\n"
        "   - Example: Direct usage of specific classes in adapters inside ports or services.\n"
        "   - Solution: Create a clear distinction between ports (interfaces) and"
        " adapters (implementations), following the Dependency Inversion Principle.\n\n"
    )


def response_format(max_len: int):
    return (
        "Analyze the Python project I provide. The project follows Hexagonal Architecture principles. "
        "Your task is: "
        "1. Provide a brief overall assessment of the project's architecture in no more than three sentences. "
        "2. Identify specific errors or architectural violations in the project. For each issue, "
        "clearly indicate the module or file where it is located, and provide the full path to that"
        " module or file. "
        "3. Offer concrete recommendations on what and how to improve, including examples if applicable. "
        f"Keep your response concise and within {max_len} characters, prioritizing critical insights. "
        "Ensure your suggestions are practical and actionable. Provide your response exclusively in Russian."
    )


def summarise():
    return (
        "I will provide you with multiple texts. Your task is to create a summary of all the provided texts. "
        "If some texts are very similar, please exclude the duplicated information and keep the unique points only. "
        "If the texts are different, make sure to preserve all relevant details in a detailed summary. "
        "Ensure that the summary is coherent, concise, and covers all essential information from the provided "
        "texts without redundancy. "
        "If you encounter very similar content, consolidate it into a single statement to avoid repetition."
    )


def translate():
    return (
        "I will provide you with a text. If the text is in Russian, return it without any changes. "
        "If the text is in English, translate it into Russian, but leave the phrase 'Hexagonal Architecture' "
        "unchanged in its original form. "
        "Make sure the translation is accurate and preserves the meaning of the "
        "original text, except for the specified phrase."
    )


def find_problems_():
    return (
        "You are tasked with analyzing a Python project that follows Hexagonal Architecture principles. "
        "Your goal is to identify common and severe architectural issues within the codebase, focusing on the following errors:\n\n"

        "1. **Encapsulation Violation in Core**: The core domain should be independent of external technologies and frameworks. "
        "Look for instances where external dependencies (e.g., database queries, framework-specific code) are directly integrated into the core business logic.\n"
        "   - **Example**: Direct SQL queries, ORM operations, or framework-specific calls inside core services or domain models instead of using abstractions via ports and adapters.\n"
        "   - **Solution**: Ensure the core interacts with external systems only through well-defined interfaces (ports), implemented by adapters. Keep the core logic isolated and independent.\n\n"

        "2. **Overcomplicated Adapters**: Adapters should focus solely on communication with external systems. Check if any adapters contain business logic, violating the Single Responsibility Principle.\n"
        "   - **Example**: Adapters performing complex data transformations, business rule validations, or other logic that belongs in the core.\n"
        "   - **Solution**: Move business logic to the core domain layer, keeping adapters simple and focused on external interactions.\n\n"

        "3. **Neglecting Testability**: Assess whether the code structure hinders unit testing due to tightly coupled dependencies in core services.\n"
        "   - **Example**: Core services instantiating concrete classes directly, making it difficult to mock dependencies during testing.\n"
        "   - **Solution**: Use dependency injection and inversion of control, passing dependencies via constructors or interfaces to facilitate mocking in tests.\n\n"

        "4. **Violation of Layer Independence**: Verify that business logic is not dependent on external frameworks or infrastructure, ensuring layer independence.\n"
        "   - **Example**: Core logic importing and using classes from web frameworks like Flask or Django.\n"
        "   - **Solution**: Keep framework-specific code confined to the infrastructure layer or adapters, and decouple the core from such dependencies.\n\n"

        "5. **Lack of Clear Separation Between Ports and Adapters**: Ensure that interfaces (ports) are clearly separated from their implementations (adapters), adhering to the Dependency Inversion Principle.\n"
        "   - **Example**: Core services directly referencing adapter implementations instead of interfaces.\n"
        "   - **Solution**: Define interfaces in the core or application layer, and implement them in adapters, ensuring the core depends only on abstractions.\n\n"

        "6. **Inconsistent Naming Conventions and Layer Boundaries**: Check for inconsistencies in naming and adherence to defined layer responsibilities.\n"
        "   - **Example**: Files or classes misplaced in incorrect layers, or inconsistent naming that confuses their purpose.\n"
        "   - **Solution**: Follow consistent naming conventions and ensure that each component resides in the appropriate layer as per architectural guidelines.\n\n"

        "7. **Overuse of Shared Modules or Utilities**: Identify if there's an over-reliance on shared modules that create hidden dependencies between layers.\n"
        "   - **Example**: A 'utils' module used across multiple layers, introducing coupling and violating separation of concerns.\n"
        "   - **Solution**: Limit shared modules to truly generic utilities and avoid placing business logic in them; ensure layers communicate through defined interfaces.\n\n"

        "8. **Data Leakage Between Layers**: Ensure that internal representations or data structures of one layer are not exposed to others, maintaining proper abstraction boundaries.\n"
        "   - **Example**: Passing database entities from the infrastructure layer directly to the presentation layer.\n"
        "   - **Solution**: Use Data Transfer Objects (DTOs) or mappers to translate data between layers.\n\n"

        "9. **Circular Dependencies**: Check for circular dependencies between modules or layers that violate the hierarchical structure of the architecture.\n"
        "   - **Example**: The domain layer importing modules from the infrastructure layer.\n"
        "   - **Solution**: Refactor code to eliminate circular dependencies, possibly by introducing interfaces or reassigning responsibilities.\n\n"

        "10. **Insufficient Error Handling and Logging**: Assess whether errors are properly handled and logged at appropriate layers without leaking implementation details.\n"
        "    - **Example**: Core services catching exceptions but not logging them, or exposing technical error messages to the presentation layer.\n"
        "    - **Solution**: Implement robust error handling strategies, ensuring exceptions are managed appropriately and logged without exposing sensitive information.\n\n"

        "11. **Performance Bottlenecks Due to Architectural Decisions**: Identify any architectural choices that negatively impact performance.\n"
        "    - **Example**: Excessive abstraction layers causing slow data access.\n"
        "    - **Solution**: Optimize critical paths and consider balancing abstraction with performance needs.\n\n"

        "12. **Lack of Documentation and Comments**: Ensure that the codebase is well-documented, aiding in the understanding of architectural decisions and component responsibilities.\n"
        "    - **Example**: Complex modules or functions without explanatory comments or documentation.\n"
        "    - **Solution**: Add meaningful comments and documentation, explaining the purpose and usage of code components.\n\n"

        "When analyzing the code, provide specific examples of the issues found, referencing the relevant code snippets or modules. "
        "Offer recommendations on how to address each problem, aligned with the principles of Hexagonal Architecture and best practices in software engineering."
    )
