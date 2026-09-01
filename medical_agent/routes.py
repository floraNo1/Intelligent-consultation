"""HTTP routes for the chat and optional browser handoff."""

from flask import Blueprint, current_app, jsonify, render_template, request

from .booking import find_doctor_page
from .departments import extract_departments


bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("chat1.html")


@bp.get("/greet")
def greet():
    return jsonify(
        reply="您好，我是课程演示助手小翼。本页面不提供医疗诊断，请在需要时咨询专业医生。"
    )


@bp.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    user_input = str(payload.get("message", "")).strip()
    if not user_input:
        return jsonify(error="message is required"), 400

    try:
        import qianfan

        response = qianfan.ChatCompletion().do(
            model=current_app.config["QIANFAN_MODEL"],
            messages=[{"role": "user", "content": user_input}],
        )
        assistant_reply = response["body"]["result"]
    except Exception:
        current_app.logger.exception("Qianfan request failed")
        return jsonify(error="The configured language-model service is unavailable"), 502

    departments = extract_departments(assistant_reply)
    return jsonify(
        reply=assistant_reply,
        departments=departments,
        disease_name=departments[0] if departments else "",
    )


@bp.post("/autoregister")
def auto_register():
    if not current_app.config["BOOKING_AUTOMATION_ENABLED"]:
        return jsonify(error="Browser automation is disabled by default"), 503

    payload = request.get_json(silent=True) or {}
    try:
        current_url = find_doctor_page(
            department=str(payload.get("disease_name", "")).strip(),
            selected_date=str(payload.get("timestamp", "")).strip(),
            search_url=current_app.config["BOOKING_SEARCH_URL"],
        )
    except (TypeError, ValueError) as exc:
        return jsonify(error=str(exc)), 400
    except Exception:
        current_app.logger.exception("Browser workflow failed")
        return jsonify(error="The browser workflow could not complete"), 502

    if not current_url:
        return jsonify(error="No matching doctor page was found"), 404
    return jsonify(current_url=current_url)
