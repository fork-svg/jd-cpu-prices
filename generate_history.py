#!/usr/bin/env python3
"""
生成历史测试数据
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# 基础价格数据
BASE_PRICES = {
    "100023456701": {"base": 1299, "variance": 100, "name": "Intel i5-14400", "category": "Intel CPU", "brand": "Intel", "model": "i5-14400", "cores": 10, "threads": 16},
    "100023456702": {"base": 1899, "variance": 120, "name": "Intel i5-14600K", "category": "Intel CPU", "brand": "Intel", "model": "i5-14600K", "cores": 14, "threads": 20},
    "100023456703": {"base": 2899, "variance": 150, "name": "Intel i7-14700K", "category": "Intel CPU", "brand": "Intel", "model": "i7-14700K", "cores": 20, "threads": 28},
    "100023456704": {"base": 4299, "variance": 200, "name": "Intel i9-14900K", "category": "Intel CPU", "brand": "Intel", "model": "i9-14900K", "cores": 24, "threads": 32},
    "100023456705": {"base": 1099, "variance": 80, "name": "AMD R5 7600", "category": "AMD CPU", "brand": "AMD", "model": "R5 7600", "cores": 6, "threads": 12},
    "100023456706": {"base": 1699, "variance": 120, "name": "AMD R7 7700", "category": "AMD CPU", "brand": "AMD", "model": "R7 7700", "cores": 8, "threads": 16},
    "100023456707": {"base": 2699, "variance": 150, "name": "AMD R7 7800X3D", "category": "AMD CPU", "brand": "AMD", "model": "R7 7800X3D", "cores": 8, "threads": 16},
    "100023456708": {"base": 2999, "variance": 180, "name": "AMD R9 7900X", "category": "AMD CPU", "brand": "AMD", "model": "R9 7900X", "cores": 12, "threads": 24},
    "100023456709": {"base": 4199, "variance": 250, "name": "AMD R9 7950X", "category": "AMD CPU", "brand": "AMD", "model": "R9 7950X", "cores": 16, "threads": 32},
    "100023456710": {"base": 999, "variance": 80, "name": "Intel i5-13400F", "category": "Intel CPU", "brand": "Intel", "model": "i5-13400F", "cores": 10, "threads": 16},
    "100023456711": {"base": 2299, "variance": 150, "name": "Intel i7-13700K", "category": "Intel CPU", "brand": "Intel", "model": "i7-13700K", "cores": 16, "threads": 24},
    "100023456712": {"base": 799, "variance": 60, "name": "AMD R5 5600", "category": "AMD CPU", "brand": "AMD", "model": "R5 5600", "cores": 6, "threads": 12},
}


def generate_day_data(date_str: str) -> dict:
    """生成某一天的价格数据"""
    products = []

    for product_id, info in BASE_PRICES.items():
        price = info["base"] + random.uniform(-info["variance"], info["variance"])
        price = round(price, 2)
        in_stock = random.random() > 0.1

        product_data = {
            "id": product_id,
            "name": info["name"],
            "category": info["category"],
            "brand": info["brand"],
            "model": info["model"],
            "cores": info["cores"],
            "threads": info["threads"],
            "url": f"https://item.jd.com/{product_id}.html",
            "price": price if in_stock else None,
            "original_price": round(price * 1.1, 2) if random.random() > 0.5 and in_stock else None,
            "in_stock": in_stock,
            "coupon": round(random.uniform(20, 100), 2) if random.random() > 0.6 and in_stock else None,
        }
        products.append(product_data)

    return {
        "date": date_str,
        "timestamp": f"{date_str}T10:00:00.000000",
        "source": "simulated",
        "products": products
    }


def main():
    """生成过去30天的历史数据"""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)

    today = datetime.now()

    for i in range(30, -1, -1):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        data_file = data_dir / f"{date_str}.json"

        if not data_file.exists():
            data = generate_day_data(date_str)
            with open(data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"生成数据: {date_str}")

    print("✅ 历史数据生成完成")


if __name__ == "__main__":
    main()
