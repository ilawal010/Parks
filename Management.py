
import os
import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from fpdf import FPDF

# -------------------- PAGE SETUP --------------------
st.set_page_config(page_title="Zamfara Parks & Garden Management", layout="wide")
st.title("🌳 Zamfara Parks & Garden Management System with Interactive Dashboards")

# -------------------- DATA STORAGE --------------------
SAVE_PATH = "Park_app/data"
os.makedirs(SAVE_PATH, exist_ok=True)

USERS_FILE = os.path.join(SAVE_PATH, "users.csv")
PARKS_FILE = os.path.join(SAVE_PATH, "parks.csv")
BOOKINGS_FILE = os.path.join(SAVE_PATH, "bookings.csv")
INVENTORY_FILE = os.path.join(SAVE_PATH, "inventory.csv")
PARKING_FILE = os.path.join(SAVE_PATH, "parking.csv")

PARKING_RATE_PER_HOUR = 500  # ₦500 per hour (change if needed)


def load_or_init(file_path, default_df):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        default_df.to_csv(file_path, index=False)
        return default_df

def save_all_data():
    st.session_state["users"].to_csv(USERS_FILE, index=False)
    st.session_state["parks"].to_csv(PARKS_FILE, index=False)
    st.session_state["bookings"].to_csv(BOOKINGS_FILE, index=False)
    st.session_state["inventory"].to_csv(INVENTORY_FILE, index=False)
    st.session_state["parking"].to_csv(PARKING_FILE, index=False)

# -------------------- LOAD DATA --------------------
st.session_state["users"] = load_or_init(USERS_FILE, pd.DataFrame([
    {"Username":"admin","Password":"admin123","Role":"Admin"},
    {"Username":"agent1","Password":"agent123","Role":"Agent"},
    {"Username":"logistics1","Password":"log123","Role":"Logistics & Inventory"},
    {"Username":"parking1","Password":"park123","Role":"Parking Management"},
    {"Username":"public","Password":"public123","Role":"Public"}
]))

st.session_state["parks"] = load_or_init(PARKS_FILE, pd.DataFrame([
    {"Park ID":1,"Name":"Central Park","Location":"Gusau","Capacity":100,"Status":"Open"},
    {"Park ID":2,"Name":"River View Garden","Location":"Gusau","Capacity":50,"Status":"Open"},
]))

st.session_state["bookings"] = load_or_init(BOOKINGS_FILE, pd.DataFrame(columns=[
    "Booking ID","Park ID","Visitor Name","Visitors Count","Date",
    "Booking Type","Amount Paid","Checked In","Checked Out"
]))

st.session_state["inventory"] = load_or_init(INVENTORY_FILE, pd.DataFrame(columns=["Item","Quantity","Unit","Park ID"]))
st.session_state["parking"] = load_or_init(PARKING_FILE, pd.DataFrame(columns=[
    "Parking Spot ID","Park ID","Occupied","Vehicle Number","Booking ID"
]))

