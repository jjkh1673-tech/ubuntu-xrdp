#!/usr/bin/env python3
"""
Hermes AI Desktop - Built-in AI Agent for Ubuntu XRDP
========================================================
A beautiful, Claude Desktop-like AI chat application with:
- Modern GUI with sidebar and chat interface
- First-run API key setup wizard
- Multiple model support
- Tool integration (file operations)
- Beautiful dark theme
- Desktop integration

Requirements: pip install customtkinter openai Pillow
"""

import sys
import os
import json
import threading
import time
from datetime import datetime

# ============================================================================
# IMPORTS
# ============================================================================

try:
    import customtkinter as ctk
    from customtkinter import filedialog
except ImportError:
    print("=" * 60)
    print("  ERROR: customtkinter is required!")
    print("  Install with: pip install customtkinter openai Pillow")
    print("=" * 60)
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("=" * 60)
    print("  ERROR: openai library is required!")
    print("  Install with: pip install openai")
    print("=" * 60)
    sys.exit(1)

from PIL import Image, ImageDraw, ImageTk

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_URL = "https://freemodelsforall.hopto.org/v1"
CONFIG_DIR = os.path.expanduser("~/.hermes")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, "credentials.json")
CHATS_DIR = os.path.join(CONFIG_DIR, "chats")
API_GUIDE_URL = "https://freemodelsforall.hopto.org/"

# Ensure directories exist
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(CHATS_DIR, exist_ok=True)

# ============================================================================
# COLORS & THEMING
# ============================================================================

class Colors:
    """Application color scheme - Dark theme like Claude Desktop"""
    BG_DARK = "#1a1a2e"
    BG_SIDEBAR = "#16213e"
    BG_CHAT = "#0f0f23"
    BG_INPUT = "#252540"
    ACCENT = "#667eea"
    ACCENT_HOVER = "#764ba2"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#a0a0b0"
    TEXT_MUTED = "#606070"
    USER_MSG = "#2d3748"
    AI_MSG = "#1e293b"
    TOOL_MSG = "#3d2d5c"
    ERROR = "#ff6b6b"
    SUCCESS = "#51cf66"
    BORDER = "#303050"

# ============================================================================
# FALLBACK MODELS (from original code)
# ============================================================================

FALLBACK_MODELS = [
    {"name": "Claude Fable 5", "id": "obsidianx/custom/claude-fable-5"},
    {"name": "Gpt 5 4", "id": "obsidianx/openai/gpt-5-4"},
    {"name": "Gpt 5 5", "id": "obsidianx/openai/gpt-5-5"},
    {"name": "Gpt 5 6 Luna", "id": "obsidianx/openai/gpt-5-6-luna"},
    {"name": "Gpt 5 6 Terra", "id": "obsidianx/openai/gpt-5-6-terra"},
    {"name": "Gpt 5.6", "id": "obsidianx/openai/gpt-5.6"},
    {"name": "Gpt 5.6 Sol", "id": "Obsidianx/openai/gpt 5.6 Sol"},
    {"name": "Claude Opus 4 7", "id": "obsidianx/custom/claude-opus-4-7"},
    {"name": "Claude Opus 4 8", "id": "obsidianx/custom/claude-opus-4-8"},
    {"name": "Claude Opus 5", "id": "obsidianx/custom/claude-opus-5"},
    {"name": "Claude Sonnet 5", "id": "obsidianx/custom/claude-sonnet-5"},
    {"name": "DeepSeek V4 Flash 0731", "id": "obsidianx/openai/DeepSeek-V4-Flash-0731"},
    {"name": "Deepseek V4 Flash Free", "id": "obsidianx/openai/deepseek-v4-flash-free"},
    {"name": "Deepseek V4 Pro", "id": "obsidianx/openai/deepseek-v4-pro"},
    {"name": "Gemini 3 1 Pro", "id": "obsidianx/custom/gemini-3-1-pro"},
    {"name": "Gemini 3 Flash", "id": "obsidianx/custom/gemini-3-flash"},
    {"name": "Gemini 3 Pro", "id": "obsidianx/custom/gemini-3-pro"},
    {"name": "Glm 5 2", "id": "obsidianx/custom/glm-5-2"},
    {"name": "Grok 4 5", "id": "obsidianx/custom/grok-4-5"},
    {"name": "Laguna S 2.1 Free", "id": "obsidianx/custom/laguna-s-2.1-free"},
    {"name": "Ling 3.0 Flash Free", "id": "obsidianx/custom/ling-3.0-flash-free"},
    {"name": "Longcat 2.0 Free", "id": "obsidianx/custom/longcat-2.0-free"},
    {"name": "Mimo V2.5 Free", "id": "obsidianx/custom/mimo-v2.5-free"},
    {"name": "Nemotron 3 Ultra Free", "id": "obsidianx/custom/nemotron-3-ultra-free"},
    {"name": "North Mini Code Free", "id": "obsidianx/custom/north-mini-code-free"},
]

# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or overwrite a file with the specified text content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "The path of the file to create or overwrite."},
                    "content": {"type": "string", "description": "The content string to write into the file."}
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Delete a file from the local file system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "The file path to delete."}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file from the local file system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "The path of the file to read."}
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List the files and folders in a directory path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "The directory path to inspect.", "default": "."}
                }
            }
        }
    }
]

# ============================================================================
# TOOL EXECUTION
# ============================================================================

def execute_tool(name, arguments_str):
    """Execute a tool function and return result."""
    try:
        args = json.loads(arguments_str) if arguments_str.strip() else {}
    except Exception as e:
        return f"Error: Failed to parse arguments JSON: {e}"

    if name == "write_file":
        filepath = args.get("filepath")
        content = args.get("content", "")
        if not filepath:
            return "Error: Missing required argument 'filepath'."
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Success: File written to '{filepath}' ({len(content)} chars)."
        except Exception as e:
            return f"Error writing file: {e}"

    elif name == "delete_file":
        filepath = args.get("filepath")
        if not filepath:
            return "Error: Missing required argument 'filepath'."
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return f"Success: File '{filepath}' deleted."
            else:
                return f"Error: File '{filepath}' not found."
        except Exception as e:
            return f"Error deleting file: {e}"

    elif name == "read_file":
        filepath = args.get("filepath")
        if not filepath:
            return "Error: Missing required argument 'filepath'."
        try:
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                return content[:10000] if len(content) > 10000 else content  # Limit output
            else:
                return f"Error: File '{filepath}' not found."
        except Exception as e:
            return f"Error reading file: {e}"

    elif name == "list_directory":
        directory = args.get("directory", ".")
        try:
            if os.path.exists(directory) and os.path.isdir(directory):
                files = os.listdir(directory)
                result = []
                for f in files:
                    full_path = os.path.join(directory, f)
                    item_type = "📁" if os.path.isdir(full_path) else "📄"
                    result.append(f"{item_type} {f}")
                return "\n".join(result)
            else:
                return f"Error: Directory '{directory}' not found."
        except Exception as e:
            return f"Error listing directory: {e}"

    else:
        return f"Error: Unknown function '{name}'."

# ============================================================================
# SPINNER CLASS (for async operations)
# ============================================================================

class Spinner:
    """Animated spinner for loading states."""
    def __init__(self, label="Loading..."):
        self.label = label
        self.chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.running = False
        self.thread = None

    def start(self, text_widget, row):
        self.running = True
        self.text_widget = text_widget
        self.row = row
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def _spin(self):
        idx = 0
        while self.running:
            symbol = self.chars[idx % len(self.chars)]
            self.text_widget.configure(state="normal")
            self.text_widget.insert(f"{self.row}.0", f"{symbol} {self.label}")
            self.text_widget.configure(state="disabled")
            idx += 1
            time.sleep(0.08)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.5)

# ============================================================================
# API KEY MANAGEMENT
# ============================================================================

def load_api_key():
    """Load API key from environment, file, or return None."""
    # 1. Environment variable
    token = os.environ.get("API_KEY") or os.environ.get("OPENAI_API_KEY")
    if token:
        return token

    # 2. Credentials file
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, "r") as f:
                creds = json.load(f)
                return creds.get("api_key")
        except:
            pass

    return None

