from . import translation_bp


@translation_bp.route("/translate", methods=["GET"])
def translate():
    return "test", 200
