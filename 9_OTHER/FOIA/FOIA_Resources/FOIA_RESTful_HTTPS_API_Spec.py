"""
https://www.foia.gov/developer/agency-api/


FOIA.gov Draft RESTful HTTPS API Spec
This is a draft spec for integrating the FOIA.gov portal with existing FOIA case management systems operated by individual agencies in the federal government. This work stems from the interviews and research that led to our FOIA Portal Discovery Recommendations.

Once an agency’s case management system supports this specification, it can receive FOIA requests directly from the FOIA.gov portal, rather than having the request data sent to the agency via e-mail.

To minimize agency effort, we’ve designed this spec so that some of the tedious bits of implementing an API can be handled by a service like api.data.gov, which provides a free API management service for federal agencies.

Change Log
Version 1.1.0
Add the new field “pdf”, to contain an object with file data for a PDF version of the request
Add the new field “testing”, to indicate when a request came from a non-production environment
Receive a FOIA Request
Notes
This draft does not address:

versioning
size or rate limits
error message/status code related to exceeded the rate limit
any subsequent calls to the internal FOIA.gov API (to capture info needed to subsequently retrieve status, for example)
detailed security controls
Security controls
Once we have confidence in our data models and the touch points for interoperability, we will be working with the security team at DOJ to ensure the Portal meets the federal requirements for security controls. For now, we include only some preliminary ideas based on the agency feedback we’ve received.

Each agency will be responsible for implementing security controls on their own end as per their agency regulations and authority to operate. This may include configuration of a web application firewall, anti-virus scanning of file attachments, and validation of HTTP headers.

HTTPS
Agency endpoints should be restricted to HTTPS only with valid TLS certificates. The Portal will validate your certificate as part of the HTTPS request.

Authentication
To ensure that your API and case management system aren’t publicly writable, we recommend restricting your API access to the FOIA.gov Portal. This can be done via a shared secret HTTP header token. You will provide this secret token to the Portal though configuration. Every request from the Portal will include this token in the HTTP header FOIA-API-SECRET, and your API should validate that it is the correct token.

Services like api.data.gov provide this authentication for you and give you additional options.

URL
There are no required parameters or format for your API URL. You may choose any pathname you wish. If your system handles requests for multiple agency components (common for decentralized agencies), we recommend using a URL structure that explicitly identifies the agency component receiving the FOIA request. Your URL should not contain any query parameters.

Recommended URL format for decentralized agencies:

/components/:id/requests/
Where id is a unique identifier for a component within your agency.

For example:

/components/88/requests/
But not:

/requests?component=88
In addition, we recommend hosting the API on a dedicated sub-domain like foia-api.agency.gov. Using this kind of pathname hierarchy allows us to add additional API endpoints for future development and features.

Method:
POST

URL parameters
Required:

id=[integer], where id is the unique identifier of the agency component that should receive the request.

Data parameters
JSON payload that contains the form fields.

Content-Type: application/json
Request fields
Field:	version
Type:	string
Description:	The version of the API used for determining compatibility. Reserved for future use.
Required:	true
Example:	"1.1.0"
Field:	request_id
Type:	integer
Description:	A unique identifier for the request within the Portal.
Required:	true
Example:	1534
Field:	agency
Type:	string
Description:	Name of the tier 1 agency.
Required:	true
Example:	"Department of Justice"
Field:	agency_component_name
Type:	string
Description:	Name of the department, bureau, or office.
Required:	true
Example:	"Office of Information Policy"
Field:	name_first
Type:	string
Description:	First name of the requester.
Required:	false
Example:	"George"
Field:	name_last
Type:	string
Description:	Last name of the requester.
Required:	false
Example:	"Washington"
Field:	address_line1
Type:	string
Description:	Requester’s street mailing address.
Required:	false
Example:	"1800 F Street"
Field:	address_line2
Type:	string
Description:	Line 2 for requester’s mailing address.
Required:	false
Example:	"Suite 400"
Field:	address_city
Type:	string
Description:	City for requester’s mailing address.
Required:	false
Example:	"Mount Vernon"
Field:	address_country
Type:	string
Description:	Country for requester’s mailing address.
Required:	false
Example:	"United States"
Field:	address_state_province
Type:	string
Description:	State or province for requester’s mailing address.
Required:	false
Example:	"Virginia"
Field:	address_zip_postal_code
Type:	string
Description:	Zip code or postal code for requester’s mailing address.
Required:	false
Example:	"98273"
Field:	request_description
Type:	string
Description:	Description of the records the requester is seeking. This field should be set to a 10,000 character limit by default.
Required:	true
Example:	"I am seeking records pertaining to ..."
Field:	fee_amount_willing
Type:	string
Description:	The amount in USD that a requester is willing to pay in order to cover costs related to this request.
Required:	false
Example:	"25"
Field:	fee_waiver
Type:	string
Description:	The requester would like to request that fees associated with the request be waived.
Required:	no, defaults to "no"
Example:	"no"
Field:	fee_waiver_explanation
Type:	string
Description:	The justification for the fee waiver. This field should be set to a 10,000 character limit by default.
Required:	false
Example:	"As a journalist organization, I am requesting these records on behalf of the public and intend to make these records accesible to the public."
Field:	request_category
Type:	string
Description:	The claimed category of the requester.
Required:	false
Example:	"individual"
Field:	expedited_processing
Type:	string
Description:	The requester would like this request to be processed on an expedited basis.
Required:	no, defaults to "no"
Example:	"no"
Field:	expedited_processing_explanation
Type:	string
Description:	The justification for why expedited processing should be granted. This field should be set to a 10,000 character limit by default.
Required:	false
Example:	"The request should be given expedited processing because…"
Field:	company_organization
Type:	string
Description:	Name of the organization or company on which the requester is making a request on behalf of.
Required:	false
Example:	"Newspaper Inc"
Field:	email
Type:	string
Description:	Email address of the requester.
Required:	false
Example:	"george.washington@example.com"
Field:	phone_number
Type:	string
Description:	Phone number of the requester.
Required:	false
Example:	"+15551234567"
Field:	fax_number
Type:	string
Description:	Fax number of the requester.
Required:	false
Example:	"+15551234589"
Field:	attachments_supporting_documentation
Type:	object
Description:	Documents or attachments supporting the request provided by the requester. This field should be set to a 20MB size limit by default.
Required:	false
Example:	[{"filename": "letter.pdf", "content_type": "application/pdf", "filesize": 27556, "filedata": "YSBiYXNlNjQgZW5jb2RlZCBmaWxlCg=="}]
Field:	pdf
Type:	object
Description:	A version of the complete request, as a PDF file.
Required:	true
Example:	{"filename": "request.pdf", "content_type": "application/pdf", "filesize": 27556, "filedata": "YSBiYXNlNjQgZW5jb2RlZCBmaWxlCg=="}
Field:	testing
Type:	boolean
Description:	A boolean flag indicating whether or not this submission came from a non-production environment. This allows an endpoint to treat test submissions differently.
Required:	true
Example:	false
Field:	*
Type:	Determined by the [agency metadata file][agency-metadata-file-schema]. See [agency component specific form fields](#agency-component-specific-form-fields) below.
Description:	Agency component specific request form field as specified in your [agency's metadata file][agency-metadata-file-schema].
Required:	if applicable
Example:	See below.
Sample payload
{
    "version": "1.1.0",
    "request_id": 1534,
    "address_city": "Mount Vernon",
    "address_country": "United States",
    "address_line1": "1800 F Street",
    "address_line2": "Suite 400",
    "address_state_province": "Virginia",
    "address_zip_postal_code": "98273",
    "agency_component_name": "Office of Information Policy",
    "agency": "Department of Justice",
    "attachments_supporting_documentation": [{"filename": "letter.pdf", "content_type": "application/pdf", "filesize": 27556, "filedata": "YSBiYXNlNjQgZW5jb2RlZCBmaWxlCg=="}],
    "company_organization": "Newspaper Inc",
    "email": "george.washington@example.com",
    "expedited_processing_explanation": "The request should be given expedited processing because…",
    "expedited_processing": "no",
    "fax_number": "+15551234589",
    "fee_amount_willing": "25",
    "fee_waiver_explanation": "As a journalist organization, I am requesting these records on behalf of the public and intend to make these records accesible to the public.",
    "fee_waiver": "no",
    "name_first": "George",
    "name_last": "Washington",
    "phone_number": "+15551234567",
    "request_category": "individual",
    "request_description": "I am seeking records pertaining to ..."
}

Agency component specific form fields
Your agency component might have additional fields that are unique to your agency and are also captured in this request payload. If you have ever received any submissions via email, then you can consult these emails to see the machine-names of each field. If you have not yet received any of these emails, simply perform a test submission on the portal and consult the email that arrives.

Responses
Responses should be in application/json format and include an appropriate HTTP status code.

Success Response
Code:	200 OK
Content:	{ "id" : 33, "status_tracking_number": "doj-1234" }
Meaning:	Confirm that the request was created and return an id that can uniquely identify the request in the case management system. The status tracking number (required) will be sent to the requester and used to track a request in your case management system.
Error Response
Code:	404 NOT FOUND
Content:	{ "code" : "A234", "message" : "agency component not found", "description": "description of the error that is specific to the case management system"}
Meaning:	The target agency component specified in URI was not found (error payload includes a place for a system-specific message, to make it easier to track down problems)
Code:	500 INTERNAL SERVER ERROR
Content:	{ "code" : "500", "message" : "internal error", "description": "description of the error that is specific to the case management system"}
Meaning:	The case management system encountered an internal error when trying to create the FOIA request (error payload includes a place for a system-specific message, to make it easier to track down problems)
Sample request
$ curl -X POST -H "Content-Type: application/json" -d @- https://foia-api.agency.gov/components/234/requests <<EOF
{
    "version": "1.1.0",
    "request_id": 1534,
    "address_city": "Mount Vernon",
    "address_country": "United States",
    "address_line1": "1800 F Street",
    "address_line2": "Suite 400",
    "address_state_province": "Virginia",
    "address_zip_postal_code": "98273",
    "agency_component_name": "Office of Information Policy",
    "agency": "Department of Justice",
    "attachments_supporting_documentation": [{"filename": "letter.pdf", "content_type": "application/pdf", "filesize": 27556, "filedata": "YSBiYXNlNjQgZW5jb2RlZCBmaWxlCg=="}],
    "company_organization": "Newspaper Inc",
    "email": "george.washington@example.com",
    "expedited_processing_explanation": "The request should be given expedited processing because…",
    "expedited_processing": "no",
    "fax_number": "+15551234589",
    "fee_amount_willing": "25",
    "fee_waiver_explanation": "As a journalist organization, I am requesting these records on behalf of the public and intend to make these records accesible to the public.",
    "fee_waiver": "no",
    "name_first": "George",
    "name_last": "Washington",
    "phone_number": "+15551234567",
    "request_category": "individual",
    "request_description": "I am seeking records pertaining to ..."
}

EOF
Troubleshooting request failures
Various factors may cause a request submitted on FOIA.gov to an agency via API to fail. In these instances, the National FOIA Portal Administrator will inform the agency/component of the failure, and will pass along the error message. Agencies/components will coordinate with their tracking system vendor to analyze this error message and address the problem to prevent similar failures in the future. The following list contains common error messages that may be helpful in this analysis.

Additional info on CURL errors can be found here: libcurl - Error Codes.

Error message:	API URL for the component must use the HTTPS protocol.
Meaning:	The URL in the API configuration must be an https:// URL. Agency endpoints should be restricted to HTTPS only with valid TLS certificates. FOIA.gov will validate your certificate as part of the HTTPS request.
Error message:	Exception message: cURL error 28: Connection timed out after 30,001 milliseconds
Meaning:	Operation timeout. The specified time-out period was reached according to the conditions. FOIA.gov must receive a 200 Successful response from the tracking system within 30 seconds, otherwise it assumes the request failed to transmit and it will continue trying to send the request 5 times until it fatally fails.

Sometimes the request will actually submit and can be seen in the agency’s tracking system despite the failure on the FOIA.gov side resulting in 5 duplicate requests.

To address this, ensure that the 200 Success response is sent to FOIA.gov within 30,000 milliseconds (30 seconds). This requirement is detailed in the “Response” section of the API Specs.
Error message:	Exception message: cURL error 60: SSL certificate problem: unable to get local issuer certificate (see https://curl.haxx.se/libcurl/c/libcurl-errors.html).
Error message:	cURL error 60: SSL certificate problem: certificate has expired
Error message:	cURL error 60: SSL certificate problem: unable to get local issuer certificate (see https://curl.haxx.se/libcurl/c/libcurl-errors.html).
Meaning:	Requests from FOIA.gov are sent over the public internet and do not have access to an agency’s private network or intranet. The SSL certificate installed on the API endpoint must use a trusted certificate authority (cannot be self-signed). The agency may need to update the certificate information.
Error message:	404 Current IP Address is not allowed
Meaning:	Agency endpoints may have an allowlist of IP addresses as a security protection. Sometimes the FOIA.gov IP address has not been added to that allowlist, the endpoint returns an error message similar to this. The appropriate fix is to add the FOIA.gov IP addresses to the allowlist. The error description should identify the IP address that needs to be added to the allowlist.
Error message:	Did not receive JSON response from component.
Meaning:	This means the response sent to FOIA.gov was not in application/JSON format or was not sent at all.
Error message:	API security token not matched.
Meaning:	Agency endpoints require a secret key as a security protection. Sometimes the secret key that FOIA.gov is using does not match what is expected by the agency endpoint, and the endpoint returns an error message similar to this. The appropriate fix is to compare the expected secret key with the actual secret key to ensure that they match.
Error message:	Maximum request length exceeded.
Meaning:	Some agency tracking systems may have a maximum length for fields. Some FOIA.gov request form fields have a 10,000 character limit by default. This error may also indicate that attachment fields are not set to accept files up to 20 MB by default. Confirm that the request_description, fee_waiver_explanation, and expedited_processing_reason fields in your tracking system accept up to 10,000 characters, and that attachments_supporting_documentation accept files up to 20MB. (See “Request Fields” above for parameters.)

Developer Resources
The FOIA request Portal is powered by a public API. In order to use the API, you must signup for an API key here. Visit the Swagger page to view the structure of the FOIA API.

If your agency is interested in receiving requests from the Portal via an API, please check out our Agency API spec and get in touch with us.

Agency Components
Agencies of the federal government submit information about their FOIA process in a machine-readable format to the Portal. This information is available through the Agency component API. This API follows the JSON API standard and leverages the Drupal JSON API module. The documentation for the JSON API module is a great resource.

The endpoint for the Agency component API.

https://api.foia.gov/api/agency_components
An agency component payload might look like this.

Examples
Request a list of agency components names.

curl -g -v -H 'X-API-Key: <your-api-key>' 'https://api.foia.gov/api/agency_components?&fields[agency_component]=title'
Fetch a list of agency components with their parent agency.

curl -g -v -H 'X-API-Key: <your-api-key>' 'https://api.foia.gov/api/agency_components?&include=agency&fields[agency]=name,abbreviation&fields[agency_component]=title,abbreviation,agency'
Fetch the Office of Information Policy.

curl -g -v -H 'X-API-Key: <your-api-key>' 'https://api.foia.gov/api/agency_components/8216158f-8089-431d-b866-dc334e8d4758?'
Fetch the Office of Information Policy’s FOIA request form.

curl -g -v -H 'X-API-Key: <your-api-key>' https://api.foia.gov/api/agency_components/8216158f-8089-431d-b866-dc334e8d4758/request_form
The FOIA XML Schema
Federal agencies publish FOIA information in accordance with guidelines prepared by the U. S. Department of Justice Office of Information Policy. These guidelines, available here, describe the format and meaning of FOIA annual report information. In addition, a FOIA Annual Report XML schema has been developed allowing agency FOIA annual report information to be represented and exchanged in a standardized format. This XML schema closely follows the structure and terminology of the guidance document, and conforms to the NIEM standard (http://niem.gov). 

All agency data available through reports and graphs on the FOIA.gov website is also available for public download as XML documents conforming to the FOIA Annual Report XML schema at the link below. This enables any kind of offline processing, storage, comparison, or mashup which may be desired.  

The entire IEPD package may also be downloaded directly by clicking on the following link [Download IEPD].

Within this IEPD package you can find the XML schema defined in exchange_files/schema/extension/FoiaAnnualReportExtensions.xsd. Note that this definition inherits from others, which can be found in the package as well, under exchange_files/schema/Subset/niem/.

You can download the FOIA Data Set here.

Annual Report XML API
Individual annual reports, in XML format, are available via an API endpoint:

/api/annual-report-xml/[agency abbreviation]/[year]

For example, to receive the Department of Justice (DOJ) annual report for 2021, you could use this:

curl -H 'X-API-Key: <your-api-key>' https://api.foia.gov/api/annual-report-xml/DOJ/2021
"""
