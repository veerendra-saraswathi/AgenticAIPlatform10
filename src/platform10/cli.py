"""
Platform10 CLI

Commands:
    platform10 verify --trace-id <id>
    platform10 export --trace-id <id>
"""

import argparse
import sys

from platform10.governance.replay.regulator_replay import RegulatorReplay
from platform10.governance.replay.pdf_exporter import ReplayPDFExporter


def verify_command(trace_id: str):
    r = RegulatorReplay()

    try:
        integrity = r.verify_integrity(trace_id)
        signature = r.verify_signature(trace_id)
        chain = r.verify_chain()

        print("\n=== Platform10 Verification Report ===")
        print(f"Trace ID      : {trace_id}")
        print(f"Integrity     : {'OK' if integrity else 'FAILED'}")
        print(f"Signature     : {'OK' if signature else 'FAILED'}")
        print(f"Chain Status  : {'OK' if chain else 'FAILED'}")

        if integrity and signature and chain:
            print("\nStatus: VERIFICATION SUCCESSFUL")
        else:
            print("\nStatus: VERIFICATION FAILED")

    except Exception as e:
        print(f"Error during verification: {e}")
        sys.exit(1)


def export_command(trace_id: str):
    try:
        exporter = ReplayPDFExporter()
        path = exporter.export(trace_id)
        print(f"\nCompliance PDF generated:")
        print(path)
    except Exception as e:
        print(f"Error generating PDF: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(prog="platform10")
    subparsers = parser.add_subparsers(dest="command")

    # verify
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--trace-id", required=True)

    # export
    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("--trace-id", required=True)

    args = parser.parse_args()

    if args.command == "verify":
        verify_command(args.trace_id)
    elif args.command == "export":
        export_command(args.trace_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
    