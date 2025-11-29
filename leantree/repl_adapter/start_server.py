"""CLI script to start the Lean server."""

import argparse
import os
import signal
import sys
from pathlib import Path

from leantree.repl_adapter.server import start_server
from leantree.repl_adapter.process_pool import LeanProcessPool


def main():
    """CLI entry point for the Lean server."""
    parser = argparse.ArgumentParser(description="Start a Lean server")
    parser.add_argument(
        "--address",
        type=str,
        default="localhost",
        help="Server address (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (default: 8000)"
    )
    parser.add_argument(
        "--repl-exe",
        type=str,
        default=None,
        help="Path to Lean REPL executable (default: from LEAN_REPL_EXE env or ../lean-repl/.lake/build/bin/repl)"
    )
    parser.add_argument(
        "--project-path",
        type=str,
        default=None,
        help="Path to Lean project (default: from LEAN_PROJECT_PATH env or ./leantree_project)"
    )
    parser.add_argument(
        "--max-processes",
        type=int,
        default=8,
        help="Maximum number of parallel processes (default: 2)"
    )

    args = parser.parse_args()

    # Determine repl_exe path
    if args.repl_exe:
        repl_exe = Path(args.repl_exe)
    elif os.getenv("LEAN_REPL_EXE"):
        repl_exe = Path(os.getenv("LEAN_REPL_EXE"))
    else:
        # Default relative to current working directory
        repl_exe = Path("../lean-repl/.lake/build/bin/repl").resolve()
    
    if not repl_exe.exists():
        print(f"Error: REPL executable not found at {repl_exe}", file=sys.stderr)
        print("Please specify --repl-exe or set LEAN_REPL_EXE environment variable", file=sys.stderr)
        sys.exit(1)

    # Determine project_path
    if args.project_path:
        project_path = Path(args.project_path)
    elif os.getenv("LEAN_PROJECT_PATH"):
        project_path = Path(os.getenv("LEAN_PROJECT_PATH"))
    else:
        # Default relative to current working directory
        project_path = Path("leantree_project").resolve()
    
    if not project_path.exists():
        print(f"Error: Project path not found at {project_path}", file=sys.stderr)
        print("Please specify --project-path or set LEAN_PROJECT_PATH environment variable", file=sys.stderr)
        sys.exit(1)

    # Create process pool
    pool = LeanProcessPool(
        repl_exe=repl_exe,
        project_path=project_path,
        max_processes=args.max_processes,
    )

    # Start server
    server = start_server(pool, address=args.address, port=args.port)
    print(f"Server started on http://{args.address}:{args.port}")
    print("Press Ctrl+C to stop")

    # Handle shutdown gracefully
    def signal_handler(sig, frame):
        print("\nShutting down server...")
        server.stop()
        pool.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()

