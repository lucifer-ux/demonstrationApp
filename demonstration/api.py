import os
import re

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

# Load environment variables at module level
load_dotenv()

app = Flask(__name__)

# Get the directory containing this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(CURRENT_DIR, "public")


SAFE_PAGE_NAME = re.compile(r"^[a-zA-Z0-9_-]+$")


def _serve_html_page(page_name: str):
    """Serve a page from public directory as <page_name>.html."""
    if not SAFE_PAGE_NAME.fullmatch(page_name):
        return jsonify({"error": "Invalid page name"}), 400

    html_file = f"{page_name}.html"
    html_path = os.path.join(PUBLIC_DIR, html_file)
    if not os.path.exists(html_path):
        return jsonify({"error": "Page not found", "page": page_name}), 404

    return send_from_directory(PUBLIC_DIR, html_file)


@app.route("/otp", methods=["GET"])
def otp_screen():
    """Serve the OTP verification screen."""
    return _serve_html_page("otp_screen")


@app.route("/payment-success", methods=["GET"])
def payment_success():
    """Serve the payment success screen."""
    return _serve_html_page("payment_success")


@app.route("/otp-verifying", methods=["GET"])
def otp_verifying():
    """OTP verification loader screen."""
    return _serve_html_page("otp_verifying")


@app.route("/otp-success", methods=["GET"])
def otp_success():
    """OTP success transition screen."""
    return _serve_html_page("otp_success_transition")


@app.route("/eligibility-check", methods=["GET"])
def eligibility_check():
    """Eligibility check form screen."""
    return _serve_html_page("eligibility_check")


@app.route("/details-verifying", methods=["GET"])
def details_verifying():
    """Details verification loader screen."""
    return _serve_html_page("details_verifying")


@app.route("/about-you", methods=["GET"])
def about_you():
    """Additional details form screen."""
    return _serve_html_page("about_you")


@app.route("/camera-verification", methods=["GET"])
def camera_verification():
    """Face verification screen with camera access."""
    return _serve_html_page("camera_verification")


@app.route("/offer", methods=["GET"])
def offer_screen():
    """Offer details and order confirmation screen."""
    return _serve_html_page("offer_screen")


@app.route("/fetching-lenders", methods=["GET"])
def fetching_lenders():
    """Lender fetching loader screen."""
    return _serve_html_page("fetching_lenders")


@app.route("/offer-list", methods=["GET"])
def offer_list():
    """Offer list screen with lender cards."""
    return _serve_html_page("offer_list")


@app.route("/processing-application", methods=["GET"])
def processing_application():
    """Processing application loader screen."""
    return _serve_html_page("processing_application")


@app.route("/approval-success", methods=["GET"])
def approval_success():
    """Credit approval success screen."""
    return _serve_html_page("approval_success")


@app.route("/loading-best-plans", methods=["GET"])
def loading_best_plans():
    """Best plans loader screen."""
    return _serve_html_page("loading_best_plans")


@app.route("/choose-plan", methods=["GET"])
def choose_plan():
    """Choose plan screen."""
    return _serve_html_page("choose_plan")


@app.route("/plan-summary", methods=["GET"])
def plan_summary():
    """Selected plan summary screen."""
    return _serve_html_page("plan_summary")


@app.route("/initiating-mandate", methods=["GET"])
def initiating_mandate():
    """Mandate initiation loader screen."""
    return _serve_html_page("initiating_mandate")


@app.route("/mandate-setup", methods=["GET"])
def mandate_setup():
    """Mandate setup and agreement screen."""
    return _serve_html_page("mandate_setup")


@app.route("/setting-up-mandate", methods=["GET"])
def setting_up_mandate():
    """Mandate setup processing loader screen."""
    return _serve_html_page("setting_up_mandate")


@app.route("/mandate-complete", methods=["GET"])
def mandate_complete():
    """Mandate setup completion screen."""
    return _serve_html_page("mandate_complete")


@app.route("/preparing-agreement", methods=["GET"])
def preparing_agreement():
    """Agreement preparation loader screen."""
    return _serve_html_page("preparing_agreement")


@app.route("/loan-agreement", methods=["GET"])
def loan_agreement():
    """Loan agreement review and consent screen."""
    return _serve_html_page("loan_agreement")


@app.route("/finalising-emi", methods=["GET"])
def finalising_emi():
    """Final EMI processing loader screen."""
    return _serve_html_page("finalising_emi")


@app.route("/all-set", methods=["GET"])
def all_set():
    """Final loan completion summary screen."""
    return _serve_html_page("all_set")


@app.route("/", methods=["GET"])
def index():
    """Serve default entry point."""
    return _serve_html_page("otp_screen")


@app.route("/pages/<page_name>", methods=["GET"])
def serve_page(page_name: str):
    """Serve any HTML page by name, e.g. /pages/otp_screen -> otp_screen.html."""
    return _serve_html_page(page_name)


