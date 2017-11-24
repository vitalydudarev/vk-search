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

// contained in https://vk.com/js/cmodules/web/audioplayer.js

function o(t) {
    if (~t.indexOf("audio_api_unavailable")) {
        var e = t.split("?extra=")[1].split("#"),
            o = "" === e[1] ? "" : a(e[1]);
        if (e = a(e[0]), "string" != typeof o || !e) return t;
        o = o ? o.split(String.fromCharCode(9)) : [];
        for (var s, r, n = o.length; n--;) {
            if (r = o[n].split(String.fromCharCode(11)), s = r.splice(0, 1, e)[0], !l[s]) return t;
            e = l[s].apply(null, r)
        }
        if (e && "http" === e.substr(0, 4)) return e
    }
    return t
}

function a(t) {
    if (!t || t.length % 4 == 1) return !1;
    for (var e, i, o = 0, a = 0, s = ""; i = t.charAt(a++);) i = r.indexOf(i), ~i && (e = o % 4 ? 64 * e + i : i, o++ % 4) && (s += String.fromCharCode(255 & e >> (-2 * o & 6)));
    return s
}

function s(t, e) {
    var i = t.length,
        o = [];
    if (i) {
        var a = i;
        for (e = Math.abs(e); a--;) e = (i * (a + 1) ^ e + a) % i, o[a] = e
    }
    return o
}

var r = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN0PQRSTUVWXYZO123456789+/=",
l = {
    v: function(t) {
        return t.split("").reverse().join("")
    },
    r: function(t, e) {
        t = t.split("");
        for (var i, o = r + r, a = t.length; a--;) i = o.indexOf(t[a]), ~i && (t[a] = o.substr(i - e, 1));
        return t.join("")
    },
    s: function(t, e) {
        var i = t.length;
        if (i) {
            var o = s(t, e),
                a = 0;
            for (t = t.split(""); ++a < i;) t[a] = t.splice(o[i - 1 - a], 1, t[a])[0];
            t = t.join("")
        }
        return t
    },
    i: function(t, e) {
        return l.s(t, e ^ getCookie('vkUserId'))
    },
    x: function(t, e) {
        var i = [];
        return e = e.charCodeAt(0), each(t.split(""), function(t, o) {
            i.push(String.fromCharCode(o.charCodeAt(0) ^ e))
        }), i.join("")
    }
}

function decodeLink(url) {
    return o(url);
}