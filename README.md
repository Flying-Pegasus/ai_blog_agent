<h1>Setup :</h1>
<p>1. git clone "Repo Link" on your terminal </p>
<p>2. Then run the command '''py -3.11 -m venv venv''' to create a virtual python environment to install all the relevant dependencies inside the directory. (Make sure you have Python v.11 installed on your local machine) </p>
<p>3. Then run '''.\venv\Scripts\activate''' to activate the environment for windows</p>
<p>4. Then run the command '''pip install -r requirements.txt''' </p>
<p>5. Create a '.env' file in the '''ai_blog_agent''' directory</p>
<p>6. In the .env file write:</p>
<p>    GOOGLE_API_KEY = Your_api_key (Generate this api key from Google Gemini API)</p>
<p>    NEWSDATA_API_KEY= Your_api_key (Generate the api key from NewsData.io)</p>
<p>7. Run the command '''python main.py --topic "How Python is used in AI" --tone educational''' to generate the required blog output.</p>