def save_api_key(key):
    """Save API key securely."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump({"api_key": key, "saved_at": datetime.now().isoformat()}, f)
    os.chmod(CREDENTIALS_FILE, 0o600)

def clear_api_key():
    """Remove saved API key."""
    if os.path.exists(CREDENTIALS_FILE):
        os.remove(CREDENTIALS_FILE)

# ============================================================================
# CLIENT SETUP
# ============================================================================

def create_client(api_key):
    """Create OpenAI client with custom base URL."""
    return OpenAI(
        base_url=BASE_URL,
        api_key=api_key,
    )

def fetch_models(client):
    """Fetch available models from gateway."""
    try:
        response = client.models.list()
        models = [{"name": m.id, "id": m.id} for m in response.data]
        return sorted(models, key=lambda x: x["name"])
    except Exception as e:
        error_str = str(e).lower()
        if "401" in error_str or "unauthorized" in error_str:
            raise PermissionError("Invalid API key")
        raise e

# ============================================================================
# MESSAGES FORMATTER
# ============================================================================

def format_message(role, content, tool_calls=None, tool_results=None):
    """Format message for API."""
    msg = {"role": role, "content": content}
    if tool_calls:
        msg["tool_calls"] = tool_calls
    if role == "tool" and tool_results:
        msg["tool_call_id"] = tool_results.get("tool_call_id")
        msg["name"] = tool_results.get("name")
        msg["content"] = tool_results.get("content")
    return msg

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class HermesDesktopApp:
    """
    Hermes AI Desktop - Main Application Class
    Beautiful GUI with sidebar, chat, and model selection.
    """

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Hermes AI Desktop")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        self.root.iconname("Hermes AI")

        # State
        self.api_key = None
        self.client = None
        self.models = []
        self.selected_model = None
        self.messages = []
        self.chats = []
        self.current_chat_id = None
        self.support_tools = True

        # Setup theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        # Create custom theme colors
        self._apply_custom_theme()

        # Build UI
        self._build_ui()

        # Check for existing API key
        self.api_key = load_api_key()
        if self.api_key:
            self._initialize_client()
        else:
            self._show_welcome_screen()

    def _apply_custom_theme(self):
        """Apply custom dark theme colors."""
        # We'll use this for styling throughout
        pass

    def _build_ui(self):
        """Build the main application UI."""
        # Main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True)

        # ===== SIDEBAR =====
        self.sidebar = ctk.CTkFrame(
            self.main_container,
            width=280,
            fg_color=Colors.BG_SIDEBAR,
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Sidebar header
        self.sidebar_header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_header.pack(fill="x", padx=20, pady=(20, 10))

        # Logo/title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_header,
            text="✨ Hermes AI",
            font=ctk.CTkFont(size=20, weight="bold", family="Segoe UI")
        )
        self.logo_label.pack()

        self.subtitle_label = ctk.CTkLabel(
            self.sidebar_header,
            text="Desktop Assistant",
            font=ctk.CTkFont(size=11, family="Segoe UI"),
            text_color=Colors.TEXT_SECONDARY
        )
        self.subtitle_label.pack()

        # Model selection section
        self.model_section = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.model_section.pack(fill="x", padx=15, pady=10)

        self.model_label = ctk.CTkLabel(
            self.model_section,
            text="MODEL",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=Colors.TEXT_MUTED
        )
        self.model_label.pack(anchor="w")

        self.model_var = ctk.StringVar()
        self.model_combobox = ctk.CTkComboBox(
            self.model_section,
            values=[],
            variable=self.model_var,
            width=240,
            height=38,
            font=ctk.CTkFont(size=12),
            corner_radius=8,
            state="disabled"
        )
        self.model_combobox.pack(fill="x", pady=(5, 0))
        self.model_combobox.set("Loading models...")

        # New chat button
        self.new_chat_btn = ctk.CTkButton(
            self.sidebar,
            text="➕ New Chat",
            command=self._new_chat,
            width=240,
            height=38,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER
        )
        self.new_chat_btn.pack(pady=10)

        # Chat history section
        self.history_section = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.history_section.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.history_label = ctk.CTkLabel(
            self.history_section,
            text="CHAT HISTORY",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=Colors.TEXT_MUTED
        )
        self.history_label.pack(anchor="w", pady=(0, 5))

        # Scrollable chat history
        self.history_frame = ctk.CTkScrollableFrame(
            self.history_section,
            fg_color="transparent",
            width=230
        )
        self.history_frame.pack(fill="both", expand=True)

        # Sidebar footer
        self.sidebar_footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_footer.pack(fill="x", padx=15, pady=15)

        self.settings_btn = ctk.CTkButton(
            self.sidebar_footer,
            text="⚙️ Settings",
            command=self._show_settings,
            width=240,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="#253550",
            text_color=Colors.TEXT_SECONDARY
        )
        self.settings_btn.pack()

        self.api_status_label = ctk.CTkLabel(
            self.sidebar_footer,
            text="🔑 API: Not configured",
            font=ctk.CTkFont(size=10),
            text_color=Colors.TEXT_MUTED
        )
        self.api_status_label.pack(pady=(5, 0))

        # ===== MAIN CHAT AREA =====
        self.chat_area = ctk.CTkFrame(
            self.main_container,
            fg_color=Colors.BG_CHAT,
            corner_radius=0
        )
        self.chat_area.pack(side="right", fill="both", expand=True)

        # Chat header
        self.chat_header = ctk.CTkFrame(self.chat_area, fg_color="transparent")
        self.chat_header.pack(fill="x", padx=20, pady=(20, 10))

        self.chat_title = ctk.CTkLabel(
            self.chat_header,
            text="💬 Chat",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.chat_title.pack()

        # Chat messages area (scrollable)
        self.messages_frame = ctk.CTkScrollableFrame(
            self.chat_area,
            fg_color="transparent",
            width=800
        )
        self.messages_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Welcome message in chat area
        self.welcome_label = ctk.CTkLabel(
            self.messages_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color=Colors.TEXT_SECONDARY,
            justify="center"
        )
        self.welcome_label.pack(pady=50)

        # Input area
        self.input_frame = ctk.CTkFrame(
            self.chat_area,
            fg_color=Colors.BG_INPUT,
            corner_radius=12
        )
        self.input_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.input_field = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type your message... (Enter to send)",
            placeholder_text_color=Colors.TEXT_MUTED,
            font=ctk.CTkFont(size=14),
            height=48,
            corner_radius=12,
            fg_color=Colors.BG_DARK
        )
        self.input_field.pack(side="left", fill="x", padx=(15, 10), pady=10)
        self.input_field.bind("<Return>", lambda e: self._send_message())

        self.send_btn = ctk.CTkButton(
            self.input_frame,
            text="Send",
            command=self._send_message,
            width=100,
            height=48,
            corner_radius=12,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER
        )
        self.send_btn.pack(side="right", padx=(0, 15), pady=10)

        # Status bar at bottom
        self.status_bar = ctk.CTkFrame(self.chat_area, fg_color="transparent")
        self.status_bar.pack(fill="x", side="bottom", padx=20, pady=(0, 10))

        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color=Colors.TEXT_MUTED
        )
        self.status_label.pack(anchor="w")

    def _show_welcome_screen(self):
        """Show welcome/setup screen on first launch."""
        self.welcome_label.configure(
            text="",
            font=ctk.CTkFont(size=16, weight="bold")
        )

        # Welcome frame
        self.welcome_frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color=Colors.BG_DARK,
            corner_radius=12,
            width=600
        )
        self.welcome_frame.pack(pady=30, padx=20, fill="x")

        # Welcome content
        welcome_text = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ✨ Welcome to Hermes AI Desktop                        ║
║                                                           ║
║   Your intelligent AI assistant with powerful capabilities║
║                                                           ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║   To get started, you need an API key:                    ║
║                                                           ║
║   🔑 Get your free API key from:                          ║
║   https://freemodelsforall.hopto.org/                    ║
║                                                           ║
║   Steps:                                                  ║
║   1. Visit the website above                              ║
║   2. Sign up / Log in                                     ║
║   3. Copy your API key                                    ║
║   4. Paste it below                                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """

        self.welcome_text = ctk.CTkLabel(
            self.welcome_frame,
            text=welcome_text,
            font=ctk.CTkFont(size=12),
            text_color=Colors.TEXT_PRIMARY,
            justify="left"
        )
        self.welcome_text.pack(padx=30, pady=20)

        # API Key input
        self.api_key_frame = ctk.CTkFrame(
            self.welcome_frame,
            fg_color="transparent"
        )
        self.api_key_frame.pack(pady=15)

        self.api_key_label = ctk.CTkLabel(
            self.api_key_frame,
            text="Enter your API Key:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.api_key_label.pack(anchor="w", padx=30)

        self.api_key_entry = ctk.CTkEntry(
            self.api_key_frame,
            placeholder_text="Paste your API key here...",
            placeholder_text_color=Colors.TEXT_MUTED,
            font=ctk.CTkFont(size=13),
            height=44,
            corner_radius=8,
            show="*",
            width=540
        )
        self.api_key_entry.pack(padx=30, pady=(5, 15))

        self.api_hint = ctk.CTkLabel(
            self.api_key_frame,
            text="🔗 Get key from: https://freemodelsforall.hopto.org/",
            font=ctk.CTkFont(size=11),
            text_color=Colors.ACCENT,
            cursor="hand2"
        )
        self.api_hint.pack(padx=30, pady=(0, 15))
        self.api_hint.bind("<Button-1>", lambda e: self._open_api_guide())

        # Continue button
        self.continue_btn = ctk.CTkButton(
            self.welcome_frame,
            text="🚀 Continue with API Key",
            command=self._setup_api_key,
            width=540,
            height=44,
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER
        )
        self.continue_btn.pack(padx=30, pady=10)

        # Or use without API
        self.skip_btn = ctk.CTkButton(
            self.welcome_frame,
            text="Skip - Use Local Mode Only",
            command=self._skip_api_setup,
            width=540,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="#253550",
            text_color=Colors.TEXT_SECONDARY
        )
        self.skip_btn.pack(padx=30, pady=(0, 20))

    def _open_api_guide(self):
        """Open the API guide URL."""
        try:
            import webbrowser
            webbrowser.open(API_GUIDE_URL)
        except:
            self._set_status("Could not open browser. Visit: " + API_GUIDE_URL)

    def _setup_api_key(self):
        """Process API key setup."""
        api_key = self.api_key_entry.get().strip()

        if not api_key:
            self._show_error("Please enter an API key!")
            return

        # Save API key
        save_api_key(api_key)
        self.api_key = api_key

        # Initialize client
        self._initialize_client()

        # Hide welcome screen
        if hasattr(self, 'welcome_frame'):
            self.welcome_frame.destroy()

        self._set_status("✅ API key configured successfully!")

    def _skip_api_setup(self):
        """Skip API setup and use local mode."""
        self.api_key = None
        self._set_status("Running in local mode (no API key)")

        if hasattr(self, 'welcome_frame'):
            self.welcome_frame.destroy()

        self._show_local_mode_info()

    def _show_local_mode_info(self):
        """Show information about local mode."""
        info_text = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   📍 Running in Local Mode                               ║
║                                                           ║
║   Without an API key, Hermes provides:                    ║
║   • System information and monitoring                     ║
║   • Basic assistance and guidance                         ║
║   • File operations help                                   ║
║                                                           ║
║   To enable full AI capabilities:                         ║
║   Run 'hermes-agent setup' in terminal                    ║
║   Or click Settings to configure API key                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """

        label = ctk.CTkLabel(
            self.messages_frame,
            text=info_text,
            font=ctk.CTkFont(size=11),
            text_color=Colors.TEXT_SECONDARY,
            justify="left"
        )
        label.pack(pady=20)

    def _initialize_client(self):
        """Initialize OpenAI client and fetch models."""
        try:
            self.client = create_client(self.api_key)
            self._set_status("🔄 Connecting to AI gateway...")

            # Fetch models
            self.models = fetch_models(self.client)

            if not self.models:
                self.models = FALLBACK_MODELS
                self._set_status("⚠️ Using fallback model list")

            # Update UI
            model_names = [m["name"] for m in self.models]
            self.model_combobox.configure(values=model_names, state="normal")
            self.model_combobox.set(model_names[0] if model_names else "No models available")

            self.selected_model = self.models[0]["id"] if self.models else None

            # Update API status
            self.api_status_label.configure(
                text=f"🔑 API: Configured ({self.api_key[:8]}...)",
                text_color=Colors.SUCCESS
            )

            self._set_status(f"✅ Connected! {len(self.models)} models available")
            self.welcome_label.configure(
                text=f"Ready to chat with {len(self.models)} AI models",
                font=ctk.CTkFont(size=14, weight="bold")
            )

        except PermissionError:
            self._show_error("Invalid API key! Please check and try again.")
            clear_api_key()
            self.api_key = None
            self._show_welcome_screen()
        except Exception as e:
            self._set_status(f"⚠️ Connection error: {str(e)[:50]}")
            self.models = FALLBACK_MODELS
            model_names = [m["name"] for m in self.models]
            self.model_combobox.configure(values=model_names, state="normal")
            self.model_combobox.set(model_names[0])
            self.selected_model = self.models[0]["id"]
            self._show_error(f"Using fallback models. API error: {str(e)[:100]}")

    def _new_chat(self):
        """Start a new chat conversation."""
        self.messages = []
        self.current_chat_id = None

        # Clear chat area
        for widget in self.messages_frame.winfo_children():
            widget.destroy()

        self.welcome_label.configure(
            text="💬 New chat started. Type your message below!",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self._set_status("New chat created")

    def _send_message(self):
        """Send a message to the AI."""
        user_input = self.input_field.get().strip()
        if not user_input:
            return

        # Clear input
        self.input_field.delete(0, "end")

        # Hide welcome message
        if self.welcome_label.winfo_ismapped():
            self.welcome_label.pack_forget()

        # Add user message to chat display
        self._add_user_message(user_input)
        self.messages.append({"role": "user", "content": user_input})

        # Disable input during processing
        self.input_field.configure(state="disabled")
        self.send_btn.configure(state="disabled")
        self._set_status("⏳ Thinking...")

        # Process AI response
        self._process_ai_response(user_input)

    def _add_user_message(self, content):
        """Add a user message bubble to the chat."""
        frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color=Colors.USER_MSG,
            corner_radius=12,
            width=500
        )
        frame.pack(anchor="e", fill="x", padx=(0, 20), pady=(5, 5))

        label = ctk.CTkLabel(
            frame,
            text=content,
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_PRIMARY,
            justify="left",
            wraplength=480
        )
        label.pack(padx=15, pady=12)

    def _add_ai_message(self, content, is_tool=False):
        """Add an AI message bubble to the chat."""
        frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color=Colors.AI_MSG if not is_tool else Colors.TOOL_MSG,
            corner_radius=12,
            width=500
        )
        frame.pack(anchor="w", fill="x", padx=(20, 0), pady=(5, 5))

        prefix = "🔧 " if is_tool else "✨ "
        label = ctk.CTkLabel(
            frame,
            text=f"{prefix}{content}",
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_PRIMARY,
            justify="left",
            wraplength=480
        )
        label.pack(padx=15, pady=12)

        # Scroll to bottom
        self.messages_frame._parent_canvas.yview_moveto(1)

    def _add_system_message(self, content):
        """Add a system/info message."""
        label = ctk.CTkLabel(
            self.messages_frame,
            text=content,
            font=ctk.CTkFont(size=11),
            text_color=Colors.TEXT_MUTED,
            justify="center"
        )
        label.pack(pady=5)

    def _process_ai_response(self, user_input):
        """Process AI response with streaming and tool support."""
        threading.Thread(target=self._ai_response_thread, args=(user_input,), daemon=True).start()

    def _ai_response_thread(self, user_input):
        """Thread worker for AI response."""
        if not self.client or not self.selected_model:
            self.root.after(0, lambda: self._add_system_message("⚠️ AI not configured. Please set up API key."))
            self._reset_input()
            return

        try:
            # Build API request
            api_kwargs = {
                "model": self.selected_model,
                "messages": self.messages,
                "stream": True,
            }
            if self.support_tools:
                api_kwargs["tools"] = TOOLS_SCHEMA

            response = self.client.chat.completions.create(**api_kwargs)

            assistant_response = ""
            tool_calls_accumulator = {}
            has_tool_calls = False

            for chunk in response:
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta

                # Handle tool calls
                if hasattr(delta, 'tool_calls') and delta.tool_calls:
                    has_tool_calls = True
                    for tc in delta.tool_calls:
                        idx = tc.index
                        if idx not in tool_calls_accumulator:
                            tool_calls_accumulator[idx] = {
                                "id": tc.id if tc.id else None,
                                "name": tc.function.name if tc.function and tc.function.name else "",
                                "arguments": ""
                            }
                        if tc.function and tc.function.name:
                            tool_calls_accumulator[idx]["name"] = tc.function.name
                        if tc.function and tc.function.arguments:
                            tool_calls_accumulator[idx]["arguments"] += tc.function.arguments

                # Handle content
                if hasattr(delta, 'content') and delta.content:
                    assistant_response += delta.content
                    # Update UI in real-time
                    self.root.after(0, lambda c=delta.content: self._update_ai_message(c))

            # Check for tool calls
            if tool_calls_accumulator:
                self.root.after(0, lambda: self._handle_tool_calls(tool_calls_accumulator, assistant_response))
            else:
                self.root.after(0, lambda: self._finish_message(assistant_response))

        except Exception as e:
            error_msg = str(e)
            if "tool" in error_msg.lower() and self.support_tools:
                self.support_tools = False
                self.root.after(0, lambda: self._add_system_message("🔧 Switching to text-only mode (tools not supported)"))
                self.root.after(0, lambda: self._process_ai_response(user_input))
            else:
                self.root.after(0, lambda: self._add_system_message(f"⚠️ Error: {error_msg[:100]}"))
                self._reset_input()

    def _update_ai_message(self, content):
        """Update the AI message being typed in real-time."""
        # Find the last AI message frame and update it
        for widget in self.messages_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkLabel) and child.cget("text").startswith("✨"):
                        current = child.cget("text")[2:]  # Remove "✨ "
                        child.configure(text=f"✨ {current}{content}")
                        return

        # If no existing AI message, create one
        self._add_ai_message(content)

    def _handle_tool_calls(self, tool_calls, assistant_response):
        """Handle tool calls from AI."""
        # Add assistant message with tool calls
        serialized_calls = []
        assistant_msg_tools = []

        for idx in sorted(tool_calls.keys()):
            tc = tool_calls[idx]
            call_id = tc["id"] or f"call_{int(time.time())}_{idx}"
            tool_call = {
                "id": call_id,
                "type": "function",
                "function": {
                    "name": tc["name"],
                    "arguments": tc["arguments"]
                }
            }
            serialized_calls.append(tool_call)
            assistant_msg_tools.append(tool_call)

        if assistant_response:
            self.messages.append({
                "role": "assistant",
                "content": assistant_response,
                "tool_calls": assistant_msg_tools
            })

            # Show tool execution
            for tc in serialized_calls:
                name = tc["function"]["name"]
                args = tc["function"]["arguments"]
                self._add_system_message(f"⚙️ Running tool: {name}({args[:50]}...)")

                result = execute_tool(name, args)
                self._add_ai_message(f"📄 {result[:200]}{'...' if len(result) > 200 else ''}", is_tool=True)

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "name": name,
                    "content": result
                })

            # Continue conversation with tool results
            self._continue_with_tools()
        else:
            if assistant_response:
                self.messages.append({"role": "assistant", "content": assistant_response})
            self._reset_input()

    def _continue_with_tools(self):
        """Continue conversation after tool execution."""
        try:
            api_kwargs = {
                "model": self.selected_model,
                "messages": self.messages,
                "stream": True,
            }

            response = self.client.chat.completions.create(**api_kwargs)

            final_response = ""
            for chunk in response:
                if chunk.choices and hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                    final_response += chunk.choices[0].delta.content

            self.root.after(0, lambda: self._finish_message(final_response))
            self.messages.append({"role": "assistant", "content": final_response})

        except Exception as e:
            self.root.after(0, lambda: self._add_system_message(f"⚠️ Error: {str(e)[:100]}"))
            self._reset_input()

    def _finish_message(self, content):
        """Finish and finalize the AI message."""
        if content:
            self._add_ai_message(content)
        self._reset_input()

    def _reset_input(self):
        """Re-enable input after AI response."""
        self.input_field.configure(state="normal")
        self.send_btn.configure(state="normal")
        self.input_field.focus()
        self._set_status("✅ Ready")

    def _show_settings(self):
        """Show settings dialog."""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.configure(fg_color=Colors.BG_DARK)
        settings_window.grab_set()

        # Title
        title = ctk.CTkLabel(
            settings_window,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)

        # API Key section
        api_frame = ctk.CTkFrame(settings_window, fg_color=Colors.BG_DARK, corner_radius=10)
        api_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            api_frame,
            text="API Configuration",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 5))

        if self.api_key:
            ctk.CTkLabel(
                api_frame,
                text=f"✓ API Key configured ({self.api_key[:8]}...)",
                text_color=Colors.SUCCESS,
                font=ctk.CTkFont(size=12)
            ).pack()

            ctk.CTkButton(
                api_frame,
                text="Change API Key",
                command=lambda: self._change_api_key(settings_window)
            ).pack(pady=10)
        else:
            ctk.CTkLabel(
                api_frame,
                text="✗ No API key configured",
                text_color=Colors.ERROR,
                font=ctk.CTkFont(size=12)
            ).pack()

            ctk.CTkButton(
                api_frame,
                text="Set Up API Key",
                command=lambda: self._change_api_key(settings_window)
            ).pack(pady=10)

        # Model info
        model_frame = ctk.CTkFrame(settings_window, fg_color=Colors.BG_DARK, corner_radius=10)
        model_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            model_frame,
            text="Model Information",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            model_frame,
            text=f"Selected: {self.selected_model or 'None'}",
            font=ctk.CTkFont(size=12)
        ).pack()

        ctk.CTkLabel(
            model_frame,
            text=f"Available: {len(self.models)} models",
            font=ctk.CTkFont(size=12)
        ).pack()

        # Support info
        support_frame = ctk.CTkFrame(settings_window, fg_color=Colors.BG_DARK, corner_radius=10)
        support_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            support_frame,
            text="Support & Info",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            support_frame,
            text="API Guide: https://freemodelsforall.hopto.org/",
            font=ctk.CTkFont(size=11),
            text_color=Colors.TEXT_SECONDARY,
            justify="left"
        ).pack()

        # Close button
        ctk.CTkButton(
            settings_window,
            text="Close",
            command=settings_window.destroy,
            width=100,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=12)
        ).pack(pady=20)

    def _change_api_key(self, parent_window):
        """Change API key dialog."""
        dialog = ctk.CTkToplevel(parent_window)
        dialog.title("Change API Key")
        dialog.geometry("450x300")
        dialog.configure(fg_color=Colors.BG_DARK)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Enter New API Key",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20)

        entry = ctk.CTkEntry(
            dialog,
            placeholder_text="Paste API key here...",
            show="*",
            font=ctk.CTkFont(size=13),
            height=44,
            corner_radius=8,
            width=400
        )
        entry.pack(pady=10)

        def save_new_key():
            new_key = entry.get().strip()
            if new_key:
                save_api_key(new_key)
                self.api_key = new_key
                self._initialize_client()
                dialog.destroy()
                self._show_settings()  # Refresh settings
                self._set_status("✅ API key updated!")

        ctk.CTkButton(
            dialog,
            text="Save",
            command=save_new_key,
            width=100,
            height=36,
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER
        ).pack(pady=20)

    def _show_error(self, message):
        """Show error message."""
        error_window = ctk.CTkToplevel(self.root)
        error_window.title("Error")
        error_window.geometry("400x150")
        error_window.configure(fg_color=Colors.BG_DARK)
        error_window.grab_set()

        ctk.CTkLabel(
            error_window,
            text="⚠️ " + message,
            font=ctk.CTkFont(size=13),
            text_color=Colors.ERROR,
            justify="center"
        ).pack(pady=30)

        ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy,
            width=80,
            height=32,
            corner_radius=6
        ).pack()

    def _set_status(self, message):
        """Update status bar."""
        self.status_label.configure(text=message)

    def _create_icon(self):
        """Create application icon."""
        size = 64
        image = Image.new('RGBA', (size, size), (26, 26, 46, 255))
        draw = ImageDraw.Draw(image)

        # Gradient circle
        for i in range(size // 2):
            color = (
                int(102 + (118 - 102) * i / (size // 2)),
                int(126 + (75 - 126) * i / (size // 2)),
                int(234 + (186 - 234) * i / (size // 2)),
                255
            )
            draw.ellipse(
                [(size // 2 - i, size // 2 - i), (size // 2 + i, size // 2 + i)],
                outline=color,
                width=2
            )

        # H letter
        draw.text((size // 2 - 8, size // 2 - 10), "H", fill=(255, 255, 255, 255))

        return ImageTk.PhotoImage(image)

    def run(self):
        """Run the application."""
        # Try to set icon
        try:
            icon = self._create_icon()
            self.root.iconphoto(True, icon)
        except:
            pass

        self.root.mainloop()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("\n" + "═" * 60)
    print("  ✨ Hermes AI Desktop - Starting...")
    print("═" * 60 + "\n")

    app = HermesDesktopApp()
    app.run()
