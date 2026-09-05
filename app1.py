import streamlit as st
import os
import urllib.parse
import html

from violation_detection import (
    detect_violation,
    detect_number_plate,
    get_fine,
    get_user
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Traffic Challan System",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

/* =====================================================
   GLOBAL
===================================================== */

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.main {
    padding-top: 1rem;
}


/* =====================================================
   HEADER
===================================================== */

.main-title {
    font-size: 42px;
    font-weight: 800;
    line-height: 1.2;
    margin: 0 0 8px 0;
}

.main-subtitle {
    font-size: 17px;
    opacity: 0.72;
    margin: 0 0 18px 0;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 14px;
    border-radius: 20px;
    border: 1px solid rgba(0, 190, 110, 0.45);
    background: rgba(0, 190, 110, 0.08);
    color: #55e6a5;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 28px;
}


/* =====================================================
   SECTION HEADINGS
===================================================== */

.section-title {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 27px;
    font-weight: 750;
    line-height: 1.3;
    margin-top: 38px;
    margin-bottom: 16px;
}

.section-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
    font-size: 27px;
}

.sub-section-title {
    font-size: 17px;
    font-weight: 650;
    margin-top: 12px;
    margin-bottom: 8px;
}


/* =====================================================
   KPI CARDS
===================================================== */

.kpi-card {
    border: 1px solid rgba(120, 130, 150, 0.28);
    border-radius: 16px;
    padding: 22px 18px;
    min-height: 115px;
    text-align: center;
    background: rgba(255, 255, 255, 0.015);
}

.kpi-title {
    font-size: 13px;
    font-weight: 600;
    opacity: 0.65;
    margin-bottom: 7px;
}

.kpi-value {
    font-size: 25px;
    font-weight: 800;
}


/* =====================================================
   UPLOAD AREA
===================================================== */

[data-testid="stFileUploader"] {
    margin-top: 8px;
}

[data-testid="stFileUploader"] section {
    border: 2px dashed rgba(100, 130, 180, 0.55);
    border-radius: 16px;
    padding: 28px 20px;
    min-height: 145px;
    background: rgba(50, 80, 120, 0.05);
}

[data-testid="stFileUploader"] section > div {
    justify-content: center;
    align-items: center;
}

[data-testid="stFileUploader"] button {
    border-radius: 9px !important;
    font-weight: 650 !important;
}


/* =====================================================
   UPLOAD SUCCESS
===================================================== */

.uploaded-status {
    display: flex;
    align-items: center;
    gap: 8px;
    border: 1px solid rgba(0, 190, 110, 0.35);
    background: rgba(0, 190, 110, 0.07);
    border-radius: 11px;
    padding: 12px 16px;
    margin-top: 14px;
    margin-bottom: 22px;
    font-weight: 650;
}


/* =====================================================
   IMAGE PREVIEW
===================================================== */

.image-card {
    border: 1px solid rgba(120, 130, 150, 0.25);
    border-radius: 16px;
    padding: 12px;
    margin-top: 5px;
    margin-bottom: 18px;
}

[data-testid="stImage"] img {
    max-height: 600px;
    object-fit: contain !important;
    border-radius: 12px;
}


/* =====================================================
   GENERATE BUTTON
===================================================== */

.generate-wrapper {
    text-align: center;
    margin-top: 20px;
    margin-bottom: 28px;
}

div[data-testid="stButton"] button[kind="primary"] {
    background: #2563eb !important;
    border: 1px solid #3b82f6 !important;
    color: white !important;
    border-radius: 10px !important;
    font-size: 16px !important;
    font-weight: 750 !important;
    min-height: 48px !important;
    padding: 0 30px !important;
}

div[data-testid="stButton"] button[kind="primary"]:hover {
    background: #1d4ed8 !important;
    border-color: #60a5fa !important;
}


/* =====================================================
   RESULT CARDS
===================================================== */

.result-card {
    border: 1px solid rgba(120, 130, 150, 0.27);
    border-radius: 15px;
    padding: 20px;
    min-height: 125px;
    background: rgba(255, 255, 255, 0.015);
}

.result-label {
    font-size: 13px;
    font-weight: 650;
    opacity: 0.62;
    margin-bottom: 7px;
}

.result-value {
    font-size: 21px;
    font-weight: 750;
    line-height: 1.3;
}


/* =====================================================
   SUCCESS MESSAGE
===================================================== */

