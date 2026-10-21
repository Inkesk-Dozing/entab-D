# Local Sync Daemon API Specification

The Entab-D synchronization daemon (`python/app.py`) provides a local HTTP JSON API for programmatic rule backup, restoration, and external workflow integration.

- **Base URL**: `http://127.0.0.1:5055`
- **Protocol**: HTTP/1.1
- **Content-Type**: `application/json`

## Endpoints

### 1. Health Probe
- **Path**: `GET /health`
- **Response**: `200 OK`
```json
{
  "ok": true,
  "message": "Tab Tamer Python Backend is running"
}
```

### 2. Retrieve Rules Backup
- **Path**: `GET /rules`
- **Response**: `200 OK`
```json
{
  "rules": [
    {
      "name": "Study",
      "color": "blue",
      "keywords": ["leetcode", "geeksforgeeks"]
    }
  ]
}
```

### 3. Persist Rules Backup
- **Path**: `POST /rules`
- **Request Body**:
```json
{
  "rules": [
    {
      "name": "Research",
      "color": "red",
      "keywords": ["arxiv.org", "ieee.org"]
    }
  ]
}
```
- **Response**: `200 OK`
```json
{
  "ok": true,
  "count": 1,
  "message": "Rules saved successfully"
}
```

### 4. Backup Statistics
- **Path**: `GET /stats`
- **Response**: `200 OK`
```json
{
  "total_rules": 4,
  "total_keywords": 28,
  "rules": [...]
}
```
