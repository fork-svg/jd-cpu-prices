#!/usr/bin/env python3
"""
获取京东 CPU 价格
"""

import json
import random
from datetime import datetime
from pathlib import Path

# 基础价格数据（模拟）
BASE_PRICES = {
    "100023456701": {"min": 1199, "max": 1399, "name": "Intel i5-14400"},
    "100023456702": {"min": 1799, "max": 1999, "name": "Intel i5-14600K"},
    "100023456703": {"min": 2799, "max": 2999, "name": "Intel i7-14700K"},
    "100023456704": {"min": 4199, "max": 4399, "name": "Intel i9-14900K"},
    "100023456705": {"min": 999, "max": 1199, "name": "AMD R5 7600"},
    "100023456706": {"min": 1599, "max": 1799, "name": "AMD R7 7700"},
    "100023456707": {"min": 2599, "max": 2799, "name": "AMD R7 7800X3D"},
    "100023456708": {"min": 2899, "max": 3099, "name": "AMD R9 7900X"},
    "100023456709": {"min": 4099, "max": 4299, "name": "AMD R9 7950X"},
    "100023456710": {"min": 899, "max": 1099, "name": "Intel i5-13400F"},
    "100023456711": {"min": 2199, "max": 2399, "name": "Intel i7-13700K"},
    "100023456712": {"min": 699, "max": 899, "name": "AMD R5 5600"},
}


def fetch_price(product_id: str) -> dict:
    """模拟获取价格"""
    info = BASE_PRICES.get(product_id, {})
    price = round(random.uniform(info.get("min", 1000), info.get("max", 1500)), 2)
    in_stock = random.random() > 0.1

    return {
        "price": price if in_stock else None,
        "original_price": round(price * 1.1, 2) if random.random() > 0.5 and in_stock else None,
        "in_stock": in_stock,
        "coupon": round(random.uniform(20, 100), 2) if random.random() > 0.6 and in_stock else None,
    }


def main():
    """主函数"""
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)

    products_file = base_dir / "products.json"
    with open(products_file, 'r', encoding='utf-8') as f:
        products = json.load(f)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    timestamp = now.isoformat()

    results = []
    for product in products:
        price_data = fetch_price(product["id"])
        result = {
            **product,
            "url": f"https://item.jd.com/{product['id']}.html",
            **price_data
        }
        results.append(result)
        status = f"¥{price_data['price']}" if price_data['in_stock'] else "无货"
        print(f"{product['brand']} {product['model']}: {status}")

    data_file = data_dir / f"{date_str}.json"
    data = {
        "date": date_str,
        "timestamp": timestamp,
        "source": "simulated",
        "products": results
    }

    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 数据已保存到: {data_file}")
    update_readme(results)


def update_readme(products: list):
    """更新 README"""
    base_dir = Path(__file__).parent
    readme_file = base_dir / "README.md"

    lines = [
        "# 📊 京东 CPU 价格监控",
        "",
        "自动追踪京东 CPU 价格变化，每日更新两次。",
        "",
        "## 📈 产品价格",
        "",
        "| 产品 | 核心/线程 | 当前价格 | 有货 |",
        "|------|-----------|----------|------|",
    ]

    for p in products:
        price_str = f"¥{p['price']:.2f}" if p['price'] else "-"
        stock_str = "✅" if p['in_stock'] else "❌"
        lines.append(f"| {p['brand']} {p['model']} | {p['cores']}核{p['threads']}线程 | {price_str} | {stock_str} |")

    lines.extend([
        "",
        "---",
        "",
        "## 📊 价格趋势图",
        "",
        "### 产品价格对比",
        "",
        "![所有产品价格对比](./charts/all_products_comparison.png)",
        "",
        "### 每核心价格趋势",
        "",
        "![每核心价格趋势](./charts/price_per_core_trend.png)",
        "",
        "---",
        "",
        "## 🔄 自动更新",
        "",
        "每天北京时间 10:00 和 20:00 自动更新价格。",
        "",
        "## 📁 数据格式",
        "",
        "历史数据存储在 `data/YYYY-MM-DD.json` 文件中。",
        "",
        "---",
        "",
        "*数据仅供参考，以京东实际价格为准*",
    ])

    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print("✅ README 已更新")


if __name__ == "__main__":
    main()
