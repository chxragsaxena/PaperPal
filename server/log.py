import logging
def setup_logger(name="JioGPT"):
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)
	
	conhandler = logging.StreamHandler()
	conhandler.setLevel(logging.DEBUG)
	
	formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
	conhandler.setFormatter(formatter)
	
	if not logger.hasHandlers():
		logger.addHandler(conhandler)
	return logger
	

logger = setup_logger()