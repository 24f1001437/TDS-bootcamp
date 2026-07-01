from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid

# 1. Initialize the app
app = FastAPI()

# 2. The Bouncer: Setup strict CORS policy
# We ONLY put your specific assigned URL here. No wildcards (*).
allowed_origin = "https://dash-225zln.example.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[allowed_origin], # Only this origin gets the ACAO header
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, OPTIONS (preflight), etc.
    allow_headers=["*"],
)

# 3. The Toll Booth: Custom Middleware for Headers
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    # Start the stopwatch
    start_time = time.time()
    
    # Let the request pass through to the calculator
    response = await call_next(request)
    
    # Stop the stopwatch and calculate duration
    process_time = time.time() - start_time
    
    # Stamp the required headers on the way out
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    
    return response

# 4. The Calculator: The /stats endpoint
@app.get("/stats")
def get_stats(values: str):
    # Convert the string "1,2,3" into a list of actual integers [1, 2, 3]
    # We split by comma, and convert each piece to an int.
    numbers = [int(v) for v in values.split(",")]
    
    # Calculate the math
    count_val = len(numbers)
    sum_val = sum(numbers)
    min_val = min(numbers)
    max_val = max(numbers)
    mean_val = sum_val / count_val
    
    # Return the exact JSON structure the grader wants
    # Return the exact JSON format required
    return {
        "email": "24f1001437@ds.study.iitm.ac.in", 
        "count": count,
        "sum": total_sum,
        "min": minimum,
        "max": maximum,
        "mean": mean
    }
