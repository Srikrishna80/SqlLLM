from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
import mysql.connector

app = FastAPI()

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel('gemini-pro')

# Model prompt
prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    
    Your database consists of two tables: `1_live_career_counseling_sessions_speaker`,`1_live_career_counseling_sessions`,`1_contactus`,`1_sessions_speaker_mapping`,`1_exhibitor_gallery`,`1_event_master`,`1_exhibitor_master`,1_exhibitor_hall_category.
    
    The `1_live_career_counseling_sessions_speaker` table has the following columns:
    - lccss_id (Primary Key)
    - lccss_name
    - lccss_email
    - lccss_company_name
    - lccss_time
    - lccss_designation
    - lccss_description
    - lccss_linkedin
    - lccss_twitter
    - lccss_instagram
    - lccss_pic
    - speaker_status
    - lccss_status

    The `1_exhibitor_hall_category`  table has the following columns:
    - ehc_id
    - aem_id
    - ehc_hall_name
    - ehc_name
    - ehc_hall_bgimage
    - ehc_hall_presentation_video
    - gcm_id
    - ehc_is_booth_list
    - ehc_is_product_list
    - ehc_product_main_title
    - ehc_product_title
    - ehc_order
    - ehc_status


    The `1_exhibitor_master` table has the following colums:
    - exhim_id
    - exhim_organization_name
    - exhim_custom_page
    - ot_id
    - ebm_id
    - exhim_logo
    - exhim_stall_no
    - exhim_hall_no
    - exhim_stall_size
    - exhim_banner
    - exhim_mo_v_banner
    - exhim_standee
    - exhim_standee1
    - exhim_standee2
    - exhim_standee3
    - exhim_standee4
    - exhim_mo_standee
    - exhim_right_standee
    - exhim_right_standee_mo
    - exhim_stall_backdropofvideo
    - exhim_stall_video
    - exhim_desk_logo
    - exhim_lobby_image
    - exhim_lobbyvideo
    - exhim_punchline
    - exhim_detail
    - section_head
    - exhim_fact_sheet_html
    - exhim_contact_us
    - counm_id
    - sm_id
    - cm_id
    - exhim_address
    - exhim_type_of_institute
    - exhim_ownership
    - exhim_estd_year
    - exhim_accreditation
    - exhim_recognition
    - exhim_campus_area
    - exhim_approval
    - exhim_brochure
    - exhim_qs_i_gauge
    - exhim_qs_logo
    - exhim_scholarship
    - exhim_scholarship_percentage
    - exhim_NoPaperForms
    - exhim_np_secret_key
    - exhim_np_college_id
    - exhim_admission_details_html
    - exhim_facebook_link
    - exhim_web_link
    - exhim_youtube_link
    - exhim_instagram_link
    - exhim_twitter_link
    - exhim_linkedIn_link
    - exhim_whatsapp
    - exhim_profile
    - exhim_industry
    - exhim_group
    - exhim_contact_person
    - exhim_contact_email
    - exhim_organisation_email
    - exhim_login_id
    - em_chatbot_script
    - exhim_insert
    - exhim_update
    - exhim_status
    - display
    - contact_person_incharge
    - exhim_designation
    - office_phone_code
    - office_contact_number
    - fax_code
    - fax_number
    - ppm_id_custom
    - ppm_id
    - ppmm_id
    - mail_sent
    - exhim_scroller_text
    - wall_poster
    - wall_poster1
    - wall_poster2
    - wall_poster3
    - wall_poster4
    - wall_poster5
    - wall_poster6
    - wall_poster7
    - wall_poster8
    - th_wall_poster
    - th_wall_poster1
    - th_wall_poster2
    - th_wall_poster3
    - th_wall_poster4
    - th_wall_poster5
    - th_wall_poster6
    - th_wall_poster7


    The `1_live_career_counseling_sessions` table has the follwing colums:
    - lccs_id
    - aem_id
    - lccs_type
    - lccs_name
    - lccs_sub_title
    - lccs_speaker_name
    - lccs_moderator_pic
    - lccs_moderator_name
    - lccs_moderator_designation
    - lccs_moderator_desc
    - lccs_host_pic
    - lccs_host_designation: varchar(255) DEFAULT NULL
    - lccs_host_desc: varchar(255) DEFAULT NULL
    - lccs_start_datewtime_for_showlive: datetime DEFAULT NULL
    - lccs_start_datewtime: datetime DEFAULT NULL
    - lccs_end_datewtime: datetime DEFAULT NULL
    - lccs_zoom_id: varchar(255) DEFAULT NULL
    - lccs_zoom_pwd: varchar(120) DEFAULT NULL
    - lcss_room_id: varchar(255) DEFAULT NULL
    - lccs_live_status: enum('live','yet_to_start','finished') NOT NULL DEFAULT 'yet_to_start'
    - lccs_past_session_video_url: varchar(255) DEFAULT NULL
    - lccs_orderby: int(11) DEFAULT NULL
    - lccs_status: enum('active','inactive') DEFAULT 'active'
    - lccss_meeting_id: longtext NOT NULL
    - lccss_meeting_room_name: longtext NOT NULL
    - lccss_meeting_url: longtext NOT NULL

    

    The `1_sessions_speaker_mapping` table has the following colums:
    -  ssm_id
    -  lccs_id
    -  lccss_id
    -  ssm_status
  
    
    
    The `1_contactus` table has the following columns:
    - cu_id (Primary Key)
    - First_name
    - Last_name
    - Designation
    - Email
    - Mobile
    - Message
    - DateTime

    The `1_exhibitor_gallery` table has the following colums:
    - eg_name
    - eg_caption
    - eg_status

    The `1_event_master` table has the following columns;
    - aem_id
    - tm_id
    - parent_aem_id
    - bm_id
    - aem_event_nickname
    - aem_name
    - aem_short_name
    - aem_description
    - aem_tag_line
    - aem_organized_by
    - aem_organizer_website
    - aem_full_address
    - aem_location
    - aem_location_coordinates
    - aem_live_date_time
    - aem_custom_start_date
    - aem_start_date
    - aem_end_date
    - aem_relaxation_date
    - aem_date
    - aem_event_date
    - aem_day
    - aem_date_intext
    - aem_time
    - aem_timezones
    - aem_mail_html
    - aem_mail_subject
    - aem_otp_mail_html
    - aem_otp_mail_subject
    - aem_sms_text
    - aem_sms_template
    - aem_is_send_whatsapp
    - aem_logo_image
    - aem_logo_poweredby
    - aem_header_img
    - aem_orderby
    - aem_viewinlist
    - aem_ai_enabled
    - aem_colors
    - aem_status
    - aem_insert_time
    - aem_update_time \n\n For example,\nExample 1: Give me the contact details?
    The SQL command will be something like this SELECT First_name,Last_name,Email,Mobile FROM 1_contactus;
    \nExample 2: List all speakers of superangles summit?.
    The SQL command will be something like this SELECT lccss_name, FROM 1_live_career_counseling_sessions_speaker;
    \nExample 3: List all the speakers of Opening Ceremony?.
    The SQL command will be something like this SELECT s.lccss_name FROM 1_live_career_counseling_sessions ses JOIN 1_sessions_speaker_mapping map ON ses.lccs_id = map.lccs_id JOIN 1_live_career_counseling_sessions_speaker s ON map.lccss_id = s.lccss_id WHERE ses.lccs_name = 'Opening Ceremony';
    /nExample 4: List all the sessions of Ashneer Grover.
    The SQL command will be something like this: SELECT ses.lccs_name FROM 1_live_career_counseling_sessions ses JOIN 1_sessions_speaker_mapping map ON ses.lccs_id = map.lccs_id JOIN 1_live_career_counseling_sessions_speaker s ON map.lccss_id = s.lccss_id WHERE s.lccss_name = 'Ashneer Grover';
    \nExample 5: List all exhibitors of superangles summit?.
    The SQL command will be something like this SELECT eg_name FROM 1_exhibitor_gallery;
    \nExample 6: List all the  events?.
    The SQL command will be something like this SELECT aem_name, FROM 1_event_master;
    \nExample 7: List all the Exhibitors of Super Angels summit?.
    The SQL command will be something like this SELECT em.exhim_organization_name FROM `1_exhibitor_event_mapping` eem JOIN `1_exhibitor_master` em ON eem.exhim_id = em.exhim_id JOIN `1_event_master` ev ON eem.aem_id = ev.aem_id WHERE ev.aem_event_nickname = 'super_angels_summit';
    \nExample 8:List all the hall names  of the ibentos?
    The SQL command will be something like SELECT DISTINCT ehc.ehc_hall_name,ehc.ehc_name FROM `1_event_master` aem JOIN `1_exhibitor_event_mapping` eem ON aem.aem_id = eem.aem_id JOIN `1_exhibitor_hall_category` ehc ON eem.ehc_id = ehc.ehc_id WHERE aem.aem_organized_by = 'ibentos';
    \nExample 9: List all organization names of the exhibitors?
    The SQL command will be something like SELECT exhim_organization_name from 1_exhibitor_master;

    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Function to generate Gemini response
