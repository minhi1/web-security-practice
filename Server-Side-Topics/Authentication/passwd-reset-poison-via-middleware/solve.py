'''
Attempting posting a comment with simple XSS payload, nothing happens. So the input might be escaped or sanitized already.

What is the currently password reset logic in the web?
1. POST /forgot-password sends a reset link to email via username.
2. The link contains a token. GET /reset-password?temp-forgot-password-token=... shows a form to enter new password.
3. POST /reset-password?temp-forgot-password-token=... with new password resets it.
   Body: temp-forgot-password-token=xlt67zt5t4hh0ikdhwgrvazzqyl23hfo&new-password-1=uia256&new-password-2=uia256
   
Hmm, at step 3, the token is both in URL and body. Which one does it actually use? Let's test it.
-> It uses the token from the body.

Observe the HTML response of step 2, there's a code snippet like this:
<input required type=hidden name=temp-forgot-password-token value=9geayoass07paoiajaieqlzqbye0p447>

The token value from URL is reflected, so there might be a potential HTML injection vulnerability here. But it's not possible,
because the token is validated when sends a GET request to /reset-password?temp-forgot-password-token=...

A piece of information from the problem is that: The user carlos will carelessly click on any links in emails that he receives.

The token is created dynamically each time the user requests a password reset and it is attached on the URL.
So what if we can get the URL via our malicious server?
To do that, the only way now is to see if we can inject or manipulate the HTTP header when request a change password.
--> Search on Mozilla docs, find out that there is also another header called X-Forwarded-Host
which is used to identify the original host requested by the client in the Host HTTP request header.

Set the X-Forwarded-Host header to our malicious server when requesting password reset for carlos.
'''