#!/usr/bin/env python3
"""
AI Canvas - Full-Featured AI Desktop Application
==================================================
A beautiful, Claude Desktop-like AI chat application with complete functionality.

Features:
- Modern GUI with sidebar and chat interface
- First-run API key setup wizard with guidance
- Multiple model support via gateway
- Tool integration (file operations)
- Chat history management
- Real-time streaming responses
- Error handling with retry logic

API Key Portal: https://freemodelsforall.hopto.org/

Requirements: pip install customtkinter openai Pillow
"""

import sys
import os
import threading
import time
import json
from datetime import datetime
from pathlib import Path

# ============================================================================
# IMPORTS
# ============================================================================

try:
    import customtkinter as ctk
    from customtkinter import filedialog
except ImportError:
    print("=" * 70)
    print("  ERROR: customtkinter is required!")
    print("  Install with: pip install customtkinter openai Pillow")
    print("=" * 70)
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("=" * 70)
    print("  ERROR: openai library is required!")
    print("  Install with: pip install openai")
    print("=" * 70)
    sys.exit(1)

from PIL import Image, ImageDraw, ImageTk

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_URL = "https://freemodelsforall.hopto.org/v1"
APP_NAME = "AI Canvas"
CONFIG_DIR = os.path.expanduser("~/.ai_canvas")
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
    """Application color scheme - Beautiful dark theme"""
    BG_DARK = "#0d1117"           # GitHub dark
    BG_SIDEBAR = "#161b22"        # Sidebar background
    BG_CHAT = "#0d1117"           # Chat area background
    BG_INPUT = "#21262d"          # Input field background
    BG_USER_MSG = "#1f2329"       # User message bubble
    BG_AI_MSG = "#1c2128"         # AI message bubble
    BG_TOOL_MSG = "#1a1f2e"       # Tool message
    ACCENT = "#58a6ff"            # Blue accent
    ACCENT_HOVER = "#79c0ff"      # Lighter blue
    TEXT_PRIMARY = "#e6edf3"      # Main text
    TEXT_SECONDARY = "#8b949e"    # Secondary text
    TEXT_MUTED = "#6e7681"        # Muted text
    USER_MSG_ACCENT = "#238636"   # Green for user
    BORDER = "#30363d"            # Border color
    SPINNER_COLOR = "#58a6ff"     # Spinner color
    TOOL_COLOR = "#d29922"        # Yellow for tools
    ERROR_COLOR = "#f85149"       # Red for errors
    SUCCESS_COLOR = "#3fb950"     # Green for success

# ============================================================================
# FALLBACK MODELS (from original AI Canvas.txt)
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
# TOOL DEFINITIONS (from original code)
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
# TOOL EXECUTION (from original code)
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
            return f"Success: File successfully written to '{filepath}' ({len(content)} chars)."
        except Exception as e:
            return f"Error writing file: {e}"

    elif name == "delete_file":
        filepath = args.get("filepath")
        if not filepath:
            return "Error: Missing required argument 'filepath'."
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return f"Success: File '{filepath}' successfully deleted."
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
                # Limit output size
                if len(content) > 10000:
                    return content[:10000] + "\n\n... [Truncated: file too long]"
                return content
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
                for f in sorted(files):
                    full_path = os.path.join(directory, f)
                    if os.path.isdir(full_path):
                        result.append(f"📁 {f}/")
                    else:
                        result.append(f"📄 {f}")
                return "\n".join(result) if result else "(empty directory)"
            else:
                return f"Error: Directory '{directory}' not found."
        except Exception as e:
            return f"Error listing directory: {e}"

    else:
        return f"Error: Unknown function name '{name}'."

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
        json.dump({
            "api_key": key,
            "saved_at": datetime.now().isoformat(),
            "provider": "custom_gateway"
        }, f, indent=2)
    os.chmod(CREDENTIALS_FILE, 0o600)

def clear_api_key():
    """Remove saved API key."""
    if os.path.exists(CREDENTIALS_FILE):
        os.remove(CREDENTIALS_FILE)

def has_api_key():
    """Check if API key exists."""
    return load_api_key() is not None

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
# SPINNER CLASS (from original code)
# ============================================================================

