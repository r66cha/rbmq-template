# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a RabbitMQ template project demonstrating asynchronous message handling using Python and aiopika. The project provides a simple producer-consumer pattern implementation for RabbitMQ message queues.

## Architecture

The codebase follows a modular architecture:

- `rabbit/` - Core messaging components
  - `config.py` - Connection configuration and logging setup
  - `producer.py` - RabbitMQProducer class with context manager for message publishing
  - `consumer.py` - RabbitMQConsumer class with context manager for message consumption
- `run_produce.py` - Producer entrypoint script
- `run_consume.py` - Consumer entrypoint script

### Key Design Patterns

- **Context Managers**: Both producer and consumer use async context managers (`get_rabbitmq_producer()` and `get_rabbitmq_consumer()`) for proper resource cleanup
- **Channel Management**: Explicit channel creation and management for message operations
- **Exchange/Queue Pattern**: Uses direct exchanges with durable queues for reliable message delivery
- **Routing Key**: Default routing key is "news" (configurable in config.py)

## Development Commands

### RabbitMQ Infrastructure
```bash
# Start RabbitMQ container
make docker-build

# Access RabbitMQ management UI at http://localhost:15672 (guest/guest)
```

### Running Applications
```bash
# Run producer (publishes 10 messages with 1-second intervals)
make run-prod
# or directly: uv run run_produce.py

# Run consumer (listens continuously for messages)
make run-cons
# or directly: uv run run_consume.py
```

### Manual Commands
```bash
# Run producer script directly
uv run run_produce.py

# Run consumer script directly  
uv run run_consume.py

# Stop Docker services
docker compose down
```

## Configuration

Key configuration is in `rabbit/config.py`:
- RabbitMQ connection: localhost:5672 (guest/guest)
- Default exchange: "" (default exchange)
- Default routing key: "news"
- Connection URL format: `amqp://guest:guest@0.0.0.0:5672/`

## Development Notes

- The project uses `uv` as the Python package runner
- Consumer includes a 10-second processing delay to simulate real work
- Messages are acknowledged after processing to ensure delivery guarantee
- Both producer and consumer use robust connections for automatic reconnection
- Russian language comments and print statements are used in the example code

## Dependencies

The project uses:
- `aiopika` for async RabbitMQ operations
- Python async/await patterns throughout
- Docker Compose for RabbitMQ infrastructure

## Message Flow

1. Producer creates a channel and publishes messages to the "direct_name" exchange
2. Messages are routed using "news" routing key
3. Consumer declares the same exchange and binds a durable queue
4. Consumer processes messages with acknowledgment for reliability
