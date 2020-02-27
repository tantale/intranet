<%inherit file="local:templates.master"/>
<%
import re
mf = re.compile(r'(</?)script', re.IGNORECASE)
def fixmessage(message):
    return mf.sub(r'\1noscript', message)
%>

<%def name="title()">Erreur ${code}</%def>

<p>${fixmessage(message) | n}</p>
