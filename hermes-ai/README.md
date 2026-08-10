# Hermes AI Agent
## Built-in Agent Setup & Configuration

Hermes AI Agent handles the initial setup, API key configuration, and basic assistance for the Ubuntu XRDP environment.

**Features:**
- Simple terminal-based agent interface
- API key setup wizard
- System information queries
- Basic troubleshooting help
- Local mode (no API key needed)

**Usage:**
```bash
hermes-agent    # Launch Hermes agent
hermes-agent setup  # Run setup wizard
hermes-agent status  # Check status
```

---

# AI Canvas
## Full-Featured AI Desktop Application

**AI Canvas** is the main AI application with complete functionality - a beautiful GUI similar to Claude Desktop or other AI applications.

### Features

✅ **Beautiful Modern GUI**
- Dark theme interface like Claude Desktop
- Left sidebar with navigation
- Chat interface with streaming
- Model selection dropdown
- Settings panel

✅ **First-Run Setup Wizard**
- API key input with guided instructions
- Link to API key portal: https://freemodelsforall.hopto.org/
- Automatic validation and saving
- Secure credential storage

✅ **Complete AI Functionality**
- Real-time streaming chat
- Multiple model support via gateway
- Tool integration (file operations)
- Chat history management
- New chat creation

✅ **Available Tools**
- `write_file` - Create/overwrite files
- `delete_file` - Delete files
- `read_file` - Read file contents
- `list_directory` - List directory contents

✅ **Model Support**
- Fetches available models from gateway
- Falls back to hardcoded model list
- Default model selection (Claude Opus 5)
- Easy model switching via dropdown

### Workflow

```
1. Deploy Ubuntu XRDP container
2. Connect via RDP (localhost:3389)
3. Open Applications menu → AI Canvas
4. First time: API key setup wizard appears
   - Visit https://freemodelsforall.hopto.org/
   - Get API key
   - Paste in input box
   - Click Continue
5. AI Canvas opens with full functionality
6. Select model, start chatting!
```

### Usage

**From Desktop:**
- Open Applications menu
- Click "AI Canvas"

**From Terminal:**
```bash
ai-canvas
```

### Interface Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  AI Canvas                                      ⚙️ Settings   │
├──────────────┬───────────────────────────────────────────────────┤
│  MODEL       │                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Claude Opus 5 ▼                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                         │
│  CHATS                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 💬 Chat History                                   │   │
│  │                                                   │   │
│  │ • Conversation 1                            [📂] │   │
│  │ • Conversation 2                            [📂] │   │
│  │ • New Chat                                    [+] │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                         │
│  +----------------------------------------------------+ │
│  |  💬 Chat Area                                      | │
│  |                                                   | │
│  |  You: Hello!                                     | │
│  |  ✨ Hello! How can I help you today?             | │
│  |                                                   | │
│  |  You: Create a file test.txt with content Hello   │ │
│  |  ✨ [Thinking...]                                | │
│  |  ✨ ⚙️ Running tool write_file...                 | │
│  |  ✨ 📄 Success: File written to 'test.txt'       | │
│  |                                                   | │
│  +----------------------------------------------------+ │
│                                                         │
│  [Input field: Type your message...]         [Send]     │
└──────────────────────────────────────────────────────────────────┘
```

### API Key Setup

**First Launch:**
1. Welcome screen appears with API key input
2. Text explains where to get API key
3. Link: https://freemodelsforall.hopto.org/
4. Enter key and click Continue
5. Key validated and saved securely

**Key Storage:**
- Location: `~/.hermes-ai/credentials.json`
- Permissions: 600 (owner only)
- Environment variable also supported: `API_KEY` or `OPENAI_API_KEY`

### Models Available

The application fetches models from the gateway. If gateway is unavailable, falls back to:

- Claude Fable 5, Claude Opus 4/5, Claude Sonnet 5
- GPT-5 variants (4, 5, 5.6, etc.)
- DeepSeek V4 Flash/Pro
- Gemini 3 Pro/Flash
- GLM 5, Grok 4, and more

### Tool Execution

AI can use tools during conversation:

1. AI decides to use a tool
2. Tool name and arguments displayed
3. Tool executes
4. Result shown in chat
5. AI continues with tool output

Example:
```
You: Create a file /tmp/test.txt with content "Hello World"

AI: [Thinking with spinner...]
AI: ⚙️ Running tool write_file({"filepath": "/tmp/test.txt", "content": "Hello World"})...
AI: 📄 Success: File successfully written to '/tmp/test.txt' (11 chars).
```

### Error Handling

- API errors with retry logic (3 retries, exponential backoff)
- Tool compatibility fallback (if tools not supported, continue without)
- Invalid API key detection and prompt to reconfigure
- Network error handling with user-friendly messages
- Upstream gateway error detection

### Settings Panel

- API key configuration (change/update)
- Model information display
- Connection status
- Support links

---

## Technical Details

**GUI Framework:** CustomTkinter (modern Tkinter theme)
**AI Library:** OpenAI Python SDK (configured for custom gateway)
**Icons:** Custom SVG/PNG Hermes logo
**Theme:** Dark mode with purple accent colors

**Dependencies:**
- customtkinter>=5.2.2
- openai>=1.10.0
- Pillow>=10.0.0

---

## File Structure

```
ubuntu-xrdp/
├── Dockerfile
├── README.md
│
├── hermes-ai/                    # ← Hermes AI Agent (simple)
│   ├── main.py                    # Terminal agent
│   └── README.md                  # This file
│
├── ai-canvas/                    # ← AI Canvas (full GUI app)
│   ├── main.py                    # Main GUI application
│   ├── requirements.txt           # Python dependencies
│   └── icons/                     # Application icons
│
├── start.sh
└── pulse-client.conf
```

---

## Commands

```bash
# Launch Hermes AI Agent (simple)
hermes-agent

# Launch AI Canvas (full GUI)
ai-canvas

# Or directly
python3 /opt/ai-canvas/main.py
```
