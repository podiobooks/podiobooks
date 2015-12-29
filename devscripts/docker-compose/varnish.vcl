vcl 4.0;

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