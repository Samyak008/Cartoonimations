from flask import Blueprint, jsonify, request, redirect, url_for
from ..controllers.animation_controller import create_animation

bp = Blueprint('main', __name__, url_prefix='/api')

@bp.route('/', methods=['GET'])
def root():
    """Root endpoint."""
    return redirect(url_for('main.health_check'))

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Server is running"}), 200

@bp.route('/generate', methods=['POST'])
def generate_animation():
    """Generate an educational animation from a prompt."""
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        # This will be implemented later in the animation controller
        result = create_animation(prompt)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500