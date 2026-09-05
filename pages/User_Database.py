import streamlit as st
import sqlite3
import os
import pandas as pd


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="User Database",
    page_icon="👥",
    layout="wide"
)


# =========================================================
# DATABASE FUNCTION
# =========================================================

def get_users():

    conn = sqlite3.connect("user.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            vehicle_reg,
            vehicle_type,
            vehnum,
            mobile,
            driver_photo
        FROM users
        ORDER BY id
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# =========================================================
# TITLE
# =========================================================

st.title("👥 Registered Drivers")

st.write(
    "Registered vehicle owners retrieved from the SQL users table."
)


# =========================================================
# RETRIEVE DATABASE
# =========================================================

if st.button("🔄 Retrieve User Database"):

    try:

        users = get_users()

        if users:

            st.success(
                f"{len(users)} registered drivers found."
            )

            data = []

            for user in users:

                data.append({
                    "ID": user[0],
                    "Name": user[1],
                    "Vehicle Number": user[2],
                    "Vehicle Type": user[3],
                    "Vehicle ID": user[4],
                    "Mobile": user[5],
                    "Driver Photo": user[6]
                })

            df = pd.DataFrame(data)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No registered users found."
            )

    except Exception as e:

        st.error(
            f"Database error: {e}"
        )


# =========================================================
# DRIVER PHOTOS
# =========================================================

st.divider()

st.subheader("📸 Driver Photos")


if st.button("👤 Show Registered Drivers"):

    try:

        users = get_users()

        if not users:

            st.warning(
                "No registered drivers found."
            )

        else:

            for user in users:

                name = user[1]
                vehicle = user[2]
                vehicle_type = user[3]
                mobile = user[5]
                photo = user[6]

                with st.container():

                    col1, col2 = st.columns([1, 3])

                    with col1:

                        if os.path.exists(photo):

                            st.image(
                                photo,
                                width=180
                            )

                        else:

                            st.warning(
                                "Photo not found"
                            )

                    with col2:

                        st.markdown(
                            f"### {name}"
                        )

                        st.write(
                            f"**Vehicle:** {vehicle}"
                        )

                        st.write(
                            f"**Vehicle Type:** {vehicle_type}"
                        )

                        st.write(
                            f"**Mobile:** {mobile}"
                        )

                        st.write(
                            f"**Photo:** {photo}"
                        )

                    st.divider()

    except Exception as e:

        st.error(
            f"Database error: {e}"
        )