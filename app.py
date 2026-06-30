"""Weather App - Tkinter GUI. Run: python app.py"""
import tkinter as tk

import requests

import weather_api as api

NAVY, BLUE, BG, GREY, RED = "#17324d", "#2f6fed", "#eef1f8", "#64748b", "#d93025"


def show_weather(event=None):
    for widget in result_frame.winfo_children():
        widget.destroy()
    error_label.config(text="")

    try:
        w = api.get_weather(city_entry.get())
        api.save_history(w)
    except ValueError as e:
        error_label.config(text=str(e))
        return
    except LookupError as e:
        error_label.config(text=str(e))
        return
    except api.ApiKeyError as e:
        error_label.config(text=str(e))
        return
    except requests.exceptions.RequestException:
        error_label.config(text="No internet connection. Please try again.")
        return

    tk.Label(result_frame, text=w["city"], font=("Arial", 16, "bold"),
             fg=NAVY, bg="white").pack()
    tk.Label(result_frame, text=f"{w['temp']} °C", font=("Arial", 32, "bold"),
             fg=BLUE, bg="white").pack()
    tk.Label(result_frame, text=w["description"], font=("Arial", 11),
             fg=GREY, bg="white").pack(pady=(0, 10))

    boxes = tk.Frame(result_frame, bg="white")
    boxes.pack()
    items = [("Feels Like", f"{w['feels_like']} °C"),
             ("Humidity", f"{w['humidity']} %"),
             ("Wind Speed", f"{w['wind']} m/s"),
             ("Pressure", f"{w['pressure']} hPa")]
    for title, value in items:
        box = tk.Frame(boxes, bg=BG, padx=10, pady=8)
        box.pack(side="left", padx=4)
        tk.Label(box, text=title, font=("Arial", 9), fg=GREY, bg=BG).pack()
        tk.Label(box, text=value, font=("Arial", 11, "bold"), fg=NAVY, bg=BG).pack()


api.init_db()

root = tk.Tk()
root.title("Weather App")
root.geometry("520x470")
root.configure(bg=BG)

tk.Label(root, text="Weather App", font=("Arial", 14, "bold"),
         fg="white", bg=NAVY, anchor="w", padx=15, pady=8).pack(fill="x")

card = tk.Frame(root, bg="white", padx=25, pady=20)
card.pack(pady=20)

tk.Label(card, text="Check Weather", font=("Arial", 16, "bold"),
         fg=NAVY, bg="white").pack(pady=(0, 10))
tk.Label(card, text="Enter City Name", font=("Arial", 9, "bold"),
         fg=GREY, bg="white").pack(anchor="w")
city_entry = tk.Entry(card, width=32, font=("Arial", 11))
city_entry.pack(pady=5)
city_entry.focus()
city_entry.bind("<Return>", show_weather)

tk.Button(card, text="GET WEATHER", command=show_weather, bg=BLUE, fg="white",
          font=("Arial", 10, "bold"), relief="flat", pady=6).pack(fill="x", pady=8)
tk.Label(card, text="Real-time data from OpenWeatherMap",
         font=("Arial", 9), fg=GREY, bg="white").pack()

error_label = tk.Label(root, text="", fg=RED, bg=BG, font=("Arial", 10, "bold"))
error_label.pack()

result_frame = tk.Frame(root, bg="white", padx=15, pady=10)
result_frame.pack(pady=5)

root.mainloop()