.success-card {
    border: 1px solid rgba(0, 190, 110, 0.35);
    background: rgba(0, 190, 110, 0.08);
    border-radius: 13px;
    padding: 15px 18px;
    margin-top: 10px;
    margin-bottom: 22px;
    font-weight: 650;
}


/* =====================================================
   OWNER SECTION
===================================================== */

.owner-card {
    border: 1px solid rgba(120, 130, 150, 0.27);
    border-radius: 16px;
    padding: 22px;
    margin-top: 5px;
    background: rgba(255, 255, 255, 0.015);
}

.owner-photo {
    border: 1px solid rgba(120, 130, 150, 0.25);
    border-radius: 16px;
    padding: 10px;
    text-align: center;
}

.owner-photo img {
    width: 100%;
    max-width: 260px;
    height: 260px;
    object-fit: contain !important;
    border-radius: 12px;
}


/* =====================================================
   CHALLAN SUMMARY
===================================================== */

.challan-card {
    border: 1px solid rgba(59, 130, 246, 0.35);
    background: rgba(37, 99, 235, 0.06);
    border-radius: 16px;
    padding: 22px;
    margin-top: 5px;
}


/* =====================================================
   WARNING
===================================================== */

.warning-card {
    border: 1px solid rgba(245, 158, 11, 0.4);
    background: rgba(245, 158, 11, 0.07);
    border-radius: 15px;
    padding: 20px;
    margin-top: 10px;
}

.warning-title {
    font-size: 18px;
    font-weight: 750;
    margin-bottom: 8px;
}

.warning-text {
    opacity: 0.78;
    line-height: 1.6;
}


/* =====================================================
   ACTION BUTTONS
===================================================== */

div[data-testid="stLinkButton"] a {
    border-radius: 10px !important;
    min-height: 45px !important;
    font-weight: 700 !important;
}


/* =====================================================
   FOOTER
===================================================== */

.footer {
    text-align: center;
    opacity: 0.55;
    font-size: 13px;
    margin-top: 55px;
    padding-top: 22px;
    border-top: 1px solid rgba(120, 130, 150, 0.2);
}


/* =====================================================
   SIDEBAR
===================================================== */

.sidebar-title {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 25px;
}

.sidebar-section {
    font-size: 14px;
    font-weight: 750;
    opacity: 0.65;
    margin-top: 20px;
    margin-bottom: 12px;
}

.sidebar-item {
    font-size: 15px;
    font-weight: 600;
    padding: 8px 0;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🚦 Traffic System</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-section">Navigation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">📸 Violation Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">🚗 Vehicle Verification</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">📄 Challan Generation</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-section">System Status</div>',
        unsafe_allow_html=True
    )

    st.success("● System Online")

    st.caption("AI Detection: Active")
    st.caption("Vehicle Database: Active")
    st.caption("Challan System: Active")


# =========================================================
# MAIN H1 HEADER
# =========================================================

st.markdown(
    '<h1 class="main-title">🚦 AI Traffic Challan System</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="main-subtitle">AI-powered traffic violation detection and vehicle verification</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="status-badge">● SYSTEM ONLINE</div>',
    unsafe_allow_html=True
)


# =========================================================
# KPI
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="kpi-card">'
        '<div class="kpi-title">AI Detection</div>'
        '<div class="kpi-value">Active</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div class="kpi-card">'
        '<div class="kpi-title">Vehicle Verification</div>'
        '<div class="kpi-value">Online</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        '<div class="kpi-card">'
        '<div class="kpi-title">Challan System</div>'
        '<div class="kpi-value">Ready</div>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# UPLOAD SECTION
# =========================================================

st.markdown(
    '<h2 class="section-title">'
    '<span class="section-icon">📤</span>'
    '<span>Upload Violation Evidence</span>'
    '</h2>',
    unsafe_allow_html=True
)

st.write(
    "Upload a clear image of the traffic violation. "
    "Supported formats: JPG, JPEG and PNG."
)


uploaded_file = st.file_uploader(
    "Choose a violation image",
    type=["jpg", "jpeg", "png"],
    help="Upload a clear traffic violation image."
)


# =========================================================
# AFTER IMAGE UPLOAD
# =========================================================

