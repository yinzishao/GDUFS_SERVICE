from http.cookiejar import LWPCookieJar
from urllib import request, parse


CHARSET = 'utf-8'
FORM_URL = 'http://auth.gdufs.edu.cn/pkmslogin.form'

def login(username, password):
    cookie = LWPCookieJar()
    cookie_support = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(cookie_support , request.HTTPHandler)
    post_data = {'username':username, 'password':password, 'login-form-type':'pwd'}
    post_data = parse.urlencode(post_data).encode(CHARSET)
    req = request.Request(FORM_URL, post_data)
    try:
        opener.open(req).read().decode('utf-8')
    except:
        print("'%s's login was failed" % username)
        return None
    else:   
        print("%s's login was successful" % username)
        return cookie

COOKIE = '''Set-Cookie3: PD-ID="ufQROxGk5NVGDy+BS6EAHpsVgymWEnvJuPhMZ4hVF7pP1UN7y7vjbVntDDJwvP6WJt1G8yODUTHMAwp+yrPofhWu3nqttxSTcvSIrDUL2oq7P09V/5LDB8EIrteOCok7Qhaf8gkbLdxodCK9U7hn/2LNEViFu4eGZQAG/TS58z70XgvPQpXIf51TjkfIdSWr01pglZPoN5/RO3Q44DyOtNb1b5rCdGYxK4FG5uP1EkxHlzT81iGu5tnsc+hQoLn/NMfqKldBLjo="; path="/"; domain=".gdufs.edu.cn"; path_spec; domain_dot; discard; version=0
Set-Cookie3: PD-H-SESSION-ID="4_+a+HtbfLW1yUTtpyJ2szvdVcVHQ0Eio17aahObfwiF5FXp7t"; path="/"; domain="auth.gdufs.edu.cn"; path_spec; discard; version=0
'''
if __name__ == '__main__':
    print(login('20131003502', '').as_lwp_str(True, True))