#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

import argparse
import time
from rich.console import Console
from rich.table import Table
from rich import box

from banner import show_banner
from ssh_brute  import ssh_brute
from ftp_brute  import ftp_brute
from http_brute import http_brute

console = Console()

# ─── Argument Parser ──────────────────────────────────────────
parser = argparse.ArgumentParser(
    prog="brutex",
    description="BruteX — SSH, FTP & HTTP Brute Force Tool",
    epilog="Example: brutex -t 192.168.1.1 --service ssh -u root -w rockyou.txt"
)

parser.add_argument("-v", "--version", action="version", version="BruteX v1.0.0")
parser.add_argument("-t", "--target",  required=True, help="Target IP or URL")
parser.add_argument("-u", "--username", help="Single username")
parser.add_argument("-U", "--userlist", help="Username list file")
parser.add_argument("-w", "--wordlist", required=True, help="Password wordlist")
parser.add_argument("--service", required=True,
                    choices=["ssh", "ftp", "http"],
                    help="Service to attack")
parser.add_argument("--port", type=int, help="Custom port (default: 22/21/80)")
parser.add_argument("--timeout", type=int, default=3, help="Timeout in seconds")

parser.add_argument("-x", "--verbose", action="store_true", help="Show detailed attack info (verbose mode)")
parser.add_argument("--user-field", default="username", help="HTTP username field name")
parser.add_argument("--pass-field", default="password", help="HTTP password field name")
parser.add_argument("--fail-text",  help="Text that appears on failed login")
parser.add_argument("--cookie",     help="Cookie header (e.g. 'session=abc123')")
parser.add_argument("--token",      help="Bearer token for Authorization header")

args = parser.parse_args()

# ─── Banner ───────────────────────────────────────────────────
show_banner()

# ─── Validate ─────────────────────────────────────────────────
if not args.username and not args.userlist:
    console.print("[red]❌ Provide -u username or -U userlist[/red]")
    exit(1)

# ─── Build username list ──────────────────────────────────────
usernames = []
if args.username:
    usernames.append(args.username)
if args.userlist:
    try:
        with open(args.userlist, "r", errors="ignore") as f:
            usernames += [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        console.print(f"[red]❌ Userlist not found: {args.userlist}[/red]")
        exit(1)

# ─── Default ports ────────────────────────────────────────────
default_ports = {"ssh": 22, "ftp": 21, "http": 80}
port = args.port or default_ports[args.service]

console.print(f"[bold red]Service  : {args.service.upper()}[/bold red]")
console.print(f"[bold red]Target   : {args.target}:{port}[/bold red]")
console.print(f"[bold red]Usernames: {len(usernames)}[/bold red]")
console.print(f"[bold red]Wordlist : {args.wordlist}[/bold red]")
console.print(f"[bold red]Verbose  : {'ON 🔍' if args.verbose else 'OFF'}[/bold red]\n")
console.print("[yellow]Starting attack...[/yellow]\n")

start = time.time()
result = None

# ─── Run attack ───────────────────────────────────────────────
for username in usernames:
    if args.service == "ssh":
        result = ssh_brute(args.target, port, username, args.wordlist, args.timeout, args.verbose)
    elif args.service == "ftp":
        result = ftp_brute(args.target, port, username, args.wordlist, args.timeout, args.verbose)
    elif args.service == "http":
        result = http_brute(
            args.target, username, args.wordlist,
            user_field=args.user_field,
            pass_field=args.pass_field,
            fail_text=args.fail_text,
            timeout=args.timeout,
            verbose=args.verbose,
            cookie=args.cookie,
            token=args.token
        )
    if result:
        break

elapsed = round(time.time() - start, 2)

# ─── Report ───────────────────────────────────────────────────
if result:
    table = Table(
        title="🔓 Credentials Found!",
        box=box.DOUBLE_EDGE,
        style="green",
        title_style="bold green",
        show_lines=True
    )
    table.add_column("Property", style="bold white", width=15)
    table.add_column("Value",    style="bold red",   width=30)

    table.add_row("Service",   args.service.upper())
    table.add_row("Target",    f"{args.target}:{port}")
    table.add_row("Username",  result["username"])
    table.add_row("Password",  result["password"])
    table.add_row("Attempts",  str(result["attempts"]))
    table.add_row("Time",      f"{elapsed}s")

    console.print()
    console.print(table)
else:
    console.print("\n[red]❌ No credentials found.[/red]\n")
