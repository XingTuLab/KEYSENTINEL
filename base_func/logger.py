import json
import logging
def setup_logger(log_file):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # 清除已有的 handler
    for handler in logger.handlers:
        logger.removeHandler(handler)

    # 创建 FileHandler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # 创建日志消息格式
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            try:
                # Attempt to parse the message as JSON
                message_json = json.loads(record.getMessage())
                log_data = {
                    'timestamp': self.formatTime(record),
                    'level': record.levelname,
                    'message': message_json,
                }
            except json.JSONDecodeError:
                # If parsing fails, treat message as a plain string
                log_data = {
                    'timestamp': self.formatTime(record),
                    'level': record.levelname,
                    'message': record.getMessage(),
                }
            return json.dumps(log_data)

    formatter = JsonFormatter()
    file_handler.setFormatter(formatter)

    # 将 FileHandler 添加到记录器
    logger.addHandler(file_handler)

    return logger