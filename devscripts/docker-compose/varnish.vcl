/*
*
* First, set up a backend to answer the request if there's not a cache hit.
*
*/
backend default {

    # Set a host.
    .host = "nginx";

    # Set a port. 80 is normal Web traffic.
    .port = "9000";
}
/*
*
* Next, configure the "receive" subroutine.
*
*/
sub vcl_recv {

  # unless sessionid/csrftoken is in the request, don't pass ANY cookies (referral_source, utm, etc)
  if (req.request == "GET" && (req.url ~ "^/static" || (req.http.cookie !~ "sessionid" && req.http.cookie !~ "csrftoken"))) {
    remove req.http.Cookie;
  }

  # normalize accept-encoding to account for different browsers
  # see: https://www.varnish-cache.org/trac/wiki/VCLExampleNormalizeAcceptEncoding
  if (req.http.Accept-Encoding) {
    if (req.http.Accept-Encoding ~ "gzip") {
      set req.http.Accept-Encoding = "gzip";
    } elsif (req.http.Accept-Encoding ~ "deflate") {
      set req.http.Accept-Encoding = "deflate";
    } else {
      # unkown algorithm
      remove req.http.Accept-Encoding;
    }
  }

}
/*
*
* Next, let's set up the subroutine to deal with cache misses.
*
*/
sub vcl_miss {

    # We're not doing anything fancy. Just pass the request along to the
    # subroutine which will fetch something from the backend.
    return(fetch);
}
/*
*
* Now, let's set up a subroutine to deal with cache hits.
*
*/
sub vcl_hit {

    # Again, nothing fancy. Just pass the request along to the subroutine
    # which will deliver a result from the cache.
    return(deliver);
}
/*
*
* This is the subroutine which will fetch a response from the backend.
* It's pretty fancy because this is where the basic logic for caching is set.
*
*/
sub vcl_fetch {

  # static files always cached
  if (req.url ~ "^/static") {
       unset beresp.http.set-cookie;
       return (deliver);
  }

  # pass through for anything with a session/csrftoken set
  if (beresp.http.set-cookie ~ "sessionid" || beresp.http.set-cookie ~ "csrftoken") {
    return (pass);
  } else {
    return (deliver);
  }

}
/*
*
* Finally, let's set up a subroutine which will deliver a response to the client.
*
*/
sub vcl_deliver {
    # Nothing fancy. Just deliver the goods.
    # Note: Both cache hits and cache misses will use this subroutine.
    return(deliver);
}