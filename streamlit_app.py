import streamlit as st

st.set_page_config(page_title="Generator S3 code consumer registration", layout="wide")

st.title("Generator S3 code consumer registration")
st.write("Campaign data")

# Crear dos columnas: una para el formulario y otra para el resultado
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Input Info")
    
    brand = st.text_input("Brand", value="Saphnelo")
    
    source_code = st.text_input("Source Code", value="ODGT")
    country_code = st.text_input("Country Code", value="USA")
    resp_source_code = st.text_input("Response Source Code", value="SLO_PSP_B_WB_1")
    survey_code = st.text_input("Survey Code (SurveyID)", value="SLO_PSP_B_WB_1")
    media_code = st.text_input("Media Code", value="SLO_C_C_123")
    
    st.subheader("Tealium data")
    tealium_ds = st.text_input("Tealium Datasource", value="0t78qu")
    tealium_acc = st.text_input("Tealium Account", value="astrazeneca")
    tealium_prof = st.text_input("Tealium Profile", value="us-consumer-test")
    brand_web = st.text_input("Brand Profile IQ", value="us-saphnelo-ic")
    tealium_trace = st.text_input("Tealium Trace ID", value="OHywBulB")

    st.subheader("Payload data (ctx variables)")
    ctx_firstname = st.text_input("First Name", value="firstname")
    ctx_lastname = st.text_input("Last Name", value="lastName")
    ctx_emailAddress = st.text_input("email", value="emailAddress")
	ctx_phonenumber = st.text_input("phonenumber", value="phonenumber")
    ctx_tealiumVisitorID = st.text_input("tealiumVisitorID", value="tealiumVisitorID")

