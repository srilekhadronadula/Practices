# Movie Ticket Booking System — Visual Seat Grid with Row Pricing, Time Slots & Cancellation
# Drop into Google Colab and run the cell
!pip install gradio --quiet

import gradio as gr
import pandas as pd
import html
from typing import List

# --------- Configuration: movies, slots, seat layout, row-pricing ----------
# Row pricing: you can change values per row label
ROW_PRICING = {
    "A": 300,   # Platinum (front/center)
    "B": 220,   # Gold
    "C": 150,   # Silver
    "D": 120,   # Bronze (if used)
}

# Movie database: each slot has rows & cols; price used as base (multiplied by row price factor if you want)
movies = {
    1: {"name": "Inception", "slots": {
        "10:00 AM": {"base_price": 1.0, "rows": ["A","B","C"], "cols": [1,2,3,4,5]},
        "3:00 PM":  {"base_price": 1.0, "rows": ["A","B","C"], "cols": [1,2,3,4,5]}
    }},
    2: {"name": "Avengers: Endgame", "slots": {
        "1:00 PM": {"base_price": 1.0, "rows": ["A","B","C"], "cols": [1,2,3,4,5]},
        "6:00 PM": {"base_price": 1.0, "rows": ["A","B","C"], "cols": [1,2,3,4,5]}
    }},
    3: {"name": "Interstellar", "slots": {
        "4:00 PM": {"base_price": 1.0, "rows": ["A","B","C"], "cols": [1,2,3,4,5]}
    }},
    4: {"name": "The Dark Knight", "slots": {
        "7:00 PM": {"base_price": 1.0, "rows": ["A","B","C"], "cols": [1,2,3,4,5]}
    }}
}

# Track booked seats per (movie_id, time_slot)
booked_seats = {}   # key: (movie_id, time_slot) -> list of seat strings like "A1"
bookings = []       # list of booking dicts

# ---------- Utility functions ----------
def show_movies_df():
    rows = []
    for mid, m in movies.items():
        for time, info in m["slots"].items():
            total = len(info["rows"]) * len(info["cols"])
            booked = len(booked_seats.get((mid, time), []))
            rows.append({
                "Movie ID": mid,
                "Movie Name": m["name"],
                "Time": time,
                "Seats Available": total - booked
            })
    return pd.DataFrame(rows)

def movie_list_choices():
    return [f"{mid} - {m['name']}" for mid, m in movies.items()]

def get_time_slots(movie_choice: str):
    if not movie_choice:
        return []
    try:
        movie_id = int(movie_choice.split(" - ")[0])
        slots = list(movies[movie_id]["slots"].keys())
        return slots
    except Exception:
        return []

