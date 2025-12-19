
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# -------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------
st.set_page_config(
    page_title="Zamfara Leisure & Family Park Management System",
    page_icon="🎡",
    layout="wide"
)

# -------------------------------------------
# HEADER
# -------------------------------------------
st.title("🎡 Zamfara State Leisure & Family Park Digital Management System")
st.markdown("A technology & digital automation module proposed by **Balyak Business Solutions Ltd.**")

# -------------------------------------------
# SIDE MENU
# -------------------------------------------
MENU = [
    "Dashboard",
    "Ticketing & Access Control",
    "Ride & Attraction Monitoring",
    "Revenue Management",
    "Vendor & Shop Management",
    "Events & Facility Booking",
    "Security & Crowd Control",
    "Maintenance & Asset Management",
    "Staff & Shift Management",
    "Admin Panel"
]

choice = st.sidebar.selectbox("Navigation Menu", MENU)

# -------------------------------------------
# SIMULATED DATA GENERATORS
# -------------------------------------------
def ticket_data():
    df = pd.DataFrame({
        "Ticket ID": [f"TKT-{1000+i}" for i in range(100)],
        "Category": np.random.choice(["Adult", "Child", "VIP", "Family"], 100),
        "Amount": np.random.choice([500, 1000, 1500, 3000], 100),
        "Time": pd.date_range(start="2024-01-01", periods=100, freq="H")
    })
    return df

def rides_data():
    df = pd.DataFrame({
        "Ride": ["Ferris Wheel", "Carousel", "Bumper Cars", "Train Ride", "Haunted House"],
        "Status": np.random.choice(["Operational", "Under Maintenance", "Shut Down"], 5),
        "Current Load (%)": np.random.randint(10, 100, 5),
        "Daily Users": np.random.randint(50, 500, 5)
    })
    return df

def vendor_data():
    df = pd.DataFrame({
        "Vendor": ["Food Court A", "Food Court B", "Ice Cream Stand", "Souvenir Shop", "Drinks Stand"],
        "Category": ["Food", "Food", "Snacks", "Goods", "Beverage"],
        "Daily Sales (₦)": np.random.randint(30000, 200000, 5)
    })
    return df

tickets = ticket_data()
rides = rides_data()
vendors = vendor_data()

# -------------------------------------------
# DASHBOARD
# -------------------------------------------
if choice == "Dashboard":
    st.subheader("📊 Park Operations Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Visitors Today", "5,432")
    col2.metric("Total Revenue Today", f"₦{tickets['Amount'].sum():,}")
    col3.metric("Active Rides", str(len(rides[rides["Status"] == "Operational"])))
    col4.metric("Vendors Operating", "5")

    st.markdown("### Visitor Traffic Trend")
    fig = px.line(tickets, x="Time", y="Amount", title="Hourly Ticket Revenue")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------
# TICKETING & ACCESS CONTROL
# -------------------------------------------
elif choice == "Ticketing & Access Control":
    st.subheader("🎟️ Ticketing & Digital Entry System")

    st.markdown("""
    This module demonstrates:
    - QR-code ticketing  
    - Smart gates  
    - Online purchase integration  
    - Real-time visitor count  
    """)

    st.dataframe(tickets)

    st.markdown("### Ticket Category Breakdown")
    fig = px.pie(tickets, names="Category", title="Ticket Category Distribution")
    st.plotly_chart(fig)

# -------------------------------------------
# RIDE & ATTRACTION MONITORING
# -------------------------------------------
elif choice == "Ride & Attraction Monitoring":
    st.subheader("🎢 Rides & Attractions Monitoring")

    st.dataframe(rides)

    st.markdown("### Ride Load Levels")
    fig = px.bar(rides, x="Ride", y="Current Load (%)", color="Current Load (%)")
    st.plotly_chart(fig)

