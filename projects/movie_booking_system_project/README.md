# 🎟️ Movie Ticket Booking System

A comprehensive web-based movie ticket booking application built with **Gradio** that provides visual seat selection, row-based pricing, and complete booking management.

## ✨ Features

### 🎬 Core Functionality
- **Visual Seat Map**: Interactive seat grid showing available/booked seats
- **Multiple Selection Methods**: Dropdown selection + manual entry
- **Row-Based Pricing**: Different pricing tiers (Platinum, Gold, Silver)
- **Real-time Availability**: Live seat availability updates
- **Booking Management**: View, cancel, and manage bookings
- **Multiple Movies & Showtimes**: Support for various movies and time slots

### 🎯 User Experience
- **Responsive Design**: Works on desktop and mobile devices
- **Step-by-Step Process**: Guided booking flow
- **Visual Feedback**: Color-coded seat status and clear pricing display
- **Error Handling**: Comprehensive validation with helpful error messages
- **Multi-language Support**: Easy to customize for different languages

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation & Setup

1. **Install Dependencies**
   ```bash
   pip install gradio pandas
   ```

2. **Download the Script**
   - Save the provided Python code as `movie_booking.py`

3. **Run the Application**
   ```bash
   python movie_booking.py
   ```
   Or for Google Colab:
   ```python
   # Simply paste the code into a Colab cell and run
   ```

4. **Access the App**
   - Local: Open the URL displayed in terminal (usually `http://127.0.0.1:7860`)
   - Colab: Click the generated public link

## 📱 How to Use

### Step 1: View Available Movies
1. Go to **"🎥 Available Movies"** tab
2. Click **"🔄 Refresh Movies"** to see current availability
3. Note the Movie IDs and available seats

### Step 2: Book Tickets
1. Navigate to **"🎫 Book Tickets"** tab
2. **Enter Your Details**:
   - Fill in your full name
3. **Select Movie & Time**:
   - Choose a movie from dropdown
   - Select preferred time slot
4. **Choose Seats**:
   - **Method 1**: Use the multi-select dropdown (recommended)
   - **Method 2**: Type seat codes manually (e.g., `A1,A2,B3`)
   - **Reference**: Check the visual seat map for availability
5. **Confirm Booking**:
   - Review your selection
   - Click **"🎫 Confirm Booking"**
   - Save your Booking ID for future reference

### Step 3: Manage Bookings
- **View Bookings**: Go to **"📋 My Bookings"** tab
- **Cancel Booking**: Go to **"❌ Cancel Booking"** tab, enter Booking ID

## 💰 Pricing Structure

| Row | Seat Type | Price |
|-----|-----------|-------|
| A   | Platinum  | ₹300  |
| B   | Gold      | ₹220  |
| C   | Silver    | ₹150  |
| D   | Bronze    | ₹120  |

## 🎭 Default Movies & Showtimes

The system comes pre-configured with:

| Movie | Showtimes |
|-------|-----------|
| **Inception** | 10:00 AM, 3:00 PM |
| **Avengers: Endgame** | 1:00 PM, 6:00 PM |
| **Interstellar** | 4:00 PM |
| **The Dark Knight** | 7:00 PM |

**Seat Layout**: All shows have 3 rows (A, B, C) with 5 seats each (1-5)

## ⚙️ Customization

### Adding New Movies
```python
movies[5] = {
    "name": "Your Movie Name",
    "slots": {
        "9:00 AM": {"base_price": 1.0, "rows": ["A","B","C"], "cols": [1,2,3,4,5]},
        "12:00 PM": {"base_price": 1.2, "rows": ["A","B","C"], "cols": [1,2,3,4,5]}
    }
}
```

### Modifying Pricing
```python
ROW_PRICING = {
    "A": 350,   # Premium
    "B": 250,   # Gold
    "C": 180,   # Silver
    "D": 120,   # Bronze
    "E": 100    # Economy
}
```

### Changing Seat Layout
```python
# Example: Larger theater
"rows": ["A","B","C","D","E"],
"cols": [1,2,3,4,5,6,7,8]
```

## 🔧 Technical Details

### Architecture
- **Frontend**: Gradio web interface
- **Backend**: Python with in-memory data storage
- **Styling**: Custom CSS with responsive design
- **State Management**: Python dictionaries and lists

### Data Structure
```python
# Seat booking tracking
booked_seats = {
    (movie_id, time_slot): ["A1", "A2", "B3"]
}

# Booking records
bookings = [
    {
        "Booking ID": 1,
        "Customer": "John Doe",
        "Movie": "Inception",
        "Time": "10:00 AM",
        "Seats": "A1, A2",
        "Total (₹)": 600
    }
]
```

## 🛠️ Troubleshooting

### Common Issues

**Q: Seat selection not working?**
- Use the dropdown method instead of clicking seats
- Try typing seat codes manually (e.g., `A1,A2`)
- Click the "🔄 Refresh Seat Map" button

**Q: Time slots not appearing?**
- Make sure you've selected a movie first
- Check if the movie has available showtimes

**Q: Booking failed?**
- Ensure all fields are filled correctly
- Check if selected seats are still available
- Verify seat codes are valid (e.g., `A1` not `a1`)

**Q: Can't cancel booking?**
- Make sure you're entering the correct Booking ID
- Check the "📋 My Bookings" tab for the right ID

### Browser Compatibility
- **Recommended**: Chrome, Firefox, Safari, Edge (latest versions)
- **Mobile**: Works on mobile browsers but desktop is recommended

## 📊 Features Comparison

| Feature | Status | Description |
|---------|---------|-------------|
| ✅ Visual Seat Map | Available | HTML-based seat layout display |
| ✅ Multiple Selection | Available | Dropdown + manual entry |
| ✅ Real-time Updates | Available | Live availability tracking |
| ✅ Booking Management | Available | View and cancel bookings |
| ✅ Row-based Pricing | Available | Different prices per row |
| ✅ Input Validation | Available | Comprehensive error checking |
| ✅ Responsive Design | Available | Mobile-friendly interface |
| ⚠️ Clickable Seats | Limited | Use dropdown method instead |
| ❌ Payment Integration | Not Available | Can be added separately |
| ❌ User Authentication | Not Available | Single-session use |

## 🚀 Future Enhancements

### Possible Improvements
- **Database Integration**: SQLite/PostgreSQL support
- **User Authentication**: Login/signup system
- **Payment Gateway**: Stripe/PayPal integration
- **Email Notifications**: Booking confirmations
- **Admin Panel**: Movie/showtime management
- **Seat Categories**: VIP, Couple seats, etc.
- **Discount Codes**: Promotional pricing
- **Mobile App**: React Native version

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the code comments for technical details
3. Open an issue on the project repository

---

**Made with ❤️ using Gradio**

*Perfect for movie theaters, event venues, or learning web development!*
