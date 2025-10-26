# Port Configuration Guide

## Overview
The application now supports dynamic port configuration for different environments.

## Port Configuration by Platform

### 🏠 Local Development
- **Port**: `5000` (default)
- **Usage**: `python app.py`
- **Environment Variable**: Set `PORT=5000` in `.env` (optional, already default)

**How it works:**
```python
# In app.py
port = int(os.getenv('PORT', '5000'))  # Uses 5000 if PORT not set
socketio.run(app, host="0.0.0.0", port=port)
```

**Access:** http://localhost:5000

---

### 🌐 Render (Current Deployment)
- **Port**: Auto-assigned by Render (typically `10000`)
- **Environment Variable**: `$PORT` (auto-injected by Render)
- **Configuration**: Already set in `render.yaml`

```yaml
# render.yaml
startCommand: gunicorn --worker-class eventlet --workers 1 --bind 0.0.0.0:$PORT app:app
```

**Note:** Render automatically sets the `$PORT` environment variable. You don't need to set it manually.

**Access:** https://road-pothole-detector.onrender.com

---

### 🚂 Railway
- **Port**: Auto-assigned by Railway (typically starts from `3000`)
- **Environment Variable**: `$PORT` (auto-injected by Railway)
- **Configuration**: Set in `railway.toml`

```toml
# railway.toml
[deploy]
startCommand = "gunicorn --worker-class eventlet --workers 1 --bind 0.0.0.0:$PORT app:app"
```

**Note:** Railway automatically sets the `$PORT` environment variable.

---

### ☁️ Google Cloud Run
- **Port**: `8080` (default, can be overridden)
- **Environment Variable**: `$PORT` (auto-injected by Cloud Run)
- **Configuration**: Dockerfile sets default to 8080

```dockerfile
# Dockerfile
ENV PORT=8080
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --worker-class eventlet app:app
```

**Access:** Assigned by Cloud Run (e.g., https://your-service.run.app)

---

### ✈️ Fly.io
- **Port**: `8080` (defined in fly.toml)
- **Configuration**: Set in `fly.toml`

```toml
# fly.toml
[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
```

**Access:** https://pothole-detector.fly.dev

---

## Port Summary Table

| Platform | Port | How It's Set | Where Configured |
|----------|------|--------------|------------------|
| **Local** | 5000 | `.env` or default | `app.py` line 495 |
| **Render** | Auto (10000) | Auto by platform | `render.yaml` line 18 |
| **Railway** | Auto (3000+) | Auto by platform | `railway.toml` line 6 |
| **Cloud Run** | 8080 | Dockerfile ENV | `Dockerfile` line 31 |
| **Fly.io** | 8080 | fly.toml | `fly.toml` line 8 |

---

## Testing Locally

### Start on Port 5000 (Default)
```bash
python app.py
# Runs on http://localhost:5000
```

### Start on Custom Port
```bash
# Windows PowerShell
$env:PORT="3000"; python app.py

# Linux/Mac
PORT=3000 python app.py
```

Or set in `.env` file:
```env
PORT=3000
```

---

## Troubleshooting

### Issue: "Port already in use"
**Solution:** Change the port in `.env`:
```env
PORT=5001
```

### Issue: "Connection refused" on deployment
**Solution:** Check that your deployment platform is using the correct port:
- **Render**: Should use `$PORT` automatically
- **Railway**: Should use `$PORT` automatically
- **Cloud Run**: Should use `$PORT` (8080)
- **Fly.io**: Should use port 8080

### Issue: App not accessible after deployment
**Solution:** 
1. Check deployment logs
2. Verify `$PORT` environment variable is set
3. Ensure gunicorn is binding to `0.0.0.0:$PORT`

---

## Important Notes

1. **Never hardcode port numbers in code** - Always use the `PORT` environment variable
2. **Platforms auto-assign ports** - Don't manually set PORT on Render/Railway
3. **Use 0.0.0.0 as host** - This allows the app to accept connections from any IP
4. **Check deployment logs** - If the app doesn't start, look for "Listening on port" messages

---

## Quick Reference Commands

```bash
# Local development (port 5000)
python app.py

# Local with custom port
PORT=8000 python app.py

# Check what port is configured
echo $PORT  # Linux/Mac
echo %PORT%  # Windows CMD
$env:PORT    # Windows PowerShell

# Test local connection
curl http://localhost:5000/health
```
