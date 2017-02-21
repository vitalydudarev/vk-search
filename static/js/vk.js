function isObject(obj) { return Object.prototype.toString.call(obj) === '[object Object]'; }

function each(object, callback) {
  if (!isObject(object) && typeof object.length !== 'undefined') {
    for (var i = 0, length = object.length; i < length; i++) {
      var value = object[i];
      if (callback.call(value, i, value) === false) break;
    }
  } else {
    for (var name in object) {
      if (!Object.prototype.hasOwnProperty.call(object, name)) continue;
      if (callback.call(object[name], name, object[name]) === false)
        break;
    }
  }

  return object;
}

function e(t) {
    if (~t.indexOf("audio_api_unavailable")) {
        var i = t.split("?extra=")[1].split("#")
          , e = o(i[1]);
        if (i = o(i[0]),
        !e || !i)
            return t;
        e = e.split(String.fromCharCode(9));
        for (var a, r, l = e.length; l--; ) {
            if (r = e[l].split(String.fromCharCode(11)),
            a = r.splice(0, 1, i)[0],
            !s[a])
                return t;
            i = s[a].apply(null, r)
        }
        if (i && "http" === i.substr(0, 4))
            return i
    }
    return t
}

function o(t) {
    if (!t || t.length % 4 == 1)
        return !1;
    for (var i, e, o = 0, s = 0, r = ""; e = t.charAt(s++); )
        e = a.indexOf(e),
        ~e && (i = o % 4 ? 64 * i + e : e,
        o++ % 4) && (r += String.fromCharCode(255 & i >> (-2 * o & 6)));
    return r
}

var a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN0PQRSTUVWXYZO123456789+/="
  , s = {
    v: function(t) {
        return t.split("").reverse().join("")
    },
    r: function(t, i) {
        t = t.split("");
        for (var e, o = a + a, s = t.length; s--; )
            e = o.indexOf(t[s]),
            ~e && (t[s] = o.substr(e - i, 1));
        return t.join("")
    },
    x: function(t, i) {
        var e = [];
        return i = i.charCodeAt(0),
        each(t.split(""), function(t, o) {
            e.push(String.fromCharCode(o.charCodeAt(0) ^ i))
        }),
        e.join("")
    }
}

function decodeLink(url) {
    return e(url);
}