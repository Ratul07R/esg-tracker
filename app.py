"""
ESG Risk Tracker | Open Source Intelligence
===========================================

A Streamlit application displaying verified, micro-level environmental
risks across global supply chains in South & Southeast Asia.

Dependencies
------------
    pip install streamlit folium streamlit-folium pandas

Run
---
    streamlit run app.py
"""

import streamlit as st
import folium
from folium.plugins import Fullscreen, MousePosition
from streamlit_folium import st_folium
import pandas as pd
import requests

# ----------------------------------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="ESG Risk Tracker | OSINT",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# DATA — 15 verified, historically accurate ESG risk incidents across
# South & Southeast Asia (India, Bangladesh, Vietnam, Indonesia).
# Compiled from open-source intelligence: Blacksmith Institute / Pure Earth
# reports, UNEP assessments, Greenpeace investigations, CPCB filings and
# peer-reviewed environmental studies.
# ----------------------------------------------------------------------------
ESG_DATA = [
    # --- India -------------------------------------------------------------
    {
        "Location_Name": "Bhopal (Union Carbide Plant)",
        "Country": "India",
        "Latitude": 23.2599,
        "Longitude": 77.4126,
        "Industry": "Pesticide Manufacturing",
        "Issue": "Methyl isocyanate (MIC) gas leak (1984) and ongoing groundwater contamination from the abandoned site.",
        "Risk_Level": "CRITICAL",
    },
    {
        "Location_Name": "Vapi Industrial Cluster",
        "Country": "India",
        "Latitude": 20.3710,
        "Longitude": 72.9056,
        "Industry": "Chemical & Dye Manufacturing",
        "Issue": "Heavy metal and chloride effluent discharge into the Daman Ganga river; CPCB-listed 'critically polluted' cluster.",
        "Risk_Level": "HIGH",
    },
    {
        "Location_Name": "Kanpur Tanneries (Ganga)",
        "Country": "India",
        "Latitude": 26.4499,
        "Longitude": 80.3319,
        "Industry": "Leather Tanneries",
        "Issue": "Hexavalent chromium discharge into the Ganges exceeding permissible limits by up to 60x.",
        "Risk_Level": "HIGH",
    },
    {
        "Location_Name": "Patancheru-Bollaram",
        "Country": "India",
        "Latitude": 17.6259,
        "Longitude": 78.2661,
        "Industry": "Bulk Pharmaceuticals (API)",
        "Issue": "Unprecedented antibiotic and heavy-metal contamination in local water bodies; documented 'superbug' reservoir.",
        "Risk_Level": "CRITICAL",
    },
    {
        "Location_Name": "Singrauli Industrial Zone",
        "Country": "India",
        "Latitude": 24.1987,
        "Longitude": 82.6677,
        "Industry": "Coal Mining & Thermal Power",
        "Issue": "Mercury and fly-ash contamination across tribal communities; recurrent ash-pond breaches.",
        "Risk_Level": "HIGH",
    },
    {
        "Location_Name": "Tirupur Textile Hub",
        "Country": "India",
        "Latitude": 11.1150,
        "Longitude": 77.3370,
        "Industry": "Textile Dyeing & Bleaching",
        "Issue": "Saline and toxic effluent runoff rendering the Noyyal River biologically dead downstream.",
        "Risk_Level": "HIGH",
    },
    {
        "Location_Name": "Najafgarh Drain, Delhi",
        "Country": "India",
        "Latitude": 28.7041,
        "Longitude": 77.1025,
        "Industry": "Mixed Industrial Effluent",
        "Issue": "Untreated industrial discharge carrying heavy metals and dyes into the Yamuna; recurring toxic-foam events.",
        "Risk_Level": "HIGH",
    },
    {
        "Location_Name": "Hazira-Piplod Coastal Belt",
        "Country": "India",
        "Latitude": 21.1800,
        "Longitude": 72.7100,
        "Industry": "Petrochemicals & Fertilizer",
        "Issue": "Coastal ecosystem degradation from hydrocarbon and ammonia runoff into the Arabian Sea.",
        "Risk_Level": "HIGH",
    },
    {
        "Location_Name": "Taloja MIDC",
        "Country": "India",
        "Latitude": 19.0709,
        "Longitude": 73.0799,
        "Industry": "Chemical Manufacturing",
        "Issue": "Persistent VOC emissions and CETP non-compliance affecting downstream agricultural land.",
        "Risk_Level": "HIGH",
    },
    # --- Bangladesh --------------------------------------------------------
    {
        "Location_Name": "Buriganga River, Dhaka",
        "Country": "Bangladesh",
        "Latitude": 23.7000,
        "Longitude": 90.4167,
        "Industry": "Textile Dyeing & Tanneries",
        "Issue": "Collapsing river ecosystem from chromium, cadmium, and dye effluent; biological oxygen demand near zero.",
        "Risk_Level": "CRITICAL",
    },
    {
        "Location_Name": "Chittagong Ship Breaking Yards",
        "Country": "Bangladesh",
        "Latitude": 22.4087,
        "Longitude": 91.7265,
        "Industry": "Ship Breaking & Recycling",
        "Issue": "Asbestos, heavy metals, and PCBs released directly onto tidal flats; documented worker mortality.",
        "Risk_Level": "CRITICAL",
    },
    # --- Vietnam -----------------------------------------------------------
    {
        "Location_Name": "Mekong Delta Industrial Stretch",
        "Country": "Vietnam",
        "Latitude": 10.0250,
        "Longitude": 105.7669,
        "Industry": "Textile & Footwear Manufacturing",
        "Issue": "Persistent dye and solvent discharge contributing to delta eutrophication and fisheries decline.",
        "Risk_Level": "HIGH",
    },
    {
        "Location_Name": "Vedan Factory Outfall, Thi Vai River",
        "Country": "Vietnam",
        "Latitude": 10.6333,
        "Longitude": 107.0000,
        "Industry": "Monosodium Glutamate (MSG)",
        "Issue": "Undisclosed decade-long discharge of ammonia and nitrate effluent; river declared 'dead' in 2008.",
        "Risk_Level": "CRITICAL",
    },
    # --- Indonesia ---------------------------------------------------------
    {
        "Location_Name": "Citarum River, West Java",
        "Country": "Indonesia",
        "Latitude": -7.0500,
        "Longitude": 107.5500,
        "Industry": "Textile & Chemical Manufacturing",
        "Issue": "Lead, mercury, and arsenic levels among the highest ever measured in any river; formerly cited as the world's most polluted.",
        "Risk_Level": "CRITICAL",
    },
    {
        "Location_Name": "Lapindo Mud Volcano, Sidoarjo",
        "Country": "Indonesia",
        "Latitude": -7.5250,
        "Longitude": 112.7150,
        "Industry": "Natural Gas Drilling",
        "Issue": "Continuous mud eruption since 2006 linked to drilling negligence; submerged villages and displaced 60,000+ people.",
        "Risk_Level": "HIGH",
    },
]

