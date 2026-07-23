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
    ctx_phonenumber = st.text_input("Phone Number", value="phonenumber")
    ctx_tealiumVisitorID = st.text_input("tealiumVisitorID", value="tealiumVisitorID")

# --- CONSTRUCCIÓN CONDICIONAL DEL JAVASCRIPT ---
config_lines = []
if source_code:
    config_lines.append(f'var sourceCode = "{source_code}";')
if country_code:
    config_lines.append(f'var countryCode = "{country_code}";')
if resp_source_code:
    config_lines.append(f'var respSourceCode = "{resp_source_code}";')
if survey_code:
    config_lines.append(f'var surveyCode = "{survey_code}";')
if media_code:
    config_lines.append(f'var mediaCode = "{media_code}";')
if brand_web:
    config_lines.append(f'var brandWebsiteCode = "{brand_web}";')
if brand:
    config_lines.append(f'var brandName = "{brand}";')

# Unimos las líneas con saltos de línea para inyectarlas limpiamente
config_block = "\n\t\t\t\t".join(config_lines)

# Lógica condicional para las variables del payload (ctx)
visitor_id_line = (
    f'var tealiumVisitorID = ctx.{ctx_tealiumVisitorID} ? ctx.{ctx_tealiumVisitorID} : ctx.{ctx_emailAddress} + Date.now();' 
    if ctx_tealiumVisitorID and ctx_emailAddress 
    else ''
)

firstname_line = f'var firstName = ctx.{ctx_firstname};' if ctx_firstname else 'var firstName = "";'
lastname_line = f'var lastName = ctx.{ctx_lastname};' if ctx_lastname else 'var lastName = "";'
email_line = f'var emailAddress = ctx.{ctx_emailAddress};' if ctx_emailAddress else 'var emailAddress = "";'
phonenumber_line = f'var phonenumber = ctx.{ctx_phonenumber};' if ctx_phonenumber else 'var phonenumber = "";'

# Email array
email_array = ""
if ctx_emailAddress:
    email_array = f"""var emailAddresses = new ArrayList();
                emailAddresses.add({{
                    "EmailType": "Unknown",
                    "Email": emailAddress
                }});"""
else:
    email_array = f"""var emailAddresses = new ArrayList();
                emailAddresses.add({{
                    "EmailType": "Unknown",
                    "Email": ""
                }});"""

# phone array
phone_array = ""
if ctx_phonenumber:
    phone_array = f"""var phoneNumbers = new ArrayList();
                phoneNumbers.add({{
                    "Number": phonenumber,
                    "PhoneType": "Unknown"
                }});"""
else:
    phone_array = f"""var phoneNumbers = new ArrayList();
                phoneNumbers.add({{
                    "Number": "",
                    "PhoneType": "Unknown"
                }});"""

# Generación del String de JS dinámicamente con los bloques condicionales
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

                // Configuración general inyectada dinámicamente
                {config_block}

                // Consumer form elements
                {visitor_id_line}
                {firstname_line}
                {lastname_line}
                {email_line}
                {phonenumber_line}
                var SLO_PRSCRB = ctx.SLO_PRSCRB; 
                var SLO_INDICATION = ctx.indication_received_by_selections;
                var SLO_TXDATE = ctx.SLO_CONFIRMATION_selections;
                var SLO_INTEREST = ctx.SLO_INTEREST;
                var SLO_TEXT = ctx.SLO_TEXT_selections;

                //Arrays Payload
                {email_array}
                {phone_array}
                                        
                var sourceKey = new ArrayList();
                sourceKey.add({{
                    "Type": sourceCode,
                    "Value": tealiumVisitorID
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
