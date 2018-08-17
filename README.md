# Idea Pool API

In order requirements, I implemented some customizations to for JWT. I
updated things to match API documentation as closely as possible.

Two implementations are present: Simple JWT with DRF and a JWT solution
I built manually to mirror requirements.

The particular requirements that caused me to go with custom work are:

* Refresh token
* Custom endpoints (such as /me, /access-tokens, etc)

### TODO
1. Check that tokens are properly expiring
2. Deploy to Heroku
3. Email links