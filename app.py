from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route("/analyze")
def analyze():
    price = float(request.args.get("price", 100))
    cost = float(request.args.get("cost", 50))
    time = int(request.args.get("time", 12))

    demand = lambda p: 1000 * np.exp(-p / 50)
    
    prices = np.linspace(cost, price*2, 20)
    profits = [(p - cost) * demand(p) for p in prices]

    best_index = int(np.argmax(profits))
    best_price = float(prices[best_index])

    return jsonify({
        "收益": float(demand(price) * price),
        "利潤": float((price - cost) * demand(price)),
        "最佳價格": round(best_price, 2),
        "策略": [
            "價格略低於市場平均可提升銷量",
            "中午時段需求較穩定",
            "建議搭配促銷提升轉換率"
        ],
        "價格曲線": list(prices),
        "利潤曲線": list(profits)
    })

@app.route("/chat")
def chat():
    q = request.args.get("q", "")
    return jsonify({"reply": f"建議：針對「{q}」，可降低成本並優化定價策略。"})

app.run(host="0.0.0.0", port=10000)
