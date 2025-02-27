import streamlit as st
import pandas as pd
from PIL import Image
import os

# Set Streamlit page configuration (Must be the first command)
st.set_page_config(page_title="Professional Unit Converter", layout="wide")

# Apply custom button styling
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #ff4b4b;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #ff1f1f;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Conversion functions
def convert_units(value, from_unit, to_unit, category):
    conversion_factors = {
        "Length": {
            ("Meter", "Kilometer"): 0.001, ("Meter", "Mile"): 0.000621371, ("Meter", "Foot"): 3.28084, ("Meter", "Inch"): 39.3701,
            ("Kilometer", "Meter"): 1000, ("Kilometer", "Mile"): 0.621371, ("Kilometer", "Foot"): 3280.84, ("Kilometer", "Inch"): 39370.1,
            ("Mile", "Meter"): 1609.34, ("Mile", "Kilometer"): 1.60934, ("Mile", "Foot"): 5280, ("Mile", "Inch"): 63360,
            ("Foot", "Meter"): 0.3048, ("Foot", "Kilometer"): 0.0003048, ("Foot", "Mile"): 0.000189394, ("Foot", "Inch"): 12,
            ("Inch", "Meter"): 0.0254, ("Inch", "Kilometer"): 0.0000254, ("Inch", "Mile"): 0.0000157828, ("Inch", "Foot"): 0.0833333
        },
        "Weight": {
            ("Kilogram", "Gram"): 1000, ("Kilogram", "Pound"): 2.20462, ("Kilogram", "Ounce"): 35.274,
            ("Gram", "Kilogram"): 0.001, ("Gram", "Pound"): 0.00220462, ("Gram", "Ounce"): 0.035274,
            ("Pound", "Kilogram"): 0.453592, ("Pound", "Gram"): 453.592, ("Pound", "Ounce"): 16,
            ("Ounce", "Kilogram"): 0.0283495, ("Ounce", "Gram"): 28.3495, ("Ounce", "Pound"): 0.0625
        },
        "Temperature": {
            ("Celsius", "Fahrenheit"): lambda x: (x * 9/5) + 32, ("Celsius", "Kelvin"): lambda x: x + 273.15,
            ("Fahrenheit", "Celsius"): lambda x: (x - 32) * 5/9, ("Fahrenheit", "Kelvin"): lambda x: (x - 32) * 5/9 + 273.15,
            ("Kelvin", "Celsius"): lambda x: x - 273.15, ("Kelvin", "Fahrenheit"): lambda x: (x - 273.15) * 9/5 + 32
        },
        "Time": {
            ("Seconds", "Minutes"): 1/60, ("Seconds", "Hours"): 1/3600, ("Seconds", "Days"): 1/86400, ("Seconds", "Weeks"): 1/604800,
            ("Minutes", "Seconds"): 60, ("Minutes", "Hours"): 1/60, ("Minutes", "Days"): 1/1440, ("Minutes", "Weeks"): 1/10080,
            ("Hours", "Seconds"): 3600, ("Hours", "Minutes"): 60, ("Hours", "Days"): 1/24, ("Hours", "Weeks"): 1/168,
            ("Days", "Seconds"): 86400, ("Days", "Minutes"): 1440, ("Days", "Hours"): 24, ("Days", "Weeks"): 1/7,
            ("Weeks", "Seconds"): 604800, ("Weeks", "Minutes"): 10080, ("Weeks", "Hours"): 168, ("Weeks", "Days"): 7
        },
        "Data Storage": {
            ("Bytes", "KB"): 1/1024, ("Bytes", "MB"): 1/1048576, ("Bytes", "GB"): 1/1073741824, ("Bytes", "TB"): 1/1099511627776,
            ("KB", "Bytes"): 1024, ("KB", "MB"): 1/1024, ("KB", "GB"): 1/1048576, ("KB", "TB"): 1/1073741824,
            ("MB", "Bytes"): 1048576, ("MB", "KB"): 1024, ("MB", "GB"): 1/1024, ("MB", "TB"): 1/1048576,
            ("GB", "Bytes"): 1073741824, ("GB", "KB"): 1048576, ("GB", "MB"): 1024, ("GB", "TB"): 1/1024,
            ("TB", "Bytes"): 1099511627776, ("TB", "KB"): 1073741824, ("TB", "MB"): 1048576, ("TB", "GB"): 1024
        },
        "Speed": {
            ("m/s", "km/h"): 3.6, ("m/s", "mph"): 2.23694, ("km/h", "m/s"): 1/3.6, ("km/h", "mph"): 0.621371,
            ("mph", "m/s"): 0.44704, ("mph", "km/h"): 1.60934
        }
    }

    try:
        factor = conversion_factors[category].get((from_unit, to_unit)) or conversion_factors[category].get((to_unit, from_unit))
        if factor:
            return factor(value) if callable(factor) else value * factor
        return None
    except KeyError:
        return None

# Save conversion history
def save_conversion(category, value, from_unit, to_unit, result):
    history = read_conversion_history()
    new_entry = pd.DataFrame([[category, value, from_unit, to_unit, result]], columns=["Category", "Value", "From", "To", "Result"])
    history = pd.concat([history, new_entry], ignore_index=True)
    history.to_csv("conversion_history.csv", index=False)

# Read conversion history
def read_conversion_history():
    if os.path.exists("conversion_history.csv"):
        return pd.read_csv("conversion_history.csv")
    return pd.DataFrame(columns=["Category", "Value", "From", "To", "Result"])

# Main Streamlit app
def main():
    # Display logo
    try:
        img = Image.open("unit.png")
        st.image(img, use_container_width=True)
    except:
        st.warning("Image not found. Please make sure the image exists in the same directory as the script.")

    with st.sidebar:
        st.title("⚙️ Settings")

        st.subheader("📜 Recent Conversions ")
        recent_history = read_conversion_history()
        if not recent_history.empty:
            st.dataframe(recent_history.tail(10), use_container_width=True)
        else:
            st.write("No recent conversions available.")

        st.markdown("---")

        st.markdown(""" 
         ### ℹ️ About This App
        This **Professional Unit Converter** app provides an easy and intuitive way to convert various units across multiple categories, helping you quickly get accurate results. Whether you're working with **Length**, **Weight**, **Temperature**, **Time**, **Data Storage**, or **Speed**, this app has you covered.
        """)

    # User input
    category = st.selectbox("Select Category", ["Length", "Weight", "Temperature", "Time", "Data Storage", "Speed"])
    value = st.number_input("Enter Value", min_value=0.0, format="%.2f")

    unit_options = {
        "Length": ["Meter", "Kilometer", "Mile", "Foot", "Inch"],
        "Weight": ["Kilogram", "Gram", "Pound", "Ounce"],
        "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
        "Time": ["Seconds", "Minutes", "Hours", "Days", "Weeks"],
        "Data Storage": ["Bytes", "KB", "MB", "GB", "TB"],
        "Speed": ["m/s", "km/h", "mph"]
    }


    # Display From and To Unit
    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From Unit", unit_options[category], key="from_unit")
    with col2:
        to_unit = st.selectbox("To Unit", unit_options[category], key="to_unit")

    # Styled Convert Button
    if st.button("Convert"):
        result = convert_units(value, from_unit, to_unit, category)
        if result is not None:
            st.success(f"Result: {result}")
            save_conversion(category, value, from_unit, to_unit, result)
        else:
            st.error("Conversion not available for the selected units.")

if __name__ == "__main__":
    main()
