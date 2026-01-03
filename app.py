from flask import Flask, render_template, request
from pytrends.request import TrendReq
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
pytrends = TrendReq(hl='en-IN', tz=330)

def get_indiamart_price(product_name):
    # Note: IndiaMart ka official API paid hota hai, yahan hum ek basic scraper logic use kar rahe hain
    try:
        url = f"https://www.indiamart.com/search.mp?ss={product_name.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Price nikalne ka basic logic (IndiaMart ki layout change hone par ise update karna hoga)
        price_tag = soup.find('span', {'class': 'prc'})
        return price_tag.text if price_tag else "100 (Approx)"
    except:
        return "N/A"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        selling_price = float(request.form.get('selling_price', 0))
        
        # 1. Google Trends Data
        pytrends.build_payload([keyword], timeframe='now 7-d', geo='IN')
        trends_data = pytrends.interest_over_time()
        trend_score = int(trends_data[keyword].iloc[-1]) if not trends_data.empty else 0
        
        # 2. IndiaMart Price
        wholesale_price = get_indiamart_price(keyword)
        clean_price = float(''.join(filter(str.isdigit, str(wholesale_price))))
        
        # 3. Profit Calculator
        # (Selling Price - Wholesale Price - 15% Platform Fee - 70 Shipping)
        platform_fee = selling_price * 0.15
        shipping = 70
        profit = selling_price - clean_price - platform_fee - shipping
        
        # 4. Competition Analysis (Demo Logic)
        # Competition high hoti hai agar trend score 80+ ho aur sellers zyada hon
        competition = "High" if trend_score > 70 else "Medium" if trend_score > 30 else "Low"

        result = {
            "keyword": keyword,
            "trend_score": trend_score,
            "wholesale_price": clean_price,
            "profit": round(profit, 2),
            "competition": competition
        }

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)














