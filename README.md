# Scala Backend Service

A simple Scala backend service built with Akka HTTP that replicates the functionality of the Python Flask application.

## Requirements

- Scala 2.13.x
- SBT (Scala Build Tool)
- JDK 11 or higher

## Getting Started

1. Ensure you have SBT installed on your system.

2. Clone this repository:

   ```
   git clone <repository-url>
   cd demo-customer-be
   ```

3. To run the application:

   ```
   sbt run
   ```

4. The server will start on http://localhost:5000

## Project Structure

- `Search.scala` - Main application that sets up the Akka HTTP server and routes
- `build.sbt` - SBT build configuration file with dependencies

## Adding New Routes

To add more routes, modify the `route` definition in `Search.scala`. For example:

```scala
val route =
  cors() {
    pathSingleSlash {
      get {
        complete(Message("Welcome to the backend!"))
      }
    } ~
    path("new-endpoint") {
      get {
        complete(Message("This is a new endpoint"))
      }
    }
  }
```
