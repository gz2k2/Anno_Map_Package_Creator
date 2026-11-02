"""Open configured external links in the default browser."""
import webbrowser

def open_external_url(url: str) -> None:
    """Open a trusted application-owned URL in the system browser."""
    webbrowser.open_new_tab(url)
