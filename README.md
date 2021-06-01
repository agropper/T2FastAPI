# T2FastAPI
* This is a staging repo for the standards-based [longitudinal health record project](https://github.com/HIEofOne/Trustee-Community). Check out the Trustee Community [wiki](https://github.com/HIEofOne/Trustee-Community/wiki) for background and a sequence diagram.
* Code gets pulled to Trustee Community only after it can run on DO App Platform.
* **Implementation notes are on the [wiki](https://github.com/agropper/T2FastAPI/wiki)**

Trustee is different from other health records in that it is self-sovereign to the patient. The Trustee is (soon to be) a [GNAP Authorization Server](https://www.ietf.org/archive/id/draft-ietf-gnap-core-protocol-05.html). Health record elements are W3C Verifiable Credentials (VC) and/or FHIR standard resources. W3C Decentralized Identifiers (DID) are used when practical. 

Here are the key Trustee components and API endpoints to be (eventually) demonstrated:
* Community Home: http://localhost:8081/ Where new patients subscribe to a Trustee or sign-in to an existing one.
  * The eventual authentication method (currently an unhashed password in CouchDB) is still TBD.
* Trustee Health Card: https://github.com/HIEofOne/Trustee-Community/blob/master/QFVC-QR.png A paper-compatible self-verifying W3C VC.
  * The Health Card will also be a minimal example of a GNAP-protected resource.
* HIE of One operates a CouchDB shared across all of the Trustee Communities for Trustee policy storage. Each patient's policies are encrypted with a patient-level key. HIE of One does not have the key.
  * The Trustee can only read policies from the shared CouchDB and decrypt them using a key stored in the Stripe Customer account.
  * Policies are written by the patient's user agent such as a Progressive Web App and/or PouchDB. 
* Health Records are GNAP-protected resources stored anywhere that respects the patient's Trustee-issued access tokens.
  * Health records discovery is not yet in-scope for this project. A link to a health record can be shared by the patient as email, text or a QR code.



Many thanks to Abdulazeez Abdulazeez Adeshina https://testdriven.io/blog/fastapi-jwt-auth/ and Ian Rufus https://www.youtube.com/channel/UCmRJyLjnQ035ng6XP295zXg for their fabulous tutorials that enabled this demonstration, so far.
