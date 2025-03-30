# Workshop Management System

## Overview

This project is a learning exercise aimed at understanding the fundamentals of C# and exception handling. The **Workshop Management System** is a RESTful API built with **.NET 9 Web API** for managing vehicle diagnostics and repairs in an automotive workshop. It provides endpoints to create, retrieve, update, and delete diagnostic and repair records. The system also includes error handling, middleware for logging, and structured exception handling.

## Features

- **Diagnostics Management**: Add, retrieve, and delete vehicle diagnostic records.
- **Repairs Management**: Manage repair orders, update statuses, and track costs.
- **Exception Handling**: Custom exceptions (`DiagnosticException`, `RepairsException`, etc.) for better error control.
- **Middleware for Error Logging**: Centralized error handling and logging.
- **Database Integration**: Uses **Entity Framework Core** with SQL Server (configurable).
- **RESTful API with Swagger**: API documentation is generated using **Swagger UI**.
- **Unit Testing**: Includes tests for controllers using **XUnit and Moq**.

## Technologies Used

- **C#** / **.NET 9 Web API**
- **Entity Framework Core** (SQL Server / In-Memory DB for testing)
- **ASP.NET Core MVC**
- **Swagger for API Documentation**
- **Serilog for Logging**
- **XUnit & Moq for Unit Testing**

## Installation

### Prerequisites

- **.NET 9 SDK** installed
- **Docker** installed
- **Visual Studio Code** or **Visual Studio 2022**

## API Endpoints

### DiagnosticsController

| Method | Endpoint                | Description                      |
| ------ | ----------------------- | -------------------------------- |
| GET    | `/api/diagnostics`      | Retrieve all diagnostic records  |
| POST   | `/api/diagnostics`      | Add a new diagnostic record      |
| DELETE | `/api/diagnostics/{id}` | Delete a diagnostic record by ID |

### RepairsController

| Method | Endpoint                   | Description                         |
| ------ | -------------------------- | ----------------------------------- |
| GET    | `/api/repairs`             | Retrieve all repair orders          |
| GET    | `/api/repairs/{id}`        | Get details of a repair order       |
| POST   | `/api/repairs`             | Add a new repair order              |
| PUT    | `/api/repairs/{id}/status` | Update the status of a repair order |

## Exception Handling

The project includes structured exception handling using custom exception classes:

- **DiagnosticException** for diagnostics-related errors.
- **RepairsException** for repair-related errors.
- **Middleware** (`ErrorLoggingMiddleware.cs`) is implemented to catch and log exceptions globally.

## Running Tests

To run unit tests:

```sh
dotnet test
```

Tests are located in:

- `Tests/Controllers/RepairsControllerTests.cs`
- `Tests/Controllers/DiagnosticsControllerTests.cs`

## Deployment with Docker Compose

1. **Ensure Docker and Docker Compose are installed**
2. **Run the application with Docker Compose**

   ```sh
   docker-compose up --build
   ```

3. **Access the API**
   - The application will be available at `http://localhost:5051` (Swagger Ui will be available at `http://localhost:5051/swagger`)
   - The database will be running in a separate container

To stop the containers, run:

   ```sh
   docker-compose down
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
