from RestrictedPython import compile_restricted
from RestrictedPython import safe_builtins
from RestrictedPython.PrintCollector import PrintCollector
import platform

_print_ = PrintCollector

source_code = """
def f(x):
	return x

result = f(123)
"""

locals = {}

try:
	byte_code = compile_restricted(
		source		= source_code,
		filename	= '<inline>',
		mode		= 'exec'
	)
	exec(byte_code, safe_builtins, locals)

except SyntaxError as e:
	pass
	
print((locals['result']))
print((locals['f'](1)))