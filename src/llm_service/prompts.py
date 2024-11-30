PROMPTS = [
    "Analyze this Python project for potential violations of the Hexagonal Architecture principles. Specifically, check if the domain layer contains infrastructure-related code, such as direct database queries, HTTP requests, or other external system calls. Highlight any instances and suggest how to refactor them to ensure proper separation of concerns.",
    "Review the ports and adapters in this Python project. Are they designed with appropriate granularity? Look for ports that are either too broad (e.g., handling unrelated operations in a single interface) or too fine-grained (e.g., splitting highly related operations into separate interfaces). Provide recommendations to balance granularity in alignment with business context.",
    "Assess the testing strategy in this Python project. Are there sufficient unit tests for the domain logic, and are they isolated from external dependencies? Check if ports are tested using mock objects or fakes, and whether adapters are validated with integration tests. Identify gaps in test coverage and suggest improvements to align with Hexagonal Architecture principles.",
]

ARCHITECTURE_CONTEXT_PROMPT = """
The project is implemented in Python and adheres to the principles of hexagonal architecture (Ports and Adapters). This approach emphasizes the separation of concerns, organizing the system into distinct, interdependent layers. The layers and their responsibilities are as follows:

Configuration Layer: Handles project setup, initialization, and environment-specific settings (e.g., settings.py, config.py).
Presentation Layer: Manages interaction with users or external systems via APIs, web interfaces, or CLI utilities. It validates inputs and formats outputs. Includes controllers, serializers, and routing files.
Application Layer: Coordinates use cases and workflows, connecting the Presentation and Domain layers. It executes business processes, enforces validation, and interacts with external systems via defined interfaces (e.g., services.py, orchestrators).
Domain Layer: The core business logic, including entities, rules, and domain services. This layer is independent of frameworks or external systems and contains models, value objects, and domain-specific operations (e.g., product.py, order_validation.py).
Infrastructure Layer: Manages technical concerns such as databases, external APIs, logging, and caching. It provides secondary adapters and implements interfaces defined in the Application Layer (e.g., repositories.py, api_clients.py).
This modular structure supports dependency inversion, ensuring that the core business logic is decoupled from external systems. It promotes testability, scalability, and flexibility, enabling independent development and modification of each layer.
"""

DIVIDE_PRESENTATION_LAYER_PROMPT = f"""
I am providing you with a JSON structure that represents the file and module organization of a project. The structure includes details such as folder hierarchies.

Your task is to analyze this structure and extract the components related to the Presentation architectural layer. The Presentation layer manages interaction with users or external systems via APIs, web interfaces, or CLI utilities.

Specifically, you should:

Identify and group all files, modules, classes, and functions that belong to the Presentation layer.
Include only files/modules that manage user or external system interaction, such as controllers, serializers, routing, and input/output formatting (e.g., `controllers.py`, `serializers.py`, `routes.py`).
Return the result as a single dictionary where:

The key is "Presentation".
The value is a dictionary listing the corresponding files and their details.
Start json-part with START_JSON. 
End json-part with END_JSON. 
"""

DIVIDE_APPLICATION_LAYER_PROMPT = f"""
I am providing you with a JSON structure that represents the file and module organization of a project. The structure includes details such as folder hierarchies.

Your task is to analyze this structure and extract the components related to the Application architectural layer. The Application layer includes services, use cases, and application-specific logic.

Specifically, you should:

Identify and group all files, modules, classes, and functions that belong to the Application layer.
Include only files/modules that define application services, orchestration logic, or use cases that connect the domain with external interfaces.
Return the result as a single dictionary where:

The key is "Application".
The value is a dictionary listing the corresponding files and their details.
Start json-part with START_JSON. 
End json-part with END_JSON. 
"""

DIVIDE_DOMAIN_LAYER_PROMPT = f"""
I am providing you with a JSON structure that represents the file and module organization of a project. The structure includes details such as folder hierarchies.

Your task is to analyze this structure and extract the components related to the Domain architectural layer. The Domain layer includes models and core business rules.

Specifically, you should:

Identify and group all files, modules, classes, and functions that belong to the Domain layer.
Include only files/modules that define core business logic, entities, or domain-specific rules.
Return the result as a single dictionary where:

The key is "Domain".
The value is a dictionary listing the corresponding files and their details.
Start json-part with START_JSON. 
End json-part END_JSON. 
"""

DIVIDE_INFRASTRUCTURE_LAYER_PROMPT = f"""
I am providing you with a JSON structure that represents the file and module organization of a project. The structure includes details such as folder hierarchies.

Your task is to analyze this structure and extract the components related to the Infrastructure architectural layer. The Infrastructure layer includes components that implement the technical details for communication, persistence, and other infrastructure concerns.

Specifically, you should:

Identify and group all files, modules, classes, and functions that belong to the Infrastructure layer.
Include only files/modules that provide the technical implementations of persistence, communication, and other infrastructure services such as databases, external APIs, or messaging systems.
Return the result as a single dictionary where:

The key is "Infrastructure".
The value is a dictionary listing the corresponding files and their details.
Start json-part with START_JSON. 
End json-part with END_JSON. 
"""

DIVIDE_TEST_LAYER_PROMPT = f"""
I am providing you with a JSON structure that represents the file and module organization of a project. The structure includes details such as folder hierarchies.

Your task is to analyze this structure and extract the components related to the Test architectural layer. The Test layer includes all testing-related files and modules.

Specifically, you should:

Identify and group all files, modules, classes, and functions that belong to the Test layer.
Include only files/modules that define unit, integration, or functional tests that validate the behavior of other layers.
Return the result as a single dictionary where:

The key is "Test".
The value is a dictionary listing the corresponding files and their details.
Start json-part with START_JSON. 
End json-part with END_JSON. 
"""

STRUCTURE_FROM_PATHS_ONLY = """
I will provide you with a list of file paths representing the files in a project. Your task is to organize these paths into a hierarchical structure that represents the project's directory tree in the form of a nested dictionary. Each key represents a folder or file name. For folders, the value should be another dictionary representing its contents. For files, the value should be the index of the corresponding path in the list I provide.

Return the structure as a nested dictionary. Wrap the result between `START_JSON` and `END_JSON`. Each file's value should correspond to the index of the path in the list I provide, starting from 0.

Here is an example:

START_JSON
{
    "Root": {
        "Folder1": {
            "Subfolder1": {
                "file1.txt": 0,
                "file2.txt": 1
            },
            "file3.txt": 2
        },
        "Folder2": {
            "file4.txt": 3,
            "file5.txt": 4
        },
        "file6.txt": 5
    }
}
END_JSON

Additionally, create another dictionary with the following structure:
- The keys should be: `Domain`, `Application`, `Presentation`, `Infrastructure`.
- The values should be lists containing the indices of the paths that belong to the respective layer.

For example:

START_JSON
{
    "Domain": [0, 1],
    "Application": [2],
    "Presentation": [3, 4],
    "Infrastructure": [5]
}
END_JSON

Ensure that:
1. Paths are categorized into these layers based on their folder structure or naming conventions.
2. Each index corresponds to the position of the path in the provided list.
3. Both dictionaries (hierarchical structure and layer mapping) are returned wrapped in `START_JSON` and `END_JSON`.

"""
