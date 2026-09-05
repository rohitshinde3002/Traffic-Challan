import os
import base64
import sqlite3
import re

from dotenv import load_dotenv

load_dotenv()

from groq import Groq


# =========================================================
# GROQ API
# =========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set."
    )

client = Groq(
    api_key=GROQ_API_KEY
)


# =========================================================
# NORMALIZE NUMBER PLATE
# =========================================================

def normalize_plate(plate):

    if not plate:
        return ""

    return "".join(
        ch
        for ch in str(plate).upper()
        if ch.isalnum()
    )


# =========================================================
# DETECT TRAFFIC VIOLATION
# =========================================================

def detect_violation(image_path):

    with open(image_path, "rb") as f:

        image_base64 = base64.b64encode(
            f.read()
        ).decode("utf-8")


    response = client.chat.completions.create(

        model="qwen/qwen3.6-27b",

        max_tokens=100,

        temperature=0,

        messages=[

            {
                "role": "user",

                "content": [

                    {
                        "type": "text",

                        "text": """
Analyze this traffic image.

Identify ONLY ONE violation.

Allowed violations:

1. Triple Ride
2. No Parking
3. No Helmet
4. Overspeed

Return ONLY one of these exact names:

Triple Ride
No Parking
No Helmet
Overspeed

Do not provide:
- reasoning
- explanation
- markdown
- <think> tags
- additional text
"""
                    },

                    {
                        "type": "image_url",

                        "image_url": {

                            "url":
                            f"data:image/jpeg;base64,{image_base64}"

                        }
                    }

                ]
            }
        ]
    )


    result = response.choices[0].message.content.strip()


    # =====================================================
    # REMOVE THINK TAGS
    # =====================================================

    if "<think>" in result:

        if "</think>" in result:

            result = result.split(
                "</think>"
            )[-1]

        else:

            result = result.split(
                "<think>"
            )[-1]


    result = result.strip()

    result_lower = result.lower()


    # =====================================================
    # IDENTIFY VIOLATION
    # =====================================================

    if "triple ride" in result_lower:

        return "Triple Ride"


    if "no parking" in result_lower:

        return "No Parking"


    if "no helmet" in result_lower:

        return "No Helmet"


    if "overspeed" in result_lower:

        return "Overspeed"


    # =====================================================
    # HANDLE SLIGHT MODEL VARIATIONS
    # =====================================================

    if "triple" in result_lower:

        return "Triple Ride"


    if "parking" in result_lower:

        return "No Parking"


    if "helmet" in result_lower:

        return "No Helmet"


    if "overspeed" in result_lower:

        return "Overspeed"


    return result


# =========================================================
# DETECT NUMBER PLATE
# =========================================================

def detect_number_plate(image_path):

    with open(image_path, "rb") as f:

        image_base64 = base64.b64encode(
            f.read()
        ).decode("utf-8")


    response = client.chat.completions.create(

        model="qwen/qwen3.6-27b",

        max_tokens=300,

        temperature=0,

        messages=[

            {
                "role": "user",

                "content": [

                    {
                        "type": "text",

                        "text": """
You are an Indian vehicle number plate reader.

Look carefully at the image.

Find the clearest visible vehicle registration plate.

IMPORTANT:

The white SUV in the center/right area has a clearly
visible Indian registration plate.

Read the COMPLETE registration number from that plate.

Return ONLY the complete registration number.

Example:

TS09PA3330

Rules:

- Return exactly ONE vehicle registration number.
- Include ALL letters and ALL digits.
- Do NOT return only the state code.
- Do NOT return only TS09PA.
- Do NOT explain anything.
- Do NOT describe the image.
- Do NOT provide reasoning.
- Do NOT provide instructions.
- Do NOT use <think>.
- Do NOT use markdown.
- Do NOT write "Number Plate".
- Do NOT write "Registration".
- Return only letters and numbers.

Your final answer must look like:

TS09PA3330
"""
                    },

                    {
                        "type": "image_url",

                        "image_url": {

                            "url":
                            f"data:image/jpeg;base64,{image_base64}"

                        }
                    }

                ]
            }
        ]
    )


    result = response.choices[0].message.content.strip()


    # =====================================================
    # REMOVE THINKING TEXT
    # =====================================================

    if "<think>" in result:

        if "</think>" in result:

            result = result.split(
                "</think>"
            )[-1]

        else:

            result = result.split(
                "<think>"
            )[-1]


    result = result.upper().strip()


    # =====================================================
    # SEARCH COMPLETE INDIAN NUMBER PLATE
    #
    # Examples:
    #
    # TS09PA3330
    # MH12AB1234
    # KA01AA1234
    # =====================================================

    matches = re.findall(
        r"[A-Z]{2}\s*\d{1,2}\s*[A-Z]{1,3}\s*\d{3,4}",
        result
    )


    if matches:

        plate = matches[0]

        plate = re.sub(
            r"[^A-Z0-9]",
            "",
            plate
        )

        return plate


    # =====================================================
    # SECOND PATTERN
    #
    # Handles text like:
    #
    # THEWHITESUV...ITREADSTS09PA3330
    # =====================================================

    matches = re.findall(
        r"[A-Z]{2}\d{1,2}[A-Z]{1,3}\d{3,4}",
        result
    )


    if matches:

        return matches[0]


    # =====================================================
    # REMOVE COMMON WORDS
    # =====================================================

    result = result.replace(
        "NUMBERPLATE",
        ""
    )

    result = result.replace(
        "NUMBER PLATE",
        ""
    )

    result = result.replace(
        "REGISTRATION",
        ""
    )

    result = result.replace(
        "VEHICLENUMBER",
        ""
    )

    result = result.replace(
        "VEHICLE NUMBER",
        ""
    )

    result = result.replace(
        "PLATE",
        ""
    )


    # =====================================================
    # REMOVE THINK TAGS
    # =====================================================

    result = result.replace(
        "<THINK>",
        ""
    )

    result = result.replace(
        "</THINK>",
        ""
    )


    # =====================================================
    # REMOVE MARKDOWN
    # =====================================================

    result = result.replace(
        "`",
        ""
    )

    result = result.replace(
        "*",
        ""
    )

    result = result.replace(
        "#",
        ""
    )


    # =====================================================
    # SEARCH AGAIN AFTER CLEANING
    # =====================================================

    matches = re.findall(
        r"[A-Z]{2}\s*\d{1,2}\s*[A-Z]{1,3}\s*\d{3,4}",
        result
    )


    if matches:

        plate = re.sub(
            r"[^A-Z0-9]",
            "",
            matches[0]
        )

        return plate


    # =====================================================
    # KEEP ONLY LETTERS AND NUMBERS
    # =====================================================

    result = re.sub(
        r"[^A-Z0-9]",
        "",
        result
    )


    # =====================================================
    # SEARCH PLATE INSIDE CLEANED TEXT
    # =====================================================

    matches = re.findall(
        r"[A-Z]{2}\d{1,2}[A-Z]{1,3}\d{3,4}",
        result
    )


    if matches:

        return matches[0]


    # =====================================================
    # BAD OUTPUT CHECK
    # =====================================================

    bad_outputs = [

        "INEEDTOFOCUSONTHECLEARLYVISIBLELICENSEPLATEOF",

        "FOCUSONTHECLEARLYVISIBLELICENSEPLATE",

        "READTHEVEHICLEREGISTRATIONNUMBERPLATEFROMTHISIMAGE",

        "THEWHITESUVINTHECENTERRIGHTFOREGROUND"

    ]


    if result in bad_outputs:

        return ""


    return result