if uploaded_file is not None:

    # -----------------------------------------------------
    # SAVE IMAGE
    # -----------------------------------------------------

    temp_dir = os.path.join(
        os.path.dirname(__file__),
        "temp"
    )

    os.makedirs(
        temp_dir,
        exist_ok=True
    )

    image_path = os.path.join(
        temp_dir,
        uploaded_file.name
    )

    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())


    # -----------------------------------------------------
    # UPLOAD SUCCESS
    # -----------------------------------------------------

    safe_filename = html.escape(
        uploaded_file.name
    )

    st.markdown(
        '<div class="uploaded-status">'
        f'✓ <span>{safe_filename}</span> uploaded successfully'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # VIOLATION PHOTO
    # =====================================================

    st.markdown(
        '<h2 class="section-title">'
        '<span class="section-icon">📸</span>'
        '<span>Violation Photo</span>'
        '</h2>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="image-card">',
        unsafe_allow_html=True
    )

    st.image(
        uploaded_file,
        caption="Uploaded traffic violation evidence",
        width="stretch"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # GENERATE CHALLAN
    # =====================================================

    st.markdown(
        '<div class="sub-section-title">Ready to analyze?</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Click the button below to detect the violation, "
        "number plate and registered vehicle owner."
    )


    generate_challan = st.button(
        "Generate Challan",
        type="primary",
        width="content"
    )


    # =====================================================
    # AI PROCESSING
    # =====================================================

    if generate_challan:

        with st.spinner(
            "AI is analyzing the traffic violation..."
        ):

            try:

                # -----------------------------------------
                # VIOLATION
                # -----------------------------------------

                violation = detect_violation(
                    image_path
                )


                # -----------------------------------------
                # FINE
                # -----------------------------------------

                fine = get_fine(
                    violation
                )


                # -----------------------------------------
                # NUMBER PLATE
                # -----------------------------------------

                number_plate = detect_number_plate(
                    image_path
                )


                # -----------------------------------------
                # USER
                # -----------------------------------------

                user = get_user(
                    number_plate
                )


            except Exception as e:

                st.error(
                    f"Processing error: {str(e)}"
                )

                st.stop()


        # =================================================
        # SUCCESS
        # =================================================

        st.markdown(
            '<div class="success-card">'
            '✓ AI analysis completed successfully.'
            '</div>',
            unsafe_allow_html=True
        )


        # =================================================
        # VIOLATION DETAILS
        # =================================================

        st.markdown(
            '<h2 class="section-title">'
            '<span class="section-icon">🚨</span>'
            '<span>Violation Details</span>'
            '</h2>',
            unsafe_allow_html=True
        )


        col1, col2, col3 = st.columns(3)


        # -------------------------------------------------
        # VIOLATION
        # -------------------------------------------------

        with col1:

            safe_violation = html.escape(
                str(violation)
            )

            st.markdown(
                '<div class="result-card">'
                '<div class="result-label">Violation</div>'
                f'<div class="result-value">{safe_violation}</div>'
                '</div>',
                unsafe_allow_html=True
            )


        # -------------------------------------------------
        # FINE
        # -------------------------------------------------

        with col2:

            st.markdown(
                '<div class="result-card">'
                '<div class="result-label">Fine Amount</div>'
                f'<div class="result-value">₹{fine}</div>'
                '</div>',
                unsafe_allow_html=True
            )


        # -------------------------------------------------
        # NUMBER PLATE
        # -------------------------------------------------

        with col3:

            safe_plate = html.escape(
                str(number_plate)
            )

            st.markdown(
                '<div class="result-card">'
                '<div class="result-label">Number Plate</div>'
                f'<div class="result-value">{safe_plate}</div>'
                '</div>',
                unsafe_allow_html=True
            )


        # =================================================
        # REGISTERED OWNER
        # =================================================

        st.markdown(
            '<h2 class="section-title">'
            '<span class="section-icon">👤</span>'
            '<span>Registered Vehicle Owner</span>'
            '</h2>',
            unsafe_allow_html=True
        )


        if user:

            name = user[0]
            vehicle_reg = user[1]
            vehicle_type = user[2]
            vehnum = user[3]
            mobile = user[4]
            driver_photo = user[5]


            # -------------------------------------------------
            # PHOTO + OWNER DETAILS
            # -------------------------------------------------

            photo_col, details_col = st.columns(
                [1, 2]
            )


            # =================================================
            # DRIVER PHOTO
            # =================================================

            with photo_col:

                st.markdown(
                    '<div class="owner-photo">',
                    unsafe_allow_html=True
                )

                photo_path = driver_photo


                if not os.path.exists(photo_path):

                    photo_path = os.path.join(
                        os.path.dirname(__file__),
                        driver_photo
                    )


                if os.path.exists(photo_path):

                    st.image(
                        photo_path,
                        caption="Registered Driver Photo",
                        width="stretch"
                    )

                else:

                    st.info(
                        "Driver photo not available."
                    )


                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )


            # =================================================
            # OWNER DETAILS
            # =================================================

            with details_col:

                safe_name = html.escape(
                    str(name)
                )

                safe_vehicle_reg = html.escape(
                    str(vehicle_reg)
                )

                safe_vehicle_type = html.escape(
                    str(vehicle_type)
                )

                safe_vehnum = html.escape(
                    str(vehnum)
                )

                safe_mobile = html.escape(
                    str(mobile)
                )


                st.markdown(
                    '<div class="owner-card">'
                    '<div class="result-label">Owner Name</div>'
                    f'<div class="result-value">{safe_name}</div>'

                    '<div class="result-label">Vehicle Registration</div>'
                    f'<div class="result-value">{safe_vehicle_reg}</div>'

                    '<div class="result-label">Vehicle Type</div>'
                    f'<div class="result-value">{safe_vehicle_type}</div>'

                    '<div class="result-label">Vehicle Number</div>'
                    f'<div class="result-value">{safe_vehnum}</div>'

                    '<div class="result-label">Mobile Number</div>'
                    f'<div class="result-value">{safe_mobile}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )


            # =================================================
            # CHALLAN SUMMARY
            # =================================================

            st.markdown(
                '<h2 class="section-title">'
                '<span class="section-icon">📄</span>'
                '<span>Challan Summary</span>'
                '</h2>',
                unsafe_allow_html=True
            )


            st.markdown(
                '<div class="challan-card">'
                '<div class="result-label">Vehicle</div>'
                f'<div class="result-value">{safe_vehicle_reg}</div>'

                '<div class="result-label">Violation</div>'
                f'<div class="result-value">{safe_violation}</div>'

                '<div class="result-label">Fine Amount</div>'
                f'<div class="result-value">₹{fine}</div>'
                '</div>',
                unsafe_allow_html=True
            )


            # =================================================
            # WHATSAPP MESSAGE
            # =================================================

            message = f"""
TRAFFIC CHALLAN ALERT

Dear {name},

A traffic violation has been detected for your vehicle.

Vehicle Number: {vehicle_reg}
Violation: {violation}
Fine Amount: ₹{fine}

Please verify and complete the challan process.

Traffic Challan System
"""


            whatsapp_url = (
                "https://wa.me/"
                + str(mobile)
                + "?text="
                + urllib.parse.quote(message)
            )


            # =================================================
            # CHALLAN ACTIONS
            # =================================================

            st.markdown(
                '<h2 class="section-title">'
                '<span class="section-icon">📱</span>'
                '<span>Challan Actions</span>'
                '</h2>',
                unsafe_allow_html=True
            )


            action_col1, action_col2 = st.columns(2)


            with action_col1:

                st.link_button(
                    "📱 Send Challan on WhatsApp",
                    whatsapp_url,
                    width="stretch"
                )


            with action_col2:

                st.link_button(
                    "🔎 Verify on Official e-Challan",
                    "https://echallan.parivahan.gov.in/",
                    width="stretch"
                )


        # =================================================
        # VEHICLE NOT FOUND
        # =================================================

        else:

            safe_plate = html.escape(
                str(number_plate)
            )


            st.markdown(
                '<div class="warning-card">'
                '<div class="warning-title">'
                '⚠️ Vehicle Not Registered'
                '</div>'
                '<div class="warning-text">'
                'The number plate was detected successfully, '
                'but no matching vehicle owner was found '
                'in the registered database.'
                '</div>'
                '<br>'
                '<div class="result-label">'
                'Detected Number Plate'
                '</div>'
                f'<div class="result-value">{safe_plate}</div>'
                '</div>',
                unsafe_allow_html=True
            )


            # =================================================
            # VERIFY VEHICLE
            # =================================================

            st.markdown(
                '<h2 class="section-title">'
                '<span class="section-icon">🔎</span>'
                '<span>Vehicle Verification</span>'
                '</h2>',
                unsafe_allow_html=True
            )


            st.write(
                "You can verify this vehicle using the official "
                "e-Challan portal."
            )


            st.link_button(
                "🔎 Open Official e-Challan Verification",
                "https://echallan.parivahan.gov.in/",
                width="content"
            )


# =========================================================
# NO IMAGE
# =========================================================

else:

    st.info(
        "📤 Upload a traffic violation image to start AI analysis."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    '🚦 AI Traffic Challan System'
    '<br>'
    'AI-powered traffic violation detection and vehicle verification'
    '</div>',
    unsafe_allow_html=True
)