# Build seat-grid HTML - Simple display only, no JavaScript
def build_seat_grid_html(movie_choice: str, time_slot: str):
    if not movie_choice:
        return "<p style='color:red; text-align:center; padding:20px;'>Please select a movie first.</p>"

    if not time_slot:
        return "<p style='color:red; text-align:center; padding:20px;'>Please select a time slot.</p>"

    try:
        movie_id = int(movie_choice.split(" - ")[0])
    except Exception:
        return "<p style='color:red; text-align:center; padding:20px;'>Invalid movie selection.</p>"

    slot = movies[movie_id]["slots"].get(time_slot)
    if not slot:
        return "<p style='color:red; text-align:center; padding:20px;'>Invalid time slot selection.</p>"

    booked = set(booked_seats.get((movie_id, time_slot), []))
    rows = slot["rows"]
    cols = slot["cols"]

    # Build a simple HTML display
    html_parts = []

    # Add CSS
    html_parts.append("""
    <style>
    .movie-seat-map {
        max-width: 500px;
        margin: 0 auto;
        padding: 20px;
        font-family: Arial, sans-serif;
        text-align: center;
    }
    .screen {
        background: linear-gradient(45deg, #4a90e2, #7b68ee);
        color: white;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        font-weight: bold;
        font-size: 16px;
        letter-spacing: 2px;
    }
    .legend {
        display: flex;
        justify-content: center;
        gap: 25px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
    }
    .legend-seat {
        width: 25px;
        height: 25px;
        border-radius: 5px;
        border: 2px solid #333;
    }
    .legend-available { background: #90EE90; }
    .legend-booked { background: #FFB6C1; }

    .seat-grid {
        text-align: center;
    }
    .seat-row {
        margin-bottom: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 5px;
    }
    .row-label {
        width: 40px;
        font-weight: bold;
        font-size: 16px;
    }
    .seat {
        width: 45px;
        height: 45px;
        border: 2px solid #333;
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 12px;
        margin: 2px;
    }
    .seat-available {
        background: #90EE90;
        color: #000;
    }
    .seat-booked {
        background: #FFB6C1;
        color: #666;
    }
    .seat-info {
        background: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin-top: 20px;
        text-align: center;
    }
    .pricing-info {
        margin-top: 15px;
        font-size: 14px;
        color: #666;
        text-align: center;
    }
    </style>
    """)

    # Add the seat map HTML
    html_parts.append('<div class="movie-seat-map">')
    html_parts.append('<div class="screen">🎬 SCREEN 🎬</div>')

    # Legend
    html_parts.append('<div class="legend">')
    html_parts.append('<div class="legend-item"><div class="legend-seat legend-available"></div><span>Available</span></div>')
    html_parts.append('<div class="legend-item"><div class="legend-seat legend-booked"></div><span>Booked</span></div>')
    html_parts.append('</div>')

    # Seat grid
    html_parts.append('<div class="seat-grid">')
    available_seats = []
    for r in rows:
        html_parts.append('<div class="seat-row">')
        html_parts.append(f'<div class="row-label">{r}</div>')
        for c in cols:
            seat = f"{r}{c}"
            price = ROW_PRICING.get(r, 100)
            if seat in booked:
                html_parts.append(f'<div class="seat seat-booked" title="Seat {seat} - Booked">{seat}</div>')
            else:
                html_parts.append(f'<div class="seat seat-available" title="Seat {seat} - ₹{price}">{seat}</div>')
                available_seats.append(f"{seat} (₹{price})")
        html_parts.append('</div>')
    html_parts.append('</div>')

    # Available seats list
    html_parts.append('<div class="seat-info">')
    html_parts.append('<h4>Available Seats:</h4>')
    if available_seats:
        html_parts.append('<p><strong>Type any of these seat codes in the textbox below:</strong></p>')
        html_parts.append('<p style="word-wrap: break-word;">')
        html_parts.append(' | '.join(available_seats))
        html_parts.append('</p>')
    else:
        html_parts.append('<p style="color: red;">All seats are booked for this show!</p>')
    html_parts.append('</div>')

    # Pricing info
    html_parts.append('<div class="pricing-info">')
    pricing_text = " | ".join([f"Row {r}: ₹{p}" for r, p in ROW_PRICING.items() if r in rows])
    html_parts.append(f'<strong>Pricing:</strong> {pricing_text}')
    html_parts.append('</div>')

    html_parts.append('</div>')

    return ''.join(html_parts)

# Get available seats for a show
def get_available_seats(movie_choice: str, time_slot: str):
    if not movie_choice or not time_slot:
        return []

    try:
        movie_id = int(movie_choice.split(" - ")[0])
        slot = movies[movie_id]["slots"].get(time_slot)
        if not slot:
            return []

        booked = set(booked_seats.get((movie_id, time_slot), []))
        available = []

        for r in slot["rows"]:
            for c in slot["cols"]:
                seat = f"{r}{c}"
                if seat not in booked:
                    price = ROW_PRICING.get(r, 100)
                    available.append(f"{seat}")

        return available
    except Exception:
        return []

# Book selected seats: seat_str should be like "A1,B2"
def book_selected_seats(customer_name: str, movie_choice: str, time_slot: str, seat_str: str):
    # Input validation
    if not customer_name or not customer_name.strip():
        return "❌ Please enter your name."

    if not movie_choice:
        return "❌ Please select a movie."

    if not time_slot:
        return "❌ Please select a time slot."

    try:
        movie_id = int(movie_choice.split(" - ")[0])
    except Exception:
        return "❌ Invalid movie selection."

    if not seat_str or not seat_str.strip():
        return "❌ Please select at least one seat from the grid above."

    # Parse selected seats
    selected = [s.strip().upper() for s in seat_str.split(",") if s.strip()]
    if not selected:
        return "❌ No valid seats selected."

    # Validate movie and time slot
    if movie_id not in movies:
        return "❌ Invalid movie selected."

    slot = movies[movie_id]["slots"].get(time_slot)
    if not slot:
        return "❌ Invalid time slot selected."

    # Validate seats exist in this show
    valid_seats = {f"{r}{c}" for r in slot["rows"] for c in slot["cols"]}
    invalid_seats = [s for s in selected if s not in valid_seats]
    if invalid_seats:
        return f"❌ Invalid seats: {', '.join(invalid_seats)}"

    # Check for already booked seats
    booked = booked_seats.setdefault((movie_id, time_slot), [])
    already_booked = [s for s in selected if s in booked]
    if already_booked:
        return f"❌ These seats are already booked: {', '.join(already_booked)}. Please refresh the seat map and select different seats."

    # Calculate total price
    total_price = 0
    for s in selected:
        row = s[0]
        row_price = ROW_PRICING.get(row, 100)
        base = slot.get("base_price", 1.0)
        total_price += int(row_price * base)

    # Create booking
    booking_id = len(bookings) + 1
    bookings.append({
        "Booking ID": booking_id,
        "Customer": customer_name.strip(),
        "Movie": movies[movie_id]["name"],
        "Time": time_slot,
        "Seats": ", ".join(selected),
        "Total (₹)": total_price
    })

    # Mark seats as booked
    booked.extend(selected)

    return f"✅ Booking Successful!\n\nBooking ID: {booking_id}\nCustomer: {customer_name.strip()}\nMovie: {movies[movie_id]['name']}\nTime: {time_slot}\nSeats: {', '.join(selected)}\nTotal Amount: ₹{total_price}\n\nPlease save your Booking ID for future reference."

