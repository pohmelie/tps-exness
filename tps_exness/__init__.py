from importlib import resources

VERSION = resources.read_text("tps_exness", "version.txt").strip()
