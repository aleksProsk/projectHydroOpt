from RestrictedPython import compile_restricted_function, safe_builtins, limited_builtins, utility_builtins

someglobalvar = 123

myscript = """
import math
import tempfile
import io

#folgende befehle fuehren zu fehlern
#f = open("app.py", "rb")
#f = NamedTemporaryFile(delete=False)

def g(x):
	#return x + 1 + someglobalvar <--- kein Zugriff auf someglobalvar moeglich
	return h(x + 1)
	
result = math.exp(g(f(data)))
return result
"""

#globale variablen innerhalb der sandbox
safe_locals = {}
safe_globals = safe_builtins
additional_globals = {'data' : 2, 'f' : lambda x: x**2}
safe_globals.update(additional_globals)

#Kompilieren der Hauptfunktion
main_function_name = 'main'
main_function_compiled = compile_restricted_function(p = '', body = myscript, name = main_function_name, filename = '<inline code>')

#Kompilieren der Hilfsfunktion
support_function_name = 'h'
support_function_parameters = 'x'
support_function_body = 'return -x'
support_function_compiled = compile_restricted_function(p = support_function_parameters, body = support_function_body, name = support_function_name, filename = '<inline code>')

#Erstellen des Funktionszeigers der Hilfsfunktion
exec(support_function_compiled.code, safe_globals, safe_locals)
support_function_compiled_pointer = safe_locals[support_function_name]

print((support_function_compiled_pointer(123))) #Test der Hilfsfunktion

#Hinzufuegen der Hilfsfunktion zu den globalen Variablen der Sandbox, damit diese genutzt werden kann
updated_globals = {support_function_name : support_function_compiled_pointer}
safe_globals.update(updated_globals)

#Erzeugen des Funktionszeigers der Hauptfunktion
exec(main_function_compiled.code, safe_globals, safe_locals)
main_compiled_pointer = safe_locals[main_function_name]

print(main_compiled_pointer(*[], **{})) #Test der Hauptfunktion

#update der globalen variable 'data' 
updated_globals = {'data' : 3}
safe_globals.update(updated_globals)

#update von 'h'
support_function_compiled = compile_restricted_function(p = support_function_parameters, body = 'return +x', name = support_function_name, filename = '<inline code>')
exec(support_function_compiled.code, safe_globals, safe_locals)
support_function_compiled_pointer = safe_locals[support_function_name]
updated_globals = {support_function_name : support_function_compiled_pointer}
safe_globals.update(updated_globals)

#erneute Kompilierung
import types
main_compiled_update_pointer = types.FunctionType(
	main_compiled_pointer.__code__,
	safe_globals,
	'<' + main_function_name + '>',
	main_compiled_pointer.__defaults__ or ())

print(main_compiled_update_pointer(*[], **{})) #Test der Hauptfunktion