def view_bookings_df():
    if not bookings:
        return pd.DataFrame([{"Message": "No bookings found. Make your first booking!"}])
    return pd.DataFrame(bookings)

def cancel_booking_by_id(booking_id):
    if booking_id is None:
        return "❌ Please enter a Booking ID."

    try:
        bid = int(booking_id)
    except Exception:
        return "❌ Please enter a valid numeric Booking ID."

    # Find booking
    booking = next((b for b in bookings if b["Booking ID"] == bid), None)
    if not booking:
        return f"❌ Booking ID {bid} not found. Please check the ID and try again."

    # Find movie ID by name
    movie_name = booking["Movie"]
    movie_id = next((k for k, v in movies.items() if v["name"] == movie_name), None)
    if movie_id is None:
        return "❌ Error: Could not find movie information."

    # Free up the seats
    time_slot = booking["Time"]
    seats = [s.strip() for s in booking["Seats"].split(",") if s.strip()]

    booked = booked_seats.setdefault((movie_id, time_slot), [])
    freed_seats = []
    for seat in seats:
        if seat in booked:
            booked.remove(seat)
            freed_seats.append(seat)

    # Remove booking
    bookings.remove(booking)

    return f"✅ Booking Cancelled Successfully!\n\nBooking ID: {bid}\nCustomer: {booking['Customer']}\nMovie: {booking['Movie']}\nTime: {booking['Time']}\nSeats Freed: {', '.join(freed_seats)}\nRefund Amount: ₹{booking['Total (₹)']}"

# ---------- Gradio UI ----------
def refresh_data():
    """Refresh all data displays"""
    return show_movies_df(), view_bookings_df()

