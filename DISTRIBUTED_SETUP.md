## Distributed AI Story Agents

Complete guide for running agents as separate services with async communication.

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                    Message Broker                        │
│                   (Redis / In-Memory)                    │
└─────────────────────────────────────────────────────────┘
         ↑                  ↑                  ↑
         │                  │                  │
    ┌────┴────┐        ┌────┴────┐       ┌────┴────┐
    │ Author  │        │Illustr. │       │Publisher│
    │ Service │        │ Service │       │ Service │
    │:8001    │        │:8002    │       │:8003    │
    └─────────┘        └─────────┘       └─────────┘
         │                  │                  │
         └──────────────────┴──────────────────┘
                           │
                    ┌──────┴──────┐
                    │Orchestrator │
                    │  / Client   │
                    └─────────────┘
```

### Workflow

1. **Client** sends story request to **Orchestrator**
2. **Orchestrator** publishes message to **Author Service**
3. **Author Service** generates story → publishes to **Illustrator Service**
4. **Illustrator Service** generates images → publishes to **Publisher Service**
5. **Publisher Service** creates PDF → publishes result to **Orchestrator**
6. **Orchestrator** returns result to **Client**

**All steps run asynchronously and can be parallelized!**

---

## 🚀 Quick Start

### Option 1: Local (Single Machine)

**Terminal 1 - Author Service:**
```bash
python run_author_service.py
```

**Terminal 2 - Illustrator Service:**
```bash
python run_illustrator_service.py
```

**Terminal 3 - Publisher Service:**
```bash
python run_publisher_service.py
```

**Terminal 4 - Create Story:**
```bash
python distributed_client.py --plot "A brave mouse goes on an adventure"
```

### Option 2: All-in-One Launcher

```bash
# Start all services
python run_distributed_system.py

# In another terminal, create story
python distributed_client.py --plot "Your story idea"
```

### Option 3: Docker Compose

```bash
# Start all services with Docker
docker-compose up

# Create story
python distributed_client.py --plot "Your story idea"
```

---

## 📦 Installation

### Dependencies

```bash
pip install -r requirements.txt
pip install flask redis  # For distributed mode
```

### Optional: Redis (for production)

```bash
# Install Redis
# macOS:
brew install redis
redis-server

# Linux:
sudo apt-get install redis-server
sudo systemctl start redis

# Or use Docker:
docker run -d -p 6379:6379 redis:alpine
```

---

## 🎯 Usage Examples

### Basic Story Generation

```bash
python distributed_client.py \
  --plot "A shy kid discovers they can talk to animals" \
  --themes friendship courage \
  --age 8-12 \
  --length short \
  --style children_book
```

### With Detailed Plot

```bash
python distributed_client.py \
  --plot "$(cat my_detailed_plot.txt)" \
  --themes friendship courage kindness \
  --length medium
```

### Programmatic Usage

```python
from distributed.distributed_orchestrator import DistributedOrchestrator
from distributed.message_broker import get_broker

# Initialize
broker = get_broker()
orchestrator = DistributedOrchestrator(broker)

# Create story
story_idea = {
    'plot': 'A brave mouse goes on an adventure',
    'themes': ['courage', 'friendship'],
    'target_age': '8-12',
    'length': 'short',
    'art_style': 'children_book'
}

result = orchestrator.create_story(story_idea)

if result['status'] == 'complete':
    print(f"PDF: {result['publications']['pdf']}")
```

---

## 🌐 Deployment Options

### 1. Single Machine (Development)

All services run on localhost with different ports.

**Pros:**
- Easy setup
- No network configuration
- Fast communication

**Cons:**
- Limited by single machine resources
- No fault tolerance

### 2. Multiple Machines (Production)

Each service runs on a separate machine.

**Setup:**

**Machine 1 - Author Service:**
```bash
# Install dependencies
pip install -r requirements.txt flask redis

# Start service
python run_author_service.py --port 8001
```

**Machine 2 - Illustrator Service:**
```bash
python run_illustrator_service.py --port 8002
```

**Machine 3 - Publisher Service:**
```bash
python run_publisher_service.py --port 8003
```

**Configure Redis:**
```python
# In each service, set Redis URL
export REDIS_URL=redis://your-redis-server:6379
```

**Pros:**
- Scalable
- Can use GPUs on different machines
- Fault tolerant

**Cons:**
- More complex setup
- Network latency

### 3. Docker / Kubernetes

**Docker Compose:**
```bash
docker-compose up
```

**Kubernetes:**
```bash
kubectl apply -f k8s/
```

**Pros:**
- Easy deployment
- Auto-scaling
- Load balancing
- Health checks

---

## 🔧 Configuration

### Service Ports

Default ports:
- Author: 8001
- Illustrator: 8002
- Publisher: 8003

Change with `--port` flag:
```bash
python run_author_service.py --port 9001
```

### Message Broker

**In-Memory (Default):**
```python
broker = get_broker(broker_type='memory')
```

**Redis (Production):**
```python
broker = get_broker(
    broker_type='redis',
    redis_url='redis://localhost:6379'
)
```

### Agent Configuration

Each service uses `config/agents_config.yaml`:

```yaml
author:
  model_name: "mistralai/Mistral-7B-Instruct-v0.2"
  device: "cuda"  # or "cpu"
  
