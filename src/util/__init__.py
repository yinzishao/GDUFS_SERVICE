HEADER = "Set-Cookie3:"
BOOLEAN_ATTRS = ("port_spec", "path_spec", "domain_dot",
                 "secure", "discard")
VALUE_ATTRS = ("version",
               "port", "path", "domain",
               "expires",
               "comment", "commenturl")

def cookie_from_str(cookie_str):
    from http.cookiejar import split_header_words, LWPCookieJar, LoadError, Cookie, iso2time
    import time
    
    cookie_str = cookie_str.split('\n')
    cookie = LWPCookieJar()
    
    index = 0
    while 1:

        line = cookie_str[index]
        index += 1
        if line == "": break
        if not line.startswith(HEADER):
            continue
        line = line[len(HEADER):].strip()

        for data in split_header_words([line]):
            name, value = data[0]
            standard = {}
            rest = {}
            for k in BOOLEAN_ATTRS:
                standard[k] = False
            for k, v in data[1:]:
                if k is not None:
                    lc = k.lower()
                else:
                    lc = None
                if (lc in VALUE_ATTRS) or (lc in BOOLEAN_ATTRS):
                    k = lc
                if k in BOOLEAN_ATTRS:
                    if v is None: v = True
                    standard[k] = v
                elif k in VALUE_ATTRS:
                    standard[k] = v
                else:
                    rest[k] = v

            h = standard.get
            expires = h("expires")
            discard = h("discard")
            if expires is not None:
                expires = iso2time(expires)
            if expires is None:
                discard = True
            domain = h("domain")
            domain_specified = domain.startswith(".")
            c = Cookie(h("version"), name, value,
                       h("port"), h("port_spec"),
                       domain, domain_specified, h("domain_dot"),
                       h("path"), h("path_spec"),
                       h("secure"),
                       expires,
                       discard,
                       h("comment"),
                       h("commenturl"),
                       rest)
            cookie.set_cookie(c)
    return cookie