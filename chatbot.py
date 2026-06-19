from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def get_career_advice(
    education,
    skills,
    interests,
    mbti
):

    try:

        prompt = f"""
Education: {education}
Skills: {skills}
Interests: {interests}
MBTI: {mbti}

Suggest:
1. Career paths
2. Salary
3. Future scope
4. Skills to learn
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception:

        return f"""
Recommended Domains:
{', '.join(interests)}

MBTI Type:
{mbti}

Suggested Learning Path:
• Python
• SQL
• Data Structures
• Cloud Computing
• AI Tools

Expected Salary:
6-25 LPA depending on role and experience.

Future Scope:
High demand in AI, Data Science, Full Stack Development and Cyber Security.
"""