# Generación del String de JS dinámicamente
js_template = f"""// Ensure compatibility with both JDK 7 and 8 JSR-223 Script Engines 
try {{ load("nashorn:mozilla_compat.js"); }} catch (e) {{ }}

importPackage(com.snaplogic.scripting.language);
importClass(java.util.LinkedHashMap);
importClass(java.util.ArrayList);

var impl = {{
    input: input,
    output: output,
    error: error,
    log: log,

    execute: function () {{
        this.log.info("Executing Transform Script");
        while (this.input.hasNext()) {{
            try {{
                var inDoc = this.input.next();
                var outDoc = new LinkedHashMap();
                var ctx = inDoc.ctx;
                outDoc.put("ctx", inDoc.ctx);
                
                var event_data = {{}};
                var formId = ctx.formId;

                var respDate = new Date();
                var formattedRespDate = respDate.getFullYear() + "-" + 
                    ("0" + (respDate.getMonth() + 1)).slice(-2) + "-" + 
                    ("0" + respDate.getDate()).slice(-2) + " " + 
                    ("0" + respDate.getHours()).slice(-2) + ":" + 
                    ("0" + respDate.getMinutes()).slice(-2) + ":" + 
                    ("0" + respDate.getSeconds()).slice(-2);

                
                var sourceCode = "{source_code}";
                var countryCode = "{country_code}";
                var respSourceCode = "{resp_source_code}";
                var surveyCode = "{survey_code}";
                var mediaCode = "{media_code}"; 
                var brandWebsiteCode = "{brand_web}";
                var brandName = "{brand}";

                // Consumer form elements
                var tealiumVisitorID = ctx.{ctx_tealiumVisitorID} ? ctx.{ctx_tealiumVisitorID} : ctx.{ctx_emailAddress} + Date.now();                
                var firstName = ctx.{ctx_firstname};
                var lastName = ctx.{ctx_lastname};
                var emailAddress = {ctx_emailAddress};
				var phonenumber = {ctx_phonenumber};
                var SLO_PRSCRB = ctx.SLO_PRSCRB; 
                var SLO_INDICATION = ctx.indication_received_by_selections;
                var SLO_TXDATE = ctx.SLO_CONFIRMATION_selections;
                var SLO_INTEREST = ctx.SLO_INTEREST;
                var SLO_TEXT = ctx.SLO_TEXT_selections;
                
                             
                var emailAddresses = new ArrayList();
                emailAddresses.add({{
                    "EmailType": "Unknown",
                    "Email": emailAddress
                }});
                                
                var sourceKey = new ArrayList();
                sourceKey.add({{
                    "Type": sourceCode,
                    "Value": tealiumVisitorID
                }});

                var phoneNumbers = new ArrayList();
                phoneNumbers.add({{
                    "Number": phonenumber,
                    "PhoneType": "Unknown"
                }});
                
                var profile = new ArrayList();
                profile.add({{
                    "Type": "Consumer",
                    "FirstName": firstName,
                    "LastName": lastName,
                    "PhoneNumbers": phoneNumbers,
                    "Gender": "Unknown",
                    "EmailAddresses": emailAddresses,    
                    "SourceKey": sourceKey,
                    "CountryCode": countryCode
                }});

                var promotionResponses = new ArrayList();
                promotionResponses.add({{
                    "PromotionResponseID": "",
                    "ExternalConsumerID": "",
                    "VendorCode": sourceCode,
                    "ResponseSourceCode": respSourceCode,
                    "ResponseDate": formattedRespDate,
                    "MediaCode": mediaCode,
                    "CountryCode": countryCode
                }});
                        
                var surveyResponses = new ArrayList();
                if (SLO_PRSCRB) {{
                    surveyResponses.add({{
                        "SurveyQuestionID": "SLO_PRSCRB",
                        "QuestionAnswerID": SLO_PRSCRB
                    }}); 
                }}
                
                switch (SLO_INDICATION) {{
                case "001":
                    surveyResponses.add({{
                        "SurveyQuestionID": "SLO_INDICATION",
                        "QuestionAnswerID": SLO_INDICATION,
                        "OpenAnswerText": "IV infusion"                      
                    }});
                    break; 
                case "002":
                    surveyResponses.add({{
                        "SurveyQuestionID": "SLO_INDICATION",
                        "QuestionAnswerID": SLO_INDICATION,
                        "OpenAnswerText": "Self-injection"                      
                    }});
                    break;
                default:
                    surveyResponses.add({{
                        "SurveyQuestionID": "SLO_INDICATION",
                        "QuestionAnswerID": "003"                    
                    }});
                }}

                if (SLO_TXDATE) {{
                    surveyResponses.add({{
                        "SurveyQuestionID": "SLO_TXDATE",
                        "QuestionAnswerID": SLO_TXDATE
                    }});
                }}
               
                if (SLO_INTEREST) {{
                    var formattedInterest = SLO_INTEREST.replace(/^(\\d{{4}})-(\\d{{2}})-(\\d{{2}})$/, '$2/$3/$1');
                    surveyResponses.add({{
                        "SurveyQuestionID": "SLO_INTEREST",
                        "QuestionAnswerID": "001",
                        "OpenAnswerText": formattedInterest
                    }});
                }} else {{
                    surveyResponses.add({{
                        "SurveyQuestionID": "SLO_INTEREST",
                        "QuestionAnswerID": "002"
                    }});
                }}
                
                if (SLO_TEXT) {{
                    surveyResponses.add({{
                        "SurveyQuestionID": "SLO_TEXT",
                        "QuestionAnswerID": SLO_TEXT
                    }});
                }}
                
                if (mobilePhone) {{
                    surveyResponses.add({{
                        "SurveyQuestionID": "SLO_MOBILE",
                        "QuestionAnswerID": "001",
                        "OpenAnswerText": mobilePhone
                    }});
                }}

                var regPayload = {{
                    "Profile": profile,
                    "PromotionResponses": promotionResponses,
                    "SurveyResponses": surveyResponses
                }};

                var iter = surveyResponses.iterator();
                while (iter.hasNext()) {{
                    var element = iter.next();
                    element.ExternalConsumerID = "";
                    element.VendorCode = sourceCode;
                    element.ResponseDate = formattedRespDate;
                    element.SurveyID = surveyCode;
                    element.CountryCode = countryCode;
                }}

                // Enriching event_data variables
                event_data.consumer_first_name = firstName;
                event_data.consumer_last_name = lastName;
                event_data.consumer_phone_number = mobilePhone;
                event_data.consumer_email_address = emailAddress;
                event_data.consumer_brand_website_code = brandWebsiteCode;
                event_data.consumer_registration_origin = respSourceCode;
                event_data.consumer_registration_payload = regPayload;
                event_data.tealium_visitor_id = tealiumVisitorID;
                event_data.tealium_datasource = '{tealium_ds}';  
                event_data.tealium_account = '{tealium_acc}';
                event_data.tealium_profile = '{tealium_prof}';
                event_data.brand = brandName;
                event_data.tealium_trace_id = '{tealium_trace}';
                event_data.tealium_event = 'consumer_registration';

                outDoc.put("payload", regPayload);
                outDoc.put("event_data", event_data);
                outDoc.put("event_data_child", null);

                this.output.write(inDoc, outDoc);
            }} catch (err) {{
                var errDoc = new LinkedHashMap();
                errDoc.put("error", err);
                this.log.error(err);
                this.error.write(errDoc);
            }}
        }}
    }},
    cleanup: function () {{
        this.log.info("Cleaning up");
    }}
}};

var hook = new com.snaplogic.scripting.language.ScriptHook(impl);"""

with col2:
    st.header("Output: Code S3")
    st.caption("S3 Script")
    st.code(js_template, language="javascript")
