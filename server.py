from flask import Flask, request, redirect
import os
import redis

app = Flask(__name__) 
chars = [str(x) for x in range(10)] + [chr(x) for x in range(97, 123)]
r = redis.from_url(os.environ.get("REDIS_URL"))

def getid():
	return r.incr("id", 1)

def n_to_s(n):
	s = ""
	while n:
		s = s + chars[n % len(chars)]
		n = n // len(chars)
	return s

h1 = '''
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
data-clipboard-text="asd.fyi/'''

h2 = '''" />
</form>
<script>new Clipboard('.s');</script>
'''

curid = n_to_s(r.incr("id", 0) + 1)
html = h1 + curid + h2

@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
@app.route("/<path>")
def paste(path):
	if path:
		return "<pre>%s</pre>" % (r.get(path).decode("utf-8"),)
	elif request.form.get("t"):	
		t = request.form.get("t")
		curid = n_to_s(getid())
		r.set(curid, t)
		return redirect("/%s" % (curid,))
	return html

if __name__ == '__main__':
	app.run()
