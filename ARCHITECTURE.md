📄 ARCHITECTURE.md
markdown
# 🏗️ System Architecture

## High-Level Architecture
┌─────────────────────────────────────────────────────────────────────────────────┐
│ FLUTTER FRONTEND │
│ ┌───────────────────────────────────────────────────────────────────────────┐ │
│ │ UI Layer (Riverpod) │ │
│ │ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │ │
│ │ │Dashboard │ │Designer │ │Monitor │ │Market │ │Debugger │ │ │
│ │ │ (P0-P2) │ │ (P2) │ │ (P0-P2) │ │ (P2) │ │ (P0) │ │ │
│ │ └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │ │
│ └───────────────────────────────────────────────────────────────────────────┘ │
│ ┌───────────────────────────────────────────────────────────────────────────┐ │
│ │ Service Layer │ │
│ │ • WebSocket Client (Real-time logs, debug, monitoring) │ │
│ │ • REST API Client (Workflow CRUD, triggers) │ │
│ │ • Local Database (SQLite via drift) │ │
│ │ • Sync Engine (Supabase Realtime) │ │
│ └───────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
│
WebSocket (ws://) + REST (http://)
│
▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PYTHON BACKEND │
│ ┌───────────────────────────────────────────────────────────────────────────┐ │
│ │ FastAPI Application (Uvicorn) │ │
│ │ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ │ │
│ │ │ WebSocket Manager│ │ REST Endpoints │ │ Auth Middleware │ │ │
│ │ │ (logs, debug) │ │ (workflows/jobs) │ │ (JWT/Supabase) │ │ │
│ │ └──────────────────┘ └──────────────────┘ └──────────────────┘ │ │
│ └───────────────────────────────────────────────────────────────────────────┘ │
│ │
│ ┌───────────────────────────────────────────────────────────────────────────┐ │
│ │ Core Modules (by Priority) │ │
│ │ │ │
│ │ ✅ COMPLETED (Phase 0) │ │
│ │ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ │ │
│ │ │ Vision │ │ Input │ │ Bot │ │ UI │ │ │
│ │ │ Engine │ │ Controller │ │ Core │ │ (CTk) │ │ │
│ │ └────────────┘ └────────────┘ └────────────┘ └────────────┘ │ │
│ │ │ │
│ │ 🔄 P0 - CRITICAL (Phase 1) │ │
│ │ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ │ │
│ │ │ Debugger │ │ Smart │ │ Parallel │ │ Monitor │ │ │
│ │ │ (Visual) │ │ Wait │ │ Executor │ │ (Health) │ │ │
│ │ └────────────┘ └────────────┘ └────────────┘ └────────────┘ │ │
│ │ │ │
│ │ 🔄 P1 - HIGH PRIORITY (Phase 2) │ │
│ │ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ │ │
│ │ │ Recorder │ │ Hybrid │ │ Multi- │ │ Commander │ │ │
│ │ │ │ │ Vision │ │ Profile │ │ │ │ │
│ │ └────────────┘ └────────────┘ └────────────┘ └────────────┘ │ │
│ │ ┌────────────┐ │ │
│ │ │ API │ │ │
│ │ │ Gateway │ │ │
│ │ └────────────┘ │ │
│ │ │ │
│ │ 🔄 P2 - MEDIUM PRIORITY (Phase 3) │ │
│ │ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ │ │
│ │ │ Analytics │ │ Breakpoint │ │ Data-Driven│ │ Browser │ │ │
│ │ │ Dashboard │ │ │ │ │ │ Extension │ │ │
│ │ └────────────┘ └────────────┘ └────────────┘ └────────────┘ │ │
│ │ ┌────────────┐ ┌────────────┐ │ │
│ │ │ Visual │ │ Export │ │ │
│ │ │ Scripting │ │ Formats │ │ │
│ │ └────────────┘ └────────────┘ │ │
│ │ │ │
│ │ 📋 P3 - LOW PRIORITY (Phase 4 - Post v1.0) │ │
│ │ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ │ │
│ │ │ Plugin │ │ Model │ │ Region │ │ Asset │ │ │
│ │ │ System │ │ Zoo │ │ Learning │ │ Management │ │ │
│ │ └────────────┘ └────────────┘ └────────────┘ └────────────┘ │ │
│ │ ┌────────────┐ ┌────────────┐ │ │
│ │ │ Dependency │ │ Test │ │ │
│ │ │ Manager │ │ Mode │ │ │
│ │ └────────────┘ └────────────┘ │ │
│ │ │ │
│ │ 🔮 FUTURE (Post v1.0 - Advanced) │ │
│ │ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ │ │
│ │ │ AI │ │ Self- │ │Reinforce- │ │ Active │ │ │
│ │ │ Decision │ │ Healing │ │ ment │ │ Learning │ │ │
│ │ └────────────┘ └────────────┘ └────────────┘ └────────────┘ │ │
│ │ ┌────────────┐ ┌────────────┐ ┌────────────┐ │ │
│ │ │ Multi- │ │ Multi- │ │ Human-in- │ │ │
│ │ │ Model │ │ Tenancy │ │ the-Loop │ │ │
│ │ │ Ensemble │ │ │ │ │ │ │
│ │ └────────────┘ └────────────┘ └────────────┘ │ │
│ └───────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
│
┌─────────────────────────────────┼─────────────────────────────────┐
▼ ▼ ▼
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│ SQLite (Local) │ │ Supabase (Cloud) │ │ ADB Bridge │
│ • Workflows │ │ • User accounts │ │ • Android │
│ • Logs │ │ • Sync metadata │ │ • Touch events │
│ • Debug data │ │ • Templates │ │ • Screenshots │
│ • Analytics │ │ • Models (Zoo) │ │ • UI hierarchy │
│ • Monitoring │ │ • Webhooks │ │ │
└───────────────────┘ └───────────────────┘ └───────────────────┘

text

---

## Module Details (by Priority)

### 🔄 P0 - Critical (Phase 1)

#### 1. Visual Workflow Debugger (`src/debugger/`)

```python
class WorkflowDebugger:
    """
    Real-time debugging and visualization.
    
    Features:
    - Screenshot timeline (before/after each action)
    - Action replay with playback controls
    - Live overlay (bounding boxes, click coordinates)
    - Variable watch window
    - Execution step-by-step
    - Debug session storage
    """
    
    def capture_state(self):
        """Save current screen + variables + logs"""
        pass
    
    def replay(self, session_id: str):
        """Replay recorded execution"""
        pass
    
    def show_overlay(self):
        """Draw bounding boxes and info on screen"""
        pass
2. Smart Wait Strategies (src/wait/)
python
class SmartWait:
    """
    Intelligent waiting mechanisms.
    
    Strategies:
    - wait_for_element (by vision/template/OCR)
    - wait_for_text (appear/disappear)
    - wait_for_pixel_color (change detection)
    - wait_for_sound (game automation)
    - wait_for_network_idle (web)
    - wait_for_animation_complete
    - wait_for_condition (custom lambda)
    """
    
    def for_element(self, target, timeout=30, poll=0.5):
        """Wait until element appears"""
        pass
    
    def for_text(self, text, disappear=False, timeout=30):
        """Wait for text to appear or disappear"""
        pass
3. Parallel Execution Manager (src/parallel/)
python
class ParallelExecutor:
    """
    Manage concurrent workflow execution.
    
    Features:
    - Workflow queue with priority
    - Resource pool (CPU, GPU, memory)
    - Load balancing
    - Deadlock detection
    - Isolation between workflows
    """
    
    def __init__(self, max_workers=10):
        self.executor = ThreadPoolExecutor(max_workers)
        self.queue = PriorityQueue()
        self.active_workflows = {}
    
    async def submit(self, workflow, priority=5):
        """Submit workflow to queue"""
        pass
    
    def get_status(self):
        """Return active and queued workflows"""
        pass
4. Scheduled Screenshot Monitoring (src/monitor/)
python
class BotHealthMonitor:
    """
    Monitor bot health via screenshots.
    
    Features:
    - Periodic screenshot capture (every 30s)
    - Baseline comparison (normal state)
    - Crash detection (error popups, blue screen)
    - Auto-recovery (restart bot)
    - Alert notification
    """
    
    def __init__(self, interval=30):
        self.interval = interval
        self.baseline = None
    
    def set_baseline(self, screenshot):
        """Set normal state screenshot"""
        pass
    
    def check_health(self):
        """Compare current with baseline"""
        pass
    
    def auto_recover(self):
        """Attempt to restart bot"""
        pass
🔄 P1 - High Priority (Phase 2)
5. Workflow Recorder (src/recorder/)
python
class WorkflowRecorder:
    """
    Record user actions and generate workflows.
    
    Records:
    - Mouse movements, clicks, drags
    - Keyboard input
    - Screenshot on each action
    - Timestamps and delays
    
    Output:
    - JSON workflow definition
    - YAML with metadata
    - Python script (optional)
    """
    
    def start_recording(self):
        """Hook input events via pynput"""
        pass
    
    def stop_and_generate(self):
        """Convert recording to workflow"""
        pass
6. OCR + Vision Hybrid (Advanced) (src/vision/hybrid_detector.py)
python
class HybridDetector:
    """
    Combine multiple vision techniques with fallback.
    
    Strategies:
    - OCR text → YOLO region → Template confirm (3-stage)
    - YOLO detection → OCR read value
    - Template fallback → OCR fallback → coordinate (confidence-based)
    - Multi-stage with confidence threshold
    
    Returns higher accuracy than single method (target >99%).
    """
    
    def detect_button_by_text(self, text: str, confidence=0.8):
        """Multi-stage: OCR locate → YOLO verify → Template confirm"""
        pass
    
    def read_dynamic_value(self, region_type: str):
        """Detect region by YOLO, then OCR the value"""
        pass
7. Multi-Profile Management (src/profile/)
python
class ProfileManager:
    """
    Manage multiple identities to avoid detection.
    
    Profile includes:
    - Browser fingerprint (user agent, resolution, timezone, language)
    - Mouse pattern (speed, acceleration, curve intensity)
    - Typing pattern (WPM, backspace frequency, pause distribution)
    - Schedule pattern (active hours, break schedule)
    - Network pattern (proxy, IP rotation)
    """
    
    def load_profile(self, name: str):
        """Load profile configuration"""
        pass
    
    def apply_to_bot(self):
        """Apply profile settings to running bot"""
        pass
    
    def generate_random_profile(self):
        """Create random realistic profile"""
        pass
8. Telegram/Discord Commander (src/commander/)
python
class BotCommander:
    """
    Remote control via chat platforms.
    
    Commands:
    /start [workflow] - Start workflow
    /stop - Emergency stop
    /pause - Pause execution
    /resume - Resume execution
    /status - Current state and metrics
    /log [lines] - Recent logs
    /screenshot - Current screen
    /stats - Performance metrics
    /restart - Restart bot
    /workflows - List available workflows
    """
    
    async def handle_command(self, command: str, user_id: str):
        """Process chat command with authentication"""
        pass
    
    async def send_notification(self, message: str, level="info"):
        """Send alert to user"""
        pass
9. API Gateway & Webhook (src/api/)
python
class APIGateway:
    """
    REST API for external integration.
    
    Endpoints:
    POST /api/execute - Execute workflow
    POST /api/webhook/{id} - Trigger via webhook
    GET /api/status/{execution_id} - Check status
    POST /api/data - Push data to bot
    GET /api/workflows - List workflows
    POST /api/schedule - Create schedule
    """
    
    async def execute_workflow(self, workflow_id, data=None):
        """Execute workflow via API"""
        pass
    
    async def webhook_handler(self, request):
        """Handle incoming webhook"""
        pass
🔄 P2 - Medium Priority (Phase 3)
10. Workflow Analytics Dashboard (src/analytics/)
python
class AnalyticsEngine:
    """
    Track and visualize bot performance.
    
    Metrics:
    - Success rate by action/workflow
    - Average execution time
    - CPU/Memory usage timeline
    - Error heatmap (which step fails most)
    - Peak hours analysis
    - Performance trends over time
    """
    
    def record_execution(self, workflow_id, result, metrics):
        """Store execution data"""
        pass
    
    def generate_report(self, timeframe: str, format="html"):
        """Generate performance report"""
        pass
11. Conditional Breakpoints (src/debugger/breakpoint.py)
python
class BreakpointManager:
    """
    Pause execution when conditions met.
    
    Conditions:
    - value > threshold / < threshold / == value
    - iteration count reached
    - time of day
    - screen content matches template
    - error occurs
    - custom lambda expression
    """
    
    def on_value(self, var_name, operator, value):
        """Break when variable meets condition"""
        pass
    
    def on_screen(self, template_path, confidence=0.8):
        """Break when screen matches template"""
        pass
12. Variable Injection & Data-Driven (src/engine/data_driven.py)
python
class DataDrivenRunner:
    """
    Run workflow with multiple data sets.
    
    Data sources:
    - CSV file (each row = one execution)
    - JSON array
    - Database query (SQLite, Supabase)
    - API endpoint (REST)
    - Excel spreadsheet
    """
    
    def run_with_csv(self, workflow, csv_path):
        """Execute workflow for each CSV row"""
        pass
    
    def run_with_dataframe(self, workflow, dataframe):
        """Execute with pandas DataFrame"""
        pass
13. Browser Extension (extension/)
javascript
// Chrome/Edge extension for web automation
class WebRecorder {
    // Features:
    // - DOM element capture with XPath/CSS selectors
    // - Action recording (clicks, inputs, scrolls)
    // - Screenshot on each action
    // - Workflow export to JSON
    // - Sync with desktop app via WebSocket
}
14. Visual Scripting (No-Code) (src/visual_scripting/)
python
class VisualWorkflowBuilder:
    """
    Drag-drop workflow builder.
    
    Block types:
    - Trigger: schedule, file, webhook, hotkey
    - Vision: detect, read text, wait for element
    - Action: click, type, scroll, hotkey, file op
    - Logic: if/else, loop, wait, break, try/catch
    - Data: variable, clipboard, CSV, JSON, API
    - Flow: sub-workflow, parallel, sequence
    """
    
    def compile_to_json(self, blocks):
        """Convert visual blocks to workflow JSON"""
        pass
15. Export to Multiple Formats (src/export/)
python
class ExportManager:
    """
    Export data and reports to multiple formats.
    
    Formats:
    - Video recording (MP4) with annotations
    - HTML report with charts and timeline
    - PDF with screenshots
    - Excel with data and charts
    - CSV/JSON for raw data
    - Telegram notification with summary
    """
    
    def export_video(self, debug_session_id, output_path):
        """Create video from debug session"""
        pass
    
    def export_report(self, workflow_id, format="html"):
        """Generate execution report"""
        pass
📋 P3 - Low Priority (Post v1.0)
16. Plugin System (src/plugins/)
python
class PluginManager:
    """
    Load community extensions.
    
    Plugin hooks:
    - on_before_execution
    - on_after_action
    - on_element_detected
    - on_error
    - on_screenshot
    - on_workflow_complete
    """
    
    def load_plugin(self, plugin_path):
        """Load and initialize plugin"""
        pass
17. Cloud Model Zoo (src/model_zoo/)
python
class ModelZoo:
    """
    Share and download trained models.
    
    Categories:
    - Game UI (health bars, minimap, inventory)
    - Office apps (Excel cells, Word buttons)
    - Web elements (login forms, modals)
    - Mobile UI (app icons, gesture areas)
    - Custom (user-trained)
    """
    
    def download_model(self, category: str, name: str):
        """Download model from Supabase"""
        pass
18. Screen Region Learning (src/vision/region_learning.py)
python
class RegionLearner:
    """
    Learn element locations over time.
    
    Features:
    - Region memory (cache successful locations)
    - Adaptive search (expand if not found)
    - Confidence heatmap (hot zones)
    - Auto-calibration (resolution changes)
    """
    
    def remember_region(self, element_id, coordinates):
        """Store successful detection location"""
        pass
    
    def predict_region(self, element_id):
        """Predict most likely location"""
        pass
🔮 Future (Post v1.0 Advanced)
19. AI Decision Engine
20. Self-healing Workflows
21. Reinforcement Learning
22. Active Learning
23. Multi-model Ensemble
24. Custom CNN Training
25. Multi-Tenancy & User Management
26. Human-in-the-Loop
Database Schema (Updated)
SQLite (Local)
sql
-- Workflows
CREATE TABLE workflows (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    definition JSON NOT NULL,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    sync_status TEXT
);

-- Executions
CREATE TABLE executions (
    id TEXT PRIMARY KEY,
    workflow_id TEXT,
    status TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    logs JSON,
    screenshots TEXT,
    analytics JSON,
    metrics JSON,
    FOREIGN KEY (workflow_id) REFERENCES workflows(id)
);

-- Debug sessions
CREATE TABLE debug_sessions (
    id TEXT PRIMARY KEY,
    execution_id TEXT,
    step_index INTEGER,
    variables JSON,
    screenshot_path TEXT,
    timestamp TIMESTAMP
);

-- Monitoring snapshots
CREATE TABLE monitoring_snapshots (
    id TEXT PRIMARY KEY,
    timestamp TIMESTAMP,
    screenshot_path TEXT,
    health_status TEXT,
    detection_result JSON
);

-- Analytics
CREATE TABLE analytics (
    id TEXT PRIMARY KEY,
    date DATE,
    metric_name TEXT,
    value REAL,
    workflow_id TEXT
);

-- Profiles
CREATE TABLE profiles (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    config JSON NOT NULL,
    is_active BOOLEAN DEFAULT 0
);
Communication Protocol
WebSocket Messages (Updated)
json
// Debug message with screenshot
{
    "type": "debug",
    "action": "click",
    "coordinates": [100, 200],
    "screenshot": "base64...",
    "variables": {"hp": 85},
    "timestamp": "2024-01-01T12:00:00Z"
}

// Monitoring alert
{
    "type": "monitor",
    "level": "warning|critical",
    "message": "Crash detected",
    "screenshot": "base64...",
    "recovery_action": "restarting"
}

// Analytics
{
    "type": "analytics",
    "workflow_id": "abc123",
    "success": true,
    "duration_ms": 5000,
    "steps": 15,
    "cpu_usage": 25,
    "memory_usage": 512
}
Security Architecture (Updated)
Layer   Measures
Authentication  JWT tokens, biometric (mobile), session management, API keys
Encryption  SQLite encryption, TLS 1.3, credential vault (keyring)
Authorization   RBAC (admin/user/viewer), workflow-level permissions, API rate limiting
Privacy Local-first, sensitive data never leaves device, audit logs
Webhook Security    Signature verification, IP whitelisting
Performance Optimization
Component   Optimization
Vision  ONNX runtime, GPU acceleration, model quantization, caching
Debug   Screenshot compression, async storage, incremental saving
Parallel    Thread pooling, process isolation, GPU sharing
Database    Connection pooling, batch operations, indexing
Network Compression, binary protocols, caching, WebSocket keep-alive
UI  Lazy loading, virtual scrolling, isolates (Flutter)
Execution   Asyncio, thread pooling, process isolation
text