# -------------------- HELPERS --------------------
def export_excel(df, filename="Report.xlsx"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
        # writer.save()  <-- REMOVE this line
    b = output.getvalue()
    st.download_button(label=f"📥 Download {filename}", data=b, file_name=filename,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def export_pdf(df, filename="Report.pdf", title="Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, title, ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(5)
    
    for i in range(len(df)):
        row = df.iloc[i]
        row_text = " | ".join([str(val) for val in row.values])
        pdf.cell(0, 8, row_text, ln=True)
    
    # Generate PDF as bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')  # <-- 'S' returns PDF as string
    st.download_button(label=f"📥 Download {filename}", data=pdf_bytes, file_name=filename, mime="application/pdf")


def generate_pdf_receipt(title, data_dict, file_name):
    pdf = FPDF()
    pdf.add_page()
    
    # Add logo if you have one
    logo_path = "Park_app/logo.png"
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=80, y=10, w=50)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.ln(40)
    pdf.cell(0, 10, title, ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(5)
    
    # Add booking data
    for key, val in data_dict.items():
        pdf.cell(0, 8, f"{key}: {val}", ln=True)
    
    # Generate PDF in-memory
    pdf_bytes = pdf.output(dest='S').encode('latin1')  # <-- fixed
    st.download_button(
        label=f"📥 Download {file_name}",
        data=pdf_bytes,
        file_name=file_name,
        mime="application/pdf"
    )

# -------------------- PARKING INITIALIZATION --------------------
PARKING_FILE = os.path.join(SAVE_PATH, "parking.csv")

def init_parking_slots():
    slots = []
    for i in range(1, 501):
        slots.append({
            "Slot ID": f"P{i:04d}",
            "Park ID": "",
            "Status": "Free",
            "Vehicle Number": "",
            "Booking ID": "",
            "Check-in Time": "",
            "Check-out Time": "",
            "Hours Stayed": "",
            "Amount Charged": ""
        })
    return pd.DataFrame(slots)

st.session_state["parking"] = load_or_init(PARKING_FILE, init_parking_slots())

# -------------------- LOGIN --------------------
# -------------------- LOGIN --------------------
if "role" not in st.session_state:
    st.session_state["role"] = None
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

st.sidebar.subheader("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_btn = st.sidebar.button("Login")

# Perform login only when button is clicked
if login_btn:
    user_row = st.session_state["users"][
        (st.session_state["users"]["Username"]==username) &
        (st.session_state["users"]["Password"]==password)
    ]
    if not user_row.empty:
        st.session_state["role"] = user_row.iloc[0]["Role"]
        st.session_state["current_user"] = username
        st.sidebar.success(f"Logged in as {username} ({st.session_state['role']})")
    else:
        st.sidebar.error("Invalid credentials")

# Use session state to check login across reruns
if not st.session_state["role"]:
    st.warning("Please log in to access your handle.")
    st.stop()
else:
    role = st.session_state["role"]
    current_user = st.session_state["current_user"]

# -------------------- PUBLIC HANDLE --------------------
# -------------------- PUBLIC HANDLE --------------------
if role=="Public":
    st.subheader("🏞️ Park Info & Self Booking")
    st.dataframe(st.session_state["parks"])

    st.markdown("### Make a Booking")
    park_options = st.session_state["parks"]["Name"].tolist()
    selected_park_name = st.selectbox("Select Park", park_options)
    selected_park = st.session_state["parks"][st.session_state["parks"]["Name"]==selected_park_name].iloc[0]

    visitor_name = st.text_input("Your Name")
    visitors_count = st.number_input("Number of Visitors", min_value=1, max_value=int(selected_park["Capacity"]))
    booking_date = st.date_input("Booking Date", datetime.today())

    # ----------------- Public Service Selection -----------------
    st.markdown("#### Select Services")
    # Service Fees
    CANOPY_RATE_HOURLY = 5000
    CANOPY_RATE_HALF_DAY = 20000
    DAILY_PASS_ADULT = 500
    DAILY_PASS_CHILD = 0
    PARKING_FLAT = 1000
    PHOTOGRAPHY_PERMIT = 2000
    REFRESHMENT_MENU = {"Tea":300,"Water":200,"Soft Drink":500,"Snack":1000}

    canopy_option = st.selectbox("Canopy Usage", ["None", "Hourly", "Half-day"])
    canopy_hours = 0
    if canopy_option=="Hourly":
        canopy_hours = st.number_input("Number of Hours", min_value=1, max_value=12, value=1)

    daily_pass = st.checkbox("Include Daily Park Pass?")
    num_vehicles = st.number_input("Number of Vehicles (Parking Fee)", min_value=0, value=0)
    photo_permit = st.checkbox("Add Photography Permit?")
    selected_items = st.multiselect("Select Refreshments", list(REFRESHMENT_MENU.keys()))
    refreshment_qty = {}
    for item in selected_items:
        qty = st.number_input(f"Quantity of {item}", min_value=0, value=1)
        refreshment_qty[item] = qty

    # ----------------- Calculate Amount -----------------
    canopy_fee = 0
    if canopy_option=="Hourly":
        canopy_fee = canopy_hours * CANOPY_RATE_HOURLY
    elif canopy_option=="Half-day":
        canopy_fee = CANOPY_RATE_HALF_DAY

    daily_pass_fee = 0
    if daily_pass:
        # assuming visitors_count applies to all
        daily_pass_fee = (visitors_count * DAILY_PASS_ADULT)  # children free if you want, adjust logic

    parking_fee = num_vehicles * PARKING_FLAT
    photo_fee = PHOTOGRAPHY_PERMIT if photo_permit else 0
    refreshment_total = sum([REFRESHMENT_MENU[item]*qty for item, qty in refreshment_qty.items()])

    total_amount = canopy_fee + daily_pass_fee + parking_fee + photo_fee + refreshment_total
    st.markdown(f"**Total Amount to Pay: ₦{total_amount}**")

    # ----------------- Confirm Booking -----------------
    if st.button("Confirm Booking"):
        if not visitor_name:
            st.error("Please enter your name before booking.")
        else:
            booking_id = len(st.session_state["bookings"])+1
            st.session_state["bookings"] = pd.concat([
                st.session_state["bookings"],
                pd.DataFrame([{
                    "Booking ID": booking_id,
                    "Park ID": selected_park["Park ID"],
                    "Visitor Name": visitor_name,
                    "Visitors Count": visitors_count,
                    "Date": booking_date,
                    "Booking Type": "Public Booking",
                    "Amount Paid": total_amount,
                    "Checked In": False,
                    "Checked Out": False
                }])
            ], ignore_index=True)
            st.success(f"Booking confirmed for {visitor_name} at {selected_park_name}!")

            # Generate PDF Receipt (fixed)
            pdf_data = {
                "Booking ID": booking_id,
                "Visitor": visitor_name,
                "Park": selected_park_name,
                "Visitors Count": visitors_count,
                "Date": booking_date.strftime("%d/%m/%Y"),
                "Canopy Fee": canopy_fee,
                "Daily Pass Fee": daily_pass_fee,
                "Parking Fee": parking_fee,
                "Photography Fee": photo_fee,
                "Refreshment Fee": refreshment_total,
                "Total Amount Paid": total_amount
            }
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Booking Confirmation Receipt", ln=True, align='C')
            pdf.set_font("Arial", '', 12)
            pdf.ln(5)
            for key, val in pdf_data.items():
                pdf.cell(0, 8, f"{key}: {val}", ln=True)
            
            # Use 'S' to output PDF as bytes
            pdf_bytes = pdf.output(dest='S').encode('latin1')
            st.download_button("📥 Download Booking Receipt (PDF)", data=pdf_bytes,
                               file_name=f"Booking_{booking_id}.pdf", mime="application/pdf")

# -------------------- AGENT HANDLE --------------------
elif role=="Agent":
    st.subheader("🎫 Agent Dashboard - Service Menu")

    # --- Select Park ---
    park_options = st.session_state["parks"]["Name"].tolist()
    selected_park_name = st.selectbox("Select Park", park_options)
    selected_park = st.session_state["parks"][st.session_state["parks"]["Name"]==selected_park_name].iloc[0]

    # --- Service Selection Menu ---
    service_option = st.radio(
        "Select Service to Render",
        [
            "Ticket Sale",
            "Verify Booked Ticket",
            "Vehicle Parking",
            "Kiosks Sale Activity"
        ]
    )

    # -------------------- TICKET SALE --------------------
    if service_option=="Ticket Sale":
        st.markdown("### Ticket Sale for Park Services")

        customer_name = st.text_input("Customer Name")
        booking_date = st.date_input("Booking Date", datetime.today())
        num_adults = st.number_input("Number of Adults", min_value=0, value=1)
        num_children = st.number_input("Number of Children", min_value=0, value=0)

        # Service Fees
        CANOPY_RATE_HOURLY = 5000
        CANOPY_RATE_HALF_DAY = 20000
        DAILY_PASS_ADULT = 500
        DAILY_PASS_CHILD = 0
        PARKING_FLAT = 1000
        PHOTOGRAPHY_PERMIT = 2000
        REFRESHMENT_MENU = {"Tea":300,"Water":200,"Soft Drink":500,"Snack":1000}

        # --- Select services ---
        st.subheader("Select Services")
        canopy_option = st.selectbox("Canopy Usage", ["None", "Hourly", "Half-day"])
        canopy_hours = 0
        if canopy_option=="Hourly":
            canopy_hours = st.number_input("Number of Hours", min_value=1, max_value=12, value=1)
        photo_permit = st.checkbox("Add Photography Permit?")
        daily_pass = st.checkbox("Include Daily Park Pass?")
        num_vehicles = st.number_input("Number of Vehicles (Parking Fee)", min_value=0, value=1)
        selected_items = st.multiselect("Refreshments", list(REFRESHMENT_MENU.keys()))
        refreshment_qty = {}
        for item in selected_items:
            qty = st.number_input(f"Quantity of {item}", min_value=0, value=1)
            refreshment_qty[item] = qty

        # --- Calculate Fees ---
        canopy_fee = 0
        if canopy_option=="Hourly":
            canopy_fee = canopy_hours * CANOPY_RATE_HOURLY
        elif canopy_option=="Half-day":
            canopy_fee = CANOPY_RATE_HALF_DAY

        photo_fee = PHOTOGRAPHY_PERMIT if photo_permit else 0
        daily_pass_fee = (num_adults*DAILY_PASS_ADULT + num_children*DAILY_PASS_CHILD) if daily_pass else 0
        parking_fee = num_vehicles * PARKING_FLAT
        refreshment_total = sum([REFRESHMENT_MENU[item]*qty for item, qty in refreshment_qty.items()])
        total_amount = canopy_fee + photo_fee + daily_pass_fee + parking_fee + refreshment_total

        st.markdown(f"**Total Amount: ₦{total_amount}**")

        if st.button("Confirm Ticket Sale"):
            # Store Booking
            booking_id = len(st.session_state["bookings"])+1
            st.session_state["bookings"] = pd.concat([
                st.session_state["bookings"],
                pd.DataFrame([{
                    "Booking ID": booking_id,
                    "Park ID": selected_park["Park ID"],
                    "Visitor Name": customer_name,
                    "Visitors Count": num_adults+num_children,
                    "Date": booking_date,
                    "Booking Type": "Agent Ticket Sale",
                    "Amount Paid": total_amount,
                    "Checked In": False,
                    "Checked Out": False
                }])
            ], ignore_index=True)
            save_all_data()  # persist changes
            st.success(f"Ticket sale confirmed for {customer_name}!")

            receipt_data = {
                "Booking ID": booking_id,
                "Customer": customer_name,
                "Park": selected_park_name,
                "Date": booking_date.strftime("%d/%m/%Y"),
                "Adults": num_adults,
                "Children": num_children,
                "Canopy Fee": canopy_fee,
                "Daily Pass Fee": daily_pass_fee,
                "Parking Fee": parking_fee,
                "Photography Permit": photo_fee,
                "Refreshment Fee": refreshment_total,
                "Total Amount Paid": total_amount
            }
            generate_pdf_receipt("Ticket Sale Receipt", receipt_data, f"TicketSale_{booking_id}.pdf")

# -------------------- ADMIN, LOGISTICS, PARKING HANDLES --------------------
# (Similar to previous code, just call save_all_data() after any update)
elif role=="Admin":
    st.subheader("🛠 Admin Dashboard")
    # Revenue per park
    revenue = st.session_state["bookings"].groupby("Park ID")["Amount Paid"].sum().reset_index()
    revenue = revenue.merge(st.session_state["parks"][["Park ID","Name"]], on="Park ID")
    st.dataframe(revenue.rename(columns={"Name":"Park Name"}))
    
    fig, ax = plt.subplots(figsize=(10,4))
    sns.barplot(x="Name", y="Amount Paid", data=revenue.rename(columns={"Name":"Name"}), ax=ax)
    ax.set_title("Revenue per Park")
    st.pyplot(fig)
    
    if not revenue.empty:
        export_excel(revenue, filename="Revenue_Report.xlsx")
        export_pdf(revenue, filename="Revenue_Report.pdf", title="Revenue Report")

# -------------------- LOGISTICS & INVENTORY --------------------
elif role=="Logistics & Inventory":
    st.subheader("🧃 Inventory Management")
    st.dataframe(st.session_state["inventory"])
    st.markdown("### Add/Update Inventory")
    item_name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1)
    unit = st.text_input("Unit")
    park_options = st.session_state["parks"]["Name"].tolist()
    selected_park_name = st.selectbox("Select Park", park_options)
    selected_park = st.session_state["parks"][st.session_state["parks"]["Name"]==selected_park_name].iloc[0]
    if st.button("Add/Update Inventory"):
        st.session_state["inventory"] = pd.concat([
            st.session_state["inventory"],
            pd.DataFrame([{"Item":item_name,"Quantity":quantity,"Unit":unit,"Park ID":selected_park["Park ID"]}])
        ], ignore_index=True)
        st.success(f"Inventory updated for {selected_park_name}")
    if not st.session_state["inventory"].empty:
        export_excel(st.session_state["inventory"], filename="Inventory_Report.xlsx")
        export_pdf(st.session_state["inventory"], filename="Inventory_Report.pdf", title="Inventory Report")

# -------------------- PARKING HANDLE --------------------
elif role == "Parking Management":
    st.subheader("🚗 Parking Slot Management")

    PARKING_RATE_PER_HOUR = 500  # ₦ per hour

    park_options = st.session_state["parks"]["Name"].tolist()
    selected_park_name = st.selectbox("Select Park", park_options)
    selected_park = st.session_state["parks"][
        st.session_state["parks"]["Name"] == selected_park_name
    ].iloc[0]

    st.markdown("### Available Parking Slots")
    free_slots = st.session_state["parking"][
        st.session_state["parking"]["Status"] == "Free"
    ]
    st.dataframe(free_slots[["Slot ID", "Status"]])

    st.markdown("### Vehicle Check-In")
    vehicle_no = st.text_input("Vehicle Number")
    booking_id = st.text_input("Booking / Ticket ID")
    selected_slot = st.selectbox(
        "Select Free Slot",
        free_slots["Slot ID"].tolist()
    )

    if st.button("Check-In Vehicle"):
        check_in_time = datetime.now()

        st.session_state["parking"].loc[
            st.session_state["parking"]["Slot ID"] == selected_slot,
            ["Park ID", "Status", "Vehicle Number", "Booking ID", "Check-in Time"]
        ] = [
            selected_park["Park ID"],
            "Occupied",
            vehicle_no,
            booking_id,
            check_in_time.strftime("%Y-%m-%d %H:%M:%S")
        ]

        save_all_data()
        st.success(f"Vehicle {vehicle_no} checked into slot {selected_slot}")

    st.divider()
    st.markdown("### Vehicle Check-Out")

    occupied_slots = st.session_state["parking"][
        st.session_state["parking"]["Status"] == "Occupied"
    ]

    if occupied_slots.empty:
        st.info("No vehicles currently parked.")
    else:
        checkout_slot = st.selectbox(
            "Select Occupied Slot",
            occupied_slots["Slot ID"].tolist()
        )

        if st.button("Check-Out Vehicle"):
            row = st.session_state["parking"][
                st.session_state["parking"]["Slot ID"] == checkout_slot
            ].iloc[0]

            check_in_time = datetime.strptime(
                row["Check-in Time"], "%Y-%m-%d %H:%M:%S"
            )
            check_out_time = datetime.now()

            hours = max(1, int(np.ceil(
                (check_out_time - check_in_time).total_seconds() / 3600
            )))

            amount = hours * PARKING_RATE_PER_HOUR

            st.session_state["parking"].loc[
                st.session_state["parking"]["Slot ID"] == checkout_slot,
                ["Status", "Vehicle Number", "Booking ID",
                 "Check-in Time", "Check-out Time",
                 "Hours Stayed", "Amount Charged"]
            ] = [
                "Free", "", "",
                "",
                check_out_time.strftime("%Y-%m-%d %H:%M:%S"),
                hours,
                amount
            ]

            save_all_data()

            st.success(
                f"Vehicle checked out.\n"
                f"Hours Stayed: {hours} hour(s)\n"
                f"Amount Charged: ₦{amount}"
            )

    st.divider()
    st.markdown("### Parking Status Overview")
    st.dataframe(st.session_state["parking"])

   