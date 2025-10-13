import os
from datetime import datetime
import inspect
from config import LOG_LEVEL

log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "LOGFILE.log"))

class logger:
    def __init__(self, level=LOG_LEVEL, log_file=log_path):
        self.log_file = os.path.abspath(log_file)
        self.levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        self.level = level.upper()
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def _should_log(self, msg_level):
        return self.levels.index(msg_level) >= self.levels.index(self.level)

    def _format(self, msg, level):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Walk up the stack to find the first frame outside logger.py
        for frame_info in inspect.stack():
            filename = os.path.basename(frame_info.filename)
            if filename != os.path.basename(__file__):  # Skip logger.py
                caller_file = filename
                break
        else:
            caller_file = "unknown"

        return f"{timestamp} - {level} - {caller_file} - {msg}"

    def _write(self, formatted_msg):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(formatted_msg + "\n")

    def log(self, msg, level="INFO"):
        level = level.upper()
        if level not in self.levels:
            raise ValueError(f"Invalid log level: {level}")
        if self._should_log(level):
            formatted = self._format(msg, level)
            self._write(formatted)
            print(formatted)  # Optional: also print to console

    # Convenience methods
    def debug(self, msg): self.log(msg, "DEBUG")
    def info(self, msg): self.log(msg, "INFO")
    def warning(self, msg): self.log(msg, "WARNING")
    def error(self, msg): self.log(msg, "ERROR")
    def critical(self, msg): self.log(msg, "CRITICAL")