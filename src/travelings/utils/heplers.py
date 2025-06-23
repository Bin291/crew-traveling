import requests
import base64
from collections import defaultdict
from math import radians, cos, sin, asin, sqrt

# OPENWEATHER API KEY
OPENWEATHER_API_KEY = "2acc1ef3cb4b45a380d122287339ff3c"

city_coords = {
    "Ho Chi Minh": (10.7769, 106.7009),
    "Phu Quoc": (10.2899, 103.9840),
    "Nha Trang": (12.2388, 109.1967),
    "Vung Tau": (10.3470, 107.0843),
    "Da Nang": (16.0544, 108.2022),
    "Ly Son": (15.3904, 109.1203),
    "Sa Pa": (22.3400, 103.8448),
    "Ha Giang": (22.8334, 104.9836),
    "Pu Luong": (20.4878, 105.1846),
    "Da Lat": (11.9404, 108.4583),
    "Buon Me Thuot": (12.6667, 108.0500),
    "Hue": (16.4637, 107.5909),
    "Hoi An": (15.8801, 108.3380),
    "Ninh Binh": (20.2539, 105.9745),
    "Ha Noi": (21.0285, 105.8542),
    "Chau Doc": (10.7000, 105.1167)
}

def get_weather_forecast(location):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={OPENWEATHER_API_KEY}&units=metric&lang=vi"
    res = requests.get(url)
    if res.status_code != 200:
        return "Không thể lấy dự báo thời tiết.", 0

    data = res.json()
    daily_temps = defaultdict(list)
    daily_descs = defaultdict(list)
    rain_count = 0

    for item in data['list']:
        date_txt = item['dt_txt'].split(" ")[0]
        desc = item['weather'][0]['description']
        daily_temps[date_txt].append(item['main']['temp'])
        daily_descs[date_txt].append(desc)
        if "rain" in desc.lower():
            rain_count += 1

    forecast_str = ""
    for i, day in enumerate(sorted(daily_temps.keys())):
        avg_temp = sum(daily_temps[day]) / len(daily_temps[day])
        desc = max(set(daily_descs[day]), key=daily_descs[day].count)
        forecast_str += f"{day}: {desc.capitalize()}, nhiệt độ trung bình {avg_temp:.1f}°C\n"
        if i == 2:
            break

    return forecast_str.strip(), rain_count

def haversine(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return round(c * r, 1)
def print_plan(plan, destination, language="vi"):
    section_titles_vi = [
        "📍 Giới thiệu địa điểm",
        "🎎 Văn hoá & Ẩm thực",
        "🌤️ Dự báo thời tiết",
        "📅 Lịch trình chi tiết",
        "💰 Ước tính chi phí",
        "🛣️ Phương tiện di chuyển",
        "🏨 Chỗ ở đề xuất",
        "📊 Đánh giá khả thi"
    ]

    section_titles_en = [
        "📍 Destination Overview",
        "🎎 Culture & Cuisine",
        "🌤️ Weather Forecast",
        "📅 Detailed Itinerary",
        "💰 Estimated Budget",
        "🛣️ Transportation Options",
        "🏨 Suggested Accommodations",
        "📊 Feasibility Analysis"
    ]

    section_titles = section_titles_vi if language == "vi" else section_titles_en
    output = "\n=== KẾ HOẠCH DU LỊCH ===\n" if language == "vi" else "\n=== TRAVEL PLAN ===\n"

    for i, raw_output in enumerate(plan.tasks_output):
        title = section_titles[i] if i < len(section_titles) else f"Phần {i+1}" if language == "vi" else f"Section {i+1}"
        output += f"\n{title}\n{str(raw_output).strip()}\n"

    if destination in city_coords:
        dist = haversine(city_coords["Ho Chi Minh"], city_coords[destination])
        est_price = min(max(int(dist * 800), 500_000), 2_000_000)
        if language == "vi":
            output += f"\n✈️ Khoảng cách từ Hồ Chí Minh đến {destination}: {dist} km\n💸 Ước tính vé máy bay: {est_price:,} VND"
        else:
            output += f"\n✈️ Distance from Ho Chi Minh City to {destination}: {dist} km\n💸 Estimated flight cost: {est_price:,} VND"

    return output


def save_plan_to_file(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"💾 Đã lưu kế hoạch tại: {filename}")

def ask_user_preference():
    print("\nBạn thích kiểu du lịch nào?")
    print("1. Thư giãn bãi biển 🏖️\n2. Phiêu lưu núi rừng 🏞️\n3. Văn hóa - ẩm thực 🏛️")
    choice = input("Chọn (1-3): ").strip()
    while choice not in ["1", "2", "3"]:
        choice = input("Chọn lại (1-3): ").strip()
    return choice

def get_int_input(prompt, min_value=1):
    while True:
        try:
            v = int(input(prompt).strip())
            if v >= min_value:
                return v
            print(f"⚠️ Nhập số >= {min_value}")
        except:
            print("⚠️ Sai định dạng, nhập lại.")