with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="cyan"), title="Movie Ticket Booking") as demo:
    gr.Markdown("# 🎟️ Movie Ticket Booking System")
    gr.Markdown("### Visual Seat Selection with Row-Based Pricing")

    with gr.Row():
        with gr.Column(scale=3):
            # Show movies table
            with gr.Tab("🎥 Available Movies"):
                gr.Markdown("**Current movie showtimes and availability:**")
                show_btn = gr.Button("🔄 Refresh Movies", variant="secondary")
                movies_df = gr.Dataframe(
                    value=show_movies_df(),
                    headers=["Movie ID", "Movie Name", "Time", "Seats Available"],
                    interactive=False
                )
                show_btn.click(fn=show_movies_df, outputs=movies_df)

            # Booking tab with grid
            with gr.Tab("🎫 Book Tickets"):
                gr.Markdown("**Step 1:** Enter your details and select movie")
                name = gr.Textbox(
                    label="👤 Your Name",
                    placeholder="Enter your full name",
                    max_lines=1
                )

                with gr.Row():
                    movie_dd = gr.Dropdown(
                        choices=movie_list_choices(),
                        label="🎬 Select Movie",
                        interactive=True
                    )
                    times_dd = gr.Dropdown(
                        label="🕐 Select Time Slot",
                        interactive=True
                    )

                gr.Markdown("**Step 2:** Select your seats")
                seat_html = gr.HTML(value="<p>Select a movie and time slot to view the seat map.</p>")

                # Add seat selector using Gradio components
                with gr.Row():
                    available_seats_dd = gr.Dropdown(
                        label="🪑 Available Seats (Select Multiple)",
                        multiselect=True,
                        choices=[],
                        interactive=True,
                        info="Select seats from dropdown OR type manually below"
                    )

                gr.Markdown("**Step 3:** Confirm your selection")
                selected_seats_box = gr.Textbox(
                    label="Selected Seats",
                    placeholder="Use dropdown above OR type seat codes manually (e.g., A1,A2,B3)",
                    interactive=True,
                    info="Final seat selection - edit if needed"
                )

                # Add a refresh button for seat map
                with gr.Row():
                    refresh_map_btn = gr.Button("🔄 Refresh Seat Map", variant="secondary", size="sm")

                book_btn = gr.Button("🎫 Confirm Booking", variant="primary", size="lg")
                booking_status = gr.Textbox(
                    label="Booking Status",
                    interactive=False,
                    max_lines=10
                )

                # Event handlers
                def update_time_slots_and_clear_grid(movie_choice):
                    slots = get_time_slots(movie_choice)
                    if slots:
                        return (
                            gr.Dropdown(choices=slots, value=None, interactive=True),
                            "<p style='color: #666; text-align: center; padding: 20px;'>Please select a time slot to view the seat map.</p>",
                            gr.Dropdown(choices=[], value=[], interactive=True)
                        )
                    else:
                        return (
                            gr.Dropdown(choices=[], value=None, interactive=True),
                            "<p style='color: #666; text-align: center; padding: 20px;'>Select a movie first to see available time slots.</p>",
                            gr.Dropdown(choices=[], value=[], interactive=True)
                        )

                movie_dd.change(
                    fn=update_time_slots_and_clear_grid,
                    inputs=movie_dd,
                    outputs=[times_dd, seat_html, available_seats_dd]
                )

                def update_seat_grid_and_dropdown(movie_choice, time_slot):
                    if not movie_choice or not time_slot:
                        return (
                            "<p style='color: #666; text-align: center; padding: 20px;'>Please select both a movie and time slot.</p>",
                            gr.Dropdown(choices=[], value=[], interactive=True)
                        )

                    # Get available seats for dropdown
                    available_seats = get_available_seats(movie_choice, time_slot)
                    seat_choices = []

                    if available_seats:
                        try:
                            movie_id = int(movie_choice.split(" - ")[0])
                            slot = movies[movie_id]["slots"][time_slot]
                            for seat in available_seats:
                                row = seat[0]
                                price = ROW_PRICING.get(row, 100)
                                seat_choices.append(f"{seat} (₹{price})")
                        except:
                            seat_choices = available_seats

                    return (
                        build_seat_grid_html(movie_choice, time_slot),
                        gr.Dropdown(choices=seat_choices, value=[], interactive=True)
                    )

                # Update seat grid and dropdown when time slot changes
                times_dd.change(
                    fn=update_seat_grid_and_dropdown,
                    inputs=[movie_dd, times_dd],
                    outputs=[seat_html, available_seats_dd]
                )

                # Update textbox when dropdown selection changes
                def update_textbox_from_dropdown(selected_seats_with_price):
                    if not selected_seats_with_price:
                        return ""
                    # Extract just the seat codes (remove price info)
                    seat_codes = []
                    for item in selected_seats_with_price:
                        seat_code = item.split(" (₹")[0] if " (₹" in item else item
                        seat_codes.append(seat_code)
                    return ",".join(seat_codes)

                available_seats_dd.change(
                    fn=update_textbox_from_dropdown,
                    inputs=available_seats_dd,
                    outputs=selected_seats_box
                )

                # Refresh seat map button
                refresh_map_btn.click(
                    fn=update_seat_grid_and_dropdown,
                    inputs=[movie_dd, times_dd],
                    outputs=[seat_html, available_seats_dd]
                )

                book_btn.click(
                    fn=book_selected_seats,
                    inputs=[name, movie_dd, times_dd, selected_seats_box],
                    outputs=booking_status
                )

        with gr.Column(scale=2):
            with gr.Tab("📋 My Bookings"):
                gr.Markdown("**View all your bookings:**")
                view_btn = gr.Button("🔄 Refresh Bookings", variant="secondary")
                bookings_df = gr.Dataframe(
                    value=view_bookings_df(),
                    interactive=False
                )
                view_btn.click(fn=view_bookings_df, outputs=bookings_df)

            with gr.Tab("❌ Cancel Booking"):
                gr.Markdown("**Cancel an existing booking:**")
                cancel_id = gr.Number(
                    label="Booking ID",
                    precision=0,
                    minimum=1,
                    placeholder="Enter Booking ID to cancel"
                )
                cancel_btn = gr.Button("❌ Cancel Booking", variant="stop")
                cancel_status = gr.Textbox(
                    label="Cancellation Status",
                    interactive=False,
                    max_lines=8
                )
                cancel_btn.click(
                    fn=cancel_booking_by_id,
                    inputs=cancel_id,
                    outputs=cancel_status
                )

            with gr.Tab("💰 Pricing Info"):
                gr.Markdown("**Seat pricing by row:**")
                pricing_rows = [{"Row": r, "Price (₹)": p} for r, p in ROW_PRICING.items()]
                pricing_df = pd.DataFrame(pricing_rows)
                gr.Dataframe(value=pricing_df, interactive=False)

                gr.Markdown("""
                **Pricing Notes:**
                - Row A: Premium seats (closest to screen)
                - Row B: Gold seats
                - Row C: Silver seats (best value)
                - Prices are per seat and may vary by movie/time
                """)

# Launch the app
if __name__ == "__main__":
    demo.launch(share=True, debug=True)
