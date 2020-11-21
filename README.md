# python-api

Create User POST /api/user/register
{
email
password
fullname
country
}

Login User POST /api/user/login
{
email
password
}

Auth User GET /api/user/auth
header
  bearer

Create Skill POST /api/skills/register
header
  bearer
{
    "skill" : "NameSkill"
}

Get all Skills GET /api/skills
header
  bearer

Add Skill User POST /api/user/skills
header
  bearer
{
    "id":"idUser",
    "skill":"NameSkill"
}
