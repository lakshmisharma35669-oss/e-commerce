import os
from flask import Flask, render_template, request, make_response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def index():
    # 1. Render Health Check Fix
    if request.method == 'HEAD':
        return make_response('', 200)

    result_data = None
    
    # 2. Market Logic (POST Request)
    if request.method == 'POST':
        try:
            p_name = request.form.get('product', '')
            p_price = request.form.get('price', '0')
            
            if p_name and p_price:
                price_val = float(p_price)
                # Wholesale Logic (IndiaMART Style)
                wholesale = price_val * 0.55
                margin = price_val - wholesale
                
                result_data = {
                    "name": p_name,
                    "price": price_val,
                    "wholesale": round(wholesale, 2),
                    "margin": round(margin, 2),
                    "trends": "🔥 Trending on Google & IndiaMART"
                }
        except:
            result_data = {"error": "Invalid Price"}

    # 3. Page Loading (GET Request)
    # Yeh 'index.html' tabhi chalega jab aapne file ka naam badal diya ho
    return render_template('index.html', result=result_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
