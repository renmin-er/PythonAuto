# common/logger.py

import logging
import os
from logging.handlers import TimedRotatingFileHandler

# --- 日志配置 ---
# 日志文件的路径和名称
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, 'automation.log')

# --- 创建一个logger ---
logger = logging.getLogger('automation_logger')
logger.setLevel(logging.INFO)  # 设置日志记录的最低级别

# --- 创建handler，用于写入日志文件 ---
# 使用 TimedRotatingFileHandler 可以让日志按时间自动切分，防止单个文件过大
# when='D' 表示每天切分一次, backupCount=7 表示保留最近7天的日志
file_handler = TimedRotatingFileHandler(
    filename=LOG_FILE,
    when='D',
    interval=1,
    backupCount=7,
    encoding='utf-8'
)
file_handler.setLevel(logging.INFO)

# --- 创建handler，用于输出到控制台 ---
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# --- 定义handler的输出格式 ---
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# --- 给logger添加handler ---
# 防止重复添加handler
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# --- 使用示例 (可以在其他文件中通过 `from common.logger import logger` 来使用) ---
if __name__ == '__main__':
    logger.debug("这是一条 debug 级别的日志，不会被记录，因为我们设置的最低级别是 INFO。")
    logger.info("测试开始...")
    logger.warning("发现一个潜在问题！")
    try:
        result = 1 / 0
    except Exception as e:
        logger.error(f"测试失败，发生异常: {e}", exc_info=True)
    logger.info("测试结束。")