# -------------------------------------------
# REVENUE MANAGEMENT
# -------------------------------------------
elif choice == "Revenue Management":
    st.subheader("💰 Revenue Monitoring Dashboard")

    total = tickets["Amount"].sum()
    st.metric("Total Ticket Sales Today", f"₦{total:,}")

    st.markdown("### Revenue by Hour")
    fig = px.line(tickets, x="Time", y="Amount")
    st.plotly_chart(fig)

    st.markdown("### Vendor Revenue Summary")
    st.dataframe(vendors)

    vendor_fig = px.bar(vendors, x="Vendor", y="Daily Sales (₦)", color="Daily Sales (₦)")
    st.plotly_chart(vendor_fig)

# -------------------------------------------
# VENDOR & SHOP MANAGEMENT
# -------------------------------------------
elif choice == "Vendor & Shop Management":
    st.subheader("🛒 Vendor & Retail Shop Management")

    st.dataframe(vendors)

    st.markdown("### Vendor Performance Rating")
    vendors["Rating"] = np.random.randint(1, 5, 5)
    fig = px.bar(vendors, x="Vendor", y="Rating", color="Rating")
    st.plotly_chart(fig)

# -------------------------------------------
# EVENTS & FACILITY BOOKING
# -------------------------------------------
elif choice == "Events & Facility Booking":
    st.subheader("📅 Hall, Ground & Space Booking")

    with st.form("booking_form"):
        name = st.text_input("Requester Name")
        event_type = st.selectbox("Event Type", ["Wedding", "Birthday", "Meeting", "Concert", "Trade Fair"])
        date = st.date_input("Event Date")
        attendees = st.number_input("Expected Guests", 10, 5000)
        submit = st.form_submit_button("Submit Booking Request")

    if submit:
        st.success(f"Booking request submitted for {event_type} on {date}.")

# -------------------------------------------
# SECURITY & CROWD CONTROL
# -------------------------------------------
elif choice == "Security & Crowd Control":
    st.subheader("🛡️ Security Monitoring & Crowd Control")

    st.markdown("### Real-Time Crowd Density (Simulated)")
    areas = ["Entrance", "Kids Zone", "Food Court", "Water Park", "Central Walkway"]
    density = np.random.randint(10, 100, len(areas))

    df = pd.DataFrame({"Area": areas, "Crowd Level (%)": density})

    fig = px.bar(df, x="Area", y="Crowd Level (%)", color="Crowd Level (%)")
    st.plotly_chart(fig)

    st.warning("⚠️ High crowd density detected at Central Walkway")

# -------------------------------------------
# MAINTENANCE & ASSET MANAGEMENT
# -------------------------------------------
elif choice == "Maintenance & Asset Management":
    st.subheader("🔧 Maintenance & Facility Asset Management")

    assets = pd.DataFrame({
        "Asset": ["Ride Motor 1", "Gate Scanner", "Generator", "Water Pump", "Playground Set"],
        "Condition": np.random.choice(["Good", "Needs Servicing", "Critical"], 5),
        "Last Serviced": pd.date_range(end=pd.Timestamp.today(), periods=5)
    })

    st.dataframe(assets)

# -------------------------------------------
# STAFF MANAGEMENT
# -------------------------------------------
elif choice == "Staff & Shift Management":
    st.subheader("👷 Staff Duty & Shift Management")

    staff = pd.DataFrame({
        "Name": ["Amina Musa", "Kabiru Sani", "Hauwa Bello", "John Paul", "Sani Idris"],
        "Role": ["Ticketing", "Security", "Ride Operator", "Cleaner", "Technical"],
        "Shift": ["Morning", "Evening", "Afternoon", "Morning", "Night"]
    })

    st.dataframe(staff)

# -------------------------------------------
# ADMIN PANEL
# -------------------------------------------
elif choice == "Admin Panel":
    st.subheader("⚙️ System Administration")

    st.checkbox("Enable Online Ticketing")
    st.checkbox("Enable QR Code Scanning")
    st.checkbox("Enable Vendor Cashless Payment")
    st.checkbox("Enable CCTV AI Alerts")
    st.checkbox("Enable Predictive Maintenance Engine")

    st.success("Settings updated successfully.")
    