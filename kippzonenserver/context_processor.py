from markupsafe import Markup

from kippzonenserver import app


@app.context_processor
def utility_processor():
    def print_errors(errors, target=""):
        error_str = ""
        for error in errors:
            error_str += error

        return Markup("<div style='color:red; font-weight: bold;'>" + error_str + "</div>")

    return {"print_errors": print_errors}