class Spinner:
    """Animated spinner for loading states."""
    def __init__(self, message="Thinking..."):
        self.message = message
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.stop_running = threading.Event()
        self.thread = None

    def _spin(self, text_widget, position):
        idx = 0
        while not self.stop_running.is_set():
            symbol = self.spinner_chars[idx % len(self.spinner_chars)]
            text_widget.configure(state="normal")
            text_widget.delete(f"{position}.0", f"{position}.end")
            text_widget.insert(f"{position}.0", f"{symbol} {self.message}")
            text_widget.configure(state="disabled")
            idx += 1
            time.sleep(0.08)

    def start(self, text_widget, position):
        self.text_widget = text_widget
        self.position = position
        self.stop_running.clear()
        self.thread = threading.Thread(target=self._spin, args=(text_widget, position), daemon=True)
        self.thread.start()

    def stop(self):
        if self.thread:
            self.stop_running.set()
            self.thread.join(timeout=0.5)

# ============================================================================
# CHAT MESSAGE CLASS
# ============================================================================

class ChatMessage:
    """Represents a chat message."""
    def __init__(self, role, content, tool_calls=None):
        self.role = role
        self.content = content
        self.tool_calls = tool_calls or []
        self.timestamp = datetime.now()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class AICanvasApp:
    """
    AI Canvas - Main Application Class
    Full-featured AI chat with beautiful GUI.
    """

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(f"{APP_NAME}")
        self.root.geometry("1280x800")
        self.root.minsize(1000, 700)

        # State
        self.api_key = None
        self.client = None
        self.models = []
        self.selected_model = None
        self.messages = []
        self.chats = []
        self.current_chat_id = None
        self.support_tools = True
        self.is_processing = False

        # Setup theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        # Build UI
        self._build_ui()

        # Check for existing API key
        self.api_key = load_api_key()
        if self.api_key:
            self._initialize_client()
            self._show_main_interface()
        else:
            self._show_welcome_screen()

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
        self.sidebar_header.pack(fill="x", padx=20, pady=(20, 15))

        # Logo
        logo_frame = ctk.CTkFrame(self.sidebar_header, fg_color="transparent")
        logo_frame.pack()

        # Create logo image
        logo_size = 32
        logo_img = Image.new('RGBA', (logo_size, logo_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(logo_img)
        draw.rounded_rectangle([(2, 2), (logo_size-2, logo_size-2)], radius=8, fill=Colors.ACCENT)
        draw.text((logo_size//2 - 6, logo_size//2 - 8), "AI", fill="white", font_size=10)
        logo_photo = ImageTk.PhotoImage(logo_img)

        self.logo_label = ctk.CTkLabel(
            self.sidebar_header,
            image=logo_photo,
            text=f"  {APP_NAME}",
            compound="left",
            font=ctk.CTkFont(size=18, weight="bold", family="Segoe UI")
        )
        self.logo_label.pack()
        self.logo_label.image = logo_photo  # Keep reference

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
            height=36,
            font=ctk.CTkFont(size=12),
            corner_radius=6,
            state="disabled",
            button_color=Colors.ACCENT,
            button_hover_color=Colors.ACCENT_HOVER
        )
        self.model_combobox.pack(fill="x", pady=(5, 0))
        self.model_combobox.set("Loading models...")

        self.model_combobox.configure(command=self._on_model_change)

        # New chat button
        self.new_chat_btn = ctk.CTkButton(
            self.sidebar,
            text="➕ New Chat",
            command=self._new_chat,
            width=240,
            height=36,
            corner_radius=6,
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
            text="CHATS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=Colors.TEXT_MUTED
        )
        self.history_label.pack(anchor="w", pady=(0, 5))

        # Scrollable chat history
        self.history_frame = ctk.CTkScrollableFrame(
            self.history_section,
            fg_color="transparent",
            width=230,
            scrollbar_fg_color=Colors.BORDER,
            scrollbar_button_color=Colors.ACCENT
        )
        self.history_frame.pack(fill="both", expand=True)

        # Sidebar footer
        self.sidebar_footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_footer.pack(fill="x", padx=15, pady=15)

        self.api_btn = ctk.CTkButton(
            self.sidebar_footer,
            text="🔑 API Key",
            command=self._show_api_setup,
            width=240,
            height=34,
            corner_radius=6,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="#21262d",
            text_color=Colors.TEXT_SECONDARY
        )
        self.api_btn.pack(pady=(0, 5))

        self.settings_btn = ctk.CTkButton(
            self.sidebar_footer,
            text="⚙️ Settings",
            command=self._show_settings,
            width=240,
            height=34,
            corner_radius=6,
            font=ctk.CTkFont(size=12),
            fg_color="transparent",
            hover_color="#21262d",
            text_color=Colors.TEXT_SECONDARY
        )
        self.settings_btn.pack()

        # ===== MAIN CHAT AREA =====
        self.chat_area = ctk.CTkFrame(
            self.main_container,
            fg_color=Colors.BG_CHAT,
            corner_radius=0
        )
        self.chat_area.pack(side="right", fill="both", expand=True)

        # Chat header
        self.chat_header = ctk.CTkFrame(self.chat_area, fg_color="transparent")
        self.chat_header.pack(fill="x", padx=20, pady=(15, 10))

        self.chat_title = ctk.CTkLabel(
            self.chat_header,
            text="💬 Chat",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.chat_title.pack(side="left")

        self.model_indicator = ctk.CTkLabel(
            self.chat_header,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=Colors.TEXT_MUTED
        )
        self.model_indicator.pack(side="right")

        # Chat messages area (scrollable)
        self.messages_frame = ctk.CTkScrollableFrame(
            self.chat_area,
            fg_color="transparent",
            width=800,
            scrollbar_fg_color=Colors.BORDER,
            scrollbar_button_color=Colors.ACCENT
        )
        self.messages_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Welcome message in chat area (hidden initially)
        self.welcome_frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color=Colors.BG_DARK,
            corner_radius=12,
            width=600
        )
        self.welcome_label = ctk.CTkLabel(
            self.welcome_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color=Colors.TEXT_SECONDARY,
            justify="center"
        )
        self.welcome_label.pack(pady=40, padx=30)

        # Input area
        self.input_frame = ctk.CTkFrame(
            self.chat_area,
            fg_color=Colors.BG_INPUT,
            corner_radius=8
        )
        self.input_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.input_field = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type your message... (Enter to send)",
            placeholder_text_color=Colors.TEXT_MUTED,
            font=ctk.CTkFont(size=14),
            height=44,
            corner_radius=8,
            fg_color=Colors.BG_DARK,
            text_color=Colors.TEXT_PRIMARY
        )
        self.input_field.pack(side="left", fill="x", padx=(15, 10), pady=8)
        self.input_field.bind("<Return>", lambda e: self._send_message())

        self.send_btn = ctk.CTkButton(
            self.input_frame,
            text="Send",
            command=self._send_message,
            width=90,
            height=44,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            text_color="white"
        )
        self.send_btn.pack(side="right", padx=(0, 15), pady=8)

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

        self.token_label = ctk.CTkLabel(
            self.status_bar,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=Colors.TEXT_MUTED
        )
        self.token_label.pack(side="right")

    def _show_welcome_screen(self):
        """Show welcome/setup screen on first launch."""
        self.welcome_frame.pack(pady=30, padx=20, fill="x")

        welcome_text = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   ✨ Welcome to AI Canvas                                        ║
║                                                                   ║
║   Your intelligent AI assistant with powerful capabilities       ║
║                                                                   ║
║   ──────────────────────────────────────────────────────────────  ║
║                                                                   ║
║   To get started, you need an API key:                            ║
║                                                                   ║
║   🔑 Get your free API key from:                                  ║
║   ┌─────────────────────────────────────────────────────────┐    ║
║   │  https://freemodelsforall.hopto.org/                  │    ║
║   └─────────────────────────────────────────────────────────┘    ║
║                                                                   ║
║   Steps:                                                          ║
║   1. Visit the website above                                     ║
║   2. Sign up / Log in                                            ║
║   3. Copy your API key                                           ║
║   4. Paste it below                                              ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
        """

        self.welcome_label.configure(text=welcome_text)
        self.welcome_label.configure(font=ctk.CTkFont(size=11))

        # API Key input frame
        self.api_key_frame = ctk.CTkFrame(
            self.welcome_frame,
            fg_color=Colors.BG_INPUT,
            corner_radius=8
        )
        self.api_key_frame.pack(pady=20)

        self.api_key_entry = ctk.CTkEntry(
            self.api_key_frame,
            placeholder_text="Paste your API key here...",
            placeholder_text_color=Colors.TEXT_MUTED,
            font=ctk.CTkFont(size=13),
            height=44,
            corner_radius=6,
            fg_color=Colors.BG_DARK,
            text_color=Colors.TEXT_PRIMARY,
            width=520
        )
        self.api_key_entry.pack(padx=20, pady=10)

        # API hint link
        self.api_hint = ctk.CTkLabel(
            self.api_key_frame,
            text="🔗 Get key from: https://freemodelsforall.hopto.org/",
            font=ctk.CTkFont(size=11, underline=True),
            text_color=Colors.ACCENT,
            cursor="hand2"
        )
        self.api_hint.pack(padx=20, pady=(0, 10))
        self.api_hint.bind("<Button-1>", lambda e: self._open_api_guide())

        # Continue button
        self.continue_btn = ctk.CTkButton(
            self.api_key_frame,
            text="🚀 Continue with API Key",
            command=self._setup_api_key,
            width=520,
            height=40,
            corner_radius=6,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            text_color="white"
        )
        self.continue_btn.pack(padx=20, pady=(5, 10))

        # Skip button
        self.skip_btn = ctk.CTkButton(
            self.api_key_frame,
            text="Skip - Use Without API (Limited)",
            command=self._skip_api_setup,
            width=520,
            height=32,
            corner_radius=6,
            font=ctk.CTkFont(size=11),
            fg_color="transparent",
            hover_color="#21262d",
            text_color=Colors.TEXT_SECONDARY
        )
        self.skip_btn.pack(padx=20, pady=(0, 5))

    def _show_main_interface(self):
        """Show the main chat interface."""
        if self.welcome_frame.winfo_ismapped():
            self.welcome_frame.pack_forget()

        self.welcome_label.configure(
            text="💬 Ready to chat! Type your message below.",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.welcome_label.pack(pady=20)

        self._update_model_indicator()
        self._set_status(f"✅ Connected - {len(self.models)} models available")

    def _open_api_guide(self):
        """Open the API guide URL."""
        try:
            import webbrowser
            webbrowser.open(API_GUIDE_URL)
        except:
            self._set_status("Open browser: " + API_GUIDE_URL)

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
        if self.welcome_frame.winfo_ismapped():
            self.welcome_frame.pack_forget()

        self._show_main_interface()
        self._set_status("✅ API key configured successfully!")

    def _skip_api_setup(self):
        """Skip API setup."""
        self.api_key = None
        self._show_main_interface()
        self._set_status("⚠️ Running without API key - limited functionality")

        # Show info message
        info_text = """
┌─────────────────────────────────────────────────────────────┐
│  📍 Running in Limited Mode                               │
│                                                             │
│  Without an API key, AI Canvas provides:                   │
│  • Basic interface (no AI responses)                       │
│  • Model selection (will show error on chat)              │
│  • Settings and configuration                              │
│                                                             │
│  To enable full AI capabilities:                          │
│  Click "API Key" in sidebar or run:                      │
│  export API_KEY='your-key-here'                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
        """
        label = ctk.CTkLabel(
            self.welcome_frame,
            text=info_text,
            font=ctk.CTkFont(size=10),
            text_color=Colors.TEXT_SECONDARY,
            justify="left"
        )
        label.pack(pady=15)

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
            self.model_combobox.set(model_names[0] if model_names else "No models")

            # Select default model (prefer Claude Opus 5)
            self.selected_model = self._select_default_model()

            self._set_status(f"✅ Connected! {len(self.models)} models available")

        except PermissionError:
            self._show_error("Invalid API key! Please check and try again.")
            clear_api_key()
            self.api_key = None
            self._show_welcome_screen()
        except Exception as e:
            self._set_status(f"⚠️ Connection error - using fallback models")
            self.models = FALLBACK_MODELS
            model_names = [m["name"] for m in self.models]
            self.model_combobox.configure(values=model_names, state="normal")
            self.model_combobox.set(model_names[0])
            self.selected_model = self.models[0]["id"]
            self._show_error(f"Using fallback models. Error: {str(e)[:80]}")

    def _select_default_model(self):
        """Select default model (prefer Claude Opus 5)."""
        for model in self.models:
            if "opus-5" in model["id"].lower() or "claude-opus-5" in model["id"].lower():
                return model["id"]
        return self.models[0]["id"] if self.models else None

    def _on_model_change(self, value):
        """Handle model selection change."""
        for model in self.models:
            if model["name"] == value:
                self.selected_model = model["id"]
                self._update_model_indicator()
                self._set_status(f"✅ Model selected: {value}")
                break

    def _update_model_indicator(self):
        """Update model indicator in header."""
        if self.selected_model:
            # Find model name
            for m in self.models:
                if m["id"] == self.selected_model:
                    self.model_indicator.configure(text=f"Model: {m['name']}")
                    return
            self.model_indicator.configure(text=f"Model: {self.selected_model[:30]}...")

    def _new_chat(self):
        """Start a new chat conversation."""
        self.messages = []
        self.current_chat_id = None

        # Clear chat area
        for widget in self.messages_frame.winfo_children():
            widget.destroy()

        self.welcome_frame.pack(pady=20, padx=20, fill="x")
        self.welcome_label.configure(
            text="💬 New chat started. Type your message below!",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self._set_status("New chat created")

    def _send_message(self):
        """Send a message to the AI."""
        if self.is_processing:
            return

        user_input = self.input_field.get().strip()
        if not user_input:
            return

        # Clear input
        self.input_field.delete(0, "end")

        # Hide welcome message
        if self.welcome_frame.winfo_ismapped():
            self.welcome_frame.pack_forget()

        # Add user message to chat display
        self._add_user_message(user_input)
        self.messages.append({"role": "user", "content": user_input})

        # Set processing state
        self.is_processing = True
        self.send_btn.configure(state="disabled")
        self.input_field.configure(state="disabled")
        self._set_status("⏳ Thinking...")

        # Process AI response in thread
        threading.Thread(target=self._process_ai_response, args=(user_input,), daemon=True).start()

    def _add_user_message(self, content):
        """Add a user message bubble to the chat."""
        frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color=Colors.BG_USER_MSG,
            corner_radius=12,
            width=480
        )
        frame.pack(anchor="e", fill="x", padx=(0, 20), pady=(5, 5))

        # Avatar
        avatar = ctk.CTkLabel(
            frame,
            text="You",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="white",
            width=40,
            height=20,
            corner_radius=10,
            fg_color=Colors.USER_MSG_ACCENT
        )
        avatar.pack(side="left", padx=(12, 8), pady=8)

        label = ctk.CTkLabel(
            frame,
            text=content,
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_PRIMARY,
            justify="left",
            wraplength=420
        )
        label.pack(padx=5, pady=8)

        self._scroll_to_bottom()

    def _add_ai_message(self, content, is_streaming=False):
        """Add an AI message bubble to the chat."""
        frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color=Colors.BG_AI_MSG,
            corner_radius=12,
            width=480
        )
        frame.pack(anchor="w", fill="x", padx=(20, 0), pady=(5, 5))

        # Avatar
        avatar = ctk.CTkLabel(
            frame,
            text="AI",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="white",
            width=40,
            height=20,
            corner_radius=10,
            fg_color=Colors.ACCENT
        )
        avatar.pack(side="left", padx=(12, 8), pady=8)

        label = ctk.CTkLabel(
            frame,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=Colors.TEXT_PRIMARY,
            justify="left",
            wraplength=420
        )
        label.pack(padx=5, pady=8)

        if is_streaming:
            self._current_ai_frame = frame
            self._current_ai_label = label
        else:
            label.configure(text=content)
            self._scroll_to_bottom()

    def _update_ai_message(self, content):
        """Update the currently streaming AI message."""
        if hasattr(self, '_current_ai_label') and self._current_ai_label:
            current = self._current_ai_label.cget("text")
            self._current_ai_label.configure(text=current + content)
            self._scroll_to_bottom()

    def _add_tool_message(self, content):
        """Add a tool execution message."""
        frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color=Colors.BG_TOOL_MSG,
            corner_radius=8,
            width=480
        )
        frame.pack(anchor="w", fill="x", padx=(20, 0), pady=(3, 3))

        label = ctk.CTkLabel(
            frame,
            text=content,
            font=ctk.CTkFont(size=11),
            text_color=Colors.TOOL_COLOR,
            justify="left",
            wraplength=440
        )
        label.pack(padx=15, pady=6)

        self._scroll_to_bottom()

    def _add_system_message(self, content):
        """Add a system/info message."""
        frame = ctk.CTkFrame(
            self.messages_frame,
            fg_color="transparent",
            corner_radius=0,
            width=480
        )
        frame.pack(anchor="center", fill="x", padx=20, pady=(5, 5))

        label = ctk.CTkLabel(
            frame,
            text=content,
            font=ctk.CTkFont(size=11),
            text_color=Colors.TEXT_MUTED,
            justify="center"
        )
        label.pack(pady=5)

    def _scroll_to_bottom(self):
        """Scroll chat to bottom."""
        try:
            self.messages_frame._parent_canvas.yview_moveto(1)
        except:
            pass

    def _process_ai_response(self, user_input):
        """Process AI response with streaming and tool support."""
        if not self.client or not self.selected_model:
            self.root.after(0, lambda: self._add_system_message("⚠️ AI not configured. Please set up API key."))
            self._reset_input()
            return

        try:
            # Build API request (from original code)
            api_kwargs = {
                "model": self.selected_model,
                "messages": self.messages,
                "stream": True,
            }
            if self.support_tools:
                api_kwargs["tools"] = TOOLS_SCHEMA

            max_retries = 3
            retry_delay = 2.0
            api_success = False

            for attempt in range(max_retries):
                spinner = Spinner("Thinking...")
                spinner.start(self.messages_frame._text_label, "end")

                try:
                    response = self.client.chat.completions.create(**api_kwargs)

                    assistant_response = ""
                    tool_calls_accumulator = {}
                    spinner_stopped = False
                    buffer = ""

                    for chunk in response:
                        if not chunk.choices:
                            continue

                        delta = chunk.choices[0].delta

                        # Accumulate function calls
                        if hasattr(delta, 'tool_calls') and delta.tool_calls:
                            if not spinner_stopped:
                                spinner.stop()
                                spinner_stopped = True

                            for tc in delta.tool_calls:
                                idx = tc.index
                                if idx not in tool_calls_accumulator:
                                    tool_calls_accumulator[idx] = {
                                        "id": tc.id if tc.id else None,
                                        "name": tc.function.name if tc.function and tc.function.name else "",
                                        "arguments": ""
                                    }
                                else:
                                    if tc.id:
                                        tool_calls_accumulator[idx]["id"] = tc.id
                                    if tc.function and tc.function.name:
                                        tool_calls_accumulator[idx]["name"] = tc.function.name

                                if tc.function and tc.function.arguments:
                                    tool_calls_accumulator[idx]["arguments"] += tc.function.arguments

                        # Buffer initial output to intercept errors
                        content = delta.content
                        if content:
                            if not spinner_stopped:
                                buffer += content
                                if len(buffer) >= 20 or "\n" in buffer:
                                    if any(x in buffer.lower() for x in ["[error]", "service temporarily unavailable", "502 bad gateway"]):
                                        raise Exception(f"Upstream API error text: {buffer.strip()}")

                                    spinner.stop()
                                    self.root.after(0, lambda c=content: self._update_ai_message(c))
                                    assistant_response += buffer
                                    spinner_stopped = True
                            else:
                                self.root.after(0, lambda c=content: self._update_ai_message(c))
                                assistant_response += content

                    # Flush remaining buffer
                    if not spinner_stopped:
                        if buffer:
                            if any(x in buffer.lower() for x in ["[error]", "service temporarily unavailable", "502 bad gateway"]):
                                raise Exception(f"Upstream API error text: {buffer.strip()}")
                            spinner.stop()
                            if not hasattr(self, '_current_ai_label'):
                                self._add_ai_message("")
                            self.root.after(0, lambda c=buffer: self._update_ai_message(c))
                            assistant_response += buffer
                        else:
                            spinner.stop()
                            if not hasattr(self, '_current_ai_label'):
                                self._add_ai_message("[Empty response]")

                    api_success = True
                    break

                except Exception as e:
                    spinner.stop()
                    err_str = str(e)

                    # Handle tool compatibility failure
                    if self.support_tools and any(x in err_str.lower() for x in ["tool", "400", "invalid_request_error"]):
                        self.support_tools = False
                        self.root.after(0, lambda: self._add_system_message("🔧 Model doesn't support tools, falling back to text-only mode"))
                        break

                    # Detect transience for retry
                    is_transient = any(x in err_str.lower() for x in ["timeout", "502", "503", "504", "408", "rate limit", "connection error", "upstream api error"])

                    if is_transient and attempt < max_retries - 1:
                        self.root.after(0, lambda: self._add_system_message(f"⚠️ API error. Retrying in {retry_delay:.1f}s... (Attempt {attempt+1}/{max_retries})"))
                        time.sleep(retry_delay)
                        retry_delay *= 2.0
                        continue
                    else:
                        self.root.after(0, lambda: self._add_system_message(f"⚠️ Error: {err_str[:100]}"))
                        break

            if not api_success:
                self._reset_input()
                return

            # Handle tool calls
            if tool_calls_accumulator:
                self.root.after(0, lambda: self._handle_tool_calls(tool_calls_accumulator, assistant_response))
            else:
                self.root.after(0, lambda: self._finish_message(assistant_response))

        except Exception as e:
            self.root.after(0, lambda: self._add_system_message(f"⚠️ Error: {str(e)[:100]}"))
            self._reset_input()

    def _handle_tool_calls(self, tool_calls, assistant_response):
        """Handle tool calls from AI."""
        # Add assistant message
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
        else:
            self.messages.append({
                "role": "assistant",
                "tool_calls": assistant_msg_tools
            })

        # Execute tools and show results
        for tc in serialized_calls:
            name = tc["function"]["name"]
            args_str = tc["function"]["arguments"]
            call_id = tc["id"]

            self.root.after(0, lambda n=name, a=args_str: self._add_tool_message(f"⚙️ Running tool: {n}({a[:50]}...)"))

            result = execute_tool(name, args_str)
            self.root.after(0, lambda r=result: self._add_tool_message(f"📄 Result: {r[:200]}{'...' if len(r) > 200 else ''}"))

            self.messages.append({
                "role": "tool",
                "tool_call_id": call_id,
                "name": name,
                "content": result
            })

        # Continue with tool results
        self.root.after(0, lambda: self._continue_with_tools())

    def _continue_with_tools(self):
        """Continue conversation after tool execution."""
        if not self.client or not self.selected_model:
            self._reset_input()
            return

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
                    self.root.after(0, lambda c=chunk.choices[0].delta.content: self._update_ai_message(c))

            self.messages.append({"role": "assistant", "content": final_response})
            self.root.after(0, self._reset_input)

        except Exception as e:
            self.root.after(0, lambda: self._add_system_message(f"⚠️ Error: {str(e)[:100]}"))
            self._reset_input()

    def _finish_message(self, content):
        """Finish and finalize the AI message."""
        if content:
            self.messages.append({"role": "assistant", "content": content})
        self._reset_input()

    def _reset_input(self):
        """Re-enable input after AI response."""
        self.is_processing = False
        self.input_field.configure(state="normal")
        self.send_btn.configure(state="normal")
        self.input_field.focus()
        self._set_status("✅ Ready")

    def _show_settings(self):
        """Show settings dialog."""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("450x500")
        settings_window.configure(fg_color=Colors.BG_DARK)
        settings_window.grab_set()

        # Title
        ctk.CTkLabel(
            settings_window,
            text=f"⚙️ {APP_NAME} Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=20)

        # API Key section
        api_frame = ctk.CTkFrame(settings_window, fg_color=Colors.BG_DARK, corner_radius=8)
        api_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            api_frame,
            text="API Configuration",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Colors.TEXT_PRIMARY
        ).pack(pady=(15, 5))

        if self.api_key:
            ctk.CTkLabel(
                api_frame,
                text=f"✓ API Key configured ({self.api_key[:8]}...)",
                text_color=Colors.SUCCESS_COLOR,
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
                text_color=Colors.ERROR_COLOR,
                font=ctk.CTkFont(size=12)
            ).pack()

            ctk.CTkButton(
                api_frame,
                text="Set Up API Key",
                command=lambda: self._change_api_key(settings_window)
            ).pack(pady=10)

        # Model info
        model_frame = ctk.CTkFrame(settings_window, fg_color=Colors.BG_DARK, corner_radius=8)
        model_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            model_frame,
            text="Model Information",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Colors.TEXT_PRIMARY
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            model_frame,
            text=f"Selected: {self.selected_model or 'None'}",
            font=ctk.CTkFont(size=12),
            text_color=Colors.TEXT_SECONDARY
        ).pack()

        ctk.CTkLabel(
            model_frame,
            text=f"Available: {len(self.models)} models",
            font=ctk.CTkFont(size=12),
            text_color=Colors.TEXT_SECONDARY
        ).pack()

        # Gateway info
        gateway_frame = ctk.CTkFrame(settings_window, fg_color=Colors.BG_DARK, corner_radius=8)
        gateway_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            gateway_frame,
            text="Gateway Information",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Colors.TEXT_PRIMARY
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            gateway_frame,
            text=f"URL: {BASE_URL}",
            font=ctk.CTkFont(size=11),
            text_color=Colors.TEXT_SECONDARY,
            justify="left"
        ).pack()

        ctk.CTkLabel(
            gateway_frame,
            text=f"API Portal: {API_GUIDE_URL}",
            font=ctk.CTkFont(size=11),
            text_color=Colors.ACCENT,
            justify="left"
        ).pack()

        # Support info
        support_frame = ctk.CTkFrame(settings_window, fg_color=Colors.BG_DARK, corner_radius=8)
        support_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            support_frame,
            text="Tools Available",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=Colors.TEXT_PRIMARY
        ).pack(pady=(15, 5))

        tools_text = """
Available Tools:
• write_file - Create/overwrite files
• delete_file - Delete files
• read_file - Read file contents
• list_directory - List directory contents
        """
        ctk.CTkLabel(
            support_frame,
            text=tools_text,
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
            height=34,
            corner_radius=6,
            font=ctk.CTkFont(size=12),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            text_color="white"
        ).pack(pady=20)

    def _change_api_key(self, parent_window):
        """Change API key dialog."""
        dialog = ctk.CTkToplevel(parent_window)
        dialog.title("Change API Key")
        dialog.geometry("450x350")
        dialog.configure(fg_color=Colors.BG_DARK)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Enter New API Key",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=Colors.TEXT_PRIMARY
        ).pack(pady=20)

        entry = ctk.CTkEntry(
            dialog,
            placeholder_text="Paste API key here...",
            show="*",
            font=ctk.CTkFont(size=13),
            height=44,
            corner_radius=6,
            fg_color=Colors.BG_DARK,
            text_color=Colors.TEXT_PRIMARY,
            width=400
        )
        entry.pack(pady=10)

        # Hint
        ctk.CTkLabel(
            dialog,
            text="Get key from: https://freemodelsforall.hopto.org/",
            font=ctk.CTkFont(size=10),
            text_color=Colors.ACCENT,
            cursor="hand2"
        ).pack()
        dialog.children[list(dialog.children.keys())[-1]].bind("<Button-1>", lambda e: self._open_api_guide())

        def save_new_key():
            new_key = entry.get().strip()
            if new_key:
                save_api_key(new_key)
                self.api_key = new_key
                self._initialize_client()
                dialog.destroy()
                self._show_settings()
                self._set_status("✅ API key updated!")

        ctk.CTkButton(
            dialog,
            text="Save",
            command=save_new_key,
            width=100,
            height=36,
            corner_radius=6,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            text_color="white"
        ).pack(pady=20)

    def _show_api_setup(self):
        """Show API key setup dialog."""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("API Key Setup")
        dialog.geometry("500x400")
        dialog.configure(fg_color=Colors.BG_DARK)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="🔑 API Key Setup",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=Colors.TEXT_PRIMARY
        ).pack(pady=20)

        setup_text = """
To use AI Canvas, you need an API key from the gateway.

Step 1: Visit https://freemodelsforall.hopto.org/
Step 2: Sign up or log in
Step 3: Copy your API key
Step 4: Paste it below and click Save

Your key is stored securely and never shared.
        """
        ctk.CTkLabel(
            dialog,
            text=setup_text,
            font=ctk.CTkFont(size=12),
            text_color=Colors.TEXT_SECONDARY,
            justify="left"
        ).pack(pady=10)

        entry = ctk.CTkEntry(
            dialog,
            placeholder_text="Paste your API key here...",
            show="*",
            font=ctk.CTkFont(size=13),
            height=44,
            corner_radius=6,
            fg_color=Colors.BG_DARK,
            text_color=Colors.TEXT_PRIMARY,
            width=440
        )
        entry.pack(pady=10)

        def save_key():
            new_key = entry.get().strip()
            if new_key:
                save_api_key(new_key)
                self.api_key = new_key
                self._initialize_client()
                dialog.destroy()
                self._set_status("✅ API key configured!")
            else:
                self._show_error("Please enter an API key!")

        ctk.CTkButton(
            dialog,
            text="Save API Key",
            command=save_key,
            width=200,
            height=36,
            corner_radius=6,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            text_color="white"
        ).pack(pady=15)

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
            text_color=Colors.ERROR_COLOR,
            justify="center"
        ).pack(pady=30)

        ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy,
            width=80,
            height=32,
            corner_radius=6,
            font=ctk.CTkFont(size=12),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            text_color="white"
        ).pack()

    def _set_status(self, message):
        """Update status bar."""
        self.status_label.configure(text=message)

    def _create_icon(self):
        """Create application icon from file or generate fallback."""
        # Try to load the actual icon file first
        icon_paths = [
            "/opt/ai-canvas/icons/ai-canvas-icon.png",
            "/usr/share/icons/hicolor/256x256/apps/ai-canvas.png",
            "/usr/share/icons/hicolor/128x128/apps/ai-canvas.png",
        ]
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    return ImageTk.PhotoImage(Image.open(icon_path))
                except:
                    continue
        
        # Fallback: generate simple icon
        size = 64
        image = Image.new('RGBA', (size, size), (13, 17, 23, 255))
        draw = ImageDraw.Draw(image)
        
        # Gradient circle
        for i in range(size // 2):
            r = int(88 + (90 - 88) * i / (size // 2))
            g = int(166 + (160 - 166) * i / (size // 2))
            b = int(255 + (255 - 255) * i / (size // 2))
            draw.ellipse(
                [(size // 2 - i, size // 2 - i), (size // 2 + i, size // 2 + i)],
                outline=(r, g, b, 255),
                width=2
            )
        
        # AI text
        draw.text((size // 2 - 8, size // 2 - 10), "AI", fill=(255, 255, 255, 255))
        
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
    print("\n" + "═" * 70)
    print("  ✨ AI Canvas - Starting...")
    print("  API Portal: https://freemodelsforall.hopto.org/")
    print("═" * 70 + "\n")

    app = AICanvasApp()
    app.run()
