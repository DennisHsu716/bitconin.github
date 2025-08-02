**Cross Exchange Trading Core**
=
**1. Installation & Running Guide**
--
**Requirements**  
。Python 3.8+  
。ccxt  
。Other third-party packages: see requirements.txt  
<br>
**Installation**    
Step1. Clone the repository
```
git clone https://github.com/DennisHsu/blockhouse.github   
cd blockhouse.github  
```
Step 2: Install dependencies 
```
pip install -r requirements.txt
```   
Step 3: Run the demo script 
```
python main.py
```
**2. Project Structure**
--
```
├── main.py                 # Main process demo, covering all tasks
├── connectors/             # connectors/ # API modules for various exchanges
├── order_management/       # order_management/ # Order placement, order checking, and order cancellation logic
├── monitoring/             # monitoring/ # Position and PnL query
└── utils/                  # utils/ # Symbol mapping, historical data persistence, and other tools
```

**3. Open-Ended Challenge**
--
**System Design & Scalability**  
* The system is modular and supports plug-and-play connectors for multiple exchanges.

* Weaknesses:
  * Rate limits and API downtime can block or slow the workflow.
  * Centralized script has a single point of failure
  * REST APIs have higher latency than WebSocket.
  * **Note: Binance API is unavailable from some restricted locations, so live data may not be fetched if geoblocked.**
  * **Note: Deriv is not supported by the ccxt library; some features are unavailable or require custom integration.**
* Production Upgrade
  * Use async programming for concurrency.
  * Introduce message queues (RabbitMQ/Kafka) to decouple workflow.
  * Use Redis cache for frequently accessed data.
  * Switch to WebSocket for real-time market data.
  * Deploy microservices via Docker/K8s for high availability and scalability.
  * Add monitoring with Prometheus/Grafana.
 * Error Handling & Resilience
   * Catch and retry failed API requests with exponential backoff.
   * Automatically adjust frequency to respect rate limits.
   * Log and gracefully skip failed exchanges, keep others running.
   * Persist order/position data to allow recovery after a crash.
   * Implement WebSocket reconnection logic and heartbeat.
   * Ensure idempotency and transactional safety for order operations.
* Additional Notes
  * Order book snapshots are generated at runtime and are not included in the repository.
  * To add a new exchange, simply implement a new connector class and register it in main.py.
  * For any questions, please refer to the comments and docstrings in the code.
  * Known limitations:
     * Binance API may be unavailable due to regional restrictions.
     * Deriv exchange is not supported by ccxt, so only partial or simulated features are implemented.




