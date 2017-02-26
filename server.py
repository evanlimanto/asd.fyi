from flask import Flask, request, redirect
import os
import redis

app = Flask(__name__) 
chars = [str(x) for x in range(10)] + [chr(x) for x in range(97, 123)]
r = redis.from_url(os.environ.get("REDIS_URL"))

html_escape_table = {
  "&": "&amp;",
  '"': "&quot;",
  "'": "&apos;",
  ">": "&gt;",
  "<": "&lt;",
}

def html_escape(text):
   return "".join(html_escape_table.get(c,c) for c in text)

def n_to_s(n):
	s = ""
	while n:
		s = s + chars[n % len(chars)]
		n = n // len(chars)
	return s

html1 = '''
<title>asd.fyi</title>
<style>
*{font-family:monospace;}
</style>
<script src="https://cdn.jsdelivr.net/clipboard.js/1.6.0/clipboard.min.js"></script>
<p>asd.fyi - share text.</p>
<form action="/" method="post">
<textarea name="t" rows="20" cols="80"></textarea>
<br/><br/>
<input class="s" type="submit" value="submit & copy to clipboard" 
data-clipboard-text="www.asd.fyi/'''

html2 = '''" />
</form>
<script>new Clipboard('.s');</script>
'''

@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
@app.route("/<path>")
def paste(path):
	curid = n_to_s(r.incr("id", 0) + 1)
	if path:
		return "<pre>%s</pre>" % (r.get(path).decode("utf-8"),)
	elif request.form.get("t"):	
		t = html_escape(str(request.form.get("t")))
		curid = n_to_s(r.incr("id", 1))
		r.set(curid, t)
		return redirect("/%s" % (curid,))
	return html1 + curid + html2

if __name__ == '__main__':
	app.run()
