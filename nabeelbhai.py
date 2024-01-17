from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import ccxt
import pandas as pd
import numpy as np
import traceback
import uvicorn
import os
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def prices_sETH():
    try:
        ex = ccxt.binanceus()
        ohlcv = ex.fetch_ohlcv('ETH/USDT', '1m', limit=1000)

        if ohlcv:
            prices = [entry[4] for entry in ohlcv]
            mean_price = np.around(np.mean(prices), decimals=2).astype(str)
            return JSONResponse(content={'price': mean_price})
        else:
            return JSONResponse(content={'error': 'No data available'})

    except ccxt.NetworkError as ne:
        print(f"NetworkError: {ne}")
        traceback_info = traceback.format_exc()  # Capture traceback information
        return JSONResponse(content={"error": f"A network error occurred. Check network connectivity or Binance US API status.\n\n{traceback_info}"})

    except ccxt.BaseError as be:
        print(f"CCXT BaseError: {be}")
        return JSONResponse(content={"error": "An error occurred in the CCXT library."})

    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse(content={"error": "An unexpected error occurred."})

if __name__ == "__main__":
    uvicorn.run(app,port=int(os.environ.get('PORT', 8080)), host="0.0.0.0")