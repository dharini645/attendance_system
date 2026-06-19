"""
app.py

A Streamlit web dashboard to view attendance records.
Shows today's attendance, full history, and lets you export CSV.

HOW TO RUN:
  streamlit run app.py

Then open your browser at:  http://localhost:8501
"""

import streamlit as st
import pandas as pd
from datetime import date
from database import init_db, get_all_records, get_today_records
from export import export_to_csv


# ─── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Attendance System",
    page_icon="🎓",
    layout="wide"
)


# ─── Initialize database ──────────────────────────────────────
init_db()


# ─── Header ───────────────────────────────────────────────────
st.title("🎓 Smart Attendance System")
st.caption("Face Recognition — powered by OpenCV & face_recognition")
st.divider()


# ─── Today's Summary ──────────────────────────────────────────
st.subheader(f"📅 Today's Attendance — {date.today().strftime('%d %B %Y')}")

today_records = get_today_records()    # list of (name, time) tuples

col1, col2 = st.columns([1, 3])

with col1:
    st.metric("Students Present", len(today_records))

with col2:
    if today_records:
        today_df = pd.DataFrame(today_records, columns=["Name", "Time Marked"])
        st.dataframe(today_df, use_container_width=True, hide_index=True)
    else:
        st.info("No attendance marked yet today. Run attendance.py to start a session.")


st.divider()


# ─── Full History ─────────────────────────────────────────────
st.subheader("📋 Full Attendance History")

all_records = get_all_records()    # list of dicts: Name, Date, Time

if all_records:
    df = pd.DataFrame(all_records)

    # ── Filters ──
    col_filter1, col_filter2 = st.columns(2)

    with col_filter1:
        # Date filter
        unique_dates = sorted(df["Date"].unique(), reverse=True)
        selected_date = st.selectbox("Filter by date", ["All dates"] + unique_dates)

    with col_filter2:
        # Name filter
        unique_names = sorted(df["Name"].unique())
        selected_name = st.selectbox("Filter by student", ["All students"] + unique_names)

    # Apply filters
    filtered_df = df.copy()
    if selected_date != "All dates":
        filtered_df = filtered_df[filtered_df["Date"] == selected_date]
    if selected_name != "All students":
        filtered_df = filtered_df[filtered_df["Name"] == selected_name]

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(filtered_df)} of {len(df)} total records")

else:
    st.info("No records found. Run attendance.py first.")


st.divider()


# ─── Export Section ───────────────────────────────────────────
st.subheader("💾 Export Records")

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    if st.button("📥 Export Today's CSV"):
        path = export_to_csv(all_records=False)
        st.success(f"Saved: {path}")
        with open(path, "rb") as f:
            st.download_button(
                label="⬇️ Download CSV",
                data=f,
                file_name=path,
                mime="text/csv"
            )

with col_exp2:
    if st.button("📥 Export Full History CSV"):
        path = export_to_csv(all_records=True)
        st.success(f"Saved: {path}")
        with open(path, "rb") as f:
            st.download_button(
                label="⬇️ Download CSV",
                data=f,
                file_name=path,
                mime="text/csv"
            )


st.divider()


# ─── About section ────────────────────────────────────────────
with st.expander("ℹ️ How to use this system"):
    st.markdown("""
    **Step 1 — Add student photos**
    Place one clear photo per student in the `known_faces/` folder.
    Name each file as the student's name: e.g. `Dharini.jpg`

    **Step 2 — Encode the faces**
    ```bash
    python encode_faces.py
    ```

    **Step 3 — Start attendance session**
    ```bash
    python attendance.py
    ```
    The webcam will open. Press **Q** to quit, **S** to save CSV immediately.

    **Step 4 — View this dashboard**
    ```bash
    streamlit run app.py
    ```

    **Tech stack:** Python · OpenCV · face_recognition · SQLite · Pandas · Streamlit
    """)