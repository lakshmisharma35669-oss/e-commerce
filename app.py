import os
from flask import Flask, render_template, request, make_response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    if request.method == 'HEAD':
        return make_response('', 200)

    analysis_data = None
    
    if request.method == 'POST':
        product = request.form.get('product')
        price = request.form.get('price')
        
        if product and price:
            # IndiaMART & Google Trends Simulation Logic
            price_val = float(price)
            
            # Market Intelligence Logic
            market_trend = "High Demand" if "kurti" in product.lower() or "shirt" in product.lower() else "Stable"
            indiamart_avg = price_val * 0.6  # Simulated Wholesale Price
            margin = price_val - indiamart_avg
            
            analysis_data = {
                "product": product,
                "price": price_val,
                "trend": market_trend,
                "wholesale": round(indiamart_avg, 2),
                "margin": round(margin, 2),
                "google_trends": "Rising in North India",
                "competitors": "Medium (IndiaMART Analysis)"
            }

    return render_template('index.html', result=analysis_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
