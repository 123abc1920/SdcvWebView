from . import dicts_bp


@dicts_bp.route("/dicts", methods=["GET"])
def list_dicts():
    pass