df = pd.DataFrame(ESG_DATA)

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🌍 About this tracker")
    st.markdown(
        "Tracking verified micro-level environmental risks in global "
        "supply chains."
    )
    st.markdown("---")
    st.markdown(
        "All data points are compiled from open-source intelligence "
        "(OSINT): regulatory filings, environmental NGO reports, and "
        "peer-reviewed environmental assessments."
    )

    st.markdown("---")
    st.markdown("### 🔢 Dataset summary")
    st.metric(label="Verified sites", value=len(df))
    st.metric(
        label="Critical risk sites",
        value=int((df["Risk_Level"] == "CRITICAL").sum()),
    )

       st.markdown("---")
    st.markdown("### 🔒 Private Beta")
    with st.form("email_form"):
        email = st.text_input("Join the private beta waitlist (Enter Email)", placeholder="you@domain.com")
        submitted = st.form_submit_button("Join Waitlist")
        if submitted:
            if "@" in email:
                requests.post("https://script.google.com/macros/s/AKfycbzZWMQfEpvDFHgOxrs2n3c2c_6fSZMY0AsKfvpUgAzz/dev", json={"email": email})
                st.success("Thanks! You're on the waitlist.")
            else:
                st.warning("Please enter a valid email.")

# ----------------------------------------------------------------------------
# MAIN CONTENT
# ----------------------------------------------------------------------------
st.title("ESG Risk Tracker | Open Source Intelligence")
st.markdown(
    "Interactive map of verified industrial pollution and waste-dumping "
    "incidents across South & Southeast Asia. Click any marker for site details."
)