illustrator:
  model_name: "runwayml/stable-diffusion-v1-5"
  device: "cuda"
  
publisher:
  formats:
    - pdf
    - html
```

---

## 📊 Monitoring

### Health Checks

```bash
# Check if services are running
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

Response:
```json
{
  "status": "healthy",
  "agent": "AuthorService",
  "agent_status": "ready"
}
```

### Task Status

```python
from distributed.distributed_orchestrator import DistributedOrchestrator

orchestrator = DistributedOrchestrator()

# Get task status
status = orchestrator.get_task_status(correlation_id)
print(status)

# Get message history
history = orchestrator.get_message_history(correlation_id)
for msg in history:
    print(f"{msg['sender']} → {msg['receiver']}: {msg['message_type']}")
```

---

## 🚀 Performance Optimization

### Parallel Processing

The distributed architecture allows parallel processing:

1. **Author** generates story
2. **Illustrator** can start on early chapters while Author finishes later ones
3. **Publisher** can start layout while illustrations are being generated

### GPU Allocation

**Separate GPUs for each service:**

```yaml
# docker-compose.yml
author:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            device_ids: ['0']  # GPU 0
            
illustrator:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            device_ids: ['1']  # GPU 1
```

### Load Balancing

Run multiple instances of each service:

```bash
# Start 2 Author services
python run_author_service.py --port 8001 &
python run_author_service.py --port 8011 &

# Start 2 Illustrator services
python run_illustrator_service.py --port 8002 &
python run_illustrator_service.py --port 8012 &
```

---

## 🐛 Troubleshooting

### Services Not Communicating

**Check Redis connection:**
```bash
redis-cli ping
# Should return: PONG
```

**Check service logs:**
```bash
# Each service logs to stdout
# Look for "Message sent" and "Message received"
```

### Timeout Errors

Increase timeout:
```bash
python distributed_client.py --plot "..." --timeout 3600  # 1 hour
```

### Service Crashes

Check logs and restart:
```bash
# Services auto-restart in Docker
# For manual restart:
python run_author_service.py
```

---

## 📈 Scaling Guide

### Horizontal Scaling

**Run multiple instances:**

```bash
# 3 Author services
python run_author_service.py --port 8001 &
python run_author_service.py --port 8011 &
python run_author_service.py --port 8021 &

# Load balancer distributes requests
```

### Vertical Scaling

**Allocate more resources:**

```yaml
# docker-compose.yml
author:
  deploy:
    resources:
      limits:
        cpus: '4'
        memory: 16G
      reservations:
        memory: 8G
```

---

## 🔐 Security

### API Authentication

Add API keys:

```python
# In agent_service.py
@app.before_request
def check_auth():
    api_key = request.headers.get('X-API-Key')
    if api_key != os.getenv('API_KEY'):
        return jsonify({'error': 'Unauthorized'}), 401
```

### Network Security

```yaml
# docker-compose.yml
networks:
  internal:
    driver: bridge
    internal: true  # No external access
```

---

## 📚 API Reference

### REST Endpoints

**Health Check:**
```
GET /health
Response: {"status": "healthy", "agent": "AuthorService"}
```

**Send Message:**
```
POST /send
Body: {
  "sender": "client",
  "message_type": "request",
  "content": {"action": "create_story", ...}
}
Response: {"status": "accepted", "message_id": "..."}
```

**Get Status:**
```
GET /status
Response: {"agent": "AuthorService", "status": "ready"}
```

---

## 🎯 Best Practices

1. **Use Redis in production** - In-memory broker is for development only
2. **Monitor health endpoints** - Set up alerts for service failures
3. **Set appropriate timeouts** - Story generation can take 5-30 minutes
4. **Use correlation IDs** - Track requests across services
5. **Log everything** - Essential for debugging distributed systems
6. **Handle failures gracefully** - Implement retry logic
7. **Version your messages** - Add version field for backward compatibility

---

## 🆚 Monolithic vs Distributed

| Feature | Monolithic | Distributed |
|---------|-----------|-------------|
| **Setup** | Simple | Complex |
| **Performance** | Sequential | Parallel |
| **Scalability** | Limited | High |
| **Fault Tolerance** | Low | High |
| **Resource Usage** | Single machine | Multiple machines |
| **Deployment** | Single process | Multiple services |
| **Best For** | Development, testing | Production, scale |

---

## 📝 Summary

**Distributed mode allows:**
- ✅ Parallel processing (Author + Illustrator work simultaneously)
- ✅ Separate deployment (each agent on different servers)
- ✅ Independent scaling (scale Illustrator more than Author)
- ✅ Fault tolerance (one service fails, others continue)
- ✅ GPU optimization (dedicated GPU per service)

**Use distributed mode when:**
- Running in production
- Need to scale
- Have multiple GPUs/machines
- Want fault tolerance
- Processing many stories concurrently

**Use monolithic mode when:**
- Developing/testing
- Single machine
- Simple deployment
- Low volume
