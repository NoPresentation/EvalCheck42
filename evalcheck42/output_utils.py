class C:
	OK = "\033[92m"
	FAIL = "\033[91m"
	INFO = "\033[94m"
	END = "\033[0m"


def ok(msg):
	print(f"\t{C.OK}✅ {msg}{C.END}")


def fail(msg):
	print(f"\t{C.FAIL}❌ {msg}{C.END}")


def info(msg):
	print(f"\t{C.INFO}⚠️ {msg}{C.END}")
