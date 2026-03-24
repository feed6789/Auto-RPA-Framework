class WorkflowContext:
    """Holds the shared state for the workflow execution"""
    def __init__(self, vision, controller, waiter, logger):
        self.vision = vision
        self.controller = controller
        self.waiter = waiter
        self.logger = logger
        self.variables = {}
        self.is_paused = False
        self.is_running = True

class WorkflowEngine:
    """Executes a list of actions dynamically"""
    def __init__(self, context):
        self.context = context
        self.workflow_steps =[]

    def load_workflow(self, steps):
        self.workflow_steps = steps

    def execute(self):
        self.context.logger("[Engine] Starting workflow execution...")
        try:
            for i, step in enumerate(self.workflow_steps):
                # Handle pause state
                while self.context.is_paused:
                    time.sleep(0.5)
                if not self.context.is_running:
                    self.context.logger("[Engine] Execution stopped.")
                    break

                self.context.logger(f"[Engine] Step {i+1}: Executing {step.__class__.__name__}")
                
                # Execute action
                step.execute(self.context)
                
                # Built-in human delay between steps
                time.sleep(0.5)
                
            self.context.logger("[Engine] Workflow complete.")
        except Exception as e:
            self.context.logger(f"[Engine Error] Workflow failed: {e}")