def get_gemini_response(question, prompt):
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to execute SQL query
# def execute_sql_query(sql):
#     connection = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="superangles"
#     )
#     cursor = connection.cursor()
#     cursor.execute(sql)
#     rows = cursor.fetchall()
#     connection.commit()
#     connection.close()
#     return rows

import mysql.connector

def execute_sql_query(sql):
    connection = mysql.connector.connect(
        host="34.131.155.208",  # Update with your public IP address
        user="superangles-database",    # Update with your database username
        password="Sree@123",# Update with your database password
        database="superangles"   # Update with your database name
    )
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows


# Function to generate Gemini response
def get_gemini_response(question, prompt):
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to execute SQL query
def execute_sql_query(sql):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="superangles"
    )
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows

# Define request model
class Question(BaseModel):
    question: str

# Define response model
class SQLResponse(BaseModel):
    data: list
    
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# POST endpoint to handle incoming requests from Streamlit app
@app.post("/ask_question/", response_model=SQLResponse)
def ask_question(question_data: Question):
    question = question_data.question
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")
    
    # Generate Gemini response
    gemini_response = get_gemini_response(question, prompt)
    
    # Execute SQL query
    sql_response = execute_sql_query(gemini_response)
    print(sql_response)
    
    # Group the SQL response values into sets based on the number of columns returned
    num_columns = len(sql_response[0]) if sql_response else 0
    response_data = [dict(zip(range(num_columns), row)) for row in sql_response]
    
    return {"data": response_data}