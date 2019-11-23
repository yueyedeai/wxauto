import os
import logging

os.makedirs('../logs', exist_ok=True)


def log(name):
    # 创建logger，如果参数为空则返回root logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置logger日志等级
    filepath = "logs/{}.log".format(name)

    # 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
    if not logger.handlers:
        # 创建handler
        fh = logging.FileHandler(filepath, encoding="utf-8")
        ch = logging.StreamHandler()

        # 设置输出日志格式
        formatter = logging.Formatter(
            fmt="%(asctime)s\t%(name)s\t%(filename)s\t%(message)s",
            datefmt="%Y-%m-%d(%A) %X"
        )

        # 为handler指定输出格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 为logger添加的日志处理器
        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger  # 直接返回logger


if __name__ == "__main__":
    logger = log('test')
    logger.warning("泰拳警告")
    logger.info("提示")
    logger.error("错误")
    logger.debug("查错")
