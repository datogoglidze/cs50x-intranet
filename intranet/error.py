from functools import wraps

from flask import redirect, render_template, session


def apology(message: str, code: int = 400) -> tuple[str, int]:
    def escape(s: str) -> str:
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):  # type: ignore
    @wraps(f)
    def decorated_function(*args, **kwargs):  # type: ignore
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
