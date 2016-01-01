vcl 4.0;

import directors;

backend uwsgi {
   .host = "podiobooks_uwsgi";
   .port = "7000";
}

backend nginx {
   .host = "podiobooks_nginx";
   .port = "8080";
}

sub vcl_recv {
    # Proxy /static to nginx, everything else to uwsgi.
    if (req.url ~ "^/static|media/") {
        set req.backend_hint = nginx;
    } else {
        set req.backend_hint = uwsgi;
    }

    # Remove any Google Analytics based cookies
    set req.http.Cookie = regsuball(req.http.Cookie, "__utm.=[^;]+(; )?", "");
    set req.http.Cookie = regsuball(req.http.Cookie, "_ga=[^;]+(; )?", "");
    set req.http.Cookie = regsuball(req.http.Cookie, "_gat=[^;]+(; )?", "");
    set req.http.Cookie = regsuball(req.http.Cookie, "utmctr=[^;]+(; )?", "");
    set req.http.Cookie = regsuball(req.http.Cookie, "utmcmd.=[^;]+(; )?", "");
    set req.http.Cookie = regsuball(req.http.Cookie, "utmccn.=[^;]+(; )?", "");

    return(hash);
}

sub vcl_backend_response {
    # Set cached objects to expire after 1 hour instead of the default 120 seconds.
    set beresp.ttl = 1h;
}

sub vcl_deliver {
    if (obj.hits > 0) {
           set resp.http.X-Cache = "HIT";
    } else {
           set resp.http.X-Cache = "MISS";
    }
}