"""
Command Line Interface - Main entry point for MockPilot CLI
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

from . import __version__
from .server import MockServer
from .config import ConfigLoader
from .templates import TemplateManager
from .watcher import ConfigWatcher


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog="mockpilot",
        description="🚀 MockPilot-CLI - Lightweight Terminal API Mock Server Intelligent Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mockpilot init                    # Create a sample configuration file
  mockpilot start                   # Start server with mockpilot.json
  mockpilot start -c config.yaml    # Start with custom config
  mockpilot start -t rest-api       # Start with built-in template
  mockpilot templates               # List available templates
  mockpilot record                  # Start with request recording enabled
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"MockPilot-CLI v{__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Init command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize a new mock configuration file"
    )
    init_parser.add_argument(
        "-n", "--name",
        default="mockpilot",
        help="Configuration file name (default: mockpilot)"
    )
    init_parser.add_argument(
        "-f", "--format",
        choices=["json", "yaml"],
        default="json",
        help="Configuration format (default: json)"
    )
    init_parser.add_argument(
        "-t", "--template",
        help="Use a built-in template"
    )
    
    # Start command
    start_parser = subparsers.add_parser(
        "start",
        help="Start the mock server"
    )
    start_parser.add_argument(
        "-c", "--config",
        help="Path to configuration file"
    )
    start_parser.add_argument(
        "-t", "--template",
        help="Use a built-in template instead of config file"
    )
    start_parser.add_argument(
        "-p", "--port",
        type=int,
        default=8080,
        help="Server port (default: 8080)"
    )
    start_parser.add_argument(
        "-H", "--host",
        default="localhost",
        help="Server host (default: localhost)"
    )
    start_parser.add_argument(
        "-d", "--delay",
        type=float,
        default=0,
        help="Add artificial delay to responses (seconds)"
    )
    start_parser.add_argument(
        "--no-cors",
        action="store_true",
        help="Disable CORS headers"
    )
    start_parser.add_argument(
        "-r", "--record",
        action="store_true",
        help="Enable request recording"
    )
    start_parser.add_argument(
        "-w", "--watch",
        action="store_true",
        help="Watch config file for changes and reload"
    )
    
    # Templates command
    templates_parser = subparsers.add_parser(
        "templates",
        help="List available templates"
    )
    templates_parser.add_argument(
        "-d", "--details",
        action="store_true",
        help="Show detailed template information"
    )
    
    # Record command
    record_parser = subparsers.add_parser(
        "record",
        help="Start server with recording enabled"
    )
    record_parser.add_argument(
        "-c", "--config",
        help="Path to configuration file"
    )
    record_parser.add_argument(
        "-t", "--template",
        help="Use a built-in template"
    )
    record_parser.add_argument(
        "-p", "--port",
        type=int,
        default=8080,
        help="Server port (default: 8080)"
    )
    record_parser.add_argument(
        "-o", "--output",
        default="recordings.json",
        help="Output file for recordings (default: recordings.json)"
    )
    
    # Export command
    export_parser = subparsers.add_parser(
        "export",
        help="Export recordings to file"
    )
    export_parser.add_argument(
        "-o", "--output",
        default="recordings.json",
        help="Output file (default: recordings.json)"
    )
    
    return parser


def cmd_init(args: argparse.Namespace) -> int:
    """Handle init command"""
    config_name = args.name
    config_format = args.format
    template_name = args.template
    
    # Determine file extension
    ext = ".json" if config_format == "json" else ".yaml"
    config_file = f"{config_name}{ext}"
    
    if Path(config_file).exists():
        print(f"⚠️  Configuration file '{config_file}' already exists")
        response = input("Overwrite? (y/N): ")
        if response.lower() != "y":
            print("Cancelled")
            return 0
    
    # Generate configuration
    if template_name:
        template_manager = TemplateManager()
        config = template_manager.get_template_config(template_name)
        if not config:
            print(f"❌ Template '{template_name}' not found")
            print("Run 'mockpilot templates' to see available templates")
            return 1
    else:
        config = ConfigLoader.create_sample_config()
    
    # Write configuration file
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            if config_format == "json":
                json.dump(config, f, indent=2, ensure_ascii=False)
            else:
                f.write(_dict_to_yaml(config))
        
        print(f"✅ Created configuration file: {config_file}")
        print(f"   Routes: {len(config.get('routes', []))}")
        print(f"\nStart the server with:")
        print(f"   mockpilot start -c {config_file}")
        return 0
    
    except Exception as e:
        print(f"❌ Failed to create configuration: {e}")
        return 1


def cmd_start(args: argparse.Namespace) -> int:
    """Handle start command"""
    config_path = args.config
    template_name = args.template
    
    # Load configuration
    config_loader = ConfigLoader()
    
    if template_name:
        template_manager = TemplateManager()
        config = template_manager.get_template_config(template_name)
        if not config:
            print(f"❌ Template '{template_name}' not found")
            return 1
        print(f"📋 Using template: {template_name}")
    
    elif config_path:
        try:
            config = config_loader.load(config_path)
            print(f"📄 Loaded configuration: {config_path}")
        except Exception as e:
            print(f"❌ Failed to load configuration: {e}")
            return 1
    
    else:
        # Try default config files
        for default_file in ["mockpilot.json", "mockpilot.yaml", "mockpilot.yml"]:
            if Path(default_file).exists():
                try:
                    config = config_loader.load(default_file)
                    print(f"📄 Loaded configuration: {default_file}")
                    config_path = default_file
                    break
                except Exception:
                    pass
        else:
            print("❌ No configuration file found")
            print("\nCreate one with:")
            print("   mockpilot init")
            print("\nOr use a template:")
            print("   mockpilot start -t rest-api")
            return 1
    
    # Extract server settings
    server_config = config.get("server", {})
    host = args.host or server_config.get("host", "localhost")
    port = args.port or server_config.get("port", 8080)
    
    # Extract settings
    settings = config.get("settings", {})
    cors = not args.no_cors and settings.get("cors", True)
    delay = args.delay or settings.get("delay", 0)
    recording = args.record or settings.get("recording", False)
    
    # Get routes
    routes = config_loader.get_routes()
    total_routes = sum(len(r) for r in routes.values())
    
    # Create and start server
    server = MockServer(host=host, port=port)
    server.set_routes(routes)
    server.set_cors(cors)
    server.set_delay(delay)
    server.set_recording(recording)
    
    # Print startup info
    print("\n" + "=" * 50)
    print("🚀 MockPilot Server Starting...")
    print("=" * 50)
    print(f"📡 URL: http://{host}:{port}")
    print(f"🔌 Routes: {total_routes} endpoints configured")
    print(f"🌐 CORS: {'enabled' if cors else 'disabled'}")
    if delay > 0:
        print(f"⏱️  Delay: {delay}s")
    if recording:
        print(f"🎙️  Recording: enabled")
    print("=" * 50)
    print("\nPress Ctrl+C to stop\n")
    
    # Setup file watcher if requested
    watcher = None
    if args.watch and config_path:
        def reload_config():
            try:
                new_config = config_loader.load(config_path)
                new_routes = config_loader.get_routes()
                server.set_routes(new_routes)
                print(f"\n🔄 Configuration reloaded: {config_path}")
            except Exception as e:
                print(f"\n⚠️  Failed to reload configuration: {e}")
        
        watcher = ConfigWatcher(config_path, reload_config)
        watcher.start()
        print(f"👁️  Watching for changes: {config_path}\n")
    
    try:
        server.start(blocking=True)
    except KeyboardInterrupt:
        pass
    finally:
        if watcher:
            watcher.stop()
        
        # Save recordings if enabled
        if recording:
            recordings = server.get_recordings()
            if recordings:
                output_file = "recordings.json"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(recordings, f, indent=2, ensure_ascii=False)
                print(f"\n💾 Recordings saved to: {output_file}")
    
    return 0


def cmd_templates(args: argparse.Namespace) -> int:
    """Handle templates command"""
    template_manager = TemplateManager()
    templates = template_manager.list_templates()
    
    print("\n📚 Available Templates")
    print("=" * 60)
    
    categories = TemplateManager.get_categories()
    
    for category in categories:
        print(f"\n【{category['name']}】")
        
        for template_key in category['templates']:
            template = template_manager.get_template(template_key)
            if template:
                route_count = len(template.get('routes', []))
                print(f"  • {template_key:15} - {template.get('name', '')}")
                if args.details:
                    print(f"    {template.get('description', '')}")
                    print(f"    Routes: {route_count}")
    
    print("\n" + "=" * 60)
    print("\nUse a template:")
    print("  mockpilot start -t <template-name>")
    print("\nCreate config from template:")
    print("  mockpilot init -t <template-name>")
    
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    """Handle record command"""
    args.record = True
    return cmd_start(args)


def cmd_export(args: argparse.Namespace) -> int:
    """Handle export command"""
    output_file = args.output
    
    # This would typically read from a shared recording storage
    # For now, just inform the user
    print(f"💾 Recordings would be exported to: {output_file}")
    print("Use 'mockpilot record' to capture requests")
    
    return 0


def _dict_to_yaml(data: dict, indent: int = 0) -> str:
    """Convert dictionary to simple YAML string"""
    lines = []
    prefix = "  " * indent
    
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            lines.append(_dict_to_yaml(value, indent + 1))
        elif isinstance(value, list):
            lines.append(f"{prefix}{key}:")
            for item in value:
                if isinstance(item, dict):
                    lines.append(f"{prefix}  - ")
                    for k, v in item.items():
                        if isinstance(v, (dict, list)):
                            lines.append(f"{prefix}    {k}:")
                            if isinstance(v, dict):
                                lines.append(_dict_to_yaml(v, indent + 3))
                            else:
                                for vi in v:
                                    lines.append(f"{prefix}      - {json.dumps(vi)}")
                        else:
                            lines.append(f"{prefix}    {k}: {json.dumps(v) if isinstance(v, str) else v}")
                else:
                    lines.append(f"{prefix}  - {json.dumps(item) if isinstance(item, str) else item}")
        elif isinstance(value, str):
            lines.append(f"{prefix}{key}: \"{value}\"")
        else:
            lines.append(f"{prefix}{key}: {value}")
    
    return "\n".join(lines)


def main(args: Optional[list] = None) -> int:
    """Main entry point"""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.command:
        parser.print_help()
        return 0
    
    # Route to appropriate command handler
    commands = {
        "init": cmd_init,
        "start": cmd_start,
        "templates": cmd_templates,
        "record": cmd_record,
        "export": cmd_export,
    }
    
    handler = commands.get(parsed_args.command)
    if handler:
        return handler(parsed_args)
    
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