# Optional country filter (above the map)
country_filter = st.selectbox(
    "Filter by country",
    options=["All"] + sorted(df["Country"].unique().tolist()),
)
view_df = df if country_filter == "All" else df[df["Country"] == country_filter]

# ----------------------------------------------------------------------------
# MAP
# ----------------------------------------------------------------------------
SOUTH_ASIA_CENTER = [20.5937, 78.9629]

m = folium.Map(
    location=SOUTH_ASIA_CENTER,
    zoom_start=4,
    tiles="OpenStreetMap",
    attr=(
        '&copy; <a href="https://www.openstreetmap.org/copyright">'
        "OpenStreetMap</a> contributors &copy; "
        '<a href="https://carto.com/attributions">CARTO</a>'
    ),
    control_scale=True,
)

# Polish UX: fullscreen + live lat/lon readout
Fullscreen(position="topleft").add_to(m)
MousePosition(separator=" | ", prefix="Lat/Lon::").add_to(m)

# All markers are red per spec. CRITICAL sites are rendered slightly larger
# so they remain visually distinct on the dark basemap.
RED = "#ff2b2b"
RADIUS = {"CRITICAL": 11, "HIGH": 8}

for _, row in view_df.iterrows():
    popup_html = f"""
    <div style="font-family: 'Helvetica Neue', Arial, sans-serif;
                min-width: 240px; padding: 6px; color: #1a1a1a;">
      <div style="font-size: 15px; font-weight: 700;
                  color: {RED}; border-bottom: 1px solid #e0e0e0;
                  padding-bottom: 4px; margin-bottom: 6px;">
        {row['Location_Name']}
      </div>
      <table style="width:100%; font-size: 12.5px; border-collapse: collapse;">
        <tr>
          <td style="padding:2px 4px; color:#666; width:90px;">Country</td>
          <td style="padding:2px 4px;"><b>{row['Country']}</b></td>
        </tr>
        <tr>
          <td style="padding:2px 4px; color:#666;">Industry</td>
          <td style="padding:2px 4px;"><b>{row['Industry']}</b></td>
        </tr>
        <tr>
          <td style="padding:2px 4px; color:#666; vertical-align:top;">Issue</td>
          <td style="padding:2px 4px;">{row['Issue']}</td>
        </tr>
        <tr>
          <td style="padding:2px 4px; color:#666;">Risk Level</td>
          <td style="padding:2px 4px;">
            <span style="background:{RED}; color:#fff; padding:2px 8px;
                         border-radius:3px; font-weight:600; font-size:11px;">
              {row['Risk_Level']}
            </span>
          </td>
        </tr>
      </table>
    </div>
    """

    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=RADIUS.get(row["Risk_Level"], 8),
        color=RED,
        weight=2,
        fill=True,
        fill_color=RED,
        fill_opacity=0.85,
        popup=folium.Popup(popup_html, max_width=320),
        tooltip=f"{row['Location_Name']} — {row['Risk_Level']}",
    ).add_to(m)

# Legend (lower-left, themed to match dark basemap)
legend_html = """
<div style="
    position: fixed;
    bottom: 30px; left: 30px;
    z-index: 9999;
    background: rgba(20,20,20,0.85);
    color: #fff;
    padding: 10px 14px;
    border-radius: 6px;
    font-family: Arial, sans-serif;
    font-size: 12px;
    border: 1px solid #444;">
  <div style="font-weight:700; margin-bottom:6px;">ESG Risk Markers</div>
  <div><span style="display:inline-block;width:14px;height:14px;border-radius:50%;
                  background:#ff2b2b;margin-right:6px;vertical-align:middle;"></span>
       CRITICAL (larger)</div>
  <div><span style="display:inline-block;width:10px;height:10px;border-radius:50%;
                  background:#ff2b2b;margin-right:10px;vertical-align:middle;"></span>
       HIGH</div>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Render the map
st_folium(m, width=None, height=650, returned_objects=[])

# ----------------------------------------------------------------------------
# OPTIONAL: collapsible data table under the map
# ----------------------------------------------------------------------------
with st.expander("View underlying dataset"):
    st.dataframe(
        view_df[
            ["Location_Name", "Country", "Industry", "Risk_Level", "Issue"]
        ],
        use_container_width=True,
        hide_index=True,
    )
