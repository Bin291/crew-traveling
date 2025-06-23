from crew import TravelPlanner
from utils.heplers import *


def run(theme=None, budget=None, people=None, days=None, selected_destination=None, language="vi"):
    if not all([theme, budget, people, days]):
        theme = ask_user_preference()
        budget = get_int_input("Ngân sách (triệu): ")
        people = get_int_input("Số người đi: ")
        days = get_int_input("Số ngày đi: ")

    # Gợi ý địa điểm
    destination_by_theme = {
        "1": ["Phu Quoc", "Nha Trang", "Vung Tau", "Da Nang", "Ly Son"],
        "2": ["Sa Pa", "Ha Giang", "Pu Luong", "Da Lat", "Buon Me Thuot"],
        "3": ["Hue", "Hoi An", "Ninh Binh", "Ha Noi", "Chau Doc"]
    }
    destinations = destination_by_theme[theme]

    affordable = []
    for dest in destinations:
        dist = haversine(city_coords["Ho Chi Minh"], city_coords[dest])
        price = min(max(int(dist * 800), 500_000), 2_000_000)
        if price <= budget * 1_000_000 * 0.3:
            affordable.append(dest)

    if not affordable:
        affordable = destinations  # fallback if none affordable

    # Nếu chưa có selected_destination, trả về danh sách gợi ý
    if not selected_destination:
        return affordable

    # Lấy thời tiết cho điểm đến đã chọn
    weather_text, rain_score = get_weather_forecast(selected_destination)
    if rain_score >= 3 and language == "vi":
        print(f"\n⚠️ Cảnh báo mưa tại {selected_destination}.")
    elif rain_score >= 3 and language == "en":
        print(f"\n⚠️ Warning: Rainy forecast in {selected_destination}.")

    plan_inputs = {
        "destination": selected_destination,
        "days": days,
        "people": people,
        "budget": budget,
        "weather_text": weather_text
    }

    # Lên kế hoạch với CrewAI
    plan_crew = TravelPlanner().crew()
    plan_crew.tasks = [
        TravelPlanner().intro_task(),
        TravelPlanner().culture_task(),
        TravelPlanner().weather_task(),
        TravelPlanner().itinerary_task(),
        TravelPlanner().cost_task(),
        TravelPlanner().transport_task(),
        TravelPlanner().accommodation_task(),
        TravelPlanner().feasibility_task()
    ]
    plan = plan_crew.kickoff(inputs=plan_inputs)

    return print_plan(plan, selected_destination, language=language)