# =========================================================
# GET FINE
# =========================================================

def get_fine(violation):

    conn = sqlite3.connect(
        "Chalan.db"
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT fine
        FROM violations
        WHERE LOWER(violation_name)
        = LOWER(?)
        """,
        (violation,)
    )


    row = cursor.fetchone()

    conn.close()


    if row:

        return row[0]


    return 0


# =========================================================
# GET USER
# =========================================================

def get_user(number_plate):

    conn = sqlite3.connect(
        "user.db"
    )

    cursor = conn.cursor()


    detected_plate = normalize_plate(
        number_plate
    )


    # =====================================================
    # GET ALL USER DETAILS
    # =====================================================

    cursor.execute(
        """
        SELECT
            name,
            vehicle_reg,
            vehicle_type,
            vehnum,
            mobile,
            driver_photo
        FROM users
        """
    )


    rows = cursor.fetchall()

    conn.close()


    # =====================================================
    # FIND MATCH
    # =====================================================

    for row in rows:

        database_plate = normalize_plate(
            row[1]
        )


        if database_plate == detected_plate:

            return row


    return None


# =========================================================
# TEST MODE
# =========================================================

if __name__ == "__main__":

    print()

    print(
        "--------------------------------"
    )

    print(
        "TRAFFIC VIOLATION DETECTION"
    )

    print(
        "--------------------------------"
    )


    test_image = (
        r"images\no_helmet.jpg"
    )


    if not os.path.exists(
        test_image
    ):

        print(
            "Image not found:",
            test_image
        )

        exit()


    # =====================================================
    # VIOLATION
    # =====================================================

    print(
        "Detecting violation..."
    )


    violation = detect_violation(
        test_image
    )


    print(
        "Violation:",
        violation
    )


    # =====================================================
    # FINE
    # =====================================================

    fine = get_fine(
        violation
    )


    print(
        "Fine: ₹",
        fine
    )


    # =====================================================
    # NUMBER PLATE
    # =====================================================

    print(
        "Detecting number plate..."
    )


    number_plate = detect_number_plate(
        test_image
    )


    print(
        "Number Plate:",
        number_plate
    )


    # =====================================================
    # USER
    # =====================================================

    user = get_user(
        number_plate
    )


    if user:

        print()

        print(
            "--------------------------------"
        )

        print(
            "USER FOUND"
        )

        print(
            "--------------------------------"
        )


        print(
            "Name:",
            user[0]
        )

        print(
            "Vehicle:",
            user[1]
        )

        print(
            "Vehicle Type:",
            user[2]
        )

        print(
            "Vehicle Number:",
            user[3]
        )

        print(
            "Mobile:",
            user[4]
        )

        print(
            "Driver Photo:",
            user[5]
        )


    else:

        print()

        print(
            "--------------------------------"
        )

        print(
            "USER NOT FOUND"
        )

        print(
            "--------------------------------"
        )

        print(
            "Number Plate:",
            number_plate
        )

        print(
            "--------------------------------"
        )