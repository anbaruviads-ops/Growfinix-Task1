career_map = {
    "AI": [
        ("AI Engineer", "12-40 LPA"),
        ("ML Engineer", "10-35 LPA")
    ],

    "Data Science": [
        ("Data Scientist", "8-30 LPA"),
        ("Data Analyst", "6-15 LPA")
    ],

    "Web Development": [
        ("Frontend Developer", "5-20 LPA"),
        ("Full Stack Developer", "8-25 LPA")
    ],

    "Cyber Security": [
        ("Security Analyst", "6-18 LPA")
    ]
}

def recommend(interests):

    careers = []

    for interest in interests:

        if interest in career_map:

            careers.extend(
                career_map[interest]
            )

    return careers