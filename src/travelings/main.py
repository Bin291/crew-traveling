from .crew import TravelPlanner
from .utils.heplers import *
from datetime import datetime


def run():
    theme = ask_user_preference()

    destination_by_theme = {
        "1": ["Phu Quoc", "Nha Trang", "Vung Tau", "Da Nang", "Ly Son"],
        "2": ["Sa Pa", "Ha Giang", "Pu Luong", "Da Lat", "Buon Me Thuot"],
        "3": ["Hue", "Hoi An", "Ninh Binh", "Ha Noi", "Chau Doc"]
    }

    destination_list = destination_by_theme[theme]

    # Gợi ý điểm đến theo sở thích
    pref_task = TravelPlanner().preference_task()
    pref_crew = TravelPlanner().crew()
    pref_crew.tasks = [pref_task]
    pref_crew.kickoff(inputs={
        "theme": theme,
        "destinations": destination_list
    })

    # Chọn điểm đến cụ thể
    choice = get_int_input("Chọn điểm đến (1-5): ", 1)
    selected_destination = destination_list[choice - 1]

    # Lấy thời tiết
    weather_text, rain_score = get_weather_forecast(selected_destination)
    if rain_score >= 3:
        print(f"\n⚠️ Cảnh báo: Thời tiết tại {selected_destination} có thể có mưa. Hãy cân nhắc mang áo mưa hoặc chọn ngày khác.")

    # Nhập thông tin chuyến đi
    days = get_int_input("Số ngày đi: ")
    people = get_int_input("Số người đi: ")
    budget = get_int_input("Ngân sách (triệu): ")

    # Chuẩn bị input cho kế hoạch chi tiết
    plan_inputs = {
        "destination": selected_destination,
        "days": days,
        "people": people,
        "budget": budget,
        "weather_text": weather_text
    }

    # Tạo kế hoạch chi tiết
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

    # Hiển thị kết quả
    text = print_plan(plan, selected_destination)

    # Hỏi lưu file
    if input("Lưu kế hoạch? (y/n): ").lower() == 'y':
        save_plan_to_file(text, f"travel_plan_{selected_destination.lower()}.txt")
