---
name: postman-generator
description: Generate complete Postman collections and environments from OpenAPI/Swagger specs or code routing files. Includes rich JS tests validating RESTful compliance (status codes, body schema, response headers) and automates Newman setup/execution.
---

# Postman Generator

Create Postman collections (v2.1.0 format) and environments from API specs, Swagger/OpenAPI yaml/json, route handlers, or API description files. Generate JavaScript test scripts validating RESTful compliance, security headers, schema accuracy, and execute them using Newman.

## Quick Start

```bash
/postman-generator create new collections and env from <context>
/postman-generator validate --collection <collection_path> [--env <environment_path>]
/postman-generator run --collection <collection_path> --env <environment_path>
/postman-generator install-newman
```

## Commands Details

- **Create**: `/postman-generator create new collections and env from <context>`
  Parses the context and automatically outputs configured Postman Collections, Environments, and JavaScript RESTful tests.
- **Validate**: `/postman-generator validate --collection <collection_path> [--env <environment_path>]`
  Runs the Postman collection via Newman, executes all embedded JavaScript assertions, checks status codes, and outputs a validation summary highlighting errors.
- **Run**: `/postman-generator run --collection <collection_path> --env <environment_path>`
  Launches the Newman runner to execute the specified test collection under the given environment scope.
- **Install Newman**: `/postman-generator install-newman`
  Ensures the Newman execution package is properly installed on the host workspace.

## Supported Inputs
- **OpenAPI / Swagger Specs**: `openapi.yaml`, `openapi.json`, `swagger.json`
- **Code Route Files**: Express (`router.get`), Fastify (`app.get`), NestJS controllers, Next.js API route handlers, Hono, Django, FastAPI.
- **Raw API Documentation**: Markdown files, text file lists of endpoints.

## 🛠️ Step-by-Step Execution Workflow

When running `/postman-generator create new collections and env from <context>`:

### 1. Analyze Context & Discover Endpoints
- Discover endpoint paths, request methods (`GET`, `POST`, `PUT`, `DELETE`, etc.), query parameters, path variables, request bodies (JSON/form-data), and potential response structures.
- Map out authentications (Bearer token, API Keys, Basic Auth).

### 2. Identify Test Scenarios (RESTful Best Practices)
For each endpoint, design a request item in the collection with corresponding Postman JS test scripts inside `event` arrays of type `test`:
- **Success Scenarios**:
  - `GET` / `PUT` / `PATCH`: Expect `200 OK`
  - `POST` (Creation): Expect `201 Created`
  - `DELETE`: Expect `204 No Content` or `200 OK`
- **Failure/Edge-case Scenarios** (if payload/routes details exist):
  - Request with missing required parameters: Expect `400 Bad Request` or `422 Unprocessable Entity`
  - Request with invalid/missing token: Expect `401 Unauthorized`
  - Request with restricted access role: Expect `403 Forbidden`
  - Request for non-existent ID: Expect `404 Not Found`
  - Request violating uniqueness/constraints: Expect `409 Conflict`

### 3. Generate Postman Collection JSON (v2.1.0)
Structure the collection JSON following the official Schema v2.1.0. Include:
- A descriptive name and info block.
- Folders grouping endpoints logically (e.g. `Auth`, `Users`, `Products`).
- Requests with variables (`{{baseUrl}}`, `{{token}}`, path variables as `:id`).
- Pre-request scripts (if needed for timestamps or signature generation).
- Postman JS Test Scripts embedded in `"event"` arrays:
  ```json
  "event": [
    {
      "listen": "test",
      "script": {
        "exec": [
          "pm.test(\"Status code is 200\", function () {",
          "    pm.response.to.have.status(200);",
          "});",
          "pm.test(\"Response time is below 500ms\", function () {",
          "    pm.expect(pm.response.responseTime).to.be.below(500);",
          "});",
          "pm.test(\"Content-Type is application/json\", function () {",
          "    pm.response.to.have.header(\"Content-Type\", /json/);",
          "});"
        ],
        "type": "text/javascript"
      }
    }
  ]
  ```

### 4. Create Postman Environment JSON
Write a corresponding environment config file with placeholders:
- `baseUrl`: Base URL of the API.
- `token` or authentication variables.
- Dynamic ID placeholders populated from previous test scripts.

### 5. Install & Run Newman
- Install `newman` CLI for the user if it's not present:
  - Try using `plugins/postman-generator/scripts/newman-runner.sh install`
- Run the collections:
  - Run `plugins/postman-generator/scripts/newman-runner.sh run <collection_path> [environment_path]`
  - Output execution summaries to the terminal.

---

## 📄 Postman Collection Format Reference (v2.1.0)

Your generated collection MUST be valid JSON. Keep this structural boilerplate in mind:

```json
{
  "info": {
    "_postman_id": "unique-uuid",
    "name": "My API Collection",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Login User",
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test(\"Status code is 200\", function () {",
                  "    pm.response.to.have.status(200);",
                  "});",
                  "pm.test(\"Login successful - token received\", function () {",
                  "    var jsonData = pm.response.json();",
                  "    pm.expect(jsonData).to.have.property(\"token\");",
                  "    pm.environment.set(\"token\", jsonData.token);",
                  "});"
                ],
                "type": "text/javascript"
              }
            }
          ],
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"user@example.com\",\n  \"password\": \"password123\"\n}"
            },
            "url": {
              "raw": "{{baseUrl}}/auth/login",
              "host": [
                "{{baseUrl}}"
              ],
              "path": [
                "auth",
                "login"
              ]
            }
          }
        }
      ]
    }
  ]
}
```

## 📄 Postman Environment Format Reference

The generated environment file should follow this structure:

```json
{
  "name": "API Testing Environment",
  "values": [
    {
      "key": "baseUrl",
      "value": "http://localhost:3000",
      "type": "text",
      "enabled": true
    },
    {
      "key": "token",
      "value": "",
      "type": "text",
      "enabled": true
    }
  ],
  "_postman_variable_scope": "environment"
}
```

## 🛡️ Best Practice Test Assertions to Include

1. **Schema Validation via Ajv (Standard in Postman)**:
   ```javascript
   const schema = {
       "type": "object",
       "required": ["id", "name"],
       "properties": {
           "id": { "type": "string" },
           "name": { "type": "string" }
       }
   };
   pm.test("Schema matches contract", function () {
       pm.response.to.have.jsonSchema(schema);
   });
   ```
2. **Security Headers**:
   ```javascript
   pm.test("Strict-Transport-Security header is present", function () {
       pm.response.to.have.header("Strict-Transport-Security");
   });
   ```
3. **Array Type Checks**:
   ```javascript
   pm.test("Response is an array with items", function () {
       var jsonData = pm.response.json();
       pm.expect(jsonData).to.be.an("array");
       if (jsonData.length > 0) {
           pm.expect(jsonData[0]).to.have.property("id");
       }
   });
   ```

## 📥 Newman CLI Installation instructions
If Newman is not installed, inform the user they can run the installer script:
`bash plugins/postman-generator/scripts/install.sh`
Or use the runner tool `plugins/postman-generator/scripts/newman-runner.sh install` which handles dependencies natively or via `npx`.
