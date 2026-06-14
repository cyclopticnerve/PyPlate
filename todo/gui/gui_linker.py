in = ui.xml
out = handler.py
scan xml for props like "onclick"
if not in handler, make
handler has ref to main.py
main.py creates instance of handler with ref to self
main sets builder.handler to handler obj