@app.route("/public/<path:filename>", methods=["GET"])
def serve_public_asset(filename: str):
    """Serve static assets from the demonstration public directory."""
    return send_from_directory(PUBLIC_DIR, filename)


@app.route("/validate-otp", methods=["POST"])
def validate_otp():
    """Validate the OTP (mock validation)."""
    data = request.get_json() or {}
    otp = data.get("otp", "")

    # Validation: OTP should be numeric and 6 digits
    if not otp:
        return jsonify({"valid": False, "error": "OTP is required"}), 400

    if not otp.isdigit():
        return jsonify({"valid": False, "error": "OTP must contain only numbers"}), 400

    if len(otp) != 6:
        return jsonify({"valid": False, "error": "OTP must be 6 digits"}), 400

    # Mock successful validation
    return jsonify({"valid": True, "message": "OTP verified successfully"})


@app.route("/resend-otp", methods=["POST"])
def resend_otp():
    """Mock resend OTP endpoint."""
    return jsonify({"success": True, "message": "OTP resent successfully"})


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "usecase": "demonstration"})


@app.route("/extract-pan", methods=["POST"])
def extract_pan():
    """Extract PAN card details from uploaded image using Grid AI LLM.

    Request body:
        {
            "image": "base64-encoded-image",
            "upload_type": "base64"
        }

    Returns:
        {
            "success": true/false,
            "data": {
                "pan": "ABCDE1234F",
                "name": "Full Name",
                "gender": "Male/Female",
                "dob": "DD/MM/YYYY"
            },
            "error": null or error message
        }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided", "data": {}}), 400

        base64_image = data.get("image")
        if not base64_image:
            return jsonify({"success": False, "error": "No image provided", "data": {}}), 400

        # Get Grid AI configuration from environment
        grid_base_url = os.getenv("LITELLM_BASE_URL", "https://grid.ai.juspay.net")
        grid_api_key = os.getenv("GRID_AUTH_TOKEN")
        grid_model = os.getenv("GRID_MODEL", "kimi-latest")

        if not grid_api_key:
            return jsonify({"success": False, "error": "Grid API not configured", "data": {}}), 500

        # Prepare OCR prompt for PAN card extraction
        ocr_prompt = """You are an OCR assistant specialized in extracting information from Indian PAN cards.

Your task is to analyze the provided image of a PAN card and extract the following fields:
- PAN Number (key: "pan"): 10-character alphanumeric in format ABCDE1234F
- Full Name (key: "name"): Name as printed on the card
- Gender (key: "gender"): Extract if visible, typically "Male" or "Female"
- Date of Birth (key: "dob"): Extract in DD/MM/YYYY format if present

Return ONLY a valid JSON object in this exact format:
{
  "pan": "ABCDE1234F",
  "name": "John Doe",
  "gender": "Male",
  "dob": "01/01/1990"
}

If a field is not visible or unclear, use null as the value.
Example: {"pan": "ABCDE1234F", "name": null, "gender": null, "dob": null}

Do not include any markdown formatting, explanations, or additional text."""

        # Call Grid AI LLM API with image using /v1/chat/completions endpoint
        url = f"{grid_base_url}/v1/chat/completions"
        headers = {"Authorization": f"Bearer {grid_api_key}", "Content-Type": "application/json"}

        # Build the message content with image (OpenAI vision format)
        payload = {
            "model": grid_model,  # Use model from GRID_MODEL env var
            "messages": [
                {
                    "role": "system",
                    "content": "You are an OCR assistant specialized in extracting information from documents. Output only valid JSON.",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": ocr_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                },
            ],
            "max_tokens": 1024,
            "temperature": 0.2,
        }

        response = requests.post(url, headers=headers, json=payload, timeout=60)

        if response.status_code != 200:
            return jsonify({"success": False, "error": f"Grid API error: {response.status_code}", "data": {}}), 500

        response_data = response.json()
        llm_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")

        # Parse JSON from LLM response
        import json

        try:
            # Try to parse the response as JSON
            extracted_data = json.loads(llm_response.strip())
        except json.JSONDecodeError:
            # If not valid JSON, try to extract JSON from the text
            import re as regex

            json_match = regex.search(r"\{[\s\S]*\}", llm_response)
            if json_match:
                try:
                    extracted_data = json.loads(json_match.group())
                except json.JSONDecodeError:
                    extracted_data = {"pan": None, "name": None, "gender": None, "dob": None}
            else:
                extracted_data = {"pan": None, "name": None, "gender": None, "dob": None}

        # Validate PAN format if extracted
        pan_value = extracted_data.get("pan")
        if pan_value:
            pan_pattern = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")
            if not pan_pattern.match(str(pan_value).upper()):
                extracted_data["pan"] = None

        return jsonify(
            {
                "success": True,
                "data": {
                    "pan": extracted_data.get("pan"),
                    "name": extracted_data.get("name"),
                    "gender": extracted_data.get("gender"),
                    "dob": extracted_data.get("dob"),
                },
                "error": None,
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e), "data": {}}), 500
