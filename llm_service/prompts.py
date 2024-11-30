ARCHITECTURE_CONTEXT_PROMPT = """
The project is implemented in Python and adheres to the principles of hexagonal architecture (Ports and Adapters). This approach emphasizes the separation of concerns, organizing the system into distinct, interdependent layers. The layers and their responsibilities are as follows:

Configuration Layer: Handles project setup, initialization, and environment-specific settings (e.g., settings.py, config.py).
Presentation Layer: Manages interaction with users or external systems via APIs, web interfaces, or CLI utilities. It validates inputs and formats outputs. Includes controllers, serializers, and routing files.
Application Layer: Coordinates use cases and workflows, connecting the Presentation and Domain layers. It executes business processes, enforces validation, and interacts with external systems via defined interfaces (e.g., services.py, orchestrators).
Domain Layer: The core business logic, including entities, rules, and domain services. This layer is independent of frameworks or external systems and contains models, value objects, and domain-specific operations (e.g., product.py, order_validation.py).
Infrastructure Layer: Manages technical concerns such as databases, external APIs, logging, and caching. It provides secondary adapters and implements interfaces defined in the Application Layer (e.g., repositories.py, api_clients.py).
This modular structure supports dependency inversion, ensuring that the core business logic is decoupled from external systems. It promotes testability, scalability, and flexibility, enabling independent development and modification of each layer.
"""


# def domain_layer_contains_infrastructure_code():
#     return ("Analyze this Python project for potential violations of the Hexagonal Architecture principles."
#             " Specifically, check if the domain layer contains infrastructure-related code, such as "
#             "direct database queries, HTTP requests, or other external system calls. Highlight any "
#             "instances and suggest how to refactor them to ensure proper separation of concerns.")
#
#
# def review_ports():
#     return ("Review the ports and adapters in this Python project. Are they designed with "
#             "appropriate granularity? Look for ports that are either too broad (e.g., handling "
#             "unrelated operations in a single interface) or too fine-grained (e.g., splitting highly"
#             " related operations into separate interfaces). Provide recommendations to balance "
#             "granularity in alignment with business context.")
#
#
# def testing_strategy():
#     return ("Assess the testing strategy in this Python project. Are there sufficient unit tests"
#             " for the domain logic, and are they isolated from external dependencies? "
#             "Check if ports are tested using mock objects or fakes, and whether adapters"
#             " are validated with integration tests. Identify gaps in test coverage and "
#             "suggest improvements to align with Hexagonal Architecture principles.")


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
        "2. Identify specific errors or architectural violations in the project. For each issue, clearly indicate the module or file where it is located. "
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
        "If the text is in English, translate it into Russian, but leave the phrase 'Hexagonal Architecture' unchanged in its original form. "
        "Make sure the translation is accurate and preserves the meaning of the original text, except for the specified phrase